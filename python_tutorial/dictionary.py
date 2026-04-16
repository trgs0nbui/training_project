"""
    Dictinary là một kiểu dữ liệu không thứ tự, dùng để lưu trữ dữ liệu theo cặp key-value
    Mỗi key được liên kết với một value, và key phải là duy nhấ trong dictionary
    Dictionary được định nghĩa bằng cách sử dụng dấu `{}` và các cặp key-value 
    
    Đặc điểm:
    - Không có thứ tự
    - Có thể thay đổi: Giá trị của các phần tử trong dictionary có thể thay đổi sau khi khởi tạo
    - Hiệu quả truy cập: Truy cập value nhánh chóng bằng key
    - Không thể truy cập phần tử bằng chỉ mục
    - Không thể sắp xếp các phần tử theo thứ tự cụ thể
"""
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
print(len(my_dict)) # Output: 3

# Lấy ra value thông qua key
print(my_dict["name"]) # Ouput: Alice
print(my_dict["city"]) # Output: New York

# Thay đổi giá trị
my_dict["age"] = 31
print(my_dict["age"]) # Output: 31

# Lặp qua dictionary
for key, value in my_dict.items():
    print(f"Key: {key}, Value: {value}")
    
# Cập nhật phần tử
my_dict.update({"color": "red"})
print(my_dict)

# Nested dictionary
nested_dict = {
    "person1": {
        "name": "James",
        "age": 23
    },
    "person2": {
        "name": "Emily",
        "age": 39
    },
    "person3": {
        "name": "Michael",
        "age": 45
    }
}

# Lặp qua các phần tử trong nested dictionary
for person, info in nested_dict.items():
    print(person)
    
    for key, value in info.items():
        print(f" {key}: {value}")

"""
    Thực hành với dictionary
"""

# Đếm số lần xuất hiện của mỗi phần tử trong một list
words = ["apple", "banana", "apple", "orange", "banana", "apple"] # Tạo list chứa các phần tử lặp lại
word_count = {} # Tạo một dictionary rỗng để lưu số lần xuất hiện ứng với từng phần tử

for word in words: # Lặp qua từng phần tử trong list
    word_count[word] = word_count.get(word, 0) + 1 # Với mỗi phần tử, số lần xuất hiện được cập nhật trong dictionary
    
print(word_count)

# Đảo cặp giá trị key-value thành value-key
original_dict = {"a": 1, "b": 2, "c": 3}
inverted_dict = {}

for key, value in original_dict.items():
    inverted_dict[value] = key
    
print(inverted_dict)

# Lọc ra các phần tử có giá trị lớn hơn ngưỡng cho trước
threshold = 6
scores = {"Alice": 8, "Bob": 5, "Charlie": 9, "David": 4}

for key, value in scores.items():
    if value > threshold:
        print(f"{key} có điểm số lớn hơn {threshold}: {value}")
# Output: Alice có điểm số lớn hơn 6: 8, Charlie có điểm số lớn hơn 6: 9

# Dictionary comprehension 
# Cú pháp: {<biểu thức key>: <biểu thức value> for <biến> in <tập dữ liệu> if <biểu thức điều kiện>}
"""
    {}: Được sử dụng để tạo một dictionary mới
    <biểu thức key>: Biểu thức được tính toán để tạo ra key cho mỗi phần tử trong tập dữ liệu
    <biểu thức value>: Biểu thức được tính toán để tạo ra value cho mỗi phần tử trong tập dữ liệu
    <biến>: Biến đại diện cho phần tử hiện tại trong quá trình lặp qua tập dữ liệu
    <tập dữ liệu>: Tập dữ liệu có thể là list, tuple, string hay bất kỳ đối tượng nào có thể lặp qua
    <biểu thức điều kiện>: Điều kiện để lọc các phần tử, nếu biểu thức điều kiện là True thì phần thử 
        sẽ thỏa mãn, nếu không thì phần tử sẽ bị loại bỏ sau khi kết thức vòng lặp
"""

this_list = ["John", "Hannah", "James", "Jill"]
# Tạo một dictionary mới với key là phần tử trong list và value là độ dài của phần tử
new_dict = {x: len(x) for x in this_list}
print(new_dict)

# Group dữ liệu theo một tiêu chí nhất định

students = [
    { "name": "Alice", "class": "Math" },
    { "name": "Bob", "class": "Science" },
    { "name": "Charlie", "class": "Math" },
    { "name": "David", "class": "Science" },
    { "name": "Eve", "class": "Literature" }
]

# Tạo một dictionary mới với key là lớp học và value là tên của học sinh
grouped_students = {student["class"]: [student["name"]] for student in students}
print(grouped_students)