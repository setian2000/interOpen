import os
import subprocess
import time
from pathlib import Path


class AppLauncher:
    def __init__(self, config: dict):
        self.config = config or {"browsers": [], "apps": []}

    def set_config(self, config: dict) -> None:
        self.config = config or {"browsers": [], "apps": []}

    def spawn_detached(self, command):
        flags = 0

        if os.name == "nt":
            flags = (
                subprocess.CREATE_NEW_PROCESS_GROUP
                | subprocess.DETACHED_PROCESS
            )

        return subprocess.Popen(
            command,
            creationflags=flags,
            close_fds=True,
        )

    def build_browser_command(self, name, args, open_mode, urls):
        name = (name or "").lower()
        base_args = list(args) if args else []

        if name in ["chrome", "edge", "whale", "comet", "brave", "opera"]:
            if open_mode == "window":
                return base_args + ["--new-window"] + urls
            return base_args + urls

        if name == "firefox":
            if open_mode == "window":
                return base_args + ["-new-window"] + urls
            return base_args + urls

        return base_args + urls

    def run_browser(self, browser: dict):
        name = browser.get("name", "unknown")
        path = browser.get("path")
        url_items = browser.get("urls", [])
        args = browser.get("args", [])
        delay = browser.get("delay", 0.5)

        if not path or not url_items:
            return

        if not Path(path).exists():
            print(f"Warning: {name} 실행 파일을 찾을 수 없습니다.")
            return

        normalized_items = []
        for item in url_items:
            if isinstance(item, str):
                normalized_items.append({
                    "url": item.strip(),
                    "open_mode": "tab",
                })
            else:
                normalized_items.append({
                    "url": item.get("url", "").strip(),
                    "open_mode": item.get("open_mode", "tab"),
                })

        normalized_items = [x for x in normalized_items if x["url"]]
        if not normalized_items:
            return

        if len(normalized_items) == 1:
            only_url = normalized_items[0]["url"]
            launch_args = self.build_browser_command(name, args, "window", [only_url])
            self.spawn_detached([path] + launch_args)
            if delay > 0:
                time.sleep(delay)
            return

        tab_urls = [x["url"] for x in normalized_items if x["open_mode"] != "window"]
        window_urls = [x["url"] for x in normalized_items if x["open_mode"] == "window"]

        if tab_urls:
            launch_args = self.build_browser_command(name, args, "tab", tab_urls)
            self.spawn_detached([path] + launch_args)
            if delay > 0:
                time.sleep(delay)

        for url in window_urls:
            launch_args = self.build_browser_command(name, args, "window", [url])
            self.spawn_detached([path] + launch_args)
            if delay > 0:
                time.sleep(delay)

    def run_app(self, app: dict):
        name = app.get("name", "unknown")
        path = app.get("path")
        mode = app.get("mode", "direct")
        args = app.get("args", [])

        if not path:
            return

        if not Path(path).exists():
            print(f"Warning: {name} 경로를 찾을 수 없습니다.")
            return

        command = [str(path)] + list(args)

        if mode == "file" or str(path).lower().endswith(".lnk"):
            os.startfile(path)
        elif mode == "cmd":
            subprocess.Popen(["cmd", "/c", "start", "", str(path), *args], shell=True)
        else:
            subprocess.Popen(command)

    def open_all(self):
        for browser in self.config.get("browsers", []):
            self.run_browser(browser)

        for app in self.config.get("apps", []):
            self.run_app(app)