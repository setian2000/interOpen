import json
import sys
from pathlib import Path

from models import AppEntry, Browser


class ConfigManager:
    def __init__(self):
        # 설정 파일이 어느 폴더에 있어야 하는지 정함
        # .py로 실행할 때와 .exe로 실행할 때 기준 폴더를 다르게 잡음
        if getattr(sys, "frozen", False):
            # exe 파일 실행시 실행 파일(.exe)이 있는 폴더 사용
            self.base_dir = Path(sys.executable).parent.resolve()
        else:
            # 일반 파이썬 실행이면 현재 .py 파일이 있는 폴더 기준
            self.base_dir = Path(__file__).parent.resolve()
        self.config_file = self.base_dir / "interOpen_config.json"

    def load(self) -> dict: 
        # 설정 파일이 없으면 기본 설정으로 생성
        if not self.config_file.exists():
            default_config = {"browsers": [], "apps": []}
            self.save(default_config)
            return default_config

        # 설정 파일이 있으면 UTF-8로 열어서 JSON 읽기
        with open(self.config_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 브라우저와 앱 리스트가 없으면 빈 리스트로 초기화
        data.setdefault("browsers", [])
        data.setdefault("apps", [])

        browsers = [Browser.from_dict(item).to_dict() for item in data["browsers"]] # 누락된 기본값 채우기
        apps = [AppEntry.from_dict(item).to_dict() for item in data["apps"]]
        return {"browsers": browsers, "apps": apps}

    def save(self, data: dict) -> None:
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
