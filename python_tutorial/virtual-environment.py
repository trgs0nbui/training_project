import requests
import pandas as pd

"""
    - Khởi tạo môi trường ảo với lệnh:
        python -m venv myvenv
        
    - Kích hoạt môi trường ảo:
        myvenv\Scripts\activate
    
    - Cài đặt các thư viện cần thiết:
        Ví dụ đối với bài hiện tại: requests, pandas, matplotlib
        `pip install requests, pandas, matplotlib` hoặc có thể cài đặt phiên bản thư viện cụ thể
        `pip install requests==2.31.0`
        
    - Quản lý dependencies với requirements.txt
        `pip freeze > requirements.txt`
"""

def fetch_users():
    """Gọi API lấy danh sách user"""
    url = "https://jsonplaceholder.typicode.com/users"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # lỗi nếu status != 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return []

def process_users(data):
    """Xử lý dữ liệu"""
    df = pd.DataFrame(data)
    
    # Lấy các cột cần thiết
    df = df[["id", "name", "email", "phone"]]
    
    # Thêm cột mới
    df["email_domain"] = df["email"].apply(lambda x: x.split("@")[-1])
    
    return df

def save_to_csv(df):
    """Lưu dữ liệu ra file"""
    df.to_csv("users.csv", index=False)
    print("Saved to users.csv")

def main():
    data = fetch_users()
    
    if not data:
        print("No data fetched")
        return
    
    df = process_users(data)
    print(df.head())
    
    save_to_csv(df)

if __name__ == "__main__":
    main()