# Classcard-Hack
![dependencies](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)![dependencies2](https://img.shields.io/badge/selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white) ![last commit](https://img.shields.io/github/last-commit/NellLucas/classcard_hack/main?color=red&style=for-the-badge) ![license](https://img.shields.io/github/license/NellLucas/classcard_hack?style=for-the-badge)
> ✨ Selenium을 활용한 Classcard 학습 자동화 핵입니다.
## 시연영상
https://user-images.githubusercontent.com/114709497/210046306-8f532d47-3226-4731-841a-382440e74290.mp4

## Features / 지원하는 기능들
- 암기학습(API 변조, 매크로)
- 리콜학습(API 변조, 매크로)
- 스펠학습(API 변조, 매크로)
- 매칭게임(API 변조, 매크로)
- 테스트학습(매크로)
- QuizBattle(매크로)


## Getting Started / 어떻게 시작하나요?

### Prerequisites / 선행 조건

아래 사항들이 설치가 되어있어야합니다.

```
Chrome, Python3
```

### Installing / 설치

아래 사항들로 현 프로젝트에 관한 모듈들을 설치할 수 있습니다.

```
pip install -r requirements.txt
```

### How to use? / 사용 방법

#### 1) 터미널에서 실행 준비
```bash
cd /workspaces/Classcard_Hack1359
pip install -r requirements.txt
```

> 권장: 가상환경을 사용한다면 아래처럼 실행합니다.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2) 컴퓨터용 실행
```bash
python main.py --login-mode auto --device desktop
```

또는 바로 실행 파일을 사용할 수 있습니다.
```bash
python main_desktop.py
```

#### 3) 핸드폰용 실행
```bash
python main.py --login-mode auto --device mobile
```

또는 바로 실행 파일을 사용할 수 있습니다.
```bash
python main_mobile.py
```

#### 4) 로그인 모드 선택
- 자동 로그인:
```bash
python main.py --login-mode auto --device desktop
```
- 수동 로그인:
```bash
python main.py --login-mode manual --device desktop
```

수동 로그인 모드에서는 브라우저 창이 열리고 직접 Classcard에 로그인할 수 있습니다.

#### 5) 확장프로그램 실행
1. Chrome에서 `chrome://extensions`를 엽니다.
2. `압축해제된 확장 프로그램 로드`를 클릭합니다.
3. `extension/classcard_helper` 폴더를 선택합니다.

확장프로그램은 Classcard 페이지를 빠르게 여는 보조 도구로 사용합니다.

#### 옵션 설명
- `--login-mode auto`: 저장된 계정으로 자동 로그인
- `--login-mode manual`: 브라우저에서 직접 로그인
- `--device desktop`: 컴퓨터용 화면 크기
- `--device mobile`: 핸드폰 에뮬레이션 화면 크기

### 바로 실행 파일
- `python main_desktop.py`: 데스크톱 실행
- `python main_mobile.py`: 모바일 에뮬레이션 실행

## Browser Extension

`extension/classcard_helper` 폴더는 Classcard 페이지를 빠르게 여는 Chrome 확장 프로그램입니다.

1. Chrome에서 확장 프로그램 관리 페이지를 엽니다.
2. `압축해제된 확장 프로그램 로드`를 선택합니다.
3. `extension/classcard_helper` 폴더를 선택합니다.

## Issues / 이슈

동작에 문제가 있다면 사용환경과 오류코드를 꼭 남겨주세요.

## Contribution / 기여

소스 수정사항이 있다면 Pull requests를 열어주세요.
여러분들의 Contribution이 프로젝트 완성에 도움이 됩니다. 😘

## License / 라이센스

**Apache 2.0 License**가 적용되어 있습니다.
