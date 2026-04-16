import time

"""
    Chuẩn bị kiến thức về decorator
    
    Một decorator là một hàm dùng để bọc một hàm khác (hay nhận 1 hàm khác làm đối số)
    nhằm mở rộng chức năng của hàm đó mà không cần thay đổi mã nguồn của hàm được bọc.
    
    Bài toán sử dụng Decorator: 
        - Tránh lặp code
        - Tách biệt logic chính và logic phụ (logging, authentication, timing)
"""

# Nested function

def outer_func(x):
    def inner_func(y):
        return x + y
    
    return inner_func

add_five = outer_func(5)
result = add_five(6)
print(f" Kết quả: {result} ")

# Truyền hàm như một đối số
def add(x, y):
    return x + y

def calculate(func, a, b):
    return func(a, b)

result = calculate(add, 10, 20)
print(f" Kết quả: {result} " )

# Trả về một hàm như một giá trị
def greeting(name):
    def say_hello():
        return f"Hello, {name}!"
    
    return say_hello

greet = greeting("Atlas")
print(greet())

# DECORATOR
def make_pretty(func):
    def inner():
        print("I got decorated")
        
        func()
    return inner

def ordinary():
    print("I am ordinary")
    
decorated_func = make_pretty(ordinary)

decorated_func()

# @ symbol
def make_pretty1(func):
    def inner():
        print("I got decorated 1")
        func()
        
    return inner

@make_pretty1
def ordinary1():
    print("I am oridinary 1")
    
ordinary1()

# Decorator với tham số
def smart_divide(func):
    def inner(a, b):
        print("I am going to divide", a, "and", b)
        if b == 0:
            print("Whoops! cannot divide by zero")
            return
        
        return func(a, b)
    return inner

@smart_divide
def divide(a, b):
    return a / b

divide(10, 2)

divide(10, 0)

# Chaining decorators
def star(func):
    def inner(*args, **kwargs): # args và kwargs được sử dụng để truyền bất kỳ số lượng đối số nào
        print("*" * 15)
        func(*args, **kwargs)
        print("*" * 15)
    return inner

def percent(func):
    def inner(*args, **kwargs):
        print("%" * 15)
        func(*args, **kwargs)
        print("%" * 15)
    return inner

@star
@percent
def printer(msg):
    print(msg)
    
printer("Hello") 
# Output sẽ thực hiện truyền msg qua percent trước sau đó mới truyền qua star.

# Đo thời gian chạy của 1 hàm
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time: {end - start} seconds")
        return result
    return wrapper

@timer
def long_time(msg):
    print(msg)
    
long_time("Check long time function!")

