from App.database import db
from App.models import Competition, Moderator, CompetitionTeam, Team, Student#, Student, Admin, competition_student
from datetime import datetime

from flask import flash

def create_competition(mod_name, comp_name, date, location, level, max_score):
    comp = get_competition_by_name(comp_name)
    if comp:
        print(f'{comp_name} already exists!')
        return None
    
    mod = Moderator.query.filter_by(username=mod_name).first()
    if mod:
        newComp = Competition(name=comp_name, date=datetime.strptime(date, "%d-%m-%Y"), location=location, level=level, max_score=max_score)
        try:
            newComp.add_mod(mod)
            db.session.add(newComp)
            db.session.commit()
            print(f'New Competition: {comp_name} created!')
            return newComp
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None
    else:
        print("Invalid credentials!")


def edit_competition(comp_id,comp_name, date, location, level, max_score):
    comp = get_competition_by_name(comp_name)
    if comp:
        print(f'{comp_name} already exists!')
        return None
    comp = get_competition(comp_id)
    if comp:
        date=datetime.strptime(date, "%d-%m-%Y")
        comp.name = comp_name
        comp.date=date
        comp.location=location
        comp.level = level
        comp.max_score=max_score

        try:
            db.session.commit()
            flash(f'Competition: {comp_name} successfully updated!')
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None
    else:
        print("Invalid credentials!")


def get_competition_by_name(name):
    comp =Competition.query.filter_by(name=name).first()
    if not comp:
        print(f'{name} was not found!')
    return comp

def get_competition(id):
    return Competition.query.get(id)

def get_all_competitions():
    return Competition.query.all()

def is_completed(comp):
    completed = comp.confirm
    if completed:
        print(f'Results for {comp.name} has already been finalized!')
    return completed

def get_num_teams(comp):
    num_teams = len(comp.teams)
    if len(comp.teams) == 0:
        print(f'No teams found. Results can not be confirmed!')
    return num_teams
def get_all_competitions_json():
    competitions = Competition.query.all()

    if not competitions:
        return []
    else:
        return [comp.get_json() for comp in competitions]

def display_competition_results(name):
    comp = get_competition_by_name(name)

    if not comp:
        print(f'{name} was not found!')
        return None
    elif len(comp.teams) == 0:
        print(f'No teams found for {name}!')
        return []
    else:
        comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id).all()
        comp_teams.sort(key=lambda x: x.points_earned, reverse=True)

        leaderboard = []
        count = 1
        curr_high = comp_teams[0].points_earned
        curr_rank = 1
        
        for comp_team in comp_teams:
            if curr_high != comp_team.points_earned:
                curr_rank = count
                curr_high = comp_team.points_earned

            team = Team.query.filter_by(id=comp_team.team_id).first()
            leaderboard.append({"placement": curr_rank, "team": team.name, "members" : [student.username for student in team.students], "score":comp_team.points_earned})
            count += 1
        
        return leaderboard