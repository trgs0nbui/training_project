const todoList = document.getElementById("todo-list");

const addBtn = document.getElementById("add-btn");

const todoInput = document.getElementById("todo-input");

async function fetchTodos() {

    const response = await fetch(
        "http://localhost:3000/todos"
    );

    const todos = await response.json();

    renderTodos(todos);

}

async function addTodo() {

    const title = todoInput.value;

    if (!title) return;

    await fetch(
        "http://localhost:3000/todos",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title
            })
        }
    );

    todoInput.value = "";

    fetchTodos();

}

function renderTodos(todos) {

    todoList.innerHTML = "";

    todos.forEach(todo => {

        const li = document.createElement("li");

        li.innerHTML = `
            ${todo.title}

            <button onclick="deleteTodo(${todo.id})">
                Delete
            </button>
        `;

        todoList.appendChild(li);

    });

}

addBtn.addEventListener("click", addTodo);