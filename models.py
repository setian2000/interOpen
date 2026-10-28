from dataclasses import dataclass, field
from typing import List

# URL 1개를 담는 데이터 구조
# 예: {"url": "https://youtube.com", "open_mode": "tab"}
@dataclass #자동 생성자
class UrlItem:
    url: str
    open_mode: str = "tab"

    # @dataclass가 없으면 이렇게 직접 써야 함
    # def __init__(self, url: str, open_mode: str = "tab"):
    #     self.url = url
    #     self.open_mode = open_mode


    @classmethod #클래스에서 바로 쓰는 변환 함수
    def from_dict(cls, data: dict) -> "UrlItem":
        return cls(
            url=data.get("url", ""),
            open_mode=data.get("open_mode", "tab"),
        )

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "open_mode": self.open_mode,
        }

# 브라우저 1개를 담는 데이터 구조
# 예: Firefox, Edge, Brave, Chrome
@dataclass
class Browser:
    name: str # 브라우저 이름
    path: str # 브라우저 실행 파일 경로
    urls: List[UrlItem] = field(default_factory=list) # 브라우저에서 열 url 목록
    args: List[str] = field(default_factory=list) # 실행시 넘길 인자값
    delay: float = 0.5 # 실행시 딜레이 시간

    @classmethod
    def from_dict(cls, data: dict) -> "Browser":
        raw_urls = data.get("urls", [])
        urls: List[UrlItem] = []
        for item in raw_urls:
            if isinstance(item, str):
                urls.append(UrlItem(url=item, open_mode="tab"))
            else:
                urls.append(UrlItem.from_dict(item))

        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            urls=urls,
            args=data.get("args", []),
            delay=data.get("delay", 0.5),
        )
        # 인스턴스 메서드에서는 보통 self : 인스턴스 자신
        # 클래스 메서드에서는 보통 cls : 클래스 자신
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "urls": [item.to_dict() for item in self.urls],
            "args": self.args,
            "delay": self.delay,
        }

# 실행 앱 1개를 담는 데이터 구조
# 예: Cursor, VSCode, Explorer, Timer, PowerShell
@dataclass
class AppEntry:
    name: str # 실행앱 이름
    path: str # 실행앱 파일 경로
    mode: str = "direct" # 실행 방식 기본값    
    args: List[str] = field(default_factory=list) # 실행시 넘길 인자값

    @classmethod
    def from_dict(cls, data: dict) -> "AppEntry":
        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            mode=data.get("mode", "direct"),
            args=data.get("args", []),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "mode": self.mode,
            "args": self.args,
        }
