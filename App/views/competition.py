from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
#from datetime import datetime

from.index import index_views

from App.controllers import *

comp_views = Blueprint('comp_views', __name__, template_folder='../templates')

##return the json list of competitions fetched from the db
@comp_views.route('/competitions', methods=['GET'])
def get_competitions():
    competitions = get_all_competitions_json()
    return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)
    #return (jsonify(competitions),200) 

#create new comp
@comp_views.route('/createcompetition', methods=['POST'])
@login_required
@moderator_required
def create_comp():
    data = request.form
    
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    date = data['date']
    date = date[8] + date[9] + '-' + date[5] + date[6] + '-' + date[0] + date[1] + date[2] + date[3]
    
    new_comp_name = data['name']
    all_competitions = get_all_competitions()

    for comp in all_competitions:
        if comp.name == new_comp_name:
            flash('Competition name already taken! Please try another name', 'error')
            return redirect(url_for('comp_views.create_comp_page'))
        
    new_comp_score = int(data['max_score'])
    if new_comp_score < 1:
        flash('Competition max score must be above 0! Try again', 'error')
        return redirect(url_for('comp_views.create_comp_page'))

    
    response = create_competition(moderator.username, data['name'], date, data['location'], data['level'], data['max_score'])
    return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)



@comp_views.route('/editcompetition/<int:comp_id>', methods=['POST'])
@login_required
@moderator_required
def edit_comp(comp_id):
    comp = get_competition(comp_id)
    if comp.confirm:
        flash("Edits cannot be made")
        return
    data = request.form
    
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    date = data['date']
    date = date[8] + date[9] + '-' + date[5] + date[6] + '-' + date[0] + date[1] + date[2] + date[3]
    
    new_comp_name = data['name']
    all_competitions = get_all_competitions()

    for comp in all_competitions:
        if comp.name == new_comp_name:
            flash('Competition name already taken! Please try another name', 'error')
            return redirect(url_for('comp_views.edit_comp_page',comp_id=comp_id))
        
    new_comp_score = int(data['max_score'])
    if new_comp_score < 1:
        flash('Competition max score must be above 0! Try again', 'error')
        return redirect(url_for('comp_views.create_comp_page'))

    
    edit_competition(comp_id, data['name'], date, data['location'], data['level'], data['max_score'])
    return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)

#page to create new comp
@comp_views.route('/createcompetition', methods=['GET'])
@moderator_required
def create_comp_page():
    return render_template('competition_creation.html', user=current_user)

@comp_views.route('/editcompetition/<int:comp_id>', methods=['GET'])
@moderator_required
def edit_comp_page(comp_id):
    competition = get_competition(comp_id)
    return render_template('competition_modification.html', user=current_user, competition=competition)

@comp_views.route('/competitions/<int:id>', methods=['GET'])
def competition_details(id):
    competition = get_competition(id)
    if not competition:
        return render_template('404.html')
    
    #team = get_all_teams()

    #teams = get_participants(competition_name)
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(competition.name)
    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)#, team=team)

    #teams = get_participants(competition_name)
    #return render_template('Competition_Details.html', competition=competition)

@comp_views.route('/competition/<string:name>', methods=['GET'])
def competition_details_by_name(name):
    competition = get_competition_by_name(name)
    if not competition:
        return render_template('404.html')

    #teams = get_participants(competition_name)
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)
    
#page to comp upload comp results
@comp_views.route('/add_results/<int:comp_id>', methods=['GET'])
@moderator_required
def add_results_page(comp_id):
    competition = get_competition(comp_id)
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    leaderboard = display_competition_results(competition.name)

    return render_template('competition_results.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)

@comp_views.route('/add_results/<string:comp_name>', methods=['POST'])
@moderator_required
def add_competition_results(comp_name):
    competition = get_competition_by_name(comp_name)
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None
        
    #if request.method == 'POST':
    data = request.form
    entered_score = int(data['score'])
    comp_score = int(competition.max_score)
    if entered_score > competition.max_score:
        flash('Team Score exceeds the maximum score: ' + str(comp_score) + '!  Please try again', 'error')
        return redirect(url_for('comp_views.add_results_page', comp_id=competition.id))
    elif entered_score < 0:
        flash('Team Score cannot be negative! Please try again', 'error')
        return redirect(url_for('comp_views.add_results_page', comp_id=competition.id))
    else:
        students = [data['student1'], data['student2'], data['student3']]
        comp_teams = competition.teams
        for student in students:
            for team in comp_teams:
                if team.name == data['team_name']:
                    flash('Team name: ' + team.name + ' already taken for this competition! Please try another', 'error')
                    return redirect(url_for('comp_views.add_results_page', comp_id=competition.id))
                for team_student in team.students:
                    if team_student.username == student:
                        flash(student + ' already registered for ' + team.name + '! Please try again', 'error')
                        return redirect(url_for('comp_views.add_results_page', comp_id=competition.id))

        response = add_team(moderator.username, comp_name, data['team_name'], students)

        if response:
            response = add_results(moderator.username, comp_name, data['team_name'], int(data['score']))
        
        leaderboard = display_competition_results(comp_name)
        flash('Results added successfully!', 'success')
        return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)
    
@comp_views.route('/confirm_results/<string:comp_name>', methods=['GET', 'POST'])
@login_required
@moderator_required
def confirm_results(comp_name):
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None
    
    competition = get_competition_by_name(comp_name)

    update_leaderboard(moderator.username, competition.name)
    
    

    leaderboard = display_competition_results(comp_name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)


@comp_views.route('/competitions_postman', methods=['GET'])
def get_competitions_postman():
    competitions = get_all_competitions_json()
    return (jsonify(competitions),200)

@comp_views.route('/createcompetition_postman', methods=['POST'])
def create_comp_postman():
    data = request.json
    response = create_competition('robert', data['name'], data['date'], data['location'], data['level'], data['max_score'])
    if response:
        return (jsonify({'message': "Competition created!"}), 201)
    return (jsonify({'error': "Error creating competition"}),500)

@comp_views.route('/competitions_postman/<int:id>', methods=['GET'])
def competition_details_postman(id):
    competition = get_competition(id)
    if not competition:
        return (jsonify({'error': "Competition not found"}),404)
    
    
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(competition.name)
    return (jsonify(competition.toDict()),200)

@comp_views.route('/add_results_postman/<string:comp_name>', methods=['POST'])
def add_competition_results_postman(comp_name):
    competition = get_competition_by_name(comp_name)
    
    data = request.json
    
    students = [data['student1'], data['student2'], data['student3']]
    response = add_team('robert', comp_name, data['team_name'], students)

    if response:
        response = add_results('robert', comp_name, data['team_name'], int(data['score']))
    if response:
        return (jsonify({'message': "Results added successfully!"}),201)
    return (jsonify({'error': "Error adding results!"}),500)