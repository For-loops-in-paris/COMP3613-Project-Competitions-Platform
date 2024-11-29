from App.database import db
from App.models import  RankUpdater
from App.controllers import update_rankings,update_ratings

def update_leaderboard(mod_name,comp_name):
    if update_ratings(mod_name, comp_name):
        update_rankings()
        
