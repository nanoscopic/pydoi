import sqlite3
class PydoiDB:
	def __init__( self ):
		self.conn = conn = sqlite3.connect('data.db')
		if self.table_exists('test'):
			self.create_table('images_by_conf', 'imgName varchar(15) PRIMARY KEY, conf TEXT')
			#conn.commit()
			
	def __del__( self ):
		self.conn.close()
		
	def fetch_one( self, q, data = () ):
		cursor = self.conn.cursor()
		cursor.execute( q, data )
		return cursor.fetchone()
		
	def create_table( self, tbName, cols ):
		cursor = self.conn.cursor()
		q = "CREATE TABLE '%s' (%s)" % ( tbName, cols )
		cursor.execute( q )
		self.conn.commit()
	
	def table_exists( self, tbName ):
		q = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % tbName;
		result = self.fetch_one( q )
		if result:
			return True
		else:
			return False
		