#!/usr/bin/perl -w
use strict;
use IPC::Open3;

my( $inputH, $outputH, $errH );
my $pid = open3( $inputH, $outputH, $errH, './in_docker.py' );

if( 0 ) {
print $inputH <<DONE;
{
	"lang": "python3",
	"pkg": []
}
--input.txt

--main
#!/usr/bin/python
print( 'test' );
DONE
}

print $inputH <<DONE;
{
	"lang": "perl5",
	"mods": ["requires 'JSON::XS';"]
}
--input.txt

--main
#!/usr/bin/perl -w
use strict;
use JSON::XS;
print 'test';
DONE

close( $inputH );

print "===Output===:\n";

my $out = '';
if( $outputH ) {
	for( <$outputH> ) {
		my $line = $_;
		print "$line";
		$out .= $line;
	}
}

my $err = '';
if( $errH ) {
	for( <$errH> ) {
		$err .= $_;
	}
}
print "===Error===:\n$err\n";

waitpid( $pid, 0 );