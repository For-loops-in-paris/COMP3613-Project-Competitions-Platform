from App.database import db
from App.models import  RankUpdater, CompetitionTeam, Leaderboard, Team, Notification, Ranking
from App.controllers import get_decayed_students, get_competition_by_name,get_moderator_by_username, create_notification, isValid

def update_leaderboard(mod_name,comp_name):
    if update_ratings(mod_name, comp_name):
        apply_decay()
        update_rankings()
        

def apply_decay():
    students = get_decayed_students()
    for student in students:
        student.rating_score-=0.5

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
            score = (stud.rating_score*stud.comp_count + comp_team.rating_score)/(stud.comp_count+1)
            stud.update_stats(score)

    comp.confirm = True
    print("Results finalized!")
    return True


def update_rankings():
    students = RankUpdater.get_students(RankUpdater)
    
    students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

    count = 1
    
    curr_rank = 1
    
    for student in students:
        if student.rank_decay<3:
            student.rank_decay+=1

        if student.comp_count != 0:
            ranking = Ranking(student.id,Leaderboard.query.count(),count,student.rating_score)
            count += 1
    
            notification = Notification(student.id, create_notification(student.comp_count,student.curr_rank,curr_rank))
            student.update_ranking(curr_rank)
            try:
                db.session.add(student)
                db.session.add(notification)
                db.session.add(ranking)
                db.session.commit()
            except Exception as e:
                db.session.rollback()


    
    

        
