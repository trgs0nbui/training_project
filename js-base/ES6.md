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
  a. Biểu thức đơn

```
    // Cú pháp đầy đủ
    const add = (a, b) => {
        return a + b;
    }

    // Implicit Return
    const addShort = (a, b) => a + b;

    console.log(addShort(5, 3))
```

b. Object Literal
Lưu ý: Cần bọc đối tượng trong `()` để JS không hiểu nhầm `{}` là một khối hàm

```
    // Cách viết lỗi
    const getUser = name => { name: name};

    // Cách viết đúng với Implicit Return
    const getUser = name => ({ name: name, role: 'admin'});

    console.log(getUser("Sơn"));
```

c. Kết hợp với các phương thức mảng (map, filter)

```
    const numbers = [6-10];

    // Nhân đôi từng phần tử trong mảng
    const doubled = numbers.map(n => n * 2);
    // Thay vì: numbers.map(function(n) { return n * 2; })

    // Lọc các số lớn hơn 3
    const filtered = numbers.filter(n => n > 3);

    console.log(doubled);  // [7, 9, 11-13]
    console.log(filtered); // [9, 10]
```
### 3. Lexical `this`

#### Khái niệm

- Arrow Function không tạo ra `this` riêng.
- Giá trị `this` được kế thừa từ phạm vi bên ngoài nơi function được định nghĩa.

Điều này giúp tránh lỗi phổ biến khi làm việc với callback hoặc asynchronous code.

---

#### So sánh với function truyền thống

##### Function thông thường

```javascript
const user = {
    name: "Son",

    showName: function () {

        setTimeout(function () {
            console.log(this.name);
        }, 1000);

    }
};

user.showName();
```

##### Kết quả

```javascript
undefined
```

Nguyên nhân:

- `this` bên trong `setTimeout` trỏ tới object global (`window` trong browser).

---

##### Arrow Function

```javascript
const user = {
    name: "Son",

    showName: function () {

        setTimeout(() => {
            console.log(this.name);
        }, 1000);

    }
};

user.showName();
```

##### Kết quả

```javascript
Son
```

---

#### Trường hợp sử dụng thực tế

##### Event Listener

```javascript
class Counter {

    constructor() {
        this.count = 0;
    }

    start() {

        setInterval(() => {
            this.count++;
            console.log(this.count);
        }, 1000);

    }

}

const counter = new Counter();

counter.start();
```

---

#### Lưu ý quan trọng

Arrow Function KHÔNG phù hợp để:

- Làm method của object nếu cần `this` động
- Làm constructor
- Sử dụng với `new`

Ví dụ:

```javascript
const person = {
    name: "Son",

    sayHi: () => {
        console.log(this.name);
    }
};

person.sayHi();
```

##### Kết quả

```javascript
undefined
```

---

## Destructuring

### 1. Object Destructuring

#### Định nghĩa

Cho phép trích xuất dữ liệu từ object và gán vào biến nhanh chóng.

---

### Ví dụ cơ bản

```javascript
const user = {
    name: "Son",
    age: 22,
    city: "Hanoi"
};

const { name, age } = user;

console.log(name);
console.log(age);
```

##### Kết quả

```javascript
Son
22
```

---

### Đổi tên biến

```javascript
const user = {
    name: "Son"
};

const { name: username } = user;

console.log(username);
```

##### Kết quả

```javascript
Son
```

---

### Gán giá trị mặc định

```javascript
const user = {
    name: "Son"
};

const {
    name,
    age = 18
} = user;

console.log(age);
```

##### Kết quả

```javascript
18
```

---

### Nested Destructuring

```javascript
const user = {
    name: "Son",

    address: {
        city: "Hanoi",
        country: "Vietnam"
    }
};

const {
    address: { city }
} = user;

console.log(city);
```

##### Kết quả

```javascript
Hanoi
```

---

### Destructuring trong tham số hàm

```javascript
function displayUser({ name, age }) {
    console.log(name);
    console.log(age);
}

displayUser({
    name: "Son",
    age: 22
});
```

---

## 2. Array Destructuring

### Ví dụ cơ bản

