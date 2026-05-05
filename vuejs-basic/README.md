# Vue 3 + Vite

## Template Syntax
- Vue sử dụng 1 cú pháp mẫu dựa trên HTML để cho phép ta gán 1 DOM cho 1 thành phần dữ liệu. Mọi mẫu Vue đều là những cú pháp HTML hợp lệ được parse bởi browser và HTML parser.

### a. Text Interpolation
- Form cơ bản nhất của liên kết dữ liệu là nội suy văn bản sử dụng cú pháp 'Mustache' `{{ }}`:
```
    <span> Message: {{ msg }} </span>
```
- Mustache sẽ thay thế giá trị của thuộc tính msg với thành phần mà được tham chiếu, nó cũng sẽ cập nhật khi thuộc tính msg thay đổi

### b. Raw HTML
- `{{}}` biểu diễn dữ liệu như văn bản, không phải HTML. Vì vậy để output là HTML, ta cần sử dụng `v-html` directive:

```
    <p> Using text interpolation: {{ rawHtml }} </p>
    <p> Using v-html directive: <span v-html="rawHtml"></span> </p>
```

- Lưu ý: Render HTML động trên website có thể rất nguy hiểm bởi vì nó có thể dẫn tới XSS vulnerabilities. Vì vậy chỉ sử dụng `v-html` trên nội dung tin cậy và không sử dụng trên nội dung mà user cung cấp

### Attribute Bindings
- Mustache không thể sử dụng được trong thuộc tính HTML. Thay vào đó ta sẽ sử dụng `v-bind` directive

``` <div v-bind:id="dynamicId"></div> ```

- `v-bind` giữ thành phần của thuộc tính id đồng bộ với thành phần của thuộc tính dynamicId. Nếu thế giá trị trả về là null hoặc undefined, thuộc tính sẽ bị xóa bởi thành phần đã Render

- Cú pháp shorthand
``` <div :id="dynamicId"></div> ```

- Boolean attribute: là những thuộc tính chỉ ra những giá trị true/false bởi sự hiện diện của nó trên 1 thành phần.
```<button :disabled="isButtonDisabled"> Button </button> ```

- Liên kết đa thuộc tính: Ví dụ ta có 1 object biểu diễn đa thuộc tính:
```
    const objectOfAttrs = {
        id: 'container',
        class: 'wrapper',
        style: 'background-color:green'
    }
```
- ta có thể liên kết nó với 1 thành phần duy nhất bằng cách sử dụng `v-bind` không có đối số:
```
    <div v-bind="objectOfAttrs"></div>
```

### Directives

- Directives là các thuộc tính đặc biệt với các tiền tố `v-`. Vue cung cấp 1 số lượng lớn các directives được xây dựng sẵn.

#### 1. v-if
- Render 1 phần tử hoặc 1 fragment mẫu dựa trên sự đúng đắn của giá trị biểu thức
- 1 phần `v-if` được gọi, phần tử đó và các thành phần nó chứa bị hủy và tái cấu trúc. Nếu điều kiện khởi tạo là sai, nội dung bên trong sẽ không được render.

#### 2. v-else 
- Ký hiệu của khối 'else' cho `v-if` hoặc 1 chuỗi `v-if` / `v-else-if`
```
    <div v-if="Math.random() > 0.5">
        Now you see me
    </div>
    <div v-else>
        Now you don't
    </div>
```

#### 3. v-else-if
- Ký hiệu khối 'else -if' cho `v-if`
```
    <div v-if="type === 'A'">
        A 
    </div> 
    <div v-else-if="type==='B'">
        B 
    </div>
    <div v-else-if="type==='C'">
        C 
    </div> 
    <div v-else> 
        Not A/B/C 
    </div>
```

#### 4. v-for 
- Hiển thị phần tử hoặc khối mẫu nhiều lần dựa trên nguồn dữ liệu
- Giá trị của chỉ thị phải sử dụng cú pháp đặc biệt `alias in expression` để cung cấp bí danh cho phần tử hiện tại đang được duyệt: 
```
    <div v-for="item in items">
        {{ item.text }}
    </div>
```

