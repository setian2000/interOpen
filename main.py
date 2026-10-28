import tkinter as tk

from config_manager import ConfigManager
from launcher import AppLauncher
from ui.main_window import MainWindow

################ 파일 구조 ################
'''
- main.py: 앱 시작점
- config_manager.py: 설정 파일 읽기/쓰기
- launcher.py: 브라우저/앱 실행 로직
- models.py: 데이터 모델
- styles.py: 공통 스타일
- ui/main_window.py: 메인 윈도우
- ui/panels/: 브라우저/URL/앱 패널
'''
###########################################

def main():
    config_manager = ConfigManager()
    config = config_manager.load()
    launcher = AppLauncher(config)

    root = tk.Tk()
    app = MainWindow(
        root = root,
        config = config,
        config_manager = config_manager,
        launcher = launcher,
    )
    app.run()

if __name__ == "__main__":
    main()
