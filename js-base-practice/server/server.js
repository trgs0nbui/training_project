const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

let todos = [
    {
        id: 1,
        title: "Learn Promise"
    },
    {
        id: 2,
        title: "Learn Fetch API"
    }
];

app.get("/todos", (req, res) => {

    setTimeout(() => {

        res.json(todos);

    }, 1000);

});

app.post("/todos", (req, res) => {

    const newTodo = {
        id: Date.now(),
        title: req.body.title
    };

    todos.push(newTodo);

    res.status(201).json(newTodo);

});

app.delete("/todos/:id", (req, res) => {

    const id = Number(req.params.id);

    todos = todos.filter(todo => {
        return todo.id !== id;
    });

    res.json({
        message: "Deleted"
    });

});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});