# Gunicorn configuration file (wsgi_config.py)
import multiprocessing

# Server socket
bind = '127.0.0.1:8000'
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count()
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = './logs/gunicorn_access.log'
errorlog = './logs/gunicorn_error.log'
loglevel = 'info'

# Process naming
proc_name = 'flask-app'

# Server mechanics
daemon = False
pidfile = './gunicorn.pid'
umask = 0o022

# Server hooks
def on_starting(server):
    print("[Gunicorn] Starting Flask application server...")

def when_ready(server):
    print(f"[Gunicorn] Ready to accept connections on {bind}")

def on_exit(server):
    print("[Gunicorn] Exiting...")
