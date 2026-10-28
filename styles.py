import tkinter as tk

ROOT_BG = "#f5f7fb"

BROWSER_BG = "#eef6ff"
BROWSER_TITLE_FG = "#1f4e79"
BROWSER_SELECT_BG = "#cfe5ff"

URL_BG = "#f4f9ff"
URL_TITLE_FG = "#2b5d87"
URL_SELECT_BG = "#d8ecff"

APP_BG = "#e7dcff"
APP_TITLE_FG = "#45246f"
APP_SELECT_BG = "#c8b3ff"

BTN_BLUE = "#4a90e2"
BTN_BLUE_ACTIVE = "#357abd"
BTN_SKY = "#5aa9e6"
BTN_SKY_ACTIVE = "#3f92d3"
BTN_PURPLE = "#6a43c7"
BTN_PURPLE_ACTIVE = "#5533a6"
BTN_RED = "#d9534f"
BTN_RED_ACTIVE = "#c9302c"
BTN_GRAY = "#6c757d"
BTN_GRAY_ACTIVE = "#5a6268"
BTN_ORDER = "#ffffff"
BTN_ORDER_ACTIVE = "#e9ecef"
RUN_BTN_BG = "#0066cc"
RUN_BTN_ACTIVE = "#0052a3"


def make_button(parent, text, command, width=10, bg=BTN_BLUE, active=BTN_BLUE_ACTIVE, fg="white"):
    return tk.Button(
        parent,
        text=text,
        width=width,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active,
        activeforeground=fg,
        relief="flat",
        bd=0,
        font=("맑은 고딕", 9, "bold"),
        cursor="hand2",
        padx=6,
        pady=4,
    )


def make_order_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        width=8,
        command=command,
        bg=BTN_ORDER,
        fg="#333333",
        activebackground=BTN_ORDER_ACTIVE,
        activeforeground="#111111",
        relief="solid",
        bd=1,
        font=("맑은 고딕", 9, "bold"),
        cursor="hand2",
        padx=4,
        pady=3,
    )
