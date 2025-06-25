import os
import requests

def get_current_redirect_uri():
    use_ngrok = os.getenv("USE_NGROK", "False").lower() == "true"

    if use_ngrok:
        ngrok_url = get_ngrok_url_from_api()
        if ngrok_url:
            redirect_uri = f"{ngrok_url}/api/auth/callback"
            print(f"[app_utils] Using ngrok redirect_uri: {redirect_uri}")
            return redirect_uri
        else:
            raise RuntimeError("[app_utils] USE_NGROK=True nhưng chưa lấy được ngrok_url!")
    else:
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")  # đồng bộ tên biến
        print(f"[app_utils] Using static redirect_uri: {redirect_uri}")
        return redirect_uri

# Hàm lấy ngrok_url — không import ngược từ main
def get_ngrok_url_from_api():
    try:
        # Mặc định Ngrok API chạy local trên 4040
        resp = requests.get("http://localhost:4040/api/tunnels")
        resp.raise_for_status()
        tunnels = resp.json()["tunnels"]
        for tunnel in tunnels:
            public_url = tunnel["public_url"]
            if public_url.startswith("https"):
                print(f"[app_utils] Ngrok public_url: {public_url}")
                return public_url
    except Exception as e:
        print(f"[app_utils] Lỗi khi lấy ngrok_url: {e}")
    return None




