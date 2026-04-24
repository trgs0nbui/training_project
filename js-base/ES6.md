# REPORT VỀ ES6
---
## ES6 là gì?

- ES6 là phiên bản mới nhất của chuẩn ECMAScript (Tiêu chuẩn của JS) được hiệp hội Tiêu chuẩn hóa ECMA International phê duyệt vào tháng 6 năm 2015

## Kỹ thuật cốt lõi của tiêu chuẩn này
---
1. Cơ chế Quản lý phạm vi và khai báo biến
- `let` và `const` thay thế cho `var`, block scope giúp ngăn chặn việc rò rỉ biến ra ngoài khối lệnh và giảm thiểu lỗi do cơ chế "hoisting"

- Tính bất biến: `const` được thiết kế cho các liên kết gán một lần, đảm bảo địa chỉ bộ nhớ của biến không thay đổi.

2. Syntax và Function Programming

- Arrow Functions: Cung cấp cú pháp `=>` súc tích, loại bỏ nhu cầu sử dụng `function` và `return` trong các trường hợp đơn giản. 
Sử dụng "lexical this", tự động kế thừa giá trị `this` từ phạm vi bao quanh tại thời điểm định nghĩa

- Default Parameters: Cho phép thiết lập giá trị mặc định cho tham số ngay tại khai báo hàm

- Toán tử REST(...) và SPREAD (...): Toán tử Rest cho phép hàm chấp nhận số lượng đối số không xác định dưới dạng mảng, trong khi Spread cho phép trải các phần tử của mảng hoặc đối tượng vào mảng/đối tượng mới

3. OOP và Code Structure
- Classes: Cung cấp phương thức khai báo rõ ràng cho các hàm khởi tạo và chuỗi prototype. Các lớp hỗ trợ kế thừa thông qua từ khóa `extends` và cho phép gọi phương thức cha bằng `super`
- ESM: Sử dụng `import` và `export` để chuẩn hóa việc đóng gọi, chia sẻ mã nguồn. Hệ thống này có cấu trúc tĩnh, cho phép các công cụ tối ưu hóa để loại bỏ mã không cần thiết

4. Xử lý bất đồng bộ và Cấu trúc dữ liệu
- Promises: Chuẩn hóa cách xử lý các giá trị trong tương lai, thay thế cho cơ chế callback lồng nhau phức tạp (callback hell)
- Cấu trúc dữ liệu mới: Bổ sung Map và Set. Các phiên bản "Weak" (WeakMap, WeakSet) sử dụng tham chiếu yếu để hỗ trợ thu gom rác tự động, tránh rò rỉ bộ nhớ

5. Cải tiến API và các hành vi nội bộ của ngôn ngữ
- Template Literals: Sử dụng dấu (`) để hỗ trợ chuỗi nhiều dòng và nhúng biểu thức thông qua cú pháp `${expression}`
- Destructuring: Cho phép trích xuất nhanh dữ liệu từ mảng hoặc đối tượng vào các biến riêng biệt trong một câu lệnh duy nhất
- Symbols: Kiểu dữ liệu nguyên thủy mới đảm bảo tính duy nhất, giúp tạo ra các thuộc tính đối tượng không bao giờ xung đột với nhau.
- Proxies và Reflect API: Cung cấp khả năng can thiệp vào các hành vi nội bộ của ngôn ngữ, như chặn các thao tác truy cập thuộc tính hoặc gọi hàm

---
## Features
---
### Arrow Functions
#### 1. Cú pháp cơ bản và rút gọn
- AF sử dụng ký hiệu `=>` thay cho từ khóa function. Tùy vào số lượng tham số và nội dung hàm, cú pháp có thể được tối giản
    - Không có tham số: Phải sử dụng cặp ngoặc đơn trống `()`. Ví dụ:
        ```
            const sayHi = () => console.log("Hello World!");
        ```
    - Một tham số: Có thể bỏ qua cặp ngoặc đơn. Ví dụ:
        ```
            const square = x => x * x;
        ```
    - Nhiều tham số: Phải sử dụng cặp ngoặc đơn
        ```
            const sum = (a, b) => a + b;
        ```
#### 2. Trả về ngầm định (Implicit Return)
- Nếu nội dung hàm chỉ gồm một biểu thức duy nhất, ta có thể bỏ qua cặp ngoặc nhọn `{}` và từ khóa `return`.
