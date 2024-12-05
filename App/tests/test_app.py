import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *
from datetime import datetime

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UnitTests(unittest.TestCase):
    #User Unit Tests
    def test_new_user(self):
        user = User("ryan", "ryanpass")
        assert user.username == "ryan"
        
    def test_get_json(self):
        user = User("ryan", "ryanpass")
        user_id = user.id
        user_json = user.get_json()
        print(user_json)
        self.assertDictEqual(user_json, {"id": user_id, "username": "ryan"})
      
    def test_toDict(self):
        user = User("ryan", "ryanpass")
        user_id = user.id
        user_dict = user.toDict()
        self.assertDictEqual(user_dict, {"ID": user_id, "Username": "ryan"})

    def test_hashed_password(self):
        password = "ryanpass"
        user = User("ryan", password)
        assert user.password != password

    def test_check_password(self):
        password = "ryanpass"
        user = User("ryan", password)
        assert user.check_password(password)

    #Student Unit Tests
    def test_new_student(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      assert student.username == "james"

    def test_student_get_json(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      self.assertDictEqual(student.get_json(), {"id": None, "username": "james", "rating_score": 0, "comp_count": 0, "curr_rank": 0})
      
    def test_student_update_stats(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      student.update_stats(10)
      assert student.rating_score == 10
      
    def test_student_update_ranking(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      student.update_ranking(1)
      assert student.curr_rank == 1
      
    def test_student_to_Dict(self):
      db.drop_all()
      db.create_all()
      student = Student("james", "jamespass")
      self.assertDictEqual(student.to_Dict(), {"ID": None, "Username": "james", "Rating Score": 0, "Number of Competitions": 0, "Rank": 0})
      
    #Moderator Unit Tests
    def test_new_moderator(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      assert mod.username == "robert"

    def test_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      self.assertDictEqual(mod.get_json(), {"id":None, "username": "robert", "competitions": []})
      
    def test_moderator_to_Dict(self):
      db.drop_all()
      db.create_all()
      mod = Moderator("robert", "robertpass")
      self.assertDictEqual(mod.toDict(), {"ID": None, "Username": "robert", "Competitions": []})
    
    #Team Unit Tests
    def test_new_team(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      assert team.name == "Scrum Lords"
    
    def test_team_get_json(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      self.assertDictEqual(team.get_json(), {"id":None, "name":"Scrum Lords", "students": []})
      
    def test_team_to_Dict(self):
      db.drop_all()
      db.create_all()
      team = Team("Scrum Lords")
      self.assertDictEqual(team.to_Dict(), {"ID": None, "Name": "Scrum Lords", "Students": []})
    
    #Competition Unit Tests
    def test_new_competition(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      self.assertDictEqual(competition.get_json(), {"id": None, "name": "RunTime", "date": "09-02-2024", "location": "St. Augustine", "level": 1, "max_score": 25, "moderators": [], "teams": []})
      
    def test_competition_to_Dict(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      expected_date = datetime.strptime("09-02-2024", "%d-%m-%Y")
      self.assertDictEqual(competition.toDict(), {"ID": None, "Name": "RunTime", "Date": expected_date, "Location": "St. Augustine", "Level": 1, "Max Score": 25, "Moderators": [], "Teams": []})
    
    #Notification Unit Tests
    def test_new_notification(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      assert notification.student_id == 1 and notification.message == "Ranking changed!"

    def test_notification_get_json(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      self.assertDictEqual(notification.get_json(), {"id": None, "student_id": 1, "notification": "Ranking changed!"})
      
    def test_notification_to_Dict(self):
      db.drop_all()
      db.create_all()
      notification = Notification(1, "Ranking changed!")
      self.assertDictEqual(notification.to_Dict(), {"ID": None, "Notification": "Ranking changed!"})
    """
    #Ranking Unit Tests
    def test_new_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      assert ranking.student_id == 1
  
    def test_set_points(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_points(15)
      assert ranking.total_points == 15

    def test_set_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_ranking(1)
      assert ranking.curr_ranking == 1

    def test_previous_ranking(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_previous_ranking(1)
      assert ranking.prev_ranking == 1

    def test_ranking_get_json(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1)
      ranking.set_points(15)
      ranking.set_ranking(1)
      self.assertDictEqual(ranking.get_json(), {"rank":1, "total points": 15})
    """
    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      assert competition_team.comp_id == 1 and competition_team.team_id == 1

    def test_competition_team_update_points(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      assert competition_team.points_earned == 15

    def test_competition_team_update_rating(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_rating(12)
      assert competition_team.rating_score == 12

    def test_competition_team_get_json(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      self.assertDictEqual(competition_team.get_json(), {"id": None, "team_id": 1, "competition_id": 1, "points_earned": 0, "rating_score": 0})
      
    def test_competition_team_to_Dict(self):
      db.drop_all()
      db.create_all()
      competition_team = CompetitionTeam(1, 1)
      self.assertDictEqual(competition_team.toDict(), {"ID": None, "Team ID": 1, "Competition ID": 1, "Points Earned": 0, "Rating Score": 0})

    #CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      assert competition_moderator.comp_id == 1 and competition_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      self.assertDictEqual(competition_moderator.get_json(), {"id": None, "competition_id": 1, "moderator_id": 1})
      
    def test_competition_moderator_to_Dict(self):
      db.drop_all()
      db.create_all()
      competition_moderator = CompetitionModerator(1, 1)
      self.assertDictEqual(competition_moderator.to_Dict(), {"ID": None, "Competition ID": 1, "Moderator ID": 1})

    #StudentTeam Unit Tests
    def test_new_student_team(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      assert student_team.student_id == 1 and student_team.team_id == 1
    
    def test_student_team_get_json(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.get_json(), {"id": None, "student_id": 1, "team_id": 1})
      
    def test_student_team_to_Dict(self):
      db.drop_all()
      db.create_all()
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.to_Dict(), {"ID": None, "Student ID": 1, "Team ID": 1})
      
    #Leaderboard Unit Tests
    def test_new_leaderboard(self):
      db.drop_all()
      db.create_all()
      current_date = datetime.now()
      leaderboard = Leaderboard(current_date)
      assert leaderboard.id == None and leaderboard.date == current_date
      
    def test_leaderboard_get_json(self):
      db.drop_all()
      db.create_all()
      current_date = datetime.now()
      leaderboard = Leaderboard(current_date)
      current_date = current_date.strftime("%d %b %Y")
      self.assertDictEqual(leaderboard.get_json(), {"id": None, "date": current_date})
    
    #Ranking Unit Tests  
    def test_new_ranking(self):
      db.drop_all() 
      db.create_all()
      ranking = Ranking(1, 1, 10, 20, True)
      assert ranking.user_id == 1 and ranking.leaderboard_id == 1 and ranking.rank == 10 and ranking.points == 20 and ranking.decaying == True
      
    def test_ranking_get_json(self):
      db.drop_all()
      db.create_all()
      ranking = Ranking(1, 1, 10, 20, True)
      self.assertDictEqual(ranking.get_json(), {"id": None, "user_id": 1, "leaderboard_id": 1, "rank": 10, "points": 20, "decaying": True})

'''
    Integration Tests
'''
class IntegrationTests(unittest.TestCase):
    
    #Student Integration Tests
    def test01_create_student(self):
      db.drop_all()
      db.create_all()
      new_student = create_student("billy", "billypass")
      assert new_student.username == "billy"
    
    def test02_get_student_by_username(self):
      db.drop_all()
      db.create_all()
      new_student = create_student("billy", "billypass")
      returned_student = get_student_by_username("billy")
      assert returned_student.username == "billy"
      
    def test03_get_student_by_id(self):
      db.drop_all()
      db.create_all()
      new_student = create_student("billy", "billypass")
      returned_student = get_student(new_student.id)
      assert returned_student.username == "billy"
      
    def test04_get_all_students(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      all_students = get_all_students()
      usernames = [s.username for s in all_students]
      self.assertEqual(usernames, ["billy", "rob"])
      
    def test05_get_decayed_students(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      decayed_students = get_decayed_students()
      usernames = [s.username for s in decayed_students]
      self.assertEqual(usernames, [])
    
    def test06_get_all_students_json(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      all_students_json = get_all_students_json()
      expected_json = [{"id": 1, "username": "billy", "rating_score": 0, "comp_count": 0, "curr_rank": 0}, {"id": 2, "username": "rob", "rating_score": 0, "comp_count": 0, "curr_rank": 0}]
      self.assertListEqual(all_students_json, expected_json)
      
    def test07_update_student(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      update_student(student.id, "bob")
      student = get_student_by_username("bob")
      assert student.username == "bob"
    
    def test08_display_student_info(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      student_json = student.get_json()
      competitions = []
      expected = {
        "profile": student.get_json(),
        "competitions" : []
      }
      info = display_student_info(student.username)
      assert info == expected
    
    def test09_display_notifications(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      notif_message = create_notification(1,0,1)
      notif = Notification(1, notif_message)
      added_notification = student.add_notification(notif)
      expected_notif = {
        "ID": 1,
        "Notification": notif_message
      }
      
      expected_output = {
        "notifications": [expected_notif]
    }
      notifications = display_notifications(student.username)
      assert notifications == expected_output
    
    
    def test10_create_notification(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      notif_message = create_notification(1,0,1)
      expected_output = "RANK : 1. Congratulations on your first rank!"
      assert expected_output == notif_message 
      
    def test11_add_notification(self):
      db.drop_all()
      db.create_all()
      student = create_student("billy", "billypass")
      notif_message = create_notification(1,0,1)
      notif = Notification(1, notif_message)
      added_notification = student.add_notification(notif)
      assert added_notification == notif
    
    def test12_display_rankings(self):
      db.drop_all()
      db.create_all()
      student = create_student("alice", "password1")
      leaderboard = display_rankings()
      expected_leaderboard = []
      assert leaderboard == expected_leaderboard
    
    #Team Integration Tests:
    def test13_create_team(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      assert team.name == "team1"
    
    def test14_get_team_by_name(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      returned_team = get_team_by_name("team1")
      assert returned_team.name == team.name
    
    def test15_get_team_by_id(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      returned_team = get_team(team.id)
      assert returned_team.name == team.name
      
    def test16_get_all_teams(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      all_teams = get_all_teams()
      assert all_teams[0].name == team.name
      
    def test17_get_all_teams_json(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      all_teams_json = get_all_teams_json()
      team_json = {
            "id" : 1,
            "name" : "team1",
            "students" : ["billy", "rob"]
      }
      expected = [team_json]
      self.assertListEqual(all_teams_json, expected)
      
    def test18_find_team(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      returned_team = find_team("team1", students)
      assert returned_team == team
    
    def test19_add_team(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      added_team = add_team("lebron", "Code Wars", "team1", students)
      assert added_team.comp_id == 1 and added_team.team_id == 1
      
    def test20_add_student(self):
      db.drop_all()
      db.create_all()
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy"]
      team = create_team("team1", students)
      added_student = team.add_student(student2)
      assert added_student.team_id == 1 and added_student.student_id == 2
      
    def test21_create_competition(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      assert comp.name == "Code Wars" and comp.location == "St. Augustine" and comp.level == 1 and comp.max_score == 25 and comp.moderators[0].username == "lebron"
      
    def test22_get_competition_by_name(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      returned_comp = get_competition_by_name("Code Wars")
      assert returned_comp.name == comp.name
      
    def test23_get_competition_by_id(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      returned_comp = get_competition(comp.id)
      assert returned_comp.name == comp.name
      
    def test24_get_all_competitions(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      all_comps = get_all_competitions()
      assert all_comps == [comp]
      
    def test25_is_completed(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      confirmed = is_completed(comp)
      assert confirmed == False
      
    def test26_get_num_teams(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      added_team = add_team("lebron", "Code Wars", "team1", students)
      num_teams = get_num_teams(comp)
      assert num_teams == 1
      
    def test27_get_all_competitions_json(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      all_comps_json = get_all_competitions_json()
      comp_json = {
          "id" : 1,
          "name" : "Code Wars",
          "date" : "26-01-2024",
          "location" : "St. Augustine",
          "level" : 1,
          "max_score" : 25,
          "moderators" : ["lebron"],
          "teams" : []
      }
      expected = [comp_json]
      self.assertListEqual(all_comps_json, expected)
      
    def test28_display_competition_results(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team = create_team("team1", students)
      added_team = add_team("lebron", "Code Wars", "team1", students)
      leaderboard = display_competition_results("Code Wars")
      add_results("lebron","Code Wars", "team1", 0)
      expected = [{
        "placement": 1,
        "team": "team1",
        "members": ["billy", "rob"],
        "score": 0,
      }]
      print(leaderboard)
      assert leaderboard == expected
      
    def test29_add_moderator(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      mod2 = create_moderator("obama", "obamapass")
      comp_mods = comp.add_mod(mod2)
      assert comp_mods.comp_id == 1 and comp_mods.mod_id == 2
      
    def test30_add_team(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      student1 = create_student("billy", "billypass")
      student2 = create_student("rob", "robpass")
      students = ["billy", "rob"]
      team1 = create_team("team1", students)
      added_team = add_team("lebron", "Code Wars", "team1", students)
      student3 = create_student("bobby", "bobbypass")
      student4 = create_student("thor", "thorpass")
      students = ["bobby", "thor"]
      team2 = create_team("team2", students)
      new_comp_team = comp.add_team(team2)
      assert new_comp_team.comp_id == 1 and new_comp_team.team_id == 2
      
    def test31_create_moderator(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      assert moderator.username == "lebron"
      
    def test32_get_moderator_by_username(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      returned_mod = get_moderator_by_username("lebron")
      assert returned_mod.username == moderator.username
      
    def test33_get_moderator_by_id(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      returned_mod = get_moderator(moderator.id)
      assert returned_mod.username == moderator.username
      
    def test34_get_all_moderators(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      returned_mod = get_all_moderators()
      assert returned_mod[0].username == moderator.username
      
    def test35_update_moderator(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      returned_mod = update_moderator(moderator.id, "steph")
      assert returned_mod.username == "steph"
      
    def test35_isValid(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      mod2 = create_moderator("steph", "stephpass")
      comp_mods = add_mod("lebron", "Code Wars", "steph")
      returned_mod = isValid(moderator, comp)
      assert returned_mod == False
      
    def test_36_isRegisteredMod(self):
      db.drop_all()
      db.create_all()
      moderator = create_moderator("lebron", "james")
      comp = create_competition("lebron","Code Wars","26-01-2024","St. Augustine",1,25)
      returned_mod = isRegisteredMod(moderator, comp)
      assert returned_mod == True
      
  