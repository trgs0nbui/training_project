# REPORT VỀ KIẾN TRÚC CLIENT - SERVER, MÔ HÌNH MVT (MODEL - VIEW - TEMPLATE) CỦA DJANGO

---

## 1. KIẾN TRÚC CLIENT - SERVER
### Định nghĩa
- Client - Server là mô hình mạng máy tính gồm 2 thành phần chính: Máy khách (Client) và máy chủ (Server). Server là nơi lưu trữ tài nguyên cũng như cài đặt các chương trình theo yêu cầu của client. Client bao gồm
các loại máy tính cũng như các loại thiết bị điện tử nói chung sẽ gửi các yêu cầu đến server.
---
### Nguyên tắc hoạt động
- Mô hình Client - Server hoạt động dựa trên Vòng đời Yêu cầu - Phản hồi (The Request - Response Cycle)
    - User thực hiện hành động trên Client
    - Client gửi Request được đóng gói thành các gói tin (packets) và gán địa chỉ người nhận (IP Server) và đẩy vào đường truyền
    - Server xử lý: Xác nhận quyền truy cập, truy xuất thông tin, xử lý logic
    - Server gửi Response về Client: Server đóng gói kết quả và gửi ngược lại Client
    - Client hiển thị kết quả cho User

### Các thành phần của kiến trúc Client - Server
    - Client
    - Server
    - Network

### Ưu điểm
    - Khả năng kiểm soát tập trung: tất cả dữ liệu nằm ở 1 nơi duy nhất, việc sao lưu, đồng bộ hóa trở nên cực dễ dàng
    - Bảo mật: Server đóng vai trò như người bảo vệ, kiểm soát truy cập đối với tài nguyên hiện có
    - Khả năng mở rộng 
    - Khả năng truy cập: Mọi client đều có thể truy cập vào hệ thống mạng máy tính mà không hề phân biệt vị trí hay nền tảng.

### Nhược điểm
    - Tắc nghẽn lưu lượng: Nếu nhiều client tạo request từ cùng 1 server -> tắc nghẽn hệ thống
    - Chi phí
    - Bảo trì
    - Độ bền

## 2. Mô hình MVT (Model - View - Template) của Django
### Sơ lược về MVT
- Mô hình MVT là sự kết hợp của Model, View, Template:
    - Model: Thực hiện quản lý dữ liệu, kiểm soát mọi sự thay đổi của dữ liệu cũng như việc giao tiếp giữa BE và Database
    - View: Xử lý logic nghiệp vụ thông qua các url, endpoint đã được định nghĩa, khi có 1 request từ client, View sẽ thực hiện các yêu cầu của request và trả về response theo yêu cầu
    - Template: Thể hiện dữ liệu cho người dùng thông qua việc kết nối với View, đây chính UI

### Cách MVT hoạt động
- Luồng hoạt động của MVT Django sẽ như sau:
    - Client gửi request tới Server -> URL định tuyến yêu cầu tới 1 View cụ thể
    -> View xử lý logic nghiệp vụ và truyền data tới Template đồng thời trong lúc này
    Model giao tiếp với database và trả về data cho View -> Template render HTML động với data và trả về cho View
    -> Client nhận được trang với dữ liệu phù hợp từ View

## 3. So sánh MVT (Django) và MVC (Laravel)
- MVT và MVC về cơ bản là giống nhau ở bản chất. View trong MVT là Controller trong MVC, Template trong MVT là View trong MVC. MVT là biến thể của MVC

### Luồng xử lý request
- MVT (Django):
    - Client request -> URLconf
    - URL gọi tới View
    - View gọi Model lấy dữ liệu
    - View render Template
    - Trả về Response cho Client

- MVC (Laravel):
    - Client request -> Route
    - Route gọi Controller
    - Controller gọi tới Model
    - Controller trả về View
    - Trả về response cho Client

- Đối với Django, View là trung tâm logic, nhận request, xử lý, trả response
- Đối với Laravel, Controller chỉ là lớp logic trung gian, cho thấy sự tách biệt rõ ràng hơn MVT

### Set up môi trường dev: Python, Django, PostgreSQL (Local & Docker)
- Setup Local
    #### Cài đặt Python 
    ![python_version](/images_proof/python_version.jpg)
    #### Cài đặt PostgreSQL và sử dụng PgAdmin 4
    - Version PostgreSQL và pgAdmin4
    ![pgadmin4](/images_proof/pgadmin4.jpg)
    ![postgre_version](/images_proof/postgre_version.jpg)

    #### Setup Django
    ![django_setup](/images_proof/django_set_up.jpg)

    #### Docker setup
    ![docker_version](/images_proof/docker_version.jpg)