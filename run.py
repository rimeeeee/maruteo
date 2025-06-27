import os
from app import create_app


from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv
import threading
import time
import traceback

# 환경변수 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)

# CORS 설정 - Vite 개발 서버 포트에 맞게
CORS(app, origins=[os.getenv('CORS_ORIGIN', 'http://localhost:5173')], supports_credentials=True)

# Gemini AI 초기화
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# 인메모리 세션 저장소 (실제 서비스에서는 Redis나 DB 사용)
sessions = {}

# 헬스체크 엔드포인트
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK', 
        'message': 'AI 간편 요청서 백엔드가 실행 중입니다'
    })

# 새 채팅 세션 생성
@app.route('/api/chat/sessions', methods=['POST'])
def create_session():
    try:
        session_id = str(uuid.uuid4())
        session = {
            'id': session_id,
            'messages': [],
            'createdAt': datetime.now().isoformat(),
            'status': 'active'
        }
        
        sessions[session_id] = session
        
        return jsonify({
            'sessionId': session_id,
            'createdAt': session['createdAt'],
            'status': session['status']
        })
    except Exception as error:
        print(f'Session creation error: {error}')
        return jsonify({'error': '세션 생성 중 오류가 발생했습니다'}), 500

# 메시지 전송 및 AI 응답
@app.route('/api/chat/sessions/<session_id>/messages', methods=['POST'])
def send_message(session_id):
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
        
        # 어르신을 위한 시스템 프롬프트
        system_prompt = """당신은 어르신들을 위한 친절한 AI 도우미입니다. 
다음 지침을 따라 답변해주세요:
1. 존댓말을 사용하고 친근하게 대화하세요
2. 복잡한 용어는 쉬운 말로 설명해주세요  
3. 어르신이 배우고 싶어하는 내용에 맞는 적절한 프로그램이나 강의를 추천해주세요
4. 답변은 간결하고 이해하기 쉽게 작성하세요
5. 어르신의 관심사(스마트폰, 건강, 취미 등)에 따라 맞춤형 프로그램을 제안하세요"""

        # 채팅 히스토리 구성
        chat_history = []
        
        # 기존 메시지들을 히스토리에 추가 (현재 메시지 제외)
        for msg in session['messages'][:-1]:
            role = 'user' if msg['sender'] == 'user' else 'model'
            chat_history.append({
                'role': role,
                'parts': [{'text': msg['content']}]
            })

        # 채팅 세션 시작
        chat = model.start_chat(history=chat_history)
        
        # 첫 메시지인 경우 시스템 프롬프트 포함
        if len(session['messages']) == 1:
            full_content = f"{system_prompt}\n\n사용자 메시지: {content}"
        else:
            full_content = content

        # AI 응답 생성
        response = chat.send_message(full_content)
        ai_response_text = response.text

        # AI 응답 저장
        ai_message = {
            'id': str(uuid.uuid4()),
            'content': ai_response_text,
            'sender': 'ai',
            'timestamp': datetime.now().isoformat(),
            'type': 'text'
        }
        
        session['messages'].append(ai_message)
        session['updatedAt'] = datetime.now().isoformat()

        return jsonify({
            'userMessage': user_message,
            'aiResponse': ai_message
        })

    except Exception as error:
        print(f'Message send error: {error}')
        print(f'Traceback: {traceback.format_exc()}')
        
        error_str = str(error)
        if 'API_KEY' in error_str or 'API key' in error_str:
            return jsonify({'error': 'API 키 설정을 확인해주세요'}), 401
        
        return jsonify({
            'error': '메시지 처리 중 오류가 발생했습니다',
            'details': error_str if os.getenv('NODE_ENV') == 'development' else '서버 오류'
        }), 500

# 세션 메시지 히스토리 조회
@app.route('/api/chat/sessions/<session_id>/messages', methods=['GET'])
def get_messages(session_id):
    try:
        if session_id not in sessions:
            return jsonify({'error': '세션을 찾을 수 없습니다'}), 404
        
        session = sessions[session_id]
        
        return jsonify({
            'messages': session['messages'],
            'totalCount': len(session['messages'])
        })
    except Exception as error:
        print(f'Get messages error: {error}')
        return jsonify({'error': '메시지 조회 중 오류가 발생했습니다'}), 500

# 세션 상태 확인
@app.route('/api/chat/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
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

# 세션 삭제
@app.route('/api/chat/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        if session_id not in sessions:
            return jsonify({'error': '세션을 찾을 수 없습니다'}), 404
        
        del sessions[session_id]
        
        return jsonify({'message': '세션이 삭제되었습니다'})
    except Exception as error:
        print(f'Session delete error: {error}')
        return jsonify({'error': '세션 삭제 중 오류가 발생했습니다'}), 500

# 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '요청한 경로를 찾을 수 없습니다'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '서버에서 오류가 발생했습니다'}), 500

# 세션 정리 함수 (백그라운드 실행)
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
                    # 파싱 에러가 있는 세션은 삭제
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

if __name__ == '__main__':

    port = int(os.getenv('PORT', 3001))
    debug_mode = os.getenv('NODE_ENV') == 'development'
    
    print('🐍 Flask 백엔드 서버를 시작합니다...')
    print(f'📂 작업 디렉토리: {os.getcwd()}')
    print(f'🚀 AI 간편 요청서 백엔드 서버를 시작합니다...')
    print(f'📝 헬스체크: http://localhost:{port}/health')
    print(f'💬 채팅 API: http://localhost:{port}/api/chat')
    print(f'🔑 환경변수 GEMINI_API_KEY: {"✅ 설정됨" if os.getenv("GEMINI_API_KEY") else "❌ 미설정"}')
    print(f'🌐 CORS 허용 도메인: {os.getenv("CORS_ORIGIN", "http://localhost:5173")}')
    print(f'🔧 디버그 모드: {debug_mode}')
    print('-' * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )

    port = int(os.environ.get('PORT', 5000))  
    app.run(debug=True, host='0.0.0.0', port=port)