from App.database import db

class Ranking(db.model):

    id = db.Column(db.Integer, primary_key=True)
    past_leaderboards = db.relationship("Leaderboard",)
    users = db.relationship("User")

    def get_json(self):
        return {
            "comp_id": self.comp_id,
            "leaderboard_id":self.leaderboard_id

        }
    