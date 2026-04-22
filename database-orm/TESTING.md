# TESTING IN DJANGO

## 1. Pytest
- Pytest là thư viện, testing framework mạnh mẽ dành cho Python.
- Nó được các developer ưa chuộng vì cách tiếp cận "Pythonic" hơn so với thư viện kiểm thử mặc định của Django, giúp việc code kiểm thử trở nên tự nhiên và dễ đọc hơn
### Các đặc điểm chính
a. Ít boilerplate: không giống như unittest của Django, pytest không yêu cầu ta phải kế thừa từ lớp TestCase mà có thể viết các hàm kiểm thử dưới dạng hàm thông thường
b. Sử dụng câu lệnh `assert` đơn giản: Thay vì phải nhớ nhiều phương thức như `assertEqual`, `assertTrue`, `assertFalse` của unittest, pytest cho phép sử dụng câu lệnh `assert` thông thường của Python, giúp code kiểm thử dễ đọc và dễ hiểu hơn
c. Hệ thống Fixture mạnh mẽ: Fixture là các hàm được sử dụng để cung cấp dữ liệu hoặc thiết lập môi trường cho các bài kiểm thử. Pytest có hệ thống fixture rất mạnh mẽ, cho phép ta dễ dàng chia sẻ dữ liệu giữa các bài kiểm thử
d. Khả năng mở rộng cao: Pytest có khả năng mở rộng cao, cho phép ta dễ dàng thêm các tính năng mới cho pytest thông qua các plugin
e. Quy ước đặt tên: Pytest tự động tìm kiếm các tệp kiểm thử có tên bắt đầu bằng test_*.py hoặc *_test.py và các hàm kiểm thử bắt đầu bằng tiền tố test_

## 2. Pytest-django
- pytest-django là một plugin chuyên biệt dành cho Pytest
- Nó đóng vai trò là cầu nối tương thích hoàn toàn với các bộ kiểm thử tiêu chuẩn của Django
- Các tính năng mà pytest-django cung cấp:
    a. Quản lý cơ sở dữ liệu: Tự động hóa việc thiết lập và dọn dẹp cơ sở dữ liệu cho mỗi lần chạy test, đảm bảo tính cô lập giữa các bài kiểm thử
    b. Các markers chuyên dụng: Cung cấp các markers như `@pytest.mark.django_db` để yêu cầu quyền truy cập cơ sở dữ liệu dành cho 1 hàm hoặc 1 lớp kiểm thử cụ thể
    c. Hệ thống Fixtures tích hợp sẵn cho Django: Cung cấp nhiều fixtures hữu ích giúp thao tác nhau với các thành phần của Django như:
        - client: 1 instance của `django.test.Client` để giả lập các request HTTP
        - admin_client: Client đã được đăng nhập sẵn với quyền admin
        - rf: Công cụ tạo các request HTTP giả lập một cách nhau chóng mà không cần qua middleware
        - settings: Fixture cho phép thay đổi tạm thời các cài đặt của Django trong quá trình chạy test
    d. Tích hợp cấu hình: Cho phép trỏ pytest đến các module cấu hình của Django thông qua các tệp pytest.ini, pyproject,toml hoặc biến môi trường

## 3. Luồng test thực tế
- Django tuân thủ theo quy trình chặt chẽ gói gọn trong mô hình AAA (Arrange - Act - Assert)
B1. Thiết lập môi trường và cấu hình
- Tạo tệp cấu hình: pytest.ini và pyproject.toml để chỉ định modules settings của Django, quy tắc tìm kiếm tệp kiểm thử
- Cấu hình chung: Sử dụng tệp conftest.py để định nghĩa các fixtures dùng chung cho toàn bộ dự án mà không cần import thử công vào từng tập test
B2. Chuẩn bị dữ liệu (Arrange)
- Sử dụng fixtures: Khởi tạo các đối tượng giả lập hoặc dữ liệu mẫu
- Sử dụng factories: Thay vì tạo thủ công, ta sử dụng blueprint để sinh ra dữ liệu mẫu nhanh chóng và linh hoạt
- Mocking: Nếu cần test gọi API tới bên thứ 3, ta sử dụng mocker hoặc patch để thay thế hành động thật bằng một phản hồi giả lập, giúp test chạy nhanh, không phụ thuộc hệ thống bên ngoài
- Sử dụng marker để cho phép hàm test tương tác với cơ sở dữ liệu kiểm thử
B3. Thực thi đơn vị cần kiểm thử (Act)
- Gọi hàm/logic: Truyền các tham số đã chuẩn bị ở Arrange vào hàm cần test
- Mô phỏng request: Sử dụng APIClient hoặc RequestFactory để tạo 1 yêu cầu HTTP giả lập gửi đến endpoint cần kiểm tra
B4. Kiểm tra dữ liệu (Assert)
- Sử dụng câu lệnh `assert`: So sánh kết quả trả về từ bước Act với giá trị mong đợi
- Kiểm tra ngoại lệ: Sử dụng `pytest.raises` để xác nhận rằng 1 lỗi cụ thể sẽ được ném ra nếu dữ liệu đầu vào không hợp lệ
B5. Thực hiện chu trình TDD
1. Red: Viết 1 test case cho hành động chưa tồn tại và chạy để xác nhận test thất bại
2. Green: Viết code tối thiểu để test pass
3. Refactor: Tối ưu hóa code mà vẫn đảo bảo tất cả các bài test cũ vẫn vượt qua 
B6. Dọn dẹp
Sau khi kết thúc kiểm thử, Pytest và pytest-django sẽ tự động dọn dẹp:
- Rollback dữ liệu
- Xóa bộ nhớ đệm