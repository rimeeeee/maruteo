from flask import Blueprint, request, jsonify
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
        
        # 어르신을 위한 시스템 프롬프트
        system_prompt = """당신은 어르신들을 위한 친절한 AI 도우미입니다. 
다음 지침을 따라 답변해주세요:
1. 존댓말을 사용하고 친근하게 대화하세요
2. 복잡한 용어는 쉬운 말로 설명해주세요  
3. 어르신이 배우고 싶어하는 내용에 맞는 적절한 프로그램이나 강의를 추천해주세요
4. 답변은 간결하고 이해하기 쉽게 작성하세요
5. 어르신의 관심사(스마트폰, 건강, 취미 등)에 따라 맞춤형 프로그램을 제안하세요"""

        # AI 응답 생성
        try:
            if len(session['messages']) == 1:  # 첫 번째 메시지인 경우
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