import pymysql
from flask import *
import db,modules

def Contest_Players_Recalculate(contest_id):
	print('Recalculating Contest %d...'%contest_id)
	db.Execute('DELETE FROM contest_players WHERE contest_id=%s',contest_id)
	contest = db.Read_Contest(contest_id)
	submissions = list(db.Read_Submissions({'contest_id':contest_id}))
	submissions.sort(key=lambda x:x[0])
	details = {}
	for submission in submissions:
		if submission[4] <= 3: continue
		username = submission[11]
		if details.get(username) == None: details[username] = {}
		problem_id = submission[1]
		details[username][problem_id] = {
			'record_id': submission[0],
			'score': modules.Toint(submission[5]),
			'submit_cnt': 1 if details[username].get(problem_id) == None else details[username][problem_id]['submit_cnt'] + 1
		}
	for username,detail in details.items():
		db.Execute('INSERT INTO contest_players VALUES(NULL,%s,%s,%s)',(username,contest_id,json.dumps(detail)))

def Contest_Players_Recalculate_All():
	contests = db.Read_Contestlist()
	for contest in contests:
		contest_id = contest[0]
		Contest_Players_Recalculate(contest_id)

if __name__ == '__main__':
	Contest_Players_Recalculate_All()
