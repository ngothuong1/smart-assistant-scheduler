import os, pickle, json, logging, dotenv
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.utils import app_utils
from app.dao import mysql_dao

dotenv.load_dotenv()
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = [s.strip() for s in os.getenv("SCOPES", "").split()]


# tao flow OAuth2
def get_oauth_flow(scopes=None):
    if scopes is None:
        scopes = SCOPES
    
    redirect_url = app_utils.get_current_redirect_uri()

    return Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [redirect_url],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=scopes,
        redirect_uri=redirect_url 
    )

#lay thong tin user tren google
def get_user_info(creds):
    service = build('oauth2', 'v2', credentials=creds)
    user_info = service.userinfo().get().execute()
    return user_info

#lay token cua user tu CSDL
def get_users_google_token(user_id):
    creds_json = mysql_dao.get_users_token(user_id)
    if not creds_json:
        print("Không tìm thấy token trong CSDL!")
        return None
    try:
        creds_dict = json.loads(creds_json)  
        if isinstance(creds_dict, str):  
            creds_dict = json.loads(creds_dict)
        creds = Credentials.from_authorized_user_info(creds_dict)
        return creds
    except json.JSONDecodeError as e:
        logging.error("Lỗi giải mã JSON!", exc_info=True)
    except Exception as e:
        logging.error("Lỗi khôi phục Credentials!", exc_info=True)
    return None

    
def check_login_user(creds, scope=None):
    try:
        user_info = get_user_info(creds)

        # xây dựng thông điệp dựa vào scope
        if scope is None or scope == "auth":
            text = (
                f"{user_info['name']}, bạn đã đăng nhập thành công!\n"
                f"🔹 Chức năng hiện tại:\n"
                f"   + Quản lí ghi chú\n"
                f"   + Quản lí tasks\n\n"
                f"➡️ Bạn có thể cấp thêm quyền tại /scope"
            )
        elif scope == "calendar":
            text = (
                f"{user_info['name']}, bạn đã đăng nhập thành công!\n"
                f"🔹 Chức năng hiện tại:\n"
                f"   + Quản lí ghi chú\n"
                f"   + Quản lí tasks\n"
                f"   + Quản lí lịch Google Calendar\n\n"
                f"➡️ Bạn có thể cấp thêm quyền tại /scope"
            )
        else:
            text = (
                f"{user_info['name']}, bạn đã đăng nhập thành công!\n"
                f"🔹 Đầy đủ chức năng:\n"
                f"   + Quản lí ghi chú, tasks\n"
                f"   + Lịch Google\n"
                f"   + Lọc email rác, trích lịch từ email\n\n"
                f"✅ Bạn đã cấp đầy đủ quyền!"
            )

        save_or_update_user(creds, user_info)
        # chuẩn bị dữ liệu trả về
        return {
            'message': text,
            'user_info': user_info,
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'expiry': creds.expiry.isoformat(),
            'token_type': 'Bearer'
        }
    
    except Exception as e:
        logging.error("-> Lỗi khi đăng nhập!", exc_info=True)
        return {"message": "Đã xảy ra lỗi trong quá trình đăng nhập!"}

        # lưu hoặc cập nhật người dùng trong DB
def save_or_update_user(creds, user_info):
    try:
        user_id = user_info['id']
        user = mysql_dao.get_user_by_id(user_id)

        if user is None:
            mysql_dao.create_new_users(user_id, user_info['name'], user_info['picture'], user_info['email'])
            mysql_dao.create_new_users_token(user_id, json.dumps(creds.to_json()))
        else:
            mysql_dao.update_users_google_token(user_id, json.dumps(creds.to_json()))

    except Exception as e:
        logging.error("-> Lỗi khi lưu/update user!", exc_info=True)
        return False

# đăng xuất   
def logout_user(user_id):
    try:
        # Chỉ xóa token lưu trong DB
        mysql_dao.update_users_google_token(user_id=user_id, creds_json=None)
        return "Bạn đã đăng xuất thành công!"
    except Exception as e:
        logging.error("-> Lỗi khi đăng xuất!", exc_info=True)
        return "Đăng xuất thất bại!"


