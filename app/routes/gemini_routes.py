from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv
import threading
import time
import traceback
import base64
import json
import requests
from google.cloud import texttospeech

# 환경변수 로드
load_dotenv()

# Blueprint 생성
gemini_bp = Blueprint('gemini', __name__)

# Gemini AI 초기화
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# 인메모리 세션 저장소 (실제 서비스에서는 Redis나 DB 사용)
sessions = {}

@gemini_bp.route('/health', methods=['GET'])
def health_check():
    """헬스체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI 간편 요청서 백엔드',
        'timestamp': datetime.now().isoformat(),
        'gemini_api_configured': bool(os.getenv('GEMINI_API_KEY'))
    })

@gemini_bp.route('/chat/sessions', methods=['POST'])
def create_session():
    """새로운 채팅 세션 생성"""
    try:
        session_id = str(uuid.uuid4())
        
        new_session = {
            'id': session_id,
            'messages': [],
            'createdAt': datetime.now().isoformat(),
            'status': 'active'
        }
        
        sessions[session_id] = new_session
        
        return jsonify({
            'sessionId': session_id,
            'createdAt': new_session['createdAt'],
            'status': 'created'
        }), 201
    except Exception as error:
        print(f'Session creation error: {error}')
        return jsonify({'error': '세션 생성 중 오류가 발생했습니다'}), 500

@gemini_bp.route('/chat/sessions/<session_id>/messages', methods=['POST'])
def send_message(session_id):
    """메시지 전송 및 AI 응답"""
    try:
        data = request.get_json()
        content = data.get('content')
        message_type = data.get('type', 'text')

        if not content or not isinstance(content, str):
            return jsonify({'error': '메시지 내용이 필요합니다'}), 400

        # 세션 확인 또는 생성
        if session_id not in sessions:
            sessions[session_id] = {
                'id': session_id,
                'messages': [],
                'createdAt': datetime.now().isoformat(),
                'status': 'active'
            }

        session = sessions[session_id]

        # 사용자 메시지 저장
        user_message = {
            'id': str(uuid.uuid4()),
            'content': content,
            'sender': 'user',
            'timestamp': datetime.now().isoformat(),
            'type': message_type
        }
        
        session['messages'].append(user_message)

        # AI 모델 초기화 - 어르신 친화적 설정
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 수업 예약 챗봇 시스템 프롬프트
        system_prompt = """당신은 어르신들을 위한 친절한 수업 예약 전문 AI 챗봇입니다. 
다음 지침을 정확히 따라 답변해주세요:

## 기본 역할 및 태도
- 존댓말을 사용하고 친근하게 대화하세요
- 복잡한 용어는 쉬운 말로 설명해주세요
- 답변은 간결하고 이해하기 쉽게 작성하세요
- 수업 예약과 관련된 질문과 답변만 하세요

## 수업 예약 프로세스 (반드시 준수)

### 1단계: 수업 관심사 파악
- 사용자가 "○○ 수업이 듣고 싶어"라고 하면
- 해당 주제와 관련된 수업 리스트를 임의로 생성하여 제시
- 각 수업에는 반드시 다음 정보 포함:
  * 수업명
  * 날짜 (예: 12월 15일)
  * 시간 (예: 오전 10시 - 12시)
  * 장소 (예: 문화센터 2층 강의실)

### 2단계: 선호 시간 확인
- 수업 리스트 제시 후 반드시 질문: "몇월 며칠 편한 시간을 말해주세요"
- 사용자가 답변할 때까지 다른 단계로 넘어가지 마세요

### 3단계: 맞춤형 수업 추천
- 시간을 말해주면: "등록된 수업을 조회하여 사용자 맞춤형 수업을 찾아드리겠습니다"
- 임의의 구체적인 날짜/시간으로 수업 제안: "12월 20일 오후 2시 스마트폰 기초 수업은 어떠신가요?"

### 4단계: 예약 처리 (절대 거절 금지!)
- 사용자가 "○○ 수업 예약해줘" 또는 "예약해주세요" 라고 하면 MUST 무조건:
  1. "고객님의 정보를 확인합니다"
  2. "예약 신청을 완료하였습니다. 감사합니다"
  3. 예약 완료 정보 요약
- 절대로 "예약할 수 없습니다", "죄송합니다" 같은 거절 답변 금지!
- 무조건 예약 완료 처리해야 함!

### 5단계: 취소 처리
- 예약 취소 요청 시: "수업 예약을 정상적으로 취소하였습니다"

## 수업 리스트 생성 규칙 (필수)
- 사용자가 수업 리스트 요청 시 "없다"고 하지 말고 무조건 임의로 생성
- 다양한 주제의 수업 제공: 스마트폰/컴퓨터, 건강/운동, 취미활동, 문화/교양
- 각 수업마다 구체적인 시간, 날짜, 장소 정보 포함

