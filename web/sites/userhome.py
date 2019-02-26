#coding:utf-8
from flask import *
import db,modules

def Run(username):
	userdata = db.Read_User_Byname(username)
	if userdata == None:
		flash('用户 %s 不存在'%username,'error')
		return modules.Page_Back()
	else:
		userdata = list(userdata)
		return render_template('userhome.html',user=userdata)
