import socket
import os
import sqlite3 # import sqlite3 để thực hành CM với database
import requests

"""
    - Context Manager là một công cụ mạnh mẽ giúp quản lý tài nguyên một cách hiệu quả
    - Ưu điểm:
        + Đảm bảo tài nguyên được đóng đúng cách: CM tự động đóng tài nguyên sau khi khối with kết thúc,
        ngay cả khi có lỗi xảy ra.
        + Mã nguồn gọn gàng, dễ đọc: CM giúp mã đọc và ghi file trở nên gọn gàng, dễ hiểu hơn
        + Giảm thiểu lỗi: CM giúp giảm thiểu nguy cơ quên đóng tài nguyên, dẫn đến lỗi trong chương trình
    
    - Các trường hợp sử dụng:
        + Quản lý tài nguyên hệ thống:
         Kết nối mạng, Socket, Database, Locks
         
        + Thực thi hành động dọn dẹp:
        Thay đổi thư mục: CM giúp thay đổi thư mục làm việc tạm thời và tự động chuyển về thư mục ban đầu
        Cài đặt môi trường: CM giúp tạm thời thay đổi cài đặt môi trường và 
        sau đó tự động khôi phục cài đặt ban đầu
        Xử lý ngoại lệ: CM đảm bảo rằng các hành động dọn dẹp được thực hiện ngày cả khi xảy ra ngoại lệ
"""

# Sử dụng CM để quản lý file
with open("filename.txt", "r") as file: # Đọc file
    content = file.read()
    print(content)
    
with open("filename.txt", "w") as file: # Ghi file
    file.write("This is some text to write.")
    
# CM quản lý kết nối socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("www.example.com", 80))
    sock.sendall(b"GET / HTTP/1.1 \r\n\r\n")
    response = sock.recv(1024)
    print(response)
    
# CM thực thi hành động dọn dẹp ngay sau khi khối with kết thúc
with open("temp.txt", "w") as temp_file:
    temp_file.write("This is temporary file")
    
print("Temporary data written to file")
os.remove("temp.txt")
print("File deleted")

# CM để quản lý Database
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def __enter__(self): # Mở connection đến db được truyền vào
        print("Connecting to database")
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb): # Thực hiện commit sau khi query, và close connection
        print("Closing database connection")
        self.conn.commit()
        self.conn.close()
        
with DatabaseConnection("test_db") as cursor: # Thực hiện query
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (2, 'Bob')")
    
# Context Manager quản lý Network Connection
class NetworkConnection:
    def __enter__(self): # Tạo session và giữ connection pool
        print("Opening session...")
        self.session = requests.Session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb): # Đóng sesion và giải phóng connection
        print("Closing session...")
        self.session.close()
        
with NetworkConnection() as session: # Gửi request
    response = session.get("https://api.github.com")
    print(response.status_code)