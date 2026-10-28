실행 방법

1. Python 실행
   python main.py

2. 빌드 예시 (PowerShell)
   $env:TCL_LIBRARY = "C:\Python\Python311\tcl\tcl8.6"
   $env:TK_LIBRARY  = "C:\Python\Python311\tcl\tk8.6"
   python -m PyInstaller --noconsole --onedir --add-data "interOpen_config.json;." main.py

구성
- main.py: 앱 시작점
- config_manager.py: 설정 파일 읽기/쓰기
- launcher.py: 브라우저/앱 실행 로직
- models.py: 데이터 모델
- styles.py: 공통 스타일
- ui/main_window.py: 메인 윈도우
- ui/panels/: 브라우저/URL/앱 패널
