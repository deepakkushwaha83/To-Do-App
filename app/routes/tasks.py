from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=["GET", "POST"])
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()

    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=["POST"])
def add_task():
    if 'user_id' not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if not title or not title.strip():
        flash("Task cannot be empty!", "danger")
        return redirect(url_for('tasks.view_tasks'))

    user_id = session['user_id']
    new_task = Task(title=title, user_id=user_id)

    db.session.add(new_task)
    db.session.commit()

    flash("Task added successfully!", "success")
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Done"
        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods=["POST"])
def clear_tasks():
    if 'user_id' not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    Task.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash('Your tasks were deleted successfully!', 'info')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete/<int:task_id>', methods=["POST", "GET"])
def delete_task(task_id):
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        flash('Task not found or not yours!', 'danger')
        return redirect(url_for('tasks.view_tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/edit/<int:task_id>', methods=["GET", "POST"])
def edit_task(task_id):
    if 'user_id' not in session:
        flash('Please log in first!', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        flash('Task not found or not yours!', 'danger')
        return redirect(url_for('tasks.view_tasks'))

    if request.method == "POST":
        new_title = request.form.get('title')
        if not new_title or not new_title.strip():
            flash("Task title can't be empty", 'danger')
            return redirect(url_for('tasks.edit_task', task_id=task.id))

        task.title = new_title
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('tasks.view_tasks'))

    return render_template("edit_task.html", task=task)
