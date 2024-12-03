from App.database import db

class Ranking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    leaderboard_id =  db.Column(db.Integer, db.ForeignKey('leaderboard.id'), nullable=False)
    rank = db.Column(db.Integer,nullable=False)
    points = db.Column(db.Float,nullable=False)

    def get_json(self):
        return {
            "comp_id": self.comp_id,
            "leaderboard_id":self.leaderboard_id

        }
    
    def __init__(self,user_id,leaderboard_id,rank,points):
        self.user_id = user_id
        self.leaderboard_id = leaderboard_id
        self.rank=rank
        self.points=points
    
    def __repr__(self):
        return f"User: {self.user_id} Rank: {self.rank}"
    
    def search_ranking(self, page, leaderboard):
        matching_ranks = Ranking.query.filter_by(leaderboard_id = leaderboard)
        return matching_ranks.paginate(page=page, per_page=20)