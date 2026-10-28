import tkinter as tk
from tkinter import filedialog, messagebox

from styles import (
    APP_BG,
    APP_SELECT_BG,
    APP_TITLE_FG,
    BTN_GRAY,
    BTN_GRAY_ACTIVE,
    BTN_PURPLE,
    BTN_PURPLE_ACTIVE,
    BTN_RED,
    BTN_RED_ACTIVE,
    make_button,
    make_order_button,
)


class AppPanel:
    def __init__(self, parent, controller):
        self.controller = controller

        self.frame = tk.LabelFrame(
            parent,
            text="실행 어플 관리 (Apps)",
            font=("맑은 고딕", 11, "bold"),
            padx=12,
            pady=12,
            bg=APP_BG,
            fg=APP_TITLE_FG,
            bd=3,
            relief="ridge",
        )

        list_frame = tk.Frame(self.frame, bg=APP_BG)
        list_frame.pack(fill="x", expand=False, pady=5)

        self.listbox = tk.Listbox(
            list_frame,
            width=100,
            height=10,
            font=("맑은 고딕", 9),
            bg="white",
            fg="#222222",
            selectbackground=APP_SELECT_BG,
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

        order_btns = tk.Frame(list_frame, bg=APP_BG)
        order_btns.pack(side="left", fill="y", padx=(2, 0))
        make_order_button(order_btns, "▲위로", self.move_up).pack(pady=(0, 4))
        make_order_button(order_btns, "▼아래로", self.move_down).pack()

        input_frame = tk.Frame(self.frame, bg=APP_BG)
        input_frame.pack(fill="x", pady=8)

        tk.Label(
            input_frame,
            text="실행 어플 이름:",
            font=("맑은 고딕", 10),
            bg=APP_BG,
        ).grid(row=0, column=0, padx=6, pady=6, sticky="w")

        self.entry_name = tk.Entry(
            input_frame,
            width=22,
            font=("맑은 고딕", 9),
            relief="solid",
            bd=1,
        )
        self.entry_name.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        tk.Label(
            input_frame,
            text="실행 경로:",
            font=("맑은 고딕", 10),
            bg=APP_BG,
        ).grid(row=0, column=2, padx=6, pady=6, sticky="w")

        self.entry_path = tk.Entry(
            input_frame,
            width=50,
            font=("맑은 고딕", 9),
            relief="solid",
            bd=1,
        )
        self.entry_path.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        make_button(
            input_frame,
            "🔍찾아보기",
            self.browse_path,
            width=10,
            bg=BTN_PURPLE,
            active=BTN_PURPLE_ACTIVE,
        ).grid(row=0, column=4, padx=6, pady=6, sticky="w")

        tk.Label(
            input_frame,
            text="실행 인자:",
            font=("맑은 고딕", 10),
            bg=APP_BG,
        ).grid(row=1, column=0, padx=6, pady=6, sticky="w")

        self.entry_args = tk.Entry(
            input_frame,
            width=40,
            font=("맑은 고딕", 9),
            relief="solid",
            bd=1,
        )
        self.entry_args.grid(row=1, column=1, columnspan=3, padx=6, pady=6, sticky="ew")

        btns = tk.Frame(input_frame, bg=APP_BG)
        btns.grid(row=1, column=4, padx=8, pady=6, sticky="w")

        self.btn_add_update = make_button(
            btns,
            "➕실행App추가",
            self.add_or_update,
            width=10,
            bg=BTN_PURPLE,
            active=BTN_PURPLE_ACTIVE,
        )
        self.btn_add_update.pack(side="left", padx=3)

        make_button(
            btns,
            "실행App 삭제",
            self.delete_selected,
            width=10,
            bg=BTN_RED,
            active=BTN_RED_ACTIVE,
        ).pack(side="left", padx=3)

        make_button(
            btns,
            "취소",
            self.cancel_selection,
            width=8,
            bg=BTN_GRAY,
            active=BTN_GRAY_ACTIVE,
        ).pack(side="left", padx=3)

        input_frame.grid_columnconfigure(3, weight=1)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for app in self.controller.config.get("apps", []):
            name = app.get("name", "Unnamed")
            path = app.get("path", "")
            args = app.get("args", [])
            args_text = " ".join(args) if args else ""

            if args_text:
                self.listbox.insert(tk.END, f"{name}  →  {path}  →  {args_text}")
            else:
                self.listbox.insert(tk.END, f"{name}  →  {path}")

    def browse_path(self):
        file_path = filedialog.askopenfilename(
            title="실행 어플 파일 선택",
            filetypes=[("실행 파일", "*.exe;*.lnk"), ("모든 파일", "*.*")],
        )
        if file_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_path)

    def on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return

        idx = sel[0]
        self.controller.app_panel_selected_index = idx
        app = self.controller.config["apps"][idx]

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, app.get("name", ""))

        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, app.get("path", ""))

        self.entry_args.delete(0, tk.END)
        self.entry_args.insert(0, " ".join(app.get("args", [])))

        self.btn_add_update.config(text="실행 App 수정")

    def cancel_selection(self):
        self.controller.app_panel_selected_index = None

        self.entry_name.delete(0, tk.END)
        self.entry_path.delete(0, tk.END)
        self.entry_args.delete(0, tk.END)

        self.listbox.selection_clear(0, tk.END)
        self.btn_add_update.config(text="➕실행App추가")

    def add_or_update(self):
        name = self.entry_name.get().strip()
        path = self.entry_path.get().strip()
        raw_args = self.entry_args.get().strip()
        args = raw_args.split() if raw_args else []

        if not name:
            messagebox.showwarning("경고", "실행 어플 이름을 입력하세요.")
            return

        if not path:
            messagebox.showwarning("경고", "실행 경로를 입력하세요.")
            return

        selected = getattr(self.controller, "app_panel_selected_index", None)

        if selected is not None:
            app = self.controller.config["apps"][selected]
            app["name"] = name
            app["path"] = path
            app["mode"] = app.get("mode", "direct")
            app["args"] = args
            messagebox.showinfo("수정 완료", "실행 어플 정보가 수정되었습니다.")
        else:
            self.controller.config.setdefault("apps", []).append(
                {
                    "name": name,
                    "path": path,
                    "mode": "direct",
                    "args": args,
                }
            )
            messagebox.showinfo("추가 완료", f"실행 어플 '{name}'이 추가되었습니다.")

        self.controller.save()
        self.controller.refresh_all()
        self.cancel_selection()

    def delete_selected(self, _event=None):
        selected = getattr(self.controller, "app_panel_selected_index", None)
        if selected is None:
            messagebox.showwarning("경고", "삭제할 실행 어플을 선택하세요.")
            return

        if messagebox.askyesno("확인", "선택한 어플 경로를 정말 삭제하시겠습니까?"):
            del self.controller.config["apps"][selected]
            self.controller.app_panel_selected_index = None
            self.controller.save()
            self.controller.refresh_all()
            self.cancel_selection()

    def move_up(self):
        selected = getattr(self.controller, "app_panel_selected_index", None)
        if selected is None or selected <= 0:
            return

        items = self.controller.config["apps"]
        items[selected - 1], items[selected] = items[selected], items[selected - 1]
        self.controller.app_panel_selected_index = selected - 1

        self.controller.save()
        self.controller.refresh_all()
        self.listbox.selection_set(self.controller.app_panel_selected_index)
        self.listbox.see(self.controller.app_panel_selected_index)

    def move_down(self):
        selected = getattr(self.controller, "app_panel_selected_index", None)
        items = self.controller.config["apps"]

        if selected is None or selected >= len(items) - 1:
            return

        items[selected + 1], items[selected] = items[selected], items[selected + 1]
        self.controller.app_panel_selected_index = selected + 1

        self.controller.save()
        self.controller.refresh_all()
        self.listbox.selection_set(self.controller.app_panel_selected_index)
        self.listbox.see(self.controller.app_panel_selected_index)