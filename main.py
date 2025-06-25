import multiprocessing
import subprocess
import time
import signal
import os
from app.bot import run_bot

def run_fastapi():
    print("[main.py] Đang khởi động FastAPI server...")
    run_bot()

def run_streamlit():
    print("[main.py] Đang khởi động Streamlit UI...")
    subprocess.Popen(["streamlit", "run", "app/streamlit_ui.py"])

if __name__ == "__main__":
    print("[main.py] Smart Assistant Scheduler khởi động...")

    # Chạy FastAPI dưới dạng daemon process
    p1 = multiprocessing.Process(target=run_fastapi)
    p1.daemon = True
    p1.start()

    # Đợi 2 giây cho FastAPI khởi động trước
    time.sleep(2)

    # Chạy streamlit UI
    run_streamlit()

    # Vòng lặp giữ main process chạy (tránh p1.join block)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[main.py] Dừng ứng dụng...")
        os.kill(p1.pid, signal.SIGTERM)
        print("[main.py] Đã dừng FastAPI.")

















