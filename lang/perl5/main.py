from ..base.main import LangBase

class LangPerl5(LangBase):
	def write_dockerfile( self ):
		conf = self.conf
		
		folder = conf['folder']
		
		modList = []
		if 'mods' in conf:
			modList = conf['mods']
		else:
			return None
		
		# Create the requirements.txt file if needed
		
		if len(modList) == 0:
			dfContents = """\
FROM perl:5

WORKDIR /root/pydoi

CMD ["/bin/sh", "-c", "perl -I/root/pydoi/local/lib/perl5 /mnt/scripts/main > /mnt/logs/stdout.log 2> /mnt/logs/stderr.log"]
"""
		else:
			#reqText = ''
			
			rfh = open( folder + "/cpanfile", "w" )
			for req in modList:
				rfh.write( req + '\n' )
			rfh.close()
			
			# Create a dockerfile with the modules desired
			
			dfContents = """\
FROM perl:5

WORKDIR /root/pydoi

COPY cpanfile ./
RUN cpanm Carton && \
	carton install

CMD ["/bin/sh", "-c", "perl -I/root/pydoi/local/lib/perl5 /mnt/scripts/main > /mnt/logs/stdout.log 2> /mnt/logs/stderr.log"]
"""
			
		dfh = open( folder + "/dockerfile", "w" )
		dfh.write( dfContents )
		dfh.close()