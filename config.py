import os

APP_NAME = "Sistem Clustering Akademik Mahasiswa"

EPS = 1.1
MIN_SAMPLES = 4

UPLOAD_FOLDER = "data/uploads"
HISTORY_FOLDER = "data/history"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HISTORY_FOLDER, exist_ok=True)

THEMES = {
    "Light": {
        "background": "#FFFFFF",
        "text": "#000000"
    },
    "Dark": {
        "background": "#0E1117",
        "text": "#FFFFFF"
    }
}