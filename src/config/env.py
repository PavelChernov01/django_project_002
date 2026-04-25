import os
from pathlib import Path

import environ

env = environ.Env(DEBUG=(bool, False))

# Set the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
# Take environment variables from ..env file
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))