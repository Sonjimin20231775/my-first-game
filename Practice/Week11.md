# Week 11 실습

## 오늘 한 것
- PyInstaller 설치 및 빌드
- resource_path() 함수 푸가
- --add-data 옵션으로 에셋 포함
- .exe 실행 확인

## resource_path() 를 써야 하는 이유
(Assets/Sounds/Interact.wav) 처럼 외부 파일을 이용하는 경우 resource_path()없이 빌드할 경우 
정상적인 실행이 안되거나 .exe 파일의 위치를 옮길 경우 정상적으로 실행되지 않을 수 있기 때문에 resource_path()를 사용한다.

## 빌드 명령어
### pyinstaller --onefile game.py
- 기본적인 pyinstaller 형태

### pyinstaller --onefile --windowed game.py
- --windowed를 추가하여 터미널을 숨긴 형태로 배포하는 용도에 사용된다.

### pyinstaller --onefile --windowed --add-data "assets;assets" --name=MyGame game.py
- --add-data "assets;assets"을 통해 외부 에셋을 포함할 수 있고, --name=MyGame을 통해 .exe 파일의 이름을 지정할 수 있다.

## AI 활용 내역
1. 내가 만든 게임에는 외부 파일 외에 base64 형태를 사용한 것들도 많기 때문에 이러한 파일에도 resource_path()를 사용해야 하는지, 사용하지 않는다면 왜 사용하지 않는지를 질문을 통해 답변을 얻었다.
2. pyinstaller하는 과정에서 실행이 안되거나 하는 오류가 생겨 왜 그러는지 아는데 도움을 받았다.
