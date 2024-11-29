from App.database import db

class Leaderboard(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user =  db.relationship("Student",secondary="ranking")

    def get_json(self):
        
        return {
            "comp_id": self.comp_id,
            "leaderboard_id":self.leaderboard_id

        }
    