## 금지 사항 (절대 준수!)
- 수업 예약 요청시 절대 거절하면 안됨! 무조건 예약 완료!
- "예약할 수 없습니다", "죄송합니다", "불가능합니다" 같은 거절 표현 절대 금지!
- "수업이 없습니다" 같은 거절 답변 금지
- 수업과 관련 없는 정보나 잡담 금지
- 단계를 건너뛰거나 순서를 바꾸지 마세요

## 핵심 규칙 (반드시 기억!)
- 사용자가 "예약해줘", "예약해주세요", "신청해줘" 등의 표현을 쓰면 → 무조건 "예약 신청을 완료하였습니다. 감사합니다"
- 어떤 이유로도 예약을 거절하지 마세요!
- 항상 예약이 가능하다고 가정하고 처리하세요!

## 응답 예시
사용자: "스마트폰 수업 듣고 싶어요"
챗봇: "스마트폰 관련 수업 리스트를 안내해드리겠습니다.

📱 스마트폰 기초 교실 - 12월 15일 오전 10시~12시 (문화센터 2층)
📷 카메라와 사진 편집 - 12월 18일 오후 2시~4시 (복지관 3층)  
💬 카카오톡 완전정복 - 12월 20일 오전 11시~1시 (도서관 강의실)

몇월 며칠 편한 시간을 말해주세요."

사용자: "스마트폰 기초 교실 예약해줘"
챗봇: "고객님의 정보를 확인합니다. 예약 신청을 완료하였습니다. 감사합니다.

📱 예약 완료 내역
- 수업명: 스마트폰 기초 교실
- 날짜: 12월 15일 오전 10시~12시
- 장소: 문화센터 2층"

