import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

def run_ui():
    st.set_page_config(page_title="Smart Assistant", layout="wide")
    st.title("Smart Assistant Scheduler")

    # Đọc user_id từ query param
    query_params = st.query_params
    user_id = query_params.get("user_id", None)

    if not user_id:
        user_id = st.session_state.get("user_id")

    if user_id:
        # Gọi API kiểm tra trạng thái
        try:
            status_resp = requests.get(f"{API_BASE_URL}/api/auth/status/{user_id}")
            status_resp.raise_for_status()
            is_logged_in = status_resp.json().get("logged_in", False)
        except Exception as e:
            st.error(f"Lỗi khi kiểm tra trạng thái đăng nhập: {e}")
            return

        if is_logged_in:
            st.session_state["user_id"] = user_id
            # Gọi API lấy thông tin user
            try:
                user_resp = requests.get(f"{API_BASE_URL}/api/auth/user/{user_id}")
                user_resp.raise_for_status()
                user_info = user_resp.json()
            except Exception as e:
                st.error(f"Lỗi khi lấy thông tin người dùng: {e}")
                return

            # Hiển thị thông tin user
            col1, col2 = st.columns([8, 2])
            with col1:
                st.success(f"✅ Đăng nhập với: **{user_info.get('name')}** ({user_info.get('email')})")
            with col2:
                if st.button("Đăng xuất"):
                    try:
                        requests.post(f"{API_BASE_URL}/api/auth/logout/{user_id}")
                        st.session_state.pop("user_id", None)
                        st.session_state.pop("chat_history", None)
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Lỗi khi đăng xuất: {e}")

            # UI Chat
            st.markdown("---")
            st.subheader("💬 Chat với Assistant")

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            for role, message in st.session_state.chat_history:
                col1, col2 = st.columns([4, 4])
                with col1 if role == "assistant" else col2:
                    st.markdown(
                        f"<div style='text-align:{'left' if role == 'assistant' else 'right'}; "
                        f"background-color:{'#F1F0F0' if role == 'assistant' else '#DCF8C6'}; "
                        f"padding:10px; border-radius:10px; margin:5px 0;'>{message}</div>",
                        unsafe_allow_html=True
                    )

            user_input = st.chat_input("Nhập yêu cầu...")
            if user_input:
                st.session_state.chat_history.append(("user", user_input))
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/chat",
                        json={"prompt": user_input}
                    ).json().get("response", "Không có phản hồi")
                except Exception as e:
                    response = f"Lỗi khi gửi yêu cầu: {e}"
                st.session_state.chat_history.append(("assistant", response))
                st.experimental_rerun()

            return  # đã vào chat rồi → không hiện nút Login

    # Nếu chưa login → hiện nút Đăng nhập 
    st.warning("Bạn cần đăng nhập bằng Google để tiếp tục.")
    if st.button("Đăng nhập bằng Google"):
        try:
            resp = requests.get(f"{API_BASE_URL}/api/auth/start")
            resp.raise_for_status()
            auth_url = resp.json()["auth_url"]
            st.markdown(f"[Bấm vào đây để đăng nhập Google]({auth_url})", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi khi lấy link đăng nhập: {e}")

if __name__ == "__main__":
    run_ui()











