# RESTFUL API CONVENTIONS
---
## ĐỊNH NGHĨA 

- Restful API là một giao diện lập trình ứng dụng tuần thử các ràng buộc và quy ước kiến trúc REST được sử dụng trong việc 
giao tiếp giữa client và server. REST sử dụng giao thức HTTP/1 kèm theo các định nghĩa trước đó mà cả client và server tuân thủ
---
## CÁC PHƯƠNG THỨC CỦA REST

- Giữa Request và Response khi giao tiếp cần chỉ định các method sau:
    - GET
    - POST
    - PUT 
    - PATCH
    - DELETE

---

## REST API CONVENTIONS
---
### 1. Sử dụng danh từ để đại diện cho resource
- Ta sẽ chia API ra thành 4 nhóm: document, collection, store và controller

#### a. document
- Đây là một resource chỉ các đối tượng độc lập, hay 1 bản ghi trong database,
nó là 1 singleton resource bên trong collection resource
-> **Sử dụng danh từ số ít hoặc định danh của resource cho loại API này**

```
    https://api.example.com/device-management/managed-devices/{device-id}
```

#### b.collection
- Là các resource được quản lý bởi server. Client có thể yêu cầu thêm các resource mới vào collection. 
Tuy nhiên việc có được thêm hay không phụ thuộc vào 1 bên thứ 3 (admin, ...)
-> **Sử dụng tên số nhiều cho loại này** 
```
    https://api.example.com/api/device-management/managed-devices
```

#### c. store
- Là các resource được quản lý bởi client, client có toàn quyền CRUD đối với API này. Vì vậy loại resource này chỉ nên có 1 URI
và không nên tạo ra các URI khác.
-> **Với loại này, ta sử dụng tên số nhiều**
```
    https://api.example.com/api/song-management/users/{id}/playlists
```

#### d. controller
- Loại resource này đại diện cho một hành động, 1 quá trình và có input, output
-> ta nên sử dụng động từ để dễ hình dung đối với resource này
```
    https://api.example.com/api/auth/login
```
---
### 2. Nhất quán URI theo một chuẩn chung
---
    a. Sử dụng "/" để ngăn cách quan hệ trong resource
    b. Không sử dụng "/" cuối API
    c. Sử dụng "-" giữa các path dài, không nên sử dụng camelCase
    d. Không nên dùng "_" thay cho "-"
    e. Sử dụng chữ cái thường trừ scheme và host
    f. Không sử dụng định dạng file trong URI: ví dụ `http://api.example.com/api/messenger-management/group-chat/{id}/download-archived-conversation.json`
    g. Không phân định CRUD trên URI: `http://api.example.com/user-management/users/get`
    h. Sử dụng query để lọc các URI collection: `http://api.example.com/user-management/users?page=1&size=10`


# ViewSet và Router

## ViewSet
- ViewSet là một dạng class-based view nhưng không cung cấp các handler để xử lý riêng từng method request như .get(), .post(), .put(), ...
thay vào đó nó cung cấp các action. Vì vậy chỉ cần 1 ViewSet là ta có thể viết toàn bộ API cho mỗi model

- Có thể đặt tên các action method theo ý muốn, thường DRF sẽ có công thức đặt tên để dễ đoán chức năng của action:
    + list: phục vụ GET lấy toàn bộ data từ model
    + create: phục vụ POST tạo thêm 1 instance
    + retrieve: phục vụ GET để lấy data 1 instance cụ thể
    + update: phục vụ PUT để cập nhật data cho một instance
    + partial_update: phục vụ PATCH để cập nhật một vài dữ liệu cho 1 instance
    + destroy: phục vụ DELETE xóa 1 instance

## Router
- Ta sẽ sử dụng class ViewSet nhiều hơn nên quy ước để kết nối views và urls cần được xử lý tự động thay vì dùng as_view 
Vì vậy ta có class Router, việc cần làm là đăng ký view vào router và để nó làm các phần còn lại.

- Về cơ bản, Router chỉ hỗ trowjcacs action .list(), .retrieve(), .create(), .update(), .partial_update() và .destroy()
-> Để router nhận biết được action riêng mà ta viết thêm, ta sử dụng decorator @action mà Django hỗ trợ