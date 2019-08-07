from ..base.main import LangBase

class LangPython3(LangBase):
	def write_dockerfile( self ):
		conf = self.conf
		
		folder = conf['folder']
		
		pkgList = []
		if 'pkg' in conf:
			pkgList = conf['pkg']
		else:
			return null
		
		# Create the requirements.txt file if needed
		
		if len(pkgList) == 0:
			dfContents = """\
FROM python:3

WORKDIR /root/pydoi

CMD ["/bin/sh", "-c", "python /mnt/scripts/main > /mnt/logs/stdout.log 2> /mnt/logs/stderr.log"]
"""
		else:
			#reqText = ''
			
			rfh = open( folder + "/requirements.txt", "w" )
			#rfh.write( reqText )
			for req in pkgList:
				rfh.write( req + '\n' )
			rfh.close()
			
			# Create a dockerfile with the modules desired
			
			dfContents = """\
FROM python:3

WORKDIR /root/pydoi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

	CMD ["/bin/sh", "-c", "python /mnt/scripts/main > /mnt/logs/stdout.log 2> /mnt/logs/stderr.log"]
"""
		#CMD [ "python", "/mnt/scripts/script.py" ]
		
			
		dfh = open( folder + "/dockerfile", "w" )
		dfh.write( dfContents )
		dfh.close()