#### 5. v-on 
- Lắng nghe sự kiện của phần tử 
- Shorthand: `@`
- Expect: Function | Inline statement | Object (không có đối số)
- Argument: event 
- modifiers:
    - .stop: gọi tới `event.stopPropagation()`.
    - .prevent: gọi tới `event.preventDefault()`.
    - .capture: Thêm lắng nghe sự kiện trong mode capture
    - .self: chỉ xử lý nếu sự kiện được tách khỏi phần tử
    - .{keyAlias} - chỉ xử lý trên đúng khóa.
    - .once: Xử lý 1 lần duy nhất
    - .left: Chỉ xử lý khi có sự kiện của chuột trái
    - .right: Chỉ xử lý khi có sự kiện của chuột phải
    - .middle: Chỉ xử lý khi có sự kiện của chuột giữa
    - .passive: gắn 1 sự kiện DOM với { passive: true }
```
<!-- method handler -->
<button v-on:click="doThis"></button>

<!-- dynamic event -->
<button v-on:[event]="doThis"></button>

<!-- inline statement -->
<button v-on:click="doThat('hello', $event)"></button>

<!-- shorthand -->
<button @click="doThis"></button>

<!-- shorthand dynamic event -->
<button @[event]="doThis"></button>

<!-- stop propagation -->
<button @click.stop="doThis"></button>

<!-- prevent default -->
<button @click.prevent="doThis"></button>

<!-- prevent default without expression -->
<form @submit.prevent></form>

<!-- chain modifiers -->
<button @click.stop.prevent="doThis"></button>

<!-- key modifier using keyAlias -->
<input @keyup.enter="onEnter" />

<!-- the click event will be triggered at most once -->
<button v-on:click.once="doThis"></button>

<!-- object syntax -->
<button v-on="{ mousedown: doThis, mouseup: doThat }"></button>
```

#### 6. v-bind 
- Liên kết 1 hoặc nhiều thuộc tính hoặc 1 thành phần prop tới 1 biểu thức 
- Shorthand: `:`, `.` khi sử dụng `.prop`
- Expect: any (với đối số) | object (ko có đối số)
- Argument: thuộc tính hoặc prop 
- modifier:
    - .camel: Chuyển thuộc tính về dạng camelCase
    - .prop: buộc 1 liên kết trở thành tập hợp như 1 property DOM
    - .attr: buộc 1 liên kết trở thành tập hợp như 1 attribute DOM 
```
    <!-- bind an attribute -->
<img v-bind:src="imageSrc" />

<!-- dynamic attribute name -->
<button v-bind:[key]="value"></button>

<!-- shorthand -->
<img :src="imageSrc" />

<!-- same-name shorthand (3.4+), expands to :src="src" -->
<img :src />

<!-- shorthand dynamic attribute name -->
<button :[key]="value"></button>

<!-- with inline string concatenation -->
<img :src="'/path/to/images/' + fileName" />

<!-- class binding -->
<div :class="{ red: isRed }"></div>
<div :class="[classA, classB]"></div>
<div :class="[classA, { classB: isB, classC: isC }]"></div>

<!-- style binding -->
<div :style="{ fontSize: size + 'px' }"></div>
<div :style="[styleObjectA, styleObjectB]"></div>

<!-- binding an object of attributes -->
<div v-bind="{ id: someProp, 'other-attr': otherProp }"></div>

<!-- prop binding. "prop" must be declared in the child component. -->
<MyComponent :prop="someThing" />

<!-- pass down parent props in common with a child component -->
<MyComponent v-bind="$props" />

<!-- XLink -->
<svg><a :xlink:special="foo"></a></svg>
```

#### 7. v-model
- Tạo ra luồng liên kết 2 chiều trên 1 phần tử form input hoặc 1 thành phần 
- Limited to: 
    - `<input>`
    - `<select>`
    - `<textarea>`
    - component
