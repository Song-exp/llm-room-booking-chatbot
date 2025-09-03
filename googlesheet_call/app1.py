import requests
import os
import json
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv
import re

# .env 파일 로드 (로컬 테스트용)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['JSON_AS_ASCII'] = False
CORS(app, resources={r"/*": {"origins": "*"}})

# 환경 변수 설정
DEFAULT_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SERVICE_ACCOUNT_KEY = os.getenv("SERVICE_ACCOUNT_KEY")

def read_google_sheet(sheet_id, sheet_name):
    try:
        # JSON 데이터를 환경 변수에서 로드
        service_account_info = json.loads(SERVICE_ACCOUNT_KEY)
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")  # 줄바꿈 처리

        # Google API 인증
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build('sheets', 'v4', credentials=credentials)

        # 특정 시트 데이터 가져오기
        range_name = f"{sheet_name}"
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_name
        ).execute()

        # 데이터프레임 변환
        df = pd.DataFrame(result.get('values', []))
        df.columns = df.loc[0]  # 첫 번째 행을 열 이름으로 설정
        df = df[1:]  # 첫 번째 행 제거
        df = df.set_index(df.columns[0])  # 첫 번째 열을 인덱스로 설정

        return df.to_dict(orient="records")  # 데이터프레임을 딕셔너리로 변환

    except Exception as e:
        raise RuntimeError(f"Error reading Google Sheet: {str(e)}")

def append_row_to_sheet(sheet_id, sheet_name, row_data):
    try:
        # JSON 데이터를 환경 변수에서 로드
        service_account_info = json.loads(SERVICE_ACCOUNT_KEY)
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")  # 줄바꿈 처리

        # Google API 인증
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build('sheets', 'v4', credentials=credentials)

        # 데이터를 추가할 Google Sheet 범위 지정
        range_name = f"{sheet_name}!A1"

        # 데이터 추가 요청 생성
        body = {
            "values": [row_data]  # 단일 행을 리스트로 감싸야 합니다
        }
        response = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="RAW",  # 데이터 입력 방식: RAW 또는 USER_ENTERED
            insertDataOption="INSERT_ROWS",  # 행 삽입 방식
            body=body
        ).execute()

        print(f"Row successfully added to Google Sheet: {response}")
        return response

    except Exception as e:
        raise RuntimeError(f"Error appending row to Google Sheet: {str(e)}")


# 사용자 인증 정보
Authentication_dict = {
    '송정현': '2022103121',
    '김소륜': '2022103110',
    '임현우': '2023102782',
    '김가현': '2023102759',
}


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # 로그인 페이지 렌더링

    elif request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username')
        student_id = data.get('student_id')

        if username in Authentication_dict and Authentication_dict[username] == student_id:
            # 세션에 사용자 정보 저장 및 메시지 초기화
            session['username'] = username
            session['user_messages'] = []  # 대화 기록 초기화
            return jsonify({"success": True, "redirect": f"/chat?username={username}"}), 200
        else:
            return jsonify({"success": False, "message": "Invalid username or student ID"}), 400


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        username = session.get('username')
        if not username:
            return jsonify({"error": "No active session"}), 401

        # 초기 메시지 설정
        if not session.get('user_messages'):
            session['user_messages'] = [
                {"role": "assistant", "content": "안녕하세요! 경영대 장소 대여 포털입니다. 원하는 날짜를 입력해주세요!"}
            ]

        # 가장 최근 메시지 반환
        initial_message = session['user_messages'][-1]['content']
        return render_template('chat.html', initial_message=initial_message)

    elif request.method == 'POST':
        data = request.get_json()
        if not username:
                    return jsonify({"error": "사용자 이름이 필요합니다."}), 400

                min_people = data.get('minPeople')  # 최소 사용 인원 수
                userchat = data.get('userchat')  # 원하는 날짜
            
                # 프로젝트 및 API 관련 설정
                project_code = os.getenv("PROJECT_CODE")
                api_key = os.getenv("API_KEY")
                hash = os.getenv("API_HASH")
                laas_chat_url = "https://api-laas.wanted.co.kr/api/preset/v2/chat/completions"

                headers = {
                    "project": project_code,
                    "apiKey": api_key,
                    "Content-Type": "application/json; charset=utf-8"
                }
        
        # 사용자 입력 메시지 추가
        user_message = {"role": "user", "content": f"최소 사용 인원: {min_people}, 날짜: {userchat}"}
        session['user_messages'].append(user_message)

        # 사용자 입력을 Google Sheets에 저장
        append_row_to_sheet(DEFAULT_SHEET_ID, "대화기록", [username, "user", user_message['content']])

        # 어시스턴트 응답 추가
        assistant_message = {"role": "assistant", "content": "요청이 처리되었습니다."}
        session['user_messages'].append(assistant_message)

        # 어시스턴트 응답을 Google Sheets에 저장
        append_row_to_sheet(DEFAULT_SHEET_ID, "대화기록", [username, "assistant", assistant_message['content']])

        return jsonify({"success": True, "assistant_message": assistant_message['content']}), 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=3000)
