from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, session, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from App.models import db,Leaderboard, Ranking
from App.controllers import *
import csv

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def home_page():
    return redirect(url_for('index_views.leaderboard_page',leaderboard_id=0))

@index_views.route('/leaderboard/<int:leaderboard_id>', methods=['GET'])
def leaderboard_page(leaderboard_id):
    if leaderboard_id == 0:
        leaderboard_id = Leaderboard.query.count()
    page = request.args.get('page', 1, type=int)
    leaderboard = Ranking.search_ranking(Ranking, page, leaderboard_id)

    return render_template('leaderboard.html', leaderboard=leaderboard, user=current_user, leaderboard_id=leaderboard_id, all_leaderboards=Leaderboard.query.all(), num_leaderboard=Leaderboard.query.count())

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    #Create Rank Updater
    db.session.add(RankUpdater())
    db.session.commit()
    print(RankUpdater.query.get(1))
    #creates students
    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)

        for student in reader:
            stud = create_student(student['username'], student['password'])
            
    
    student_file.close()

    #creates moderators
    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)

        for moderator in reader:
            mod = create_moderator(moderator['username'], moderator['password'])
          
    
    moderator_file.close()

    #creates competitions
    with open("competitions.csv") as competition_file:
        reader = csv.DictReader(competition_file)

        for competition in reader:
            comp = create_competition(competition['mod_name'], competition['comp_name'], competition['date'], competition['location'], competition['level'], competition['max_score'])
    
    competition_file.close()
    
    with open("results.csv") as results_file:
        reader = csv.DictReader(results_file)

        for result in reader:
            students = [result['student1'], result['student2'], result['student3']]
            team = add_team(result['mod_name'], result['comp_name'], result['team_name'], students)
            add_results(result['mod_name'], result['comp_name'], result['team_name'], int(result['score']))
            
    
    results_file.close()

    with open("competitions.csv") as competitions_file:
        reader = csv.DictReader(competitions_file)

        for competition in reader:
            if competition['comp_name'] != 'TopCoder':
                update_leaderboard(competition['mod_name'], competition['comp_name'])
                
    
    competitions_file.close()

    
 

    return redirect(url_for('index_views.leaderboard_page',leaderboard_id=0))


@index_views.route('/profile')
def profile():
    user_type = session['user_type']
    id = current_user.get_id()
    
    if user_type == 'moderator':
        template = moderator_profile(id)

    if user_type == 'student':
        template = student_profile(id)

    return template

@index_views.route('/student_profile/<int:id>', methods=['GET'])
def student_profile(id):
    student = get_student(id)

    if not student:
        return render_template('404.html')
    
    profile_info = display_student_info(student.username)
    competitions = profile_info['competitions']
    return render_template('student_profile.html', student=student, competitions=competitions, user=current_user)

@index_views.route('/student_profile/<string:name>', methods=['GET'])
def student_profile_by_name(name):
    student = get_student_by_username(name)

    if not student:
        return render_template('404.html')
    
    profile_info = display_student_info(student.username)
    competitions = profile_info['competitions']
    return render_template('student_profile.html', student=student, competitions=competitions, user=current_user)

@index_views.route('/moderator_profile/<int:id>', methods=['GET'])
def moderator_profile(id):   
    moderator = get_moderator(id)

    if not moderator:
        return render_template('404.html')
    return render_template('moderator_profile.html', moderator=moderator, user=current_user)

@index_views.route('/init_postman', methods=['GET'])
def init_postman():
    
    db.drop_all()
    db.create_all()
    

    #creates students
    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)

        for student in reader:
            stud = create_student(student['username'], student['password'])
            
    
    student_file.close()

    #creates moderators
    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)

        for moderator in reader:
            mod = create_moderator(moderator['username'], moderator['password'])
            
    
    moderator_file.close()

    #creates competitions
    with open("competitions.csv") as competition_file:
        reader = csv.DictReader(competition_file)

        for competition in reader:
            comp = create_competition(competition['mod_name'], competition['comp_name'], competition['date'], competition['location'], competition['level'], competition['max_score'])
    
    competition_file.close()
    
    with open("results.csv") as results_file:
        reader = csv.DictReader(results_file)

        for result in reader:
            students = [result['student1'], result['student2'], result['student3']]
            team = add_team(result['mod_name'], result['comp_name'], result['team_name'], students)
            add_results(result['mod_name'], result['comp_name'], result['team_name'], int(result['score']))
    
    results_file.close()

    with open("competitions.csv") as competitions_file:
        reader = csv.DictReader(competitions_file)

        for competition in reader:
            update_ratings(competition['mod_name'], competition['comp_name'])
            update_rankings()
    
    
    competitions_file.close()

    return (jsonify({'message': "database_initialized"}),200)