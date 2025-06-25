from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services import google_auth
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import uvicorn
from dotenv import load_dotenv

load_dotenv()

SCOPES = [s.strip() for s in os.getenv("SCOPES", "").split()]
UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:8501")

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # có thể giới hạn domain sau
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

# bắt đầu luồng OAuth
@app.get("/api/auth/start")
async def start_auth_flow():
    auth_url = google_auth.get_oauth_flow(SCOPES).authorization_url(prompt='consent')[0]
    return JSONResponse({"auth_url": auth_url})

@app.get("/api/auth/callback")
async def auth_callback(request: Request, scope: str = "auth"):
    try:
        full_url = str(request.url)
        flow = google_auth.get_oauth_flow(SCOPES)
        flow.fetch_token(authorization_response=full_url)
        creds = flow.credentials
        user_info = google_auth.get_user_info(creds)
        google_auth.save_or_update_user(creds, user_info)
        
        user_id = user_info["id"]
        redirect_url = f"{UI_BASE_URL}?user_id={user_id}"
        return RedirectResponse(redirect_url, status_code=303)
    
    except Exception as e:
        import logging
        logging.error("-> Lỗi callback!", exc_info=True)
        error_redirect_url = f"{UI_BASE_URL}?error=auth_failed"
        return RedirectResponse(error_redirect_url)
    
# route lấy thông tin user
@app.get("/api/auth/user/{user_id}")
async def get_user_info(user_id: str):
    creds = google_auth.get_users_google_token(user_id)
    if not creds:
        return JSONResponse({"error": "User chưa đăng nhập"}, status_code=401)
    user_info = google_auth.get_user_info(creds)
    return JSONResponse(user_info)

#kiểm tra trạng thái login
@app.get("/api/auth/status/{user_id}")
async def check_auth_status(user_id: str):
    creds = google_auth.get_users_google_token(user_id)
    return JSONResponse({"logged_in": creds is not None})

# đăng xuất
@app.post("/api/auth/logout/{user_id}")
async def logout(user_id: str):
    msg = google_auth.logout_user(user_id)
    return JSONResponse({"message": msg})

# ping api
@app.get("/api/ping")
async def ping():
    return {"message": "pong"}

# api chat
@app.post("/api/chat")
async def chat(payload: dict):
    prompt = payload.get("prompt", "")
    # Tạm thời giả lập trả lời
    reply = f"Bạn vừa nói: '{prompt}'. Tính năng đang được phát triển..."
    return {"response": reply}

# run server
def run_bot():
    print("FastAPI bot đang chạy...")
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("FASTAPI_PORT", 8000)))

def stop_bot():
    print("Đang dừng FastAPI bot...")

if __name__ == "__main__":
    run_bot()





