# 테스트 자동화 프로젝트
> 이 프로젝트는 솔루션 Motion E GUI 체크리스트 자동화 기능 검증 수행하기 위해 구성된 테스트 자동화 저장소입니다.


# 테스트 목적 및 범위
- 프로그램 실행
- 로그인
  - 계정 로그인
- 대시보드
  - 환자 생성/예약/접수, 예약/접수 취소, 공지사항 추가/삭제
- 환자 차트
  - 사이드 메모 작성/사이드 차트 진입
  - 신규예약 생성/변경/예약내역 확인
  - 시술 저장/티켓팅 사용
  - 진료 저장, 처방전 출력
  - 펜차트/진료사진/동의서 CRUD
  - 수납, 환불, 수납취소, 미수처리
- 청구
  - 진료 데이터 생성 확인



# 사용 기술 및 도구
```
언어: Python
사용 라이브러리: Pywinauto, pyautogui, functools, PIL
구조 분석 툴: InspectX

Inspect 다운로드(필수아님)
https://github.com/yinkaisheng/Python-UIAutomation-for-Windows/tree/master/inspect
> 해당 프로그램 관리자 권한으로 실행(Motion 진입 불가)

```

# 테스트 실행 방법
- Motion E 설치가 되어있어야 합니다.
1. cmd 창을 관리자권한으로 실행합니다.
2. 해당 저장소가 저장되어있는 위치로 이동합니다.
3. main.py 파일을 파이썬을 통해 실행합니다.

# 디렉토리 구조
```
Motion-E/
├── dto/
|   ├── user_dto.py
├── locators/
|   ├── chart_locators.py
|   ├── dashboard_locators.py
|   ├── login_locators.py
|   ├── nav_locators.py
|   ├── receive_locators.py
|   ├── side_field_locators.py
|   ├── util_locators.py
|
├── pages/
|   ├── base_page.py
|   ├── chart_page.py
|   ├── dashboard_page.py
|   ├── login_page.py
|   ├── receive_page.py
|   ├── reservation_tab_page.py
|   ├── side_chart_page.py
|   ├── side_page.py
|   ├── user_save_page.py
|
├── tests/
|   ├── test_chart.py
|   ├── test_dashboard_page.py
|   ├── test_login.py
| 
├── utils/
|   ├── app_manager.py
|   ├── app_screen_shot.py
|   ├── element_finder.py
|   ├── multi_processing.py
|
├── .gitignore
├── README.md
├── main.py
├── package-lock.json
├── package.json
└── requirements.txt
```
dto/: 데이터 전송 객체(Data Transfer Objects)를 정의
locators/: 요소의 위치를 지정하는 로케이터
pages/: 페이지 객체 모델(POM, Page Object Model)을 따르며, UI 테스트 시 실제 페이지의 동작을 추상화
tests/: 테스트 케이스를 포함하며, 각 기능에 대한 검증을 수행
utils/: 유틸리티 함수 및 공통 모듈을 포함
