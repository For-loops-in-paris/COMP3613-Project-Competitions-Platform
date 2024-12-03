from App.database import db
from App.models import Moderator, Competition, Team, CompetitionTeam, Leaderboard
from App.controllers import get_competition_by_name, is_completed,get_num_teams

def create_moderator(username, password):
    mod = get_moderator_by_username(username)
    if mod:
        print(f'{username} already exists!')
        return None

    newMod = Moderator(username=username, password=password)
    try:
        db.session.add(newMod)
        db.session.commit()
        print(f'New Moderator: {username} created!')
        return newMod
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_moderator_by_username(username):
    mod = Moderator.query.filter_by(username=username).first()
    if not mod:
        print(f'{username} was not found!')
    return mod

def get_moderator(id):
    return Moderator.query.get(id)

def get_all_moderators():
    return Moderator.query.all()

def get_all_moderators_json():
    mods = Moderator.query.all()
    if not mods:
        return []
    mods_json = [mod.get_json() for mod in mods]
    return mods_json

def update_moderator(id, username):
    mod = get_moderator(id)
    if mod:
        mod.username = username
        try:
            db.session.add(mod)
            db.session.commit()
            print("Username was updated!")
            return mod
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def add_mod(mod1_name, comp_name, mod2_name):
    mod1 = get_moderator_by_username(mod1_name)
    mod2 = get_moderator_by_username(mod2_name)
    comp = get_competition_by_name(comp_name)

    if not mod1 or not mod2 or not comp:
        return None
    return comp.add_mod(mod2)
                
def add_results(mod_name, comp_name, team_name, score):
    mod = get_moderator_by_username(mod_name)
    comp = get_competition_by_name(comp_name)
    teams = Team.query.filter_by(name=team_name).all()

    if not isValid(mod,comp):
        return False

    for team in teams:
        comp_team = CompetitionTeam.query.filter_by(comp_id=comp.id, team_id=team.id).first()

        if comp_team:
            comp_team.points_earned = score
            comp_team.rating_score = (score/comp.max_score) * 20 * comp.level
            try:
                db.session.add(comp_team)
                db.session.commit()
                print(f'Score successfully added for {team_name}!')
                return comp_team
            except Exception as e:
                db.session.rollback()
                print("Something went wrong!")
                return None
    return None


def update_ratings(mod_name, comp_name):
    mod = get_moderator_by_username(mod_name)
    comp = get_competition_by_name(comp_name)
    
    if not isValid(mod,comp):
        return None
    comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id).all()
    
    db.session.add(Leaderboard(comp.date))
    db.session.commit()

    for comp_team in comp_teams:
        team = Team.query.filter_by(id=comp_team.team_id).first()

        for stud in team.students:
            stud.rating_score = (stud.rating_score*stud.comp_count + comp_team.rating_score)/(stud.comp_count+1)
            
            stud.comp_count += 1
            if stud.comp_count == 1:
                stud.rank_updater=1    
            stud.rank_decay = -1
            try:
                db.session.add(stud)
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    comp.confirm = True
    print("Results finalized!")
    return True


def isRegisteredMod(mod,comp):
    if mod not in comp.moderators:
        print(f'{mod.username} is not authorized to add results for {comp.name}!')
        return False
    return True

def isValid(mod,comp):
    if not mod or not comp or is_completed(comp) or not isRegisteredMod(mod,comp) or get_num_teams(comp)==0:
        return False
    return True
    
