import tkinter as tk
from tkinter import ttk, messagebox

from styles import BTN_GRAY, BTN_GRAY_ACTIVE, BTN_RED, BTN_RED_ACTIVE, BTN_SKY, BTN_SKY_ACTIVE, URL_BG, URL_SELECT_BG, URL_TITLE_FG, make_button


class UrlPanel:
    def __init__(self, parent, controller):
        self.controller = controller

        self.frame = tk.LabelFrame(
            parent,
            text="연결 URL 관리",
            font=("맑은 고딕", 11, "bold"),
            padx=10,
            pady=10,
            bg=URL_BG,
            fg=URL_TITLE_FG,
            bd=2,
            relief="groove",
        )

        list_frame = tk.Frame(self.frame, bg=URL_BG)
        list_frame.pack(fill="x", expand=False, pady=5)

        self.listbox = tk.Listbox(
            list_frame,
            width=110,
            height=10,
            font=("맑은 고딕", 9),
            bg="white",
            fg="#222222",
            selectbackground=URL_SELECT_BG,
            selectforeground="#000000",
            relief="solid",
            bd=1,
            highlightthickness=0,
        )
        self.listbox.pack(side="left", fill="x", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Delete>", self.delete_selected)

        input_frame = tk.Frame(self.frame, bg=URL_BG)
        input_frame.pack(fill="x", pady=8)

        tk.Label(input_frame, text="브라우저:", font=("맑은 고딕", 10), bg=URL_BG).grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.combo_browser = ttk.Combobox(input_frame, values=[], width=18, state="readonly")
        self.combo_browser.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        tk.Label(input_frame, text="URL:", font=("맑은 고딕", 10), bg=URL_BG).grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.entry_url = tk.Entry(input_frame, width=52, font=("맑은 고딕", 9), relief="solid", bd=1)
        self.entry_url.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        tk.Label(input_frame, text="열기 방식:", font=("맑은 고딕", 10), bg=URL_BG).grid(row=0, column=4, padx=6, pady=6, sticky="w")
        self.combo_mode = ttk.Combobox(input_frame, values=["tab", "window"], width=10, state="readonly")
        self.combo_mode.set("tab")
        self.combo_mode.grid(row=0, column=5, padx=6, pady=6, sticky="w")

        btns = tk.Frame(input_frame, bg=URL_BG)
        btns.grid(row=0, column=6, padx=8, pady=6)
        self.btn_add_update = make_button(btns, "➕URL 추가", self.add_or_update, width=10, bg=BTN_SKY, active=BTN_SKY_ACTIVE)
        self.btn_add_update.pack(side="left", padx=3)
        make_button(btns, "URL 삭제", self.delete_selected, width=10, bg=BTN_RED, active=BTN_RED_ACTIVE).pack(side="left", padx=3)
        make_button(btns, "취소", self.cancel_selection, width=8, bg=BTN_GRAY, active=BTN_GRAY_ACTIVE).pack(side="left", padx=3)
        input_frame.grid_columnconfigure(3, weight=1)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for browser in self.controller.config.get("browsers", []):
            browser_name = browser.get("name", "").upper()
            for item in browser.get("urls", []):
                url = item.get("url", "")
                mode = item.get("open_mode", "tab")
                self.listbox.insert(tk.END, f"{browser_name}  →  {url}  →  {mode}")
        names = [b.get("name", "").upper() for b in self.controller.config.get("browsers", []) if b.get("name")]
        self.combo_browser["values"] = names
        current = self.combo_browser.get()
        if current not in names:
            self.combo_browser.set(names[0] if names else "")

    def on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        line = self.listbox.get(sel[0])
        parts = [p.strip() for p in line.split("→")]
        if len(parts) < 3:
            return
        browser_name, url, mode = parts[0], parts[1], parts[2]
        self.combo_browser.set(browser_name)
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, url)
        self.combo_mode.set(mode)
        self.controller.url_panel_selected_browser_name = browser_name.lower()
        self.controller.url_panel_selected_index = self.find_url_index(browser_name.lower(), url)
        self.btn_add_update.config(text="URL 수정")

    def find_url_index(self, browser_name, target_url):
        browser = next((b for b in self.controller.config.get("browsers", []) if b.get("name", "").lower() == browser_name.lower()), None)
        if not browser:
            return None
        for i, item in enumerate(browser.get("urls", [])):
            if item.get("url", "") == target_url:
                return i
        return None

    def cancel_selection(self):
        self.controller.url_panel_selected_browser_name = None
        self.controller.url_panel_selected_index = None
        self.entry_url.delete(0, tk.END)
        self.combo_mode.set("tab")
        self.listbox.selection_clear(0, tk.END)
        self.btn_add_update.config(text="➕URL 추가")
        names = [b.get("name", "").upper() for b in self.controller.config.get("browsers", []) if b.get("name")]
        self.combo_browser.set(names[0] if names else "")

    def add_or_update(self):
        browser_name = self.combo_browser.get().strip().lower()
        url = self.entry_url.get().strip()
        open_mode = self.combo_mode.get().strip() or "tab"
        if not browser_name:
            messagebox.showwarning("경고", "브라우저를 먼저 추가한 후 선택하세요.")
            return
        if not url:
            messagebox.showwarning("경고", "URL을 입력하세요.")
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        browser = next((b for b in self.controller.config.get("browsers", []) if b.get("name", "").lower() == browser_name), None)
        if not browser:
            messagebox.showerror("오류", f"브라우저 '{browser_name}'을 찾을 수 없습니다.")
            return
        item = {"url": url, "open_mode": open_mode}
        if self.controller.url_panel_selected_index is not None and self.controller.url_panel_selected_browser_name == browser_name:
            browser["urls"][self.controller.url_panel_selected_index] = item
            messagebox.showinfo("수정 완료", "URL이 수정되었습니다.")
        else:
            browser.setdefault("urls", []).append(item)
            messagebox.showinfo("추가 완료", f"{browser_name.upper()}에 URL이 추가되었습니다.")
        self.controller.save()
        self.controller.refresh_all()
        self.cancel_selection()

    def delete_selected(self, _event=None):
        if self.controller.url_panel_selected_index is None or self.controller.url_panel_selected_browser_name is None:
            messagebox.showwarning("경고", "삭제할 URL을 선택하세요.")
            return
        browser = next((b for b in self.controller.config.get("browsers", []) if b.get("name", "").lower() == self.controller.url_panel_selected_browser_name), None)
        if not browser:
            return
        if self.controller.url_panel_selected_index < len(browser.get("urls", [])):
            removed = browser["urls"].pop(self.controller.url_panel_selected_index)
            messagebox.showinfo("삭제 완료", f"삭제됨: {removed.get('url', '')}")
        self.controller.save()
        self.controller.refresh_all()
        self.cancel_selection()
