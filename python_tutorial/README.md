# REPORT VỀ Data types, control flow, functions, OOP trong Python

---

## 1. Data types (Kiểu dữ liệu)

### Định nghĩa

Kiểu dữ liệu là các loại giá trị mà biến có thể lưu trữ trong Python, ví dụ: số, chuỗi, danh sách, tuple, v.v. Python hỗ trợ nhiều kiểu dữ liệu như:

- Numeric types: int, float, complex
- Sequence types: list, tuple, range
- Mapping type: dict
- Set types: set, frozenset
- Text type: str

### Ví dụ

```python
x = 10           # int
y = 3.14         # float
z = 1 + 2j       # complex
e = [1, 2, 3]    # list
f = (1, 2, 3)    # tuple
g = range(1, 10) # range
s = "hello"      # str
d = {"a": 1}     # dict
st = {1, 2, 3}   # set
```
---

## 2. Control flow (Cấu trúc điều khiển)

### Định nghĩa

Cấu trúc điều khiển cho phép kiểm soát luồng thực thi của chương trình dựa trên điều kiện hoặc lặp lại một khối lệnh.
Các cấu trúc phổ biến: if, elif, else, for, while, break, continue, pass.

### Ví dụ

```python
# Kiểm tra số chẵn/lẻ
x = 5
if x % 2 == 0:
    print("Số chẵn")
else:
    print("Số lẻ")

# Lặp qua danh sách
for i in range(5):
    print(i)
```

---

## 3. Functions (Hàm)

### Định nghĩa

Hàm là một khối mã thực hiện một nhiệm vụ cụ thể, có thể tái sử dụng nhiều lần. Hàm giúp chia nhỏ chương trình, tăng tính tổ chức và dễ bảo trì.

### Ví dụ

```python
def tong(a, b):
    return a + b

print(tong(3, 4)) # 7
```

---

## 4. OOP (Lập trình hướng đối tượng)

### Định nghĩa

OOP là phương pháp lập trình tổ chức chương trình thành các đối tượng (object), mỗi đối tượng là sự kết hợp giữa dữ liệu (thuộc tính) và hành vi (phương thức).

### Ví dụ

```python
class Student:
    def __init__(self, name, mssv):
        self.name = name
        self.mssv = mssv
    def show(self):
        print(f"{self.name} - {self.mssv}")

s = Student("An", "123")
s.show() # An - 123
```
---

## 5. Bốn tính chất của OOP

### 1. Đóng gói (Encapsulation)

- **Định nghĩa:** Đóng gói là việc che giấu thông tin bên trong đối tượng, chỉ cho phép truy cập hoặc thay đổi thông qua các phương thức công khai.
- **Ví dụ mô tả:** Lớp `BankAccount` có thuộc tính `balance` là private, chỉ truy cập qua các phương thức.
- **Bài toán áp dụng:** Xây dựng lớp `Student` với điểm số là private, chỉ thay đổi qua phương thức.

**Ví dụ code:**

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.__score = 0  # thuộc tính private
    def set_score(self, score):
        if 0 <= score <= 10:
            self.__score = score
    def get_score(self):
        return self.__score

s = Student("An")
s.set_score(8)
print(s.get_score())  # 8
```

---

### 2. Kế thừa (Inheritance)

- **Định nghĩa:** Kế thừa cho phép lớp con nhận lại thuộc tính/phương thức của lớp cha.
- **Ví dụ mô tả:** Lớp `Dog` kế thừa từ `Animal`, dùng lại phương thức `eat()`.
- **Bài toán áp dụng:** Tạo lớp `Vehicle`, lớp `Car` kế thừa và mở rộng.

**Ví dụ code:**

```python
class Vehicle:
    def move(self):
        print("Moving...")

class Car(Vehicle):
    def honk(self):
        print("Beep beep!")

car = Car()
car.move()   # Moving...
car.honk()   # Beep beep!
```

---

### 3. Đa hình (Polymorphism)

- **Định nghĩa:** Đa hình là khả năng đối tượng thực hiện hành động khác nhau với cùng một lời gọi phương thức.
- **Ví dụ mô tả:** Phương thức `draw()` ở các lớp con của `Shape` sẽ vẽ khác nhau.
- **Bài toán áp dụng:** Tạo danh sách các đối tượng `Shape` và gọi `draw()` cho từng đối tượng.

**Ví dụ code:**

```python
class Shape:
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Draw a circle")

class Rectangle(Shape):
    def draw(self):
        print("Draw a rectangle")

shapes = [Circle(), Rectangle()]
for shape in shapes:
    shape.draw()
# Draw a circle
# Draw a rectangle
```

---

### 4. Trừu tượng (Abstraction)

- **Định nghĩa:** Trừu tượng là chỉ tập trung vào các đặc điểm quan trọng, che giấu chi tiết cài đặt.
- **Ví dụ mô tả:** Lớp trừu tượng `Animal` định nghĩa phương thức `make_sound()`, các lớp con triển khai chi tiết.
- **Bài toán áp dụng:** Lớp trừu tượng `Employee` với phương thức `calculate_salary()`, các lớp con triển khai cụ thể.

**Ví dụ code:**

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_salary(self):
        pass

class FullTimeEmployee(Employee):
    def calculate_salary(self):
        return 20000000

class PartTimeEmployee(Employee):
    def calculate_salary(self):
        return 10000000

emps = [FullTimeEmployee(), PartTimeEmployee()]
for emp in emps:
    print(emp.calculate_salary())
# 20000000
# 10000000
```
## Thực hành setup virtual environment, pip, quản lý dependencies với requirements.txt
### Venv
![Venv](/images_proof/venv.jpg)

### Pip
![pip_list](/images_proof/pip_list.jpg)

![pip_install](/images_proof/pip_install.jpg)

### Quản lý dependencies với requirements.txt
![requirements](/images_proof/requirements.jpg)