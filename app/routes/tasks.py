from flask import Blueprint, redirect,render_template,url_for,flash,session,request
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks',__name__)

@tasks_bp.route('/',methods=["GET","POST"])
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.query.all()
    return render_template('tasks.html',tasks=tasks)


@tasks_bp.route('/add',methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    if title:
        new_task = Task(title=title,status="Pending")
        db.session.add(new_task)
        db.session.commit()
        flash('Task Added Successfully.')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status=="Pending":
            task.status='Working'
        elif task.status=="Working":
            task.status="Done"
        # else:
        #     task.status="Pending"
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear',methods=["POST"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash('All tasks are deleted successfully!','info')
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:task_id>',methods=["POST","GET"])
def delete_task(task_id):
    if 'user' not in session:
        flash('Please log in first!','warning')
        return redirect(url_for('auth.login'))
    task = Task.query.get(task_id)
    if not task:
        flash('Task not found!','danger')
        return redirect(url_for('tasks.view_tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Task delete successfully!','success')
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/edit/<int:task_id>',methods=["GET","POST"])
def edit_task(task_id):
    if 'user' not in session:
        flash('Please log in first!','danger')
        return redirect(url_for('auth.login'))
    task = Task.query.get(task_id)
    if not task:
        flash('Task not found!','danger')
        return redirect(url_for('tasks.view_tasks'))
    
    if request.method=="POST":
        new_title = request.form.get('title')
        if not new_title or not new_title.strip():
            flash("Task title can't be empty",'danger')
            return redirect(url_for('tasks.edit_task',task_id=task.id))

        task.title = new_title
        db.session.commit()
        flash('Task Updated Successfully.','success')
        return redirect(url_for('tasks.view_tasks'))
    return render_template("edit_task.html", task=task)