이 지침을 정확히 따라 어르신들이 쉽게 수업을 예약할 수 있도록 도와주세요."""

        # 채팅 히스토리 구성
        chat_history = []
        for msg in session['messages'][-10:]:  # 최근 10개 메시지만 사용
            if msg['sender'] == 'user':
                chat_history.append({'role': 'user', 'parts': [msg['content']]})
            elif msg['sender'] == 'assistant':
                chat_history.append({'role': 'model', 'parts': [msg['content']]})

        # AI 응답 생성
        try:
            if len(chat_history) == 1:  # 첫 번째 메시지인 경우
                prompt = f"{system_prompt}\n\n사용자 메시지: {content}"
            else:
                prompt = content

            response = model.generate_content(prompt)
            ai_response = response.text

        except Exception as ai_error:
            print(f'AI generation error: {ai_error}')
            ai_response = "죄송합니다. 현재 AI 서비스에 일시적인 문제가 있습니다. 잠시 후 다시 시도해주세요."

        # AI 응답 메시지 저장
        ai_message = {
            'id': str(uuid.uuid4()),
            'content': ai_response,
            'sender': 'assistant',
            'timestamp': datetime.now().isoformat(),
            'type': 'text'
        }
        
        session['messages'].append(ai_message)
        session['updatedAt'] = datetime.now().isoformat()

        return jsonify({
            'message': ai_message,
            'sessionId': session_id
        })

    except Exception as error:
        print(f'Message processing error: {error}')
        print(traceback.format_exc())
        return jsonify({'error': '메시지 처리 중 오류가 발생했습니다'}), 500

@gemini_bp.route('/chat/sessions/<session_id>/messages', methods=['GET'])
def get_messages(session_id):
    """세션의 메시지 목록 조회"""
    try:
        if session_id not in sessions:
            return jsonify({'error': '세션을 찾을 수 없습니다'}), 404

        session = sessions[session_id]
        
        return jsonify({
            'sessionId': session_id,
            'messages': session['messages'],
            'totalCount': len(session['messages'])
        })
    except Exception as error:
        print(f'Get messages error: {error}')
        return jsonify({'error': '메시지 조회 중 오류가 발생했습니다'}), 500

@gemini_bp.route('/chat/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """세션 상태 확인"""
    try:
        if session_id not in sessions:
            return jsonify({'error': '세션을 찾을 수 없습니다'}), 404

        session = sessions[session_id]

        return jsonify({
            'sessionId': session['id'],
            'status': session['status'],
            'lastActivityAt': session.get('updatedAt', session['createdAt']),
            'messageCount': len(session['messages'])
        })
    except Exception as error:
        print(f'Session status error: {error}')
        return jsonify({'error': '세션 상태 확인 중 오류가 발생했습니다'}), 500

@gemini_bp.route('/chat/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """세션 삭제"""
    try:
        if session_id not in sessions:
            return jsonify({'error': '세션을 찾을 수 없습니다'}), 404

        del sessions[session_id]

        return jsonify({'message': '세션이 삭제되었습니다'})
    except Exception as error:
        print(f'Session delete error: {error}')
        return jsonify({'error': '세션 삭제 중 오류가 발생했습니다'}), 500

# 세션 정리 함수 (백그라운드에서 실행)
def cleanup_sessions():
    """30분마다 비활성 세션을 정리합니다"""
    while True:
        try:
            time.sleep(1800)  # 30분마다 실행
            now = datetime.now()
            thirty_minutes_ago = now - timedelta(minutes=30)

            sessions_to_delete = []
            for session_id, session in sessions.items():
                try:
                    last_activity_str = session.get('updatedAt', session['createdAt'])
                    last_activity = datetime.fromisoformat(last_activity_str.replace('Z', '+00:00'))

                    # UTC 시간 처리
                    if last_activity.tzinfo is None:
                        last_activity = last_activity.replace(tzinfo=None)
                        if last_activity < thirty_minutes_ago:
                            sessions_to_delete.append(session_id)
                except Exception as e:
                    print(f'Error checking session {session_id}: {e}')
                    # 파싱 오류가 있는 세션은 삭제
                    sessions_to_delete.append(session_id)

            for session_id in sessions_to_delete:
                if session_id in sessions:
                    del sessions[session_id]
                    print(f'Session {session_id} cleaned up due to inactivity')

        except Exception as e:
            print(f'Error in cleanup_sessions: {e}')

# 백그라운드에서 세션 정리 시작
cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()

@gemini_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """음성을 텍스트로 변환"""
    try:
        # 요청에서 음성 데이터 가져오기
        if 'audio' not in request.files:
            return jsonify({'error': '음성 파일이 필요합니다'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': '음성 파일이 선택되지 않았습니다'}), 400

        # 음성 파일을 base64로 인코딩
        audio_content = audio_file.read()
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')

        # Google Speech-to-Text API 호출
        api_key = os.getenv('GOOGLE_SPEECH_API_KEY')
        if not api_key:
            return jsonify({'error': 'Google Speech API 키가 설정되지 않았습니다'}), 500

        # API 요청 데이터 구성
        request_data = {
            "config": {
                "encoding": "WEBM_OPUS",  # 웹에서 녹음된 오디오 형식
                "sampleRateHertz": 48000,
                "languageCode": "ko-KR",  # 한국어
                "enableAutomaticPunctuation": True,  # 자동 구두점
                "model": "latest_short"  # 짧은 오디오에 최적화
            },
            "audio": {
                "content": audio_base64
            }
        }

        # Google Speech-to-Text API 호출
        api_url = f"https://speech.googleapis.com/v1/speech:recognize?key={api_key}"
        
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(request_data),
            timeout=30
        )

        if response.status_code != 200:
            print(f'Google Speech API error: {response.status_code} - {response.text}')
            return jsonify({'error': 'Google Speech API 호출 중 오류가 발생했습니다'}), 500

        result = response.json()
        
        # 결과에서 텍스트 추출
        if 'results' in result and len(result['results']) > 0:
            transcript = result['results'][0]['alternatives'][0]['transcript']
            confidence = result['results'][0]['alternatives'][0].get('confidence', 0.0)
            
            return jsonify({
                'success': True,
                'transcript': transcript,
                'confidence': confidence
            })
        else:
            return jsonify({
                'success': False,
                'transcript': '',
                'message': '음성을 인식할 수 없습니다. 다시 시도해주세요.'
            })

    except Exception as error:
        print(f'Speech-to-text error: {error}')
        print(traceback.format_exc())
        return jsonify({'error': '음성 인식 중 오류가 발생했습니다'}), 500

@gemini_bp.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """텍스트를 음성으로 변환"""
    try:
        # 요청에서 텍스트 데이터 가져오기
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': '변환할 텍스트가 필요합니다'}), 400

        # Google TTS API 키 확인
        api_key = os.getenv('GOOGLE_SPEECH_API_KEY')
        if not api_key:
            return jsonify({'error': 'Google Speech API 키가 설정되지 않았습니다'}), 500

        # Google Text-to-Speech API 호출
        tts_request_data = {
            "input": {"text": text},
            "voice": {
                "languageCode": "ko-KR",
                "name": "ko-KR-Wavenet-A",  # 자연스러운 한국어 여성 음성
                "ssmlGender": "FEMALE"
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": 0.9,  # 말하기 속도 (0.25 ~ 4.0)
                "pitch": 0.0,         # 음성 높이 (-20.0 ~ 20.0)
                "volumeGainDb": 0.0   # 볼륨 조정 (-96.0 ~ 16.0)
            }
        }

        # API 호출
        api_url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
        
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(tts_request_data),
            timeout=30
        )

        if response.status_code != 200:
            print(f'Google TTS API error: {response.status_code} - {response.text}')
            return jsonify({'error': 'Google TTS API 호출 중 오류가 발생했습니다'}), 500

        result = response.json()
        
        # 결과에서 오디오 데이터 추출
        if 'audioContent' in result:
            audio_content = result['audioContent']
            
            return jsonify({
                'success': True,
                'audioContent': audio_content,  # Base64 인코딩된 MP3 데이터
                'format': 'mp3'
            })
        else:
            return jsonify({
                'success': False,
                'message': '음성 합성에 실패했습니다.'
            })

    except Exception as error:
        print(f'Text-to-speech error: {error}')
        print(traceback.format_exc())
        return jsonify({'error': '음성 합성 중 오류가 발생했습니다'}), 500 