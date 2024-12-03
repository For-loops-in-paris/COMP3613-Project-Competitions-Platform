from App.database import db
from App.models import  RankUpdater
from App.controllers import update_rankings,update_ratings, get_decayed_students

def update_leaderboard(mod_name,comp_name):
    if update_ratings(mod_name, comp_name):
        update_rankings()
        apply_decay()

def apply_decay():
    students = get_decayed_students()
    for student in students:
        student.score-=0.5


    
    

        
