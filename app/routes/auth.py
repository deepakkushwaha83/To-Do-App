from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User   # Ensure User model exists with id, username, email, password

auth_bp = Blueprint('auth', __name__)

# ---------- LOGIN ----------
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and Password are required!", "warning")
            return redirect(url_for("auth.login"))

        # Fetch user from DB
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id   # store only user_id
            flash('Login Successful', 'success')
            return redirect(url_for('tasks.view_tasks'))  # ✅ make sure route exists
        else:
            flash('Invalid Credentials', 'danger')
        
    return render_template('login.html')


# ---------- LOGOUT ----------
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)   # clear user_id
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))


# ---------- REGISTER ----------
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password or not email:
            flash("All fields are required!", "warning")
            return redirect(url_for("auth.register"))

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("auth.register"))

        # Save user in database with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
