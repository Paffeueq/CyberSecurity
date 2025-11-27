"""
Flask application with proper client IP detection
Demonstrates how to read real client IP from X-Forwarded-For headers
"""

import os
import pwd
import getpass
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# ProxyFix middleware to handle X-Forwarded-For headers from nginx
# This enables the real client IP to be read from X-Forwarded-For
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

def get_process_info():
    """Get current process user and privileges information"""
    try:
        uid = os.getuid()
        user_info = pwd.getpwuid(uid)
        return {
            'uid': uid,
            'username': user_info.pw_name,
            'gid': os.getgid(),
            'groups': os.getgroups(),
            'current_user': getpass.getuser(),
            'home': user_info.pw_dir
        }
    except Exception as e:
        return {'error': str(e)}

def get_client_ip():
    """
    Get the real client IP address.
    Handles X-Forwarded-For and X-Real-IP headers from nginx proxy.
    """
    # Try X-Forwarded-For first (most common)
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, get the first one
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    
    # Try X-Real-IP
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    
    # Fallback to remote_addr
    return request.remote_addr

@app.route('/')
def index():
    """Main page showing application status and client information"""
    return jsonify({
        'status': 'ok',
        'message': 'Flask application running with Gunicorn through Nginx SSL proxy',
        'https': request.is_secure,
        'client_ip': get_client_ip(),
        'server_info': {
            'host': request.host,
            'remote_addr': request.remote_addr,
            'scheme': request.scheme,
            'method': request.method
        },
        'process_info': get_process_info(),
        'headers': {
            'X-Real-IP': request.headers.get('X-Real-IP', 'Not provided'),
            'X-Forwarded-For': request.headers.get('X-Forwarded-For', 'Not provided'),
            'X-Forwarded-Proto': request.headers.get('X-Forwarded-Proto', 'Not provided'),
            'X-Forwarded-Host': request.headers.get('X-Forwarded-Host', 'Not provided'),
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ip': get_client_ip()
    })

@app.route('/process-info')
def process_info():
    """Endpoint showing current process privileges and user information"""
    info = get_process_info()
    info['message'] = 'Current process privileges and user information'
    return jsonify(info)

@app.route('/client-ip')
def client_ip():
    """Endpoint showing detected client IP address"""
    return jsonify({
        'client_ip': get_client_ip(),
        'x_real_ip': request.headers.get('X-Real-IP'),
        'x_forwarded_for': request.headers.get('X-Forwarded-For'),
        'remote_addr': request.remote_addr
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

if __name__ == '__main__':
    # This won't be used when running with Gunicorn
    # But good for local testing
    app.run(host='127.0.0.1', port=5000, debug=False)