```javascript
const colors = ["red", "blue", "green"];

const [first, second] = colors;

console.log(first);
console.log(second);
```

##### Kết quả

```javascript
red
blue
```

---

### Bỏ qua phần tử

```javascript
const numbers = [1, 2, 3, 4];

const [a, , c] = numbers;

console.log(a);
console.log(c);
```

##### Kết quả

```javascript
1
3
```

---

### Hoán đổi biến

```javascript
let x = 10;
let y = 20;

[x, y] = [y, x];

console.log(x);
console.log(y);
```

##### Kết quả

```javascript
20
10
```

---

### Kết hợp Rest Operator

```javascript
const numbers = [1, 2, 3, 4, 5];

const [first, ...rest] = numbers;

console.log(first);
console.log(rest);
```

##### Kết quả

```javascript
1
[2, 3, 4, 5]
```

---

## Spread Operator (...)

### Định nghĩa

Spread Operator cho phép:

- Trải phần tử của array
- Copy object/array
- Merge dữ liệu

---

## 1. Spread với Array

### Copy array

```javascript
const numbers = [1, 2, 3];

const cloned = [...numbers];

console.log(cloned);
```

---

### Merge array

```javascript
const arr1 = [1, 2];
const arr2 = [3, 4];

const merged = [...arr1, ...arr2];

console.log(merged);
```

##### Kết quả

```javascript
[1, 2, 3, 4]
```

---

### Thêm phần tử

```javascript
const numbers = [2, 3];

const result = [1, ...numbers, 4];

console.log(result);
```

##### Kết quả

```javascript
[1, 2, 3, 4]
```

---

## 2. Spread với Object

### Copy object

```javascript
const user = {
    name: "Son",
    age: 22
};

const clonedUser = {
    ...user
};

console.log(clonedUser);
```

---

### Merge object

```javascript
const basicInfo = {
    name: "Son"
};

const extraInfo = {
    age: 22,
    city: "Hanoi"
};

const user = {
    ...basicInfo,
    ...extraInfo
};

console.log(user);
```

---

### Override property

```javascript
const user = {
    name: "Son",
    age: 20
};

const updatedUser = {
    ...user,
    age: 22
};

console.log(updatedUser);
```

##### Kết quả

```javascript
{
    name: "Son",
    age: 22
}
```

---

## Rest Operator (...)

### Định nghĩa

Rest Operator gom nhiều giá trị thành:

- Một array
- Một object

---

## 1. Rest Parameters

### Ví dụ

```javascript
function sum(...numbers) {

    return numbers.reduce((total, current) => {
        return total + current;
    }, 0);

}

console.log(sum(1, 2, 3, 4));
```

##### Kết quả

```javascript
10
```

---

### Kết hợp tham số thông thường

```javascript
function introduce(name, ...hobbies) {

    console.log(name);
    console.log(hobbies);

}

introduce("Son", "Coding", "Gaming", "Music");
```

##### Kết quả

```javascript
Son
["Coding", "Gaming", "Music"]
```

---

## 2. Rest trong Destructuring

### Với object

```javascript
const user = {
    name: "Son",
    age: 22,
    city: "Hanoi"
};

const { name, ...others } = user;

console.log(name);
console.log(others);
```

##### Kết quả

```javascript
Son

{
    age: 22,
    city: "Hanoi"
}
```

---

## Async/Await

### Định nghĩa

- `async/await` giúp xử lý Promise dễ đọc hơn.
- Là cú pháp xây dựng trên Promise.

---

## 1. Async Function

### Ví dụ

```javascript
async function hello() {
    return "Hello World";
}

hello().then(console.log);
```

##### Kết quả

```javascript
Hello World
```

---

## 2. Await

### Ví dụ Promise

```javascript
function fetchData() {

    return new Promise((resolve) => {

        setTimeout(() => {
            resolve("Data loaded");
        }, 2000);

    });

}
```

---

### Sử dụng await

```javascript
async function showData() {

    const result = await fetchData();

    console.log(result);

}

showData();
```

##### Kết quả

```javascript
(sau 2 giây)

Data loaded
```

---

## 3. Xử lý lỗi với try/catch

