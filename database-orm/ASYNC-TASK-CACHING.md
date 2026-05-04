# ASYNC TASK PROCESSING

## WHAT?
- Đây là một nguyên tắc cơ bản trong phát triển phần mềm, cho phép thực thi các tác vụ một cách độc lập với luồng chính của chương trình
    - Trong mô hình này, chương trình chính có thể tiếp tục thực hiện các công việc khác mà không bị treo để đợi kết quả từ một tác vụ đang chạy
    - Cơ chế này dựa trên việc gửi thông điệp đến một nơi lưu trữ trung gian và tiếp tục xử lý mà không cần gửi phản hồi ngay lập tức

## WHY?
- Áp dụng xử lý bất đồng bộ mang lại nhiều lợi ích:
    - Tăng hiệu suất hệ thống: Giảm thời gian phản hồi trung bình. 
    - Khả năng mở rộng: Các hệ thống bất đồng bộ có thể phân phối tác vụ trên nhiều tiến trình hoặc máy chủ khác nhau
    - Cải thiện UX: ứng dụng phản ứng nhanh hơn vì người dùng không phải chờ đợi các tác vụ nặng hoàn tất
    - Độ tin cậy và khả năng chịu lỗi: Nếu 1 tác vụ bị lỗi, nó không làm sập toàn bộ hệ thống
    - Tiết kiệm chi phí: Tối ưu hóa việc sử dụng tài nguyên phần cứng, giảm nhu cầu phân bổ tài nguyên dư thừa

## WHEN?
- Ta nên xử lý bất đồng bộ trong các trường hợp sau:
    - Tác vụ tiêu tốn thời gian: Rendering, trích xuất dữ liệu từ hình ảnh
    - Tác vụ phụ thuộc bên thứ ba: Gọi API thanh toán bên ngoài, nơi hệ thống phải chờ phản hồi từ gateway
    - Gửi thông báo: Gửi email thông báo, thông báo đẩy cho người dùng
    - Tác vụ định kỳ: Các công việc cần chạy lặp lại như dọn dẹp database, sao lưu dữ liệu, gửi báo cáo hằng ngày
    - Xử lý dữ liệu phức tạp: Các phép tính toán nặng về CPU hoặc phân tích dữ liệu thời gian thực

## HOW?
- Trong hệ sinh thái Python, Django, công cụ phổ biến để thực hiện việc này là `Celery` kết hợp với một Message Broker (Redis, RabbitMQ)

- Quy trình hoạt động:
    1. Django App: Gửi yêu cầu thực hiện tác vụ vào hàng đợi
    2. Message Broker: Nhận và lưu trữ các tin nhắn/tác vụ
    3. Celery Worker: Lấy các tác vụ từ hàng đợi và thực thi độc lập
    4. Backend: Lưu trữ kết quả sau khi hoàn thành

- Ví dụ
Gửi email xác nhận sau khi người dùng đăng ký

1. Định nghĩa task trong tasks.py 
```
    from celery import shared_task
    import time

    @shared_task
    def send_welcome_email(user_email):
        # Giả lập việc gửi email tốn thời gian
        time.sleep(5)
        print(f"Đã gửi email thành công tới {user_email}")
        return "Success"

```
2. Gọi task trong views.py
```
    from django.shortcuts import render 
    from .tasks import send_welcome_email

    def register_user(request):
        if request.method == "POST":
            email = request.POST.get("email")
            # Thay vì gọi trực tiếp, ta sử dụng .delay() để gửi vào hàng đợi
            send_welcome_email.delay(email)

            # Phản hồi ngay lập tức cho người dùng
            return render(request, "success.html", {"message": "Đăng ký thành công! Email sẽ được gửi sau ít phút"} )
```

- Lưu ý khi triển khai:
    a. Đảm bảo các tác vụ có tính thực thi lại nhiều lần vẫn cho ra cùng một kết quả mà không gây tác dụng phụ
    b. Sử dụng các công cụ như Flower để giám sát trạng thái của các worker và hàng đợi
    c. Cấu hình cơ chế retry tự động khi tác vụ thất bại do lỗi tạm thời
---
## REDIS 
---
### Định nghĩa
- Redis là hệ cơ sở dữ liệu NoSQL 
- Redis hoạt động dựa trên mô hình lưu trữ key - value, cung cấp tính linh hoạt về lược đồ và khả năng mở rộng theo chiều ngang
- Redis nổi bật với thông lượng cao và tốc độ xử lý cực nhanh, thường được tối ưu hóa cho các kịch bản thực tế như phân tích thời gian thực, quản lý nội dụng hoặc mạng xã hội
- Redis thường được ưu tiên nhờ hiệu suất vượt trội của việc ghi dữ liệu vào bộ nhớ tạm DRAM so với các ổ cứng truyền thống shared_task
---

### Vai trò của Redis trong hệ thống
---
1. Message Broker: Redis đóng vai trò là thành phần trung gian đứng giữa ứng dụng (producer) và worker (consumer) để quản lý hàng đợi tin nhắn (message queue)
2. Backend Result: Lưu trữ kết quả các tác vụ sau khi chúng hoàn thành, cho phép ứng dụng truy xuất lại thông tin khi cần
3. PUB/SUB: Redis cho phép publish trạng thái của tash tới các client (thông qua WebSocket chẳng hạn) một cách thời gian thực

---
### Luồng hoạt động khi tích hợp Redis với Celery

Quy trình xử lý tác vụ khi tích hợp Redis với Celery:
1. Gửi tác vụ: Ứng dụng tạo 1 tác vụ và gửi nó vào Redis thông qua Celery
2. Quản lý hàng đợi: Redis nhận tin nhắn và lưu trữ nó trong danh sách hàng đợi, chờ worker sẵn sàng để xử lý
3. Thực thi tác vụ: Celery Worker lấy tác vụ từ Redis và thực thi logic nghiệp vụ một cách độc lập
4. Cập nhật tiến độ (PUB/SUB): Trong quá trình chạy, task có thể sử dụng cơ chế PUB/SUB của Redis để phát đi task-ID và session-ID, giúp WebSocker gửi thông tin tiến độ chính xác về cho người dùng
5. Lưu kết quả: Sau khi hoàn tất, kết quả cuối cùng được ghi vào Redis.
---

### Cách triển khai Redis
1. Sử dụng Containerization: Redis được triển khai bên trong 1 Docker container độc lập
2. Quản lý thông qua Orchestration: Redis được quản lý thông qua docker-compose kết hợp với Docker Swarm để tự động hóa việc triển khai và mở rộng
3. Cấu hình trong ứng dụng: Cần định nghĩa cấu hình Redis trong backend để Celery có thể kết nối chính xác
---
## CELERY 
---

### Định nghĩa
- Celery là một hệ thống quản lý hàng đợi xử lý task thời gian thực.
- Input của celery cần kết nối với một loại message broker, output có thể kết nối tới một hệ thống backend để lưu trữ kết quả

### Vai trò của Celery
1. Chạy những mô hình học máy
2. Gửi email xác Nhận
3. Web Scraping và crawling
4. Xử lý ảnh
5. Gen báo cáo
6. Phân tích dữ liệu
7. Thực hiện tác vụ bất đồng bộ
8. Hàng đợi tác vụ phân tán
9. Task Scheduling and Periodic Tasks 
10. Xử lý ngoại lệ và Cơ chế Retry 