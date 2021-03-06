#coding:utf-8
from flask import *
import db,modules,operator

def Run(contest_id):
	contest = db.Read_Contest(contest_id)
	submissions = db.Read_Submissions({
		'contest_id': contest_id
	})

	groups = {}
	for submission in submissions:
		user = db.Read_User_Byname(submission[11])
		group = user[7]
		if group == None or group.strip() == '': continue
		if groups.get(group) == None:
			groups[group] = {
				'tot_score_all': 0,
				'tot_submit_all': 0,
				'average_score_all': 0,
				'tot_score_finally': 0,
				'tot_submit_finally': 0,
				'average_score_finally': 0
			}
		groups[group]['tot_score_all'] += submission[5]
		groups[group]['tot_submit_all'] += 1
		groups[group]['average_score_all'] = round( groups[group]['tot_score_all'] / groups[group]['tot_submit_all'] , 2 )

	overall = {
		'tot_submit_all': 0,
		'tot_score_all': 0,
		'average_score_all': 0,
		'status_cnt_all': [ 0 for i in range(13) ],
		'score_count_all': {},
		'tot_submit_finally': 0,
		'tot_score_finally': 0,
		'average_score_finally': 0,
		'status_cnt_finally': [ 0 for i in range(13) ],
		'score_count_finally': {}
	}
	problems = {}
	for submission in submissions:
		if submission[4] <= 3: continue
		problem = db.Read_Problem(submission[1])
		if problem == None: continue
		problem_id = problem[0]
		if problems.get(problem_id) == None:
			problems[problem_id] = {
				'tot_submit_all': 0,
				'tot_score_all': 0,
				'average_score_all': 0,
				'status_cnt_all': [ 0 for i in range(13) ],
				'score_count_all': {},
				'tot_submit_finally': 0,
				'tot_score_finally': 0,
				'average_score_finally': 0,
				'status_cnt_finally': [ 0 for i in range(13) ],
				'score_count_finally': {},
				'name': problem[1]
			}
		problems[problem_id]['tot_submit_all'] += 1
		problems[problem_id]['tot_score_all'] += submission[5]
		problems[problem_id]['status_cnt_all'][submission[4]] += 1
		problems[problem_id]['average_score_all'] = round( problems[problem_id]['tot_score_all'] / problems[problem_id]['tot_submit_all'] , 2 )
		problems[problem_id]['score_count_all'][submission[5]] = 1 if submission[5] not in problems[problem_id]['score_count_all'] else problems[problem_id]['score_count_all'][submission[5]] + 1
		overall['tot_submit_all'] += 1
		overall['tot_score_all'] += submission[5]
		overall['status_cnt_all'][submission[4]] += 1
		overall['average_score_all'] = round( overall['tot_score_all'] / overall['tot_submit_all'] , 2 )
		overall['score_count_all'][submission[5]] = 1 if submission[5] not in overall['score_count_all'] else overall['score_count_all'][submission[5]] + 1
	overall['score_count_all'] = sorted(overall['score_count_all'].items())

	problems = dict(sorted(problems.items(),key=operator.itemgetter(0)))

	players = db.Read_Contest_Ranklist(contest_id)
	for player in players:
		details = json.loads(player[3])
		for problem_id,detail in details.items():
			problem_id = int(problem_id)
			if problems.get(problem_id) == None: continue
			record = db.Read_Record(detail['record_id'])
			if record == None: continue
			if record[4] <= 3: continue
			problems[problem_id]['tot_submit_finally'] += 1
			problems[problem_id]['tot_score_finally'] += record[5]
			problems[problem_id]['status_cnt_finally'][record[4]] += 1
			problems[problem_id]['average_score_finally'] = round( problems[problem_id]['tot_score_finally'] / problems[problem_id]['tot_submit_finally'] , 2 )
			problems[problem_id]['score_count_finally'][record[5]] = 1 if record[5] not in problems[problem_id]['score_count_finally'] else problems[problem_id]['score_count_finally'][record[5]] + 1

		for problem_id,detail in details.items():
			record = db.Read_Record(detail['record_id'])
			if record == None: continue
			if record[4] <= 3: continue
			user = db.Read_User_Byname(player[1])
			group = user[7]
			if group == None or group.strip() == '': continue
			if groups.get(group) == None: continue
			groups[group]['tot_submit_finally'] += 1
			groups[group]['tot_score_finally'] += record[5]
			groups[group]['average_score_finally'] = round( groups[group]['tot_score_finally'] / groups[group]['tot_submit_finally'] , 2 )

		for problem_id,detail in details.items():
			record = db.Read_Record(detail['record_id'])
			if record == None: continue
			if record[4] <= 3: continue
			overall['tot_submit_finally'] += 1
			overall['tot_score_finally'] += record[5]
			overall['status_cnt_finally'][record[4]] += 1
			overall['average_score_finally'] = round( overall['tot_score_finally'] / overall['tot_submit_finally'] , 2 )
			overall['score_count_finally'][record[5]] = 1 if record[5] not in overall['score_count_finally'] else overall['score_count_finally'][record[5]] + 1
	overall['score_count_finally'] = sorted(overall['score_count_finally'].items())
	for problem_id in problems.keys():
		problems[problem_id]['score_count_all'] = sorted(problems[problem_id]['score_count_all'].items())
		problems[problem_id]['score_count_finally'] = sorted(problems[problem_id]['score_count_finally'].items())

	return render_template('contest_statistic.html',contest=contest,groups=groups,problems=problems,overall=overall)
