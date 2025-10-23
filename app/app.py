"""
Aplicación web de To-Do List usando Flask.
Permite crear, leer, actualizar y eliminar tareas con un frontend moderno y minimalista.
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from .todo_manager import (
    create_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo,
    get_todos_by_status, get_todos_by_priority, get_overdue_todos, get_stats
)

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route("/health")
def health():
    return "OK", 200


@app.route("/")
def index():
    """Página principal de la To-Do List"""
    todos = get_all_todos()
    stats = get_stats()
    return render_template("index.html", todos=todos, stats=stats)


@app.route("/api/todos", methods=["GET"])
def api_get_todos():
    """API: Obtener todas las tareas"""
    try:
        todos = get_all_todos()
        return jsonify({"success": True, "todos": todos})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos", methods=["POST"])
def api_create_todo():
    """API: Crear una nueva tarea"""
    try:
        data = request.get_json()
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        priority = data.get("priority", "media")
        due_date = data.get("due_date")
        
        if not title:
            return jsonify({"success": False, "error": "El título es requerido"}), 400
        
        todo = create_todo(title, description, priority, due_date)
        return jsonify({"success": True, "todo": todo}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def api_get_todo(todo_id):
    """API: Obtener una tarea por ID"""
    try:
        todo = get_todo_by_id(todo_id)
        if not todo:
            return jsonify({"success": False, "error": "Tarea no encontrada"}), 404
        return jsonify({"success": True, "todo": todo})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def api_update_todo(todo_id):
    """API: Actualizar una tarea"""
    try:
        data = request.get_json()
        todo = update_todo(todo_id, **data)
        if not todo:
            return jsonify({"success": False, "error": "Tarea no encontrada"}), 404
        return jsonify({"success": True, "todo": todo})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    """API: Eliminar una tarea"""
    try:
        success = delete_todo(todo_id)
        if not success:
            return jsonify({"success": False, "error": "Tarea no encontrada"}), 404
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/status/<status>", methods=["GET"])
def api_get_todos_by_status(status):
    """API: Obtener tareas por estado"""
    try:
        todos = get_todos_by_status(status)
        return jsonify({"success": True, "todos": todos})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/todos/priority/<priority>", methods=["GET"])
def api_get_todos_by_priority(priority):
    """API: Obtener tareas por prioridad"""
    try:
        todos = get_todos_by_priority(priority)
        return jsonify({"success": True, "todos": todos})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    """API: Obtener estadísticas"""
    try:
        stats = get_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/overdue", methods=["GET"])
def api_get_overdue_todos():
    """API: Obtener tareas vencidas"""
    try:
        todos = get_overdue_todos()
        return jsonify({"success": True, "todos": todos})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Rutas para formularios HTML (compatibilidad)
@app.route("/add", methods=["POST"])
def add_todo():
    """Agregar tarea desde formulario HTML"""
    try:
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "media")
        due_date = request.form.get("due_date")
        
        if not title:
            return redirect(url_for("index"))
        
        create_todo(title, description, priority, due_date)
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("index"))


@app.route("/update/<int:todo_id>", methods=["POST"])
def update_todo_form(todo_id):
    """Actualizar tarea desde formulario HTML"""
    try:
        status = request.form.get("status")
        if status:
            update_todo(todo_id, status=status)
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo_form(todo_id):
    """Eliminar tarea desde formulario HTML"""
    try:
        delete_todo(todo_id)
        return redirect(url_for("index"))
    except Exception:
        return redirect(url_for("index"))


if __name__ == "__main__":  # pragma: no cover
    app_port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=app_port, host="0.0.0.0")