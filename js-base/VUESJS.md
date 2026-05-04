# REPORT: Cấu trúc Project Vue (Vite) và So sánh Options API vs Composition API
---

## 1. Vue.JS
- Vue.js là framework JavaScript dùng để xây dựng giao diện người dùng (UI) và Single Page Application (SPA).

- Vue nổi bật bởi:

    - Dễ học
    - Cú pháp rõ ràng
    - Reactive system mạnh
    - Component-based architecture
    - Hiệu năng tốt

## 2. Vite là gì?

- Vite là build tool hiện đại dùng để phát triển frontend nhanh hơn.

- Vite cung cấp:

   - Dev server cực nhanh
   - Hot Module Replacement (HMR)
   - Build tối ưu với Rollup
   - Hỗ trợ Vue, React, TypeScript

## 3. Cấu trúc của Vue (Vite)
---
### 3.1 Cấu trúc mặc định
```
vue-app/
│
├── node_modules/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── App.vue
│   └── main.js
│
├── .gitignore
├── index.html
├── package.json
├── vite.config.js
└── package-lock.json
```

### 3.2 Giải thích chi tiết từng thư mục
a. node_modules/
- Chức năng: Chứa toàn bộ thư viện được cài bằng npm.

- Ví dụ: Vue, Vite, Axios, Vue Router

b. public/
- Chức năng: Chứa static files:
    - image
    - favicon
    - robots.txt

- Các file trong public/:

    - Không được bundler xử lý
    - Truy cập trực tiếp qua URL
- Ví dụ: public/logo.png

c. src/
- Chức năng: Đây là thư mục chính chứa source code.

d. src/assets/
- Chức năng: chứa CSS, images, fonts

- Khác với public/: assets được Vite optimize hash filename khi build
e. src/components/
- Chức năng: chứa Vue components tái sử dụng.

- Ví dụ: Button.vue, Navbar.vue, Sidebar.vue
f. App.vue
- Chức năng: Component gốc của ứng dụng. Mọi component khác sẽ được render từ đây.

- Ví dụ
```
<template>
    <div>
        <h1>Hello Vue</h1>
    </div>
</template>
```
g. main.js
- Chức năng: Entry point của ứng dụng. Nơi mà sẽ mount Vue app, import CSS, khởi tạo plugins
- Ví dụ

```
import { createApp } from "vue";
import App from "./App.vue";
createApp(App).mount("#app");
```
h. index.html
- Chức năng: File HTML gốc. Vue sẽ mount vào file index này

```
<div id="app"></div>
```
i. package.json
- Chức năng: quản lý dependencies, scripts, project metadata

- Ví dụ scripts:

```
{
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    }
}
```
k. vite.config.js
- Chức năng: cấu hình Vite project

- Ví dụ alias path

```
import { defineConfig } from "vite";

import vue from "@vitejs/plugin-vue";

export default defineConfig({
    plugins: [vue()],

    resolve: {
        alias: {
            "@": "/src"
        }
    }
});
```
## 4. Cấu trúc Project Vue thực tế

```
src/
│
├── api/
├── assets/
├── components/
├── composables/
├── layouts/
├── pages/
├── router/
├── services/
├── stores/
├── utils/
├── views/
├── App.vue
└── main.js
```

### Giải thích cấu trúc thực tế
|Folder|Chức năng|
| :--- |   :---: |
|api| API calls|
|components|Reusable UI|
|composables|Composition logic|
|layouts|Layout components|
|pages/views|Route pages|
|router|Vue Router|
|services|Business logic|
|stores|Pinia/Vuex|
|utils|Helper functions|

## So sánh Options API và Composition API

### 1. Tổng quan

### a. Options API

- Là phương thức xây dựng thành phần Vue truyền thống, được coi là tính năng cốt lõi của Vue kể từ khi nó được xuất bản.
- Options API tổ chức logic các thành phần vào các thành phần rõ ràng như:
  - data
  - methods
  - computed
  - watch
  - lifecycle hooks

- Cung cấp cách tiếp cận gần gũi, có cấu trúc và dễ đọc cho người mới học Vue.

---

### Ví dụ Options API

