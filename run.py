import os
from app import create_app
from flask import jsonify

app = create_app()

# 루트 경로 - API 문서 제공
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'AI 간편 요청서 백엔드',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'chat_sessions': '/api/chat/sessions',
            'chat_messages': '/api/chat/sessions/<session_id>/messages',
            'auth': '/api/auth/*',
            'lessons': '/api/lessons/*',
            'apply': '/api/apply/*',
            'profile': '/api/profile/*',
            'mypage': '/api/mypage/*'
        },
        'docs': 'API 전용 서버입니다. 프론트엔드에서 접속하세요.'
    })

# 파비콘 처리
@app.route('/favicon.ico')
def favicon():
    return '', 204

# 프론트엔드 라우팅 경로 처리 (SPA를 위한 catch-all)
@app.route('/<path:path>')
def catch_all(path):
    # 프론트엔드 라우팅 경로들
    frontend_routes = ['my-talents', 'chat', 'profile', 'apply']
    
    if any(route in path for route in frontend_routes):
        return jsonify({
            'message': f'프론트엔드 경로입니다: /{path}',
            'info': '이 경로는 프론트엔드에서 처리됩니다',
            'api_base': '/api/',
            'frontend_url': 'https://your-frontend-domain.com'
        }), 200
    
    return jsonify({
        'error': f'경로를 찾을 수 없습니다: /{path}',
        'available_routes': ['/api/health', '/api/chat/sessions', '/api/auth/', '/api/lessons/', '/api/apply/', '/api/profile/', '/api/mypage/']
    }), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(debug=True, host='0.0.0.0', port=port)