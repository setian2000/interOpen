import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from styles import (
    BROWSER_BG,
    BROWSER_SELECT_BG,
    BROWSER_TITLE_FG,
    BTN_BLUE,
    BTN_BLUE_ACTIVE,
    BTN_GRAY,
    BTN_GRAY_ACTIVE,
    BTN_RED,
    BTN_RED_ACTIVE,
    BTN_SKY,
    BTN_SKY_ACTIVE,
    make_button,
    make_order_button,
)


class BrowserPanel:
    def __init__(self, parent, controller):
        self.controller = controller

        self.frame = tk.LabelFrame(
            parent,
            text="실행 브라우저 관리",
            font=("맑은 고딕", 11, "bold"),
            padx=10,
            pady=10,
            bg=BROWSER_BG,
            fg=BROWSER_TITLE_FG,
            bd=2,
            relief="groove",
        )

        list_frame = tk.Frame(self.frame, bg=BROWSER_BG)
        list_frame.pack(fill="x", expand=False, pady=5)

        self.listbox = tk.Listbox(
            list_frame,
            width=100,
            height=10,
            font=("맑은 고딕", 9),
            bg="white",
            fg="#222222",
            selectbackground=BROWSER_SELECT_BG,
            selectforeground="#000000",
            relief="solid",
            bd=1,
            highlightthickness=0,
        )
        self.listbox.pack(side="left", fill="x", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y", padx=(4, 2))
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Delete>", self.delete_selected)

        order_btns = tk.Frame(list_frame, bg=BROWSER_BG)
        order_btns.pack(side="left", fill="y", padx=(2, 0))
        make_order_button(order_btns, "▲위로", self.move_up).pack(pady=(0, 4))
        make_order_button(order_btns, "▼아래로", self.move_down).pack()

        input_frame = tk.Frame(self.frame, bg=BROWSER_BG)
        input_frame.pack(fill="x", pady=8)

        tk.Label(input_frame, text="브라우저 이름:", font=("맑은 고딕", 10), bg=BROWSER_BG).grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.entry_name = tk.Entry(input_frame, width=18, font=("맑은 고딕", 9), relief="solid", bd=1)
        self.entry_name.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        tk.Label(input_frame, text="실행 경로:", font=("맑은 고딕", 10), bg=BROWSER_BG).grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.entry_path = tk.Entry(input_frame, width=52, font=("맑은 고딕", 9), relief="solid", bd=1)
        self.entry_path.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        make_button(input_frame, "🔍찾아보기", self.browse_path, width=10, bg=BTN_SKY, active=BTN_SKY_ACTIVE).grid(row=0, column=4, padx=6, pady=6, sticky="w")

        btns = tk.Frame(input_frame, bg=BROWSER_BG)
        btns.grid(row=0, column=5, padx=8, pady=6)
        self.btn_add_update = make_button(btns, "➕브라우저 추가", self.add_or_update, width=12, bg=BTN_BLUE, active=BTN_BLUE_ACTIVE)
        self.btn_add_update.pack(side="left", padx=3)
        make_button(btns, "브라우저 삭제", self.delete_selected, width=12, bg=BTN_RED, active=BTN_RED_ACTIVE).pack(side="left", padx=3)
        make_button(btns, "취소", self.cancel_selection, width=8, bg=BTN_GRAY, active=BTN_GRAY_ACTIVE).pack(side="left", padx=3)

        input_frame.grid_columnconfigure(3, weight=1)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for browser in self.controller.config.get("browsers", []):
            self.listbox.insert(tk.END, f"{browser.get('name', '').upper()}  →  {browser.get('path', '')}")

    def browse_path(self):
        file_path = filedialog.askopenfilename(
            title="브라우저 실행 파일 선택",
            filetypes=[("실행 파일", "*.exe"), ("모든 파일", "*.*")],
        )
        if file_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_path)

    def on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.controller.browser_panel_selected_index = idx
        browser = self.controller.config["browsers"][idx]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, browser.get("name", ""))
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, browser.get("path", ""))
        self.btn_add_update.config(text="브라우저 수정")

    def cancel_selection(self):
        self.controller.browser_panel_selected_index = None
        self.entry_name.delete(0, tk.END)
        self.entry_path.delete(0, tk.END)
        self.listbox.selection_clear(0, tk.END)
        self.btn_add_update.config(text="➕브라우저 추가")

    def add_or_update(self):
        name = self.entry_name.get().strip()
        path = self.entry_path.get().strip()
        if not name:
            messagebox.showwarning("경고", "브라우저 이름을 입력하세요.")
            return
        if not path:
            messagebox.showwarning("경고", "브라우저 실행 경로를 입력하세요.")
            return

        name_lower = name.lower()
        selected = getattr(self.controller, "browser_panel_selected_index", None)

        if selected is not None:
            duplicate = next((b for i, b in enumerate(self.controller.config["browsers"]) if i != selected and b.get("name", "").lower() == name_lower), None)
            if duplicate:
                messagebox.showwarning("경고", f"브라우저 '{name}'은 이미 존재합니다.")
                return
            browser = self.controller.config["browsers"][selected]
            old_name = browser.get("name", "").lower()
            browser["name"] = name_lower
            browser["path"] = path
            browser.setdefault("urls", [])
            browser.setdefault("args", [])
            browser.setdefault("delay", 0.5)
            if self.controller.url_panel.combo_browser.get().strip().lower() == old_name:
                self.controller.url_panel.combo_browser.set(name.upper())
            messagebox.showinfo("수정 완료", "브라우저 정보가 수정되었습니다.")
        else:
            exists = next((b for b in self.controller.config["browsers"] if b.get("name", "").lower() == name_lower), None)
            if exists:
                messagebox.showwarning("경고", f"브라우저 '{name}'은 이미 존재합니다.")
                return
            self.controller.config["browsers"].append({
                "name": name_lower,
                "path": path,
                "urls": [],
                "args": [],
                "delay": 0.5,
            })
            messagebox.showinfo("추가 완료", f"브라우저 '{name}'이 추가되었습니다.")

        self.controller.save()
        self.controller.refresh_all()
        self.cancel_selection()

    def delete_selected(self, _event=None):
        selected = getattr(self.controller, "browser_panel_selected_index", None)
        if selected is None:
            messagebox.showwarning("경고", "삭제할 브라우저를 선택하세요.")
            return
        browser = self.controller.config["browsers"][selected]
        browser_name = browser.get("name", "").upper()
        if messagebox.askyesno("확인", f"브라우저 '{browser_name}'을(를) 삭제하시겠습니까?\n등록된 URL도 함께 삭제됩니다."):
            del self.controller.config["browsers"][selected]
            self.controller.browser_panel_selected_index = None
            self.controller.save()
            self.controller.refresh_all()
            self.cancel_selection()
            self.controller.url_panel.cancel_selection()

    def move_up(self):
        selected = getattr(self.controller, "browser_panel_selected_index", None)
        if selected is None or selected <= 0:
            return
        items = self.controller.config["browsers"]
        items[selected - 1], items[selected] = items[selected], items[selected - 1]
        self.controller.browser_panel_selected_index = selected - 1
        self.controller.save()
        self.controller.refresh_all()
        self.listbox.selection_set(self.controller.browser_panel_selected_index)
        self.listbox.see(self.controller.browser_panel_selected_index)

    def move_down(self):
        selected = getattr(self.controller, "browser_panel_selected_index", None)
        items = self.controller.config["browsers"]
        if selected is None or selected >= len(items) - 1:
            return
        items[selected + 1], items[selected] = items[selected], items[selected + 1]
        self.controller.browser_panel_selected_index = selected + 1
        self.controller.save()
        self.controller.refresh_all()
        self.listbox.selection_set(self.controller.browser_panel_selected_index)
        self.listbox.see(self.controller.browser_panel_selected_index)
