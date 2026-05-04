# DOCKER

## 1. Containerization
---
- Vấn đề mà dev thường gặp là phần mềm được viết và kiểm thử trên local chạy bình thường nhưng, khi đưa lên Production thì lại lỗi
-> sự khác biệt giữa local và production, gây ra sự không nhất quán và khó khăn trong việc khắc phục lỗi

- Containerization là một công nghệ ảo hóa, giúp giải quyết vấn đề này bằng cách đóng gói ứng dụng và tất cả các dependencies vào 1 đơn vị độc lập gọi là container. Container này đảm bảo rằng phần mềm sẽ chạy ổn định và nhất quán trên bất kì môi trường nào

### Vai trò của Containerization
- Nhất quán: Đảm bảo rằng ứng dụng được đóng gói trong container sẽ hoạt động giống nhau trên mọi môi trường, dù là trên local, test server hay production
- Di động: Container là các gói phần mềm nhẹ có thể dễ dàng chuyển từ hệ thống này sang hệ thống khác mà không gặp vấn đề về tương thích
- Khả năng mở rộng: Container có thể khởi động hoặc dừng nhanh chóng, cho phép các ứng dụng dễ dàng mở rộng, thu hẹp tùy theo nhu cầu sử dụng thực tế 
- Hiệu quả: Container chia sẻ kernel của HĐH chủ, không giống như các máy ảo truyền thống -> container tốn ít tài nguyên hơn, khởi động nhanh hơn, tốn ít chi phí quản lý hơn
- Cô lập: Container đảm bảo rằng các ứng dụng được độc lập với nhau, tăng cường bảo mật. Nếu một ứng dụng bị tấn công, sự cố này không ảnh hưởng đến các ứng dụng khác

## 2. Docker
---
- Nền tảng mã nguồn mở được thiết kế để đơn giản hóa việc phát triển, triển khai và chạy ứng dụng bên trong các container. So với các công nghệ container có trước Docker, yêu cầu nhiều kiến thức về hệ điều hành và cấu hình thủ công nhiều, Docker cung cấp một giao diện dòng lệnh đơn giản và trực quan, dễ sử dụng ngay cả với những người không có kinh nghiệm sâu về hệ điều hành,
cho phép Docker container có thể chạy trên bất cứ hệ thống nào có Docker

### Các thành phần chính của Docker
a. Docker Engine 
- Trung tâm của hệ thống Docker, nó là một runtime quản lý các container Docker trên một hệ thống
- Docker Engine là 1 ứng dụng client-server với 3 thành phần chính: Docker CLI, Docker API, Docker Daemon
    - Docker CLI: Là giao diện mà dev và admin sử dụng để tương tác với Docker: docker build, docker run, docker push
    - Docker API: Là giao diện cho các ứng dụng, các giải pháp phần mềm có thể tương tác với Docker Engine, điều khiển hoạt động của nó và truy xuất thông tin thông qua API này
    - Docker Daemon: Thường được gọi tắt là Dockerd, Daemon chạy trên máy chủ và thực hiện các công việc chính như build, chạy và quản lý các container. Dockerd có thể giao tiếp với các Docker Daemons khác để đồng bộ hóa dịch vụ container trên nhiều máy.

![docker_engine](/images_proof/docker.jpg)

b. Docker images
- Docker images là các bản thiết kế cho container. Một image định nghĩa tất cả những gì một ứng dụng cần để chạy. Sau khi image được tạo ra, nó có thể thay đổi, ta có thể chạy các instance của image này, được gọi là các container

c. Docker containers
- Đây là các instance đang chạy của Docker images. Container đóng gói một ứng dụng và tất cả các thành phần phụ thuộc của nó. Containers cô lập phần mềm khỏi sự ảnh hưởng của môi trường và đảm bảo rằng nó vẫn hoạt động bất kể sự khác biệt

d. Docker Hub
- Là một registry service phổ biến nhất được cung cấp bởi Docker, đây là nơi ta có thể tải lên các Docker images của mình
