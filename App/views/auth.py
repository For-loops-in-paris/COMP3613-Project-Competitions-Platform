from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from App.models import db
from App.controllers import *


from.index import index_views

from App.controllers import *

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student = get_student_by_username(request.form['username'])
        moderator = get_moderator_by_username(request.form['username'])
        if student:
            if request.form['username'] == student.username and student.check_password(request.form['password']):
                login_user(student)
                session['user_type'] = 'student'
                flash("Login successful!", category='success')
                return redirect(url_for('index_views.leaderboard_page',leaderboard_id=0))
            else:
                flash("Invalid Credentials!", category='error')
                return render_template('login.html', user=current_user)
        
        elif moderator:
            if request.form['username'] == moderator.username and moderator.check_password(request.form['password']):
                login_user(moderator)
                session['user_type'] = 'moderator'
                flash("Login successful!", category='success')
                return redirect(url_for('index_views.leaderboard_page',leaderboard_id=0))
            else:
                flash("Invalid Credentials!", category='error')
                return render_template('login.html', user=current_user)
    
        else:
            flash("Username not found!", category='error')
            return render_template('login.html',user=current_user)
    return render_template('login.html', user=current_user)

@auth_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successful!", category='success')
    session['user_type'] = None
    return redirect(url_for('index_views.leaderboard_page',leaderboard_id=0))

@auth_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        student = create_student(request.form['username'], request.form['password'])
            
        if not student:
            flash('Username not available', category="error")
            return render_template('signup.html', user=current_user)
        
        flash('Account created successfully!', category="success")
        login_user(student)
        session['user_type'] = 'student'
        return redirect(url_for('index_views.leaderboard_page',leaderboard_id=0))
    
    return render_template('signup.html', user=current_user)
