import os
import sys

# Add the project root directory to the python search path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the Flask application instance
from app import app

# Vercel serverless function entrypoint
# The 'app' variable is automatically served by Vercel's Python runtime