- modifier:
    - .lazy: lắng nghe những sự kiện thay đổi thay vì input
    - .number: cast dữ liệu string đầu vào về numbers
    - .trim: trim input 

### Reactive data 
---
#### 1. ref()
- Nhận một giá trị bên trong và trả về 1 đối tượng tham chiếu có khả năng phản ứng và thay đổi. Đối tượng này có 1 thuộc tính duy nhất là `.value` trỏ đến giá trị bên trong 

```
    function ref<T>(value: T): Ref<UnwrapRef<T>>

    interface Ref<T> {
        value: T
    }
```

- Đối tượng tham chiếu có thể thay đổi vì vậy, ta có thể gán giá trị mới cho `.value`, nó cũng tự phản ứng ví dụ: Mọi thao tác đọc đối với `.value` đều được theo dõi, các thao tác ghi sẽ kích hoạt các hiệu ứng liên quan.
- Nếu đối tượng được gán làm giá trị của `ref`, đối tượng đó sẽ được làm cho có tính phản ứng sâu bằng phương thức `reactive()`. Điều này cũng có nghĩa là nếu đối tượng chứa các `ref` lồng nhau, chúng sẽ được giải nén sâu.
- Để tránh deep conversion, sử dụng shallowRef() thay thế.

```
    const count = ref(0)
    console.log(count.value)

    const.value = 1
    console.log(count.value)
```

#### 2. reactive()
- Trả về 1 proxy tái khởi động của 1 đối tượng
- Reactive object 
```
    const obj = reactive({ count: 0 })
    obj.count++
```

- Ref unwrapping:
```
    const count = ref(1)
    const obj = reactive({ count })
    
    // ref được giải nén
    console.log(obj.count == count.value)

    // cập nhật obj.count
    count.value++
    console.log(count.value)
    console.log(obj.count)

    // cập nhật count Ref
    obj.count++
    console.log(obj.count)
    console.log(count.value)
```

#### 3. computed()
- Nhận 1 hàm getter() và trả về 1 đối tượng ref cho giá trị được trả về từ getter. Nó cũng có thể nhận 1 đối tượng với hàm get, set để tạo 1 đối tượng ref có thể ghi được.

- Type 
```
    function computed<T> (
        getter: (oldValue: T | undefined) => T, 
        debuggerOptions?: DebuggerOptions 
    ): Readonly<Ref<Readonly<T>>>

    function computed<T>(
        options: {
            get: (oldValue: T | undefined) => T 
            set: (value: T) => void 
        }, 
        debuggerOptions?: DebuggerOptions
    ): Ref<T>
```
- Ví dụ:
1. readonly computed ref:
```
    const count = ref(1)
    const plusOne = computed(() => count.value + 1)

    console.log(plusOne.value)

    plusOne.value++
```

2. Writable computed ref:
```
    const count = ref(1)
    const plusOne = computed({
        get: () => count.value + 1,
        set: (val) => {
            count.value = val - 1
        }
    })

    plusOne.value = 1
    console.log(count.value)
```

#### 4. watch()
- Quan sát 1 hoặc nhiều nguồn dữ liệu tái chủ động và gọi hàm callback khi nguồn thay đổi
- Type 
```
// watching single source
function watch<T>(
  source: WatchSource<T>,
  callback: WatchCallback<T>,
  options?: WatchOptions
): WatchHandle

// watching multiple sources
function watch<T>(
  sources: WatchSource<T>[],
  callback: WatchCallback<T[]>,
  options?: WatchOptions
): WatchHandle

type WatchCallback<T> = (
  value: T,
  oldValue: T,
  onCleanup: (cleanupFn: () => void) => void
) => void

type WatchSource<T> =
  | Ref<T> // ref
  | (() => T) // getter
  | (T extends object ? T : never) // reactive object

interface WatchOptions extends WatchEffectOptions {
  immediate?: boolean // default: false
  deep?: boolean | number // default: false
  flush?: 'pre' | 'post' | 'sync' // default: 'pre'
  onTrack?: (event: DebuggerEvent) => void
  onTrigger?: (event: DebuggerEvent) => void
  once?: boolean // default: false (3.4+)
}

interface WatchHandle {
  (): void // callable, same as `stop`
  pause: () => void
  resume: () => void
  stop: () => void
}
```
- mặc định của watch() là lazy, chỉ gọi callback 1 lần duy nhất khi nguồn được quan sát thay đổi
- Đối số đầu tiên của watch:
    - hàm getter trả về 1 giá trị 
    - 1 ref 
    - 1 đối tượng reactive 
    - hoặc 1 mảng
