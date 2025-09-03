# 프롬프톤 프로젝트

## 📋 프로젝트 개요
경희대학교와 원티드가 주최하는 프롬프톤 공모전 프로젝트입니다.
Google Sheets API를 활용한 강의실 관리 시스템을 구현했습니다.

## 🏗️ 프로젝트 구조
```
프롬프톤/
├── 📁 api/                    # API 관련 파일들
│   ├── index.py              # 메인 API 파일
│   └── requirements.txt      # Python 의존성
├── 📁 googlesheet_call/      # Google Sheets 연동 애플리케이션
│   ├── app.py               # 메인 Flask 애플리케이션
│   ├── app1.py              # 보조 애플리케이션
│   ├── requirements.txt     # Python 의존성
│   ├── templates/           # HTML 템플릿
│   │   ├── chat.html       # 채팅 인터페이스
│   │   ├── login.html      # 로그인 페이지
│   │   └── images/         # 이미지 리소스
│   └── README.md           # 하위 프로젝트 설명
├── 📊 data/                  # 데이터 파일들
│   ├── 강의실(월).csv      # 월요일 강의실 데이터
│   ├── 강의실(화).csv      # 화요일 강의실 데이터
│   ├── 강의실(수).csv      # 수요일 강의실 데이터
│   └── 강의실(일).csv      # 일요일 강의실 데이터
├── 🔧 scripts/               # 유틸리티 스크립트
│   ├── app_sheet.py        # Google Sheets 연동 스크립트
│   ├── excel_to_csv.ipynb  # Excel to CSV 변환 노트북
│   └── load_sheet_api.ipynb # Google Sheets API 로드 노트북
├── 🚀 deploy/                # 배포 관련 파일
│   └── vercel.json         # Vercel 배포 설정
├── .gitignore               # Git 무시 파일 목록
└── README.md               # 프로젝트 메인 설명서
```

## ✨ 주요 기능
- **Google Sheets API 연동**: 실시간 데이터 동기화
- **강의실 정보 관리**: 요일별 강의실 데이터 관리
- **웹 애플리케이션**: Flask 기반 사용자 인터페이스
- **데이터 변환**: Excel ↔ CSV 변환 도구

## 🛠️ 기술 스택
- **Backend**: Python, Flask
- **API**: Google Sheets API
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **Data Processing**: Jupyter Notebook, Pandas

## 📥 설치 및 실행

### 1. 환경 설정
```bash
# Python 3.7+ 설치 필요
python --version

# 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2. 의존성 설치
```bash
# API 서버 의존성
pip install -r api/requirements.txt

# 웹 애플리케이션 의존성
pip install -r googlesheet_call/requirements.txt
```

### 3. Google Cloud 설정
1. Google Cloud Console에서 프로젝트 생성
2. Google Sheets API 활성화
3. 서비스 계정 키 생성 및 다운로드
4. `db3clothbtitest-b2ab2e525277.json` 파일을 프로젝트 루트에 배치

### 4. 애플리케이션 실행
```bash
# API 서버 실행
cd api
python index.py

# 웹 애플리케이션 실행
cd googlesheet_call
python app.py
```

## 🔒 보안 주의사항
- **중요**: `db3clothbtitest-b2ab2e525277.json` 파일은 Google Cloud 서비스 계정 키입니다
- 이 파일은 절대 공개 저장소에 업로드하지 마세요
- `.gitignore`에 포함되어 있지만, 추가 보안 조치를 권장합니다

## 📝 사용법
1. 웹 애플리케이션에 접속
2. Google 계정으로 로그인
3. 강의실 데이터 조회 및 관리
4. API를 통한 데이터 접근

## 🤝 기여 방법
1. 이 저장소를 Fork
2. 새로운 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📄 라이선스
이 프로젝트는 교육 목적으로 제작되었습니다.

## 📞 문의
프로젝트 관련 문의사항이 있으시면 이슈를 생성해주세요.
