import os
import sys
import urllib.parse

# Add the project root directory to the python search path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app

class VercelPathMiddleware:
    """
    Vercel internal rewrites rewrite the incoming URL path to /api/index,
    which prevents Flask from seeing the actual route requested by the browser
    (e.g., /generate or /download-template).
    
    This middleware restores PATH_INFO from either the rewrite query parameter
    `__vercel_path` or the Vercel header `HTTP_X_MATCHED_PATH`.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        query = environ.get('QUERY_STRING', '')
        if '__vercel_path=' in query:
            params = urllib.parse.parse_qs(query)
            if '__vercel_path' in params:
                real_path = params['__vercel_path'][0]
                if not real_path.startswith('/'):
                    real_path = '/' + real_path
                environ['PATH_INFO'] = real_path
                # Clean up query string so Flask app doesn't see internal parameter
                clean_params = {k: v for k, v in params.items() if k != '__vercel_path'}
                environ['QUERY_STRING'] = urllib.parse.urlencode(clean_params, doseq=True)
        elif environ.get('HTTP_X_MATCHED_PATH'):
            path = environ['HTTP_X_MATCHED_PATH'].split('?')[0]
            environ['PATH_INFO'] = path

        return self.wsgi_app(environ, start_response)

# Apply WSGI middleware wrapper
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