```javascript
async function getUser() {

    try {

        const response = await fetch(
            "https://wrong-api-url.com"
        );

        const data = await response.json();

        console.log(data);

    } catch (error) {

        console.log("Fetch failed");

    }

}
```

---

## 4. Chạy nhiều Promise song song

### Promise.all()

```javascript
async function loadData() {

    const [users, posts] = await Promise.all([
        fetch("https://jsonplaceholder.typicode.com/users"),
        fetch("https://jsonplaceholder.typicode.com/posts")
    ]);

    console.log(users);
    console.log(posts);

}

loadData();
```

---

## Modules (ESM)

### Định nghĩa

ES Modules giúp chia nhỏ code thành nhiều file độc lập.

Sử dụng:

- `export`
- `import`

---

## 1. Named Export

### math.js

```javascript
export function add(a, b) {
    return a + b;
}

export function subtract(a, b) {
    return a - b;
}
```

---

### app.js

```javascript
import {
    add,
    subtract
} from "./math.js";

console.log(add(5, 2));
console.log(subtract(5, 2));
```

---

## 2. Default Export

### hello.js

```javascript
export default function hello() {
    console.log("Hello");
}
```

---

### app.js

```javascript
import hello from "./hello.js";

hello();
```

---

## 3. Import tất cả module

```javascript
import * as math from "./math.js";

console.log(math.add(2, 3));
```

---

## 4. Đổi tên khi import/export

### Export

```javascript
export {
    add as plus
};
```

---

### Import

```javascript
import {
    plus
} from "./math.js";

console.log(plus(2, 3));
```

---

## 5. Trường hợp sử dụng thực tế

### Tách API service

#### api.js

```javascript
export async function getUsers() {

    const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
    );

    return response.json();

}
```

---

#### app.js

```javascript
import { getUsers } from "./api.js";

getUsers().then(console.log);
```

---

## Template Literals

### Định nghĩa

Template Literals sử dụng dấu backtick `` ` `` để:

- Viết chuỗi nhiều dòng
- Nội suy biến với `${}`

---

## 1. Nội suy biến

```javascript
const name = "Son";
const age = 22;

console.log(
    `My name is ${name} and I am ${age} years old`
);
```

---

## 2. Chuỗi nhiều dòng

```javascript
const html = `
    <div>
        <h1>Hello</h1>
    </div>
`;

console.log(html);
```

---

## 3. Gọi biểu thức

```javascript
const a = 5;
const b = 10;

console.log(`${a} + ${b} = ${a + b}`);
```

##### Kết quả

```javascript
5 + 10 = 15
```

---

## Symbols

### Định nghĩa

`Symbol` là kiểu dữ liệu primitive mới trong ES6.

Mỗi Symbol luôn là duy nhất.

---

## Ví dụ cơ bản

```javascript
const id1 = Symbol("id");
const id2 = Symbol("id");

console.log(id1 === id2);
```

##### Kết quả

```javascript
false
```

---

## Trường hợp sử dụng

### Tạo thuộc tính private-like

```javascript
const ID = Symbol("id");

const user = {
    name: "Son",
    [ID]: 123
};

console.log(user[ID]);
```

---

## Map

### Định nghĩa

`Map` là cấu trúc dữ liệu lưu key-value.

Khác với object:

- Key có thể là bất kỳ kiểu dữ liệu nào

---

## Ví dụ

```javascript
const userMap = new Map();

userMap.set("name", "Son");
userMap.set("age", 22);

console.log(userMap.get("name"));
```

---

## Duyệt Map

```javascript
for (const [key, value] of userMap) {
    console.log(key, value);
}
```

---

## Set

### Định nghĩa

`Set` lưu các giá trị duy nhất.

Không cho phép trùng lặp.

---

## Ví dụ

```javascript
const numbers = new Set([1, 2, 2, 3, 3]);

console.log(numbers);
```

##### Kết quả

```javascript
Set(3) {1, 2, 3}
```

---

## Loại bỏ phần tử trùng lặp

```javascript
const arr = [1, 1, 2, 2, 3];

const unique = [...new Set(arr)];

console.log(unique);
```

##### Kết quả

```javascript
[1, 2, 3]
```

---