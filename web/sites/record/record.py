from flask import *
import pymysql

def Getrecord(id):
	db = pymysql.connect("localhost","intlsy","24","intoj")
	cur = db.cursor()
	cur.execute("SELECT * FROM records WHERE id=%d;" % id)
	urecord = cur.fetchone()
	db.close()
	return urecord
