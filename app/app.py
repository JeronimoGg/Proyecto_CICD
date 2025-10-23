from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from .todo_manager import TodoManager
import os

app = Flask(__name__)
"""Hola"""


def get_todo_manager():
    """Get TodoManager instance based on testing mode"""
    if not hasattr(g, "todo_manager"):
        if os.environ.get("TESTING") == "true":
            g.todo_manager = TodoManager("test_todos.json")
        else:
            g.todo_manager = TodoManager()
    return g.todo_manager


@app.route("/")
def index():
    """Main page with To-Do List interface"""
    todos = get_todo_manager().get_all_todos()
    stats = get_todo_manager().get_stats()
    return render_template("index.html", todos=todos, stats=stats)


@app.route("/add", methods=["POST"])
def add_todo():
    """Add a new todo item"""
    try:
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date", "")

        if not title:
            return jsonify({"error": "Title is required"}), 400

        todo = get_todo_manager().create_todo(title, description, priority, due_date)
        return redirect(url_for("index"))

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/update/<int:todo_id>", methods=["POST"])
def update_todo(todo_id):
    """Update an existing todo item"""
    try:
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "")
        priority = request.form.get("priority", "")
        due_date = request.form.get("due_date", "")

        update_data = {}
        if title:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if status:
            update_data["status"] = status
        if priority:
            update_data["priority"] = priority
        if due_date is not None:
            update_data["due_date"] = due_date

        updated_todo = get_todo_manager().update_todo(todo_id, **update_data)

        if updated_todo:
            return redirect(url_for("index"))
        else:
            return jsonify({"error": "Todo not found"}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    """Delete a todo item"""
    try:
        success = get_todo_manager().delete_todo(todo_id)
        if success:
            return redirect(url_for("index"))
        else:
            return jsonify({"error": "Todo not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# API Routes
@app.route("/api/todos", methods=["GET"])
def api_get_todos():
    """API endpoint to get all todos"""
    todos = get_todo_manager().get_all_todos()
    return jsonify(todos)


@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def api_get_todo(todo_id):
    """API endpoint to get a specific todo"""
    todo = get_todo_manager().get_todo_by_id(todo_id)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404


@app.route("/api/todos", methods=["POST"])
def api_create_todo():
    """API endpoint to create a new todo"""
    try:
        data = request.get_json()
        if not data or not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        todo = get_todo_manager().create_todo(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date", ""),
        )
        return jsonify(todo), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def api_update_todo(todo_id):
    """API endpoint to update a todo"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        updated_todo = get_todo_manager().update_todo(todo_id, **data)
        if updated_todo:
            return jsonify(updated_todo)
        return jsonify({"error": "Todo not found"}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    """API endpoint to delete a todo"""
    try:
        success = get_todo_manager().delete_todo(todo_id)
        if success:
            return jsonify({"message": "Todo deleted successfully"})
        return jsonify({"error": "Todo not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/todos/status/<status>", methods=["GET"])
def api_get_todos_by_status(status):
    """API endpoint to get todos by status"""
    todos = get_todo_manager().get_todos_by_status(status)
    return jsonify(todos)


@app.route("/api/todos/priority/<priority>", methods=["GET"])
def api_get_todos_by_priority(priority):
    """API endpoint to get todos by priority"""
    todos = get_todo_manager().get_todos_by_priority(priority)
    return jsonify(todos)


@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    """API endpoint to get todo statistics"""
    stats = get_todo_manager().get_stats()
    return jsonify(stats)


@app.route("/api/todos/overdue", methods=["GET"])
def api_get_overdue_todos():
    """API endpoint to get overdue todos"""
    overdue = get_todo_manager().get_overdue_todos()
    return jsonify(overdue)


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "To-Do List App is running"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