- Đối số thứ 2 của watch là callback được gọi khi nguồn thay đổi. Callback nhận vào 3 đối số: giá trị mới, giá trị cũ, 1 hàm được đăng ký để dọn dẹp callback.
Callback dọn dẹp sẽ được gọi ngay trước khi effect tiếp theo được chạy
- Đối số thứ 3 có thể là các đối tượng sau:
    - immediate
    - deep
    - flush
    - onTrack / onTrigger
    - once 

## Component Basic
- Components cho phép ta chia nhỏ UI thành những phần độc lập và tái sử dụng được. Vue thực thi những mô hình component cho phép ta đóng gói nội dung và logic ở bên trong mỗi component
- Để sử dụng 1 component con, ta cần import nó trong component cha
```
    <script setup>
    import ButtonCounter from './ButtonCounter.vue'
    </script>

    <template>
    <h1>Here is a child component!</h1>
    <ButtonCounter />
    </template>
```
- Component có thể tái sử dụng nhiều lần nếu muốn

### 1. Passing props
- Giả sử ta đang build 1 blog, ta cần 1 component đại diện cho 1 bài blog. Ta muốn toàn bộ các blog đều giống nhau về layout nhưng khác nhau về nội dung.
Component sẽ không còn hữu dụng nếu chúng ta không thể truyền dữ liệu vào nó (như tiêu đề, nội dung của mỗi blog riêng biệt mà ta muốn hiển thị).
- Props sẽ giải quyết vấn đề này, để truyền 1 tiêu đề cho thành phần blog, ta phải khai báo danh sách props mà thành phần này chấp nhận bằng cách sử dụng `defineProps`
```
    <script setup>
    defineProps(['title'])
    </script>

    <template>
        <h4> {{ title }} </h4>
    </template>
```
- defineProps là 1 macro compile-time, chỉ hoạt động trong <script setup> mà không cần import từ bên ngoài, defineProps trả về 1 đối tượng mà chứa các props được truyền tới component vì vậy có thể truy cập tới chúng bằng Js nếu cần.
- 1 component có thể có nhiều props nếu ta muốn
- Nói tóm lại: khi component cha muốn truyền dữ liệu tới component con -> sử dụng props

### 2. emit events
- Là cơ chế cho phép component con gửi sự kiện lên component cha
- Ví dụ:
Child Component
```
    <script setup>
    const emit = defineEmits(['click-me'])

    const handleClick = () => {
        emit('click-me')
    }
    </script>

    <template>
        <button @click="handleClick">
            Click me
        </button>
    </template>
```
Parent Component
```
    <template>
        <ChildButton @click-me="handleClick"/>
    <template>

    <script setup>
    const handleClick = () => {
        console.log('Child clicked!')
    }
    </script>
```

- Ví dụ với emit có dữ liệu
ProductItem
```
    <script setup>
    const props = defineProps({
        product: Object
    })

    const emit = defineEmits(['add-to-cart'])

    const add = () => {
        emit('add-to-cart', props.product)
    }
    </script>

    <template>
        <button @click="add">
            Add to cart
        </button>
    </template>
```
Parent
```
    <template>
        <ProductItem 
            :product="product"
            @add-to-cart="handleAdd"
        />
    </template>

    <script setup>
    const handleAdd = (product) => {
        console.log('Added: ', product)
    }
    </script>
```
-> Child không tự xử lý logic mà chỉ thông báo sự kiện tới component cha, parent sẽ quyết định hành vi sẽ thực hiện