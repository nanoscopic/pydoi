import json
import os

class LangBase:
	def test():
		print("hello")
	
	def __init__( self, conf, db, inputConf ):
		self.conf = conf
		self.inputConf = inputConf
		self.db = db
	
	# Check if we already have an appropriate docker image built
	def get_image( self ):
		row = self.get_image_by_conf()
		if row:
			imgName = row[0]
			print ("Row existed - imgName=%s" % imgName )
			return imgName
		else:
			print( "Row does not exist; building" )
			self.write_dockerfile()
			self.docker_build()
			imgName = self.conf['imgName']
			self.store_image_by_conf( imgName )
			return imgName
	
	def get_image_by_conf( self ):
		conf = self.inputConf
		confStr = json.dumps( conf )
		q = "SELECT imgName,conf from images_by_conf where conf=?"
		row = self.db.fetch_one( q, (confStr,) )
		return row
		
	def store_image_by_conf( self, imgName ):
		conf = self.inputConf
		confStr = json.dumps( conf )
		q = "INSERT into images_by_conf (imgName,conf) VALUES (?,?)"
		cursor = self.db.conn.cursor()
		cursor.execute( q, ( imgName, confStr, ) )
		self.db.conn.commit()
	
	# Build the dockerfile to an image
	def docker_build( self ):
		conf = self.conf
		
		imgName = conf['imgName'] = 'pydoi/' + conf['uid']
	
		os.system( "docker build -t %s %s" % ( imgName, conf['folder'] ) )
		
	def write_files( self ): 
		conf = self.conf
		
		files = conf['files']
		
		# Write to mount/script.py
		
		for filename in files:
			code = files[filename]
			sfh = open( conf['mount'] + "/" + filename, "w" )
			sfh.write( code )
			sfh.close()