# -*- coding: utf-8 -*-
import sqlite3
import os
import argparse
class SqlDB:
	mSqlFile = 'imageUrl.db'

	def __init__(self):
		print 'SqlDB----init----in----'
		if os.path.isfile(SqlDB.mSqlFile):
			print 'the db file creates before'
		else:
			print 'the db file does not create'
			conn = sqlite3.connect(SqlDB.mSqlFile)
			cursor = conn.cursor()
			cursor.execute('create table imageUrl (id integer primary key not null, url varchar(40), engine varchar(40), keywords varchar(40))')
			cursor.close()
			conn.commit()
			print 'the db file creates succeed'

		print 'SqlDB----init----out----'
	def insert(self, url, engine, keywords):
		print 'SqlDB----insert----in----' + 'url=' + url + "," + 'engine=' + engine
		conn = sqlite3.connect(SqlDB.mSqlFile)
		cursor = conn.cursor()
		cursor.execute('select * from imageUrl where url=:url and engine=:engine', {"url":url, "engine":engine})
		sameImageUrl = cursor.fetchone()
		if sameImageUrl is None:
			cursor.execute('insert into imageUrl (url, engine, keywords) values (?, ?, ?)', (url, engine, keywords))
			print 'SqlDB----insert----succeed'
		else:
			print sameImageUrl
			print 'SqlDB----insert----have been already'
		cursor.close()
		conn.commit()
		print 'SqlDB----insert----out----'
	
	def queryAll(self, engine=None, keywords=None):
		print 'SqlDB----queryAll----in----'
		conn = sqlite3.connect(SqlDB.mSqlFile)
		cursor = conn.cursor()
		if engine == None:
			print 'engine is None'
			cursor.execute('select * from imageUrl')
		else:
			print 'engine is ' + engine
			cursor.execute('select * from imageUrl where engine=:engine', {"engine":engine})
		values = cursor.fetchall()
		for value in values:
			print value
		cursor.close()
		conn.commit()
		print 'SqlDB----queryAll----out----'

	def clean(self, engine=None):
		print 'SqlDB----clean----in----'
		conn = sqlite3.connect(SqlDB.mSqlFile)
		cursor = conn.cursor()
		if engine == None:
			print 'engine is None'
			cursor.execute('delete from imageUrl where engine not in ("BaiduImage", "BingImage", "GoogleImage", "InstagramImage", "FlickrImage")')
		else:
			print 'engine is ' + engine
			cursor.execute('delete from imageUrl where engine=:engine', {"engine":engine})
		values = cursor.fetchall()
		for value in values:
			print value
		cursor.close()
		conn.commit()
		print 'SqlDB----queryAll----out----'

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
			"--engine",
			default=None,
			help='BaiduImage+BingImage+GoogleImage+InstagramImage+FlickrImage'
	)
	args = parser.parse_args()
	print 'SqlDB----in----' + 'engine:' + str(args.engine)
	print "SqlDB----main----in----"
	mSqlDB = SqlDB()
	mSqlDB.insert(url='www.SqlDB.com', engine="SqlDB", keywords="SqlDB")
	mSqlDB.queryAll(args.engine)
	mSqlDB.clean(None)
	print "SqlDB----main----out----"
