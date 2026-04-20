# SESSION-BASED VÀ TOKEN-BASED AUTHENTICATION

## I. SESSION-BASED AUTHENTICATION
---
### Định nghĩa
- Cơ chế xác thực phía server, stateful
---
### Luồng hoạt động
-  (Client - Server) Đăng nhập: Người dùng gửi thông tin xác thực đến 1 endpoint của server
- (Server) Xác thực và tạo session: Server kiểm tra thông tin, nếu hợp lệ, server sẽ:
    - Tạo một record session duy nhất trong kho lưu trữ (bộ nhớ, database, cache layer như Redis) chứa thông tin định danh người dùng
    - Tạo một sessionId ngẫu nhiên, an toàn để liên kết với bản ghi session vừa tạo

- (Server -> Client) Gửi cookie: Server gửi sessionId về cho client, thường được đặt trong một HTTP cookie. 
- (Client -> Server): Đối với mọi yêu cầu tiếp theo đến cùng một domain, trình duyệt sẽ tự động đính kèm cookie chứa sessionId
- (Server) Xác minh Session: Server nhận sessionId từ cookie, tra cứu nó trong kho lưu trữ của mình. Nếu thấy session hợp lệ, server sẽ biết người dùng là ai và xử lý yêu cầu
---
### Ưu điểm
- Bảo mật thông tin
- Kiểm soát hiệu quả
---
### Nhược điểm
- Tăng tải cho server: Vì server phải lưu session của tất cả người dùng đang hoạt động
- Khó mở rộng

## II. TOKEN-BASED AUTHENTICATION (JWT)
---
### Định nghĩa
- JWT là một tiêu chuẩn mở cho phép tạo ra các token chứa thông tin đã được mã hóa và ký số. Server có thể xác minh tính hợp lệ của token mà không cần lưu trữ bất kỳ trạng thái nào
---
### Cấu trúc của một JWT
- Một JWT gồm 3 phần, ngăn cách bởi dấu '.':
    - Header (Base64UrlEncoded): Chứa metadata về token, như thuật toán ký và loại token
    - Payload (Base64UrlEncoded): Chứa các claims về người dùng và các dữ liệu khác như sub, exp
    Payload chỉ được mã hóa Base64, không được mã hóa vì vậy không nên đặt thông tin nhạy cảm vào đây
    - Signature: Được tạo ra bằng cách kết hợp Header, Payload, một khóa bí mật (Secret-key) và áp dụng thuật toán ký đã chỉ định ở Header.
    Chữ ký này đảm bảo rằng token không bị sửa đổi trên đường truyền.
---
### Luồng hoạt động
- (Client -> Server) Đăng nhập
- (Server) Xác thực và tạo token: Server kiểm tra thông tin. Nếu hợp lệ, server tạo một JWT, ký nó bằng secret key của mình và gửi token về cho client
- (Client) Lưu trữ Token: Client nhận và lưu trữ JWT (thường trong localStorage hoặc bộ nhớ ứng dụng).
- (Client -> Server) Các yêu cầu tiếp theo: Client đính kèm JWT vào header của mỗi yêu cầu cần xác thực, theo chuẩn Bearer
- (Server) Xác minh Token: Với mỗi yêu cầu, server nhận token từ header, kiểm tra chữ ký bằng secret key. Nếu chữ ký hợp lệ và token chưa hết hạn, server sẽ tin tưởng các thông tin trong payload và xử lý yêu cầu. Server không cần truy vấn database hay cache để tìm thông tin phiên.
---
### Ưu điểm
- Không lưu trạng thái và dễ mở rộng
- Tách biệt hệ thống: JWT phù hợp với Microservices, ứng dụng SPA
---
### Nhược điểm
- Khó thu hồi token: Nếu token bị lộ, kẻ xấu vẫn có thể tiếp tục sử dụng dù token vẫn còn hạn. Cần dùng đến giải pháp như blocklist, phương án như Access/Refresh Token
- Kích thước lớn: JWT thường chứa nhiều thông tin hơn so với 1 session Id -> kích thước request Header tăng lên
- Nguy cơ bảo mật phía client: nếu JWT được lưu trong localStorage, nó có thể bị đánh cắp qua các lỗ hổng XSS.

## SO SÁNH SESSION-BASED VÀ TOKEN-BASED AUTHENTICATION

| Khía cạnh | Session-based | Token-based |
| --- | --- | --- |
| State | Server lưu 1 session id | Client giữ 1 access token JWT |
| Storage | HttpOnly, SamSite cookie | Ưu tiên HttpOnly Cookie, tránh token sống lâu trong JS storage |
| Revocation | Dễ dàng vì server lưu session | Sử dụng thời gian lưu trữ access token ngắn kết hợp với refresh token hoặc blocklist |
| CSRF Risk | Nguy cơ dính CSRF cao vì Cookie được gửi tự động trong request | Vì token được gửi bên trong Authorization header, nên nguy cơ gặp CSRF khá thấp |
| Use when | Web-app có 1 domain duy nhất | Mobile, Multi-domain, Microservices, SPA |