```javascript
export default {

    data() {
        return {
            name: '',
            age: 0,
            aboveAge: false
        }
    },

    computed: {

        displayProfile() {
            return `My name is ${this.name} and i am ${this.age}`;
        }

    },

    methods: {

        verifyUser() {

            if(this.age < 18) {
                this.aboveAge = false
            } else {
                this.aboveAge = true
            }

        },

    },

    mounted() {
        console.log('Application mounted');
    },

}
```

---

### b. Composition API

- Đây là một phương pháp mới trong việc xây dựng component từ Vue 3.
- Composition API cho phép dev sử dụng phong cách:
  - Functional Programming
  - Reactive Programming

- Logic được tổ chức theo:
  - feature
  - functionality

thay vì theo loại options như Options API.

---

### Ví dụ Composition API

```javascript
import {
    ref,
    reactive,
    computed,
    onMounted
} from 'vue'

const profile = reactive({
    name:'',
    age:''
})

const aboveAge = ref(false)

const verifyUser = () => {
    profile.age < 18
        ? aboveAge.value = false
        : aboveAge.value = true
}

const displayProfile = computed(() => {
    return `My name is ${profile.name} and i am ${profile.age}`;
})

onMounted(() => {
    console.log('Application mounted')
})
```

---

## 2. Structure

### a. Options API

#### Ưu điểm

- Một trong những lợi ích lớn nhất của Options API là:
  - đơn giản
  - dễ hiểu
  - dễ tiếp cận

- Nó cung cấp:
  - mẫu code rõ ràng
  - cấu trúc minh bạch
  - dễ đọc với người mới

- Logic được phân chia theo các khu vực cố định:
  - data
  - methods
  - computed
  - watch

---

#### Phù hợp với

- Người mới học Vue
- Project nhỏ và vừa
- Component đơn giản

---

#### Nhược điểm

Khi component lớn dần:

- Logic bị phân tán ở nhiều nơi
- Khó theo dõi feature hoàn chỉnh
- Khó maintain
- Dễ tạo component quá lớn

---

### Ví dụ vấn đề logic bị phân tán

```javascript
export default {

    data() {
        return {
            users: [],
            loading: false
        }
    },

    methods: {

        async fetchUsers() {
            this.loading = true

            const response = await fetch('/users')

            this.users = await response.json()

            this.loading = false
        }

    },

    computed: {

        totalUsers() {
            return this.users.length
        }

    },

    mounted() {
        this.fetchUsers()
    }

}
```

---

### Vấn đề

Logic liên quan tới:

```text
Users feature
```

bị tách ra ở nhiều nơi:

- data
- methods
- computed
- mounted

Khi component lớn hơn sẽ:

- Khó đọc
- Khó scale
- Khó maintain

---

### b. Composition API

#### Ưu điểm

Composition API tổ chức logic theo:

```text
Feature / Functionality
```

Thay vì:

```text
Option Type
```

---

### Ví dụ

```javascript
import {
    ref,
    computed,
    onMounted
} from 'vue'

export function useUsers() {

    const users = ref([])
    const loading = ref(false)

    const totalUsers = computed(() => {
        return users.value.length
    })

    async function fetchUsers() {

        loading.value = true

        const response = await fetch('/users')

        users.value = await response.json()

        loading.value = false

    }

    onMounted(fetchUsers)

    return {
        users,
        loading,
        totalUsers,
        fetchUsers
    }

}
```

---

### Lợi ích

Toàn bộ logic của:

```text
Users feature
```

được gom chung một nơi.

Giúp:

- Dễ đọc
- Dễ maintain
- Dễ tái sử dụng
- Scale project lớn tốt hơn

---

## 3. Reusability (Khả năng tái sử dụng)

### a. Options API và Mixins

Một hạn chế lớn của Options API là khó tái sử dụng logic giữa nhiều component.

Thông thường phải:

- Copy/paste code
- Hoặc dùng mixins

---

### Ví dụ Mixins

```javascript
var myMixin = {

    created: function () {
        this.hello()
    },

    methods: {

        hello: function () {
            console.log('hello from mixin!')
        }

    }

}

var Component = Vue.extend({
    mixins: [myMixin]
})

var component = new Component()
```

---

### Kết quả

```javascript
hello from mixin!
```

---

### Vấn đề của Mixins

- Khó trace source logic
- Dễ xung đột tên methods/data
- Dependency không rõ ràng
- Khó debug khi project lớn

---

### b. Composition API và Composables

Composition API giới thiệu:

```text
Composables
```

Cho phép tái sử dụng logic linh hoạt hơn.

