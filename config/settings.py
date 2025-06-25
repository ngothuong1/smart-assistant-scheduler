# import os
# from pathlib import Path 
# from dotenv import load_dotenv

# # định nghĩa thư mục của dự án
# BASE_DIR = Path(__file__).resolve().parent.parent
# # tải các biến môi trường từ file .env
# load_dotenv(dotenv_path=BASE_DIR / ".env")
# # đường dẫn đến file client_secret.json
# GOOGLE_CLIENT_SECRET_FILE = os.path.join(BASE_DIR, os.getenv("GOOGLE_CLIENT_SECRET_FILE", "auth.json"))
# # redirect uri được sử dụng trong OAuth2 flow
# REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501/")
# # các quyền truy cập mà ứng dụng yêu cầu (dưới dạng danh sách)
# SCOPES = [s.strip() for s in os.getenv("SCOPES", "").split()]
# # print("DEBUG SCOPES:", SCOPES)