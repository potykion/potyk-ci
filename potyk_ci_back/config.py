from pathlib import Path

PROJECT_NAME = 'potyk-ci'
BASE_DIR = Path(__file__).resolve().parent.parent
assert BASE_DIR.name == PROJECT_NAME
