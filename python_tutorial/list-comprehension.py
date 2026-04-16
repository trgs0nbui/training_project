"""
    Cơ bản về list
"""
# Loại bỏ phần tử trùng lặp
my_list = [1, 2, 2, 3, 3, 6, 6, 7, 7]

unique_list = list(set(my_list))
print(unique_list) # Output: [1, 2, 3, 6, 7]

# Truy cập và thay đổi phần tử trong list
this_list = ["apple","mango", "mango", "cherry",  "kiwi", "banana", "banana", "melon"]

# Truy cập phần tử
print(this_list[1]) # Output: banana -> trả về phần tử ở vị trí thứ 1
print(this_list[-1]) # Output: melon -> trả về phần tử ở vị trí cuối cùng bằng cách sử dụng chỉ mục âm

# Truy cập phần tử bằng slice
print(this_list[2:5]) # Output: ['cherry', 'kiwi', 'melon']

# Thay đổi phần tử
this_list[1] = "blackcurrant"

this_list[2:5] = ["blackcurrant", "watermelon"] # Thay đổi phần tử bằng slice

# Thêm phần tử vào list
this_list.append("orange")

this_list.insert(1, "grape") # Thêm phần tử vào vị trí được chỉ định

# Thêm phần tử của một list vào một list khác
tropical = ["mango", "pineapple", "papaya"]
this_list.extend(tropical) # Các phần tử được thêm vào cuối của list hiện tại

# Xóa phần tử xuất hiện đầu tiên khỏi list
this_list.remove("banana")

# Xóa phần tử tại vị trí được chỉ định
this_list.pop(1) # Nếu không được chỉ định vị trí, pop() sẽ xóa phần tử cuối cùng

del this_list[0]

# Xóa tất cả phần tử khỏi list
this_list.clear()

"""
    Vòng lặp đối với list
"""

fruits = ["apple", "banana", "cherry"]

# Vòng lặp for
for i in range(len(fruits)): # sử dụng hàng range() để lặp qua chỉ mục của list
    print(fruits[i])
    
for i in fruits: # Trực tiếp lặp qua phần tử của list
    print(i)

# Vòng lặp while
i = 0
while i < len(fruits):
    print(fruits[i])
    i += 1
    
"""
    List comprehension
"""
# Cú pháp: [<Biểu thức> for <biến> in <tập dữ liệu> if <biểu thức điều kiện>]
"""
    - []: Được sử dụng để tạo một list mới
    - <biểu thức>: Biểu thức được tính toán cho mỗi phần tử trong tập dữ liệu
    - <biến>: Biến đại diện cho phần tử hiện tại trong quá trình lặp
    - <tập dữ liệu>: Tập dữ liệu mà có thể là list, tuple, string, dictionary 
        hoặc bất cắ đối tượng nào có thể lặp được
    - <biểu thức điều kiện>: Điều kiện để lọc các phần tử, nếu biểu thức điều kiện là True
        thì phần tử sẽ thỏa mãn, nếu không thì phần tử sẽ bị loại bỏ sau khi kết thúc vòng lặp
"""
# In ra từng phần tử trong list với list comprehension
this_list = ["John", "Jane", "Jack", "Jill"]
[print(x) for x in this_list] # In ra từng phần tử trong list

# Lọc số chẵn từ một list
even_numbers = [x for x in range(10) if x % 2 == 0]
print(even_numbers) # Output: [0, 2, 4, 6, 8]

# Bình phương các số từ 1 đến 10
squared_numbers = [x**2 for x in range(1, 11)]
print(squared_numbers)

# Xử lý chuỗi với list comprehension, tạo một list mới chứa độ dài mỗi chuỗi của list ban đầu
this_list = ["python", "java", "c++", "golang"]
lengths = [len(x) for x in this_list]
print(lengths) # Output: [6, 4, 3, 6]

# Nested list comprehension, tạo một ma trận 4x4
matrix = [[j for j in range(4)] for i in range(4)]
print(matrix) # Output: [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

# Flatten list, tạo một list phẳng từ một list lồng nhau
nested_list = [[1, 2, 3], [4, 5], [6, 7, 8]]
# Duyệt qua từng sublist trong nested_list sau đó duyệt qua từng phần tử bên trong sublist và thêm chúng vào flattened_list
flattened_list = [item for sublist in nested_list for item in sublist] 
print(flattened_list) # Output: [1, 2, 3, 4, 5, 6, 7, 8]