---

### Ví dụ Composable

#### mouse.js

```javascript
import {
    ref,
    onMounted,
    onUnmounted
} from 'vue'

export function useMouse() {

    const x = ref(0)
    const y = ref(0)

    function update(event) {
        x.value = event.pageX
        y.value = event.pageY
    }

    onMounted(() => {
        window.addEventListener('mousemove', update)
    })

    onUnmounted(() => {
        window.removeEventListener('mousemove', update)
    })

    return {
        x,
        y
    }

}
```

---

### Sử dụng trong component

```vue
<script setup>
import { useMouse } from './mouse.js'

const { x, y } = useMouse()
</script>
```

---

### Ưu điểm của Composables

- Reuse logic tốt hơn
- Dependency rõ ràng
- Dễ test
- Dễ debug
- Dễ maintain

---

## 4. Usage (Khả năng sử dụng)

### Composition API tận dụng toàn bộ sức mạnh JavaScript

Composition API cho phép tích hợp dễ dàng:

- async/await
- Promise
- RxJS
- Functional Programming
- Reactive Programming

---

### Lợi ích

Giúp xây dựng:

- Component phức tạp
- Interactive UI
- Async workflows
- Logic tái sử dụng

một cách dễ dàng hơn.

---

## 5. Learning Curve (Độ khó học)

### a. Options API

#### Ưu điểm

- Dễ học
- Dễ đọc
- Cấu trúc rõ ràng

---

#### Phù hợp với

- Beginner
- Team mới học Vue

---

### b. Composition API

#### Nhược điểm

Composition API khó học hơn do:

- Functional Programming
- Reactive Programming
- ref/reactive
- .value
- Lifecycle hooks mới

---

### So sánh

| Tiêu chí | Options API | Composition API |
|---|---|---|
| Dễ học | Cao | Trung bình |
| Dễ đọc với beginner | Tốt | Khó hơn |
| Flexibility | Trung bình | Rất cao |
| Reusability | Hạn chế | Mạnh |
| Scale project lớn | Khó hơn | Tốt hơn |

---

## 6. Compatibility (Khả năng tương thích)

### Options API

- Hoạt động tốt với:
  - Vue 2
  - Vue 3

---

### Composition API

Composition API:

- Native support trong Vue 3
- Không hỗ trợ mặc định trong Vue 2.6 trở xuống

---

### Với Vue 2 cũ

Cần:

- Upgrade lên Vue 3

hoặc:

- Cài plugin Composition API

---

### Vấn đề

Plugin này đã:

```text
End of Life vào tháng 12/2022
```

Điều này gây khó khăn cho:

- Legacy projects
- Large enterprise systems

---

## 7. Bundle Size & Performance

### Composition API tối ưu hơn

Composition API thường:

- Bundle nhỏ hơn
- Performance tốt hơn

---

### Nguyên nhân

Template có thể truy cập trực tiếp biến trong scope:

```javascript
count.value
```

thay vì:

```javascript
this.count
```

---

### Lợi ích

- Giảm overhead
- Minification tốt hơn
- Build tối ưu hơn

---

## 8. Tổng kết

| Tiêu chí | Options API | Composition API |
|---|---|---|
| Dễ học | Tốt | Khó hơn |
| Readability | Tốt với project nhỏ | Tốt với project lớn |
| Logic organization | Theo option | Theo feature |
| Reusability | Mixins | Composables |
| Maintainability | Trung bình | Tốt |
| TypeScript support | Trung bình | Rất tốt |
| Performance | Tốt | Tốt hơn |
| Scale large project | Khó hơn | Rất tốt |

---

## 9. Kết luận

### Khi nào dùng Options API?

Phù hợp nếu:

- Mới học Vue
- Project nhỏ
- Team beginner
- Component đơn giản

---

### Khi nào dùng Composition API?

Phù hợp nếu:

- Project lớn
- Logic phức tạp
- Reuse logic nhiều
- Dùng TypeScript
- Enterprise applications

---

## Khuyến nghị học tập

### Beginner

Nên bắt đầu với:

```text
Options API
```

---

### Sau đó học Composition API

Khi đã hiểu:

- Reactivity
- Lifecycle
- Component architecture

Composition API sẽ giúp:

- Viết code clean hơn
- Scale project tốt hơn
- Reuse logic mạnh hơn

---

