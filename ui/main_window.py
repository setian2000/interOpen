import tkinter as tk
from tkinter import messagebox

from styles import ROOT_BG, RUN_BTN_ACTIVE, RUN_BTN_BG
from ui.panels.app_panel import AppPanel
from ui.panels.browser_panel import BrowserPanel
from ui.panels.url_panel import UrlPanel


class MainWindow:
    def __init__(self, root, config, config_manager, launcher):
        self.root = root
        self.config = config
        self.config_manager = config_manager
        self.launcher = launcher

        self.root.title("인터넷 오픈 런처")
        self.root.geometry("1020x980")
        self.root.resizable(True, True)
        self.root.configure(bg=ROOT_BG)

        self.browser_panel = BrowserPanel(root, self)
        self.browser_panel.frame.pack(fill="x", padx=15, pady=10)

        self.url_panel = UrlPanel(root, self)
        self.url_panel.frame.pack(fill="x", padx=15, pady=10)

        self.app_panel = AppPanel(root, self)
        self.app_panel.frame.pack(fill="x", padx=15, pady=10)

        self._build_bottom()
        self.refresh_all()

    def _build_bottom(self):
        bottom = tk.Frame(self.root, bg=ROOT_BG)
        bottom.pack(fill="x", padx=10, pady=(5, 5))

        self.btn_launch_all = tk.Button(
            bottom,
            text="전체 실행",
            font=("맑은 고딕", 12, "bold"),
            bg=RUN_BTN_BG,
            fg="white",
            activebackground=RUN_BTN_ACTIVE,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=20,
            height=2,
            command=self.launch_all_urls,
        )
        self.btn_launch_all.pack(pady=10)

    def save(self):
        self.config_manager.save(self.config)
        self.launcher.set_config(self.config)

    def refresh_all(self):
        self.browser_panel.refresh()
        self.url_panel.refresh()
        self.app_panel.refresh()
        self.launcher.set_config(self.config)

    def launch_all_urls(self):
        try:
            self.launcher.open_all()
            messagebox.showinfo("실행 완료", "모든 브라우저와 실행 어플을 실행했습니다!")
        except Exception as e:
            messagebox.showerror("실행 오류", f"실행 중 문제가 발생했습니다:\n{e}")

    def run(self):
        self.root.mainloop()
