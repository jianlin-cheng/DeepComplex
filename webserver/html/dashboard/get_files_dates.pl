
# perl /var/www/html/multicom_cluster/dashboard/get_files_dates.pl /var/www/html/multicom_cluster/work/

use Cwd;

use Carp;
use Cwd 'abs_path';
use File::Basename;
use Time::Local;
use LWP::UserAgent;
use lib dirname(abs_path($0));
use POSIX qw(strftime);

$num = @ARGV;
if($num != 1)
{
	die "The number of parameter is not correct!\n";
}
$file_dir = $ARGV[0];

opendir(DIR,"$file_dir") || die "Failed to open dir $file_dir\n";
@subdirs = readdir(DIR);
closedir(DIR);


$server_endpoint = "http://sysbio.rnet.missouri.edu/multicom_cluster/dashboard/record_submission.php";

foreach $subdir (@subdirs)
{
	chomp $subdir;
	
	if(! -e "$file_dir/$subdir/multicom_results.tar.gz")
	{
		next;
	}
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime((lstat("$file_dir/$subdir/multicom_results.tar.gz"))[9]);
	chomp $sec;
	chomp $min;
	chomp $hour;
	chomp $mday;
	chomp $mon;
	chomp $year;
	chomp $wday;
	chomp $yday;
	chomp $isdst;
	$currentdate = sprintf("%4d-%02d-%02d",($year + 1900),($mon+1),$mday);
	
	$create_time = strftime("%d %b %Y %H:%M", localtime((lstat("$file_dir/$subdir/multicom_results.tar.gz"))[9]));

	printf "%s %s\n", $file, $create_time;


	print "$currentdate\n";
	@tmp = split('-',$subdir);
	$jobname = $tmp[1];
	$jobid = $tmp[2];
	
	$location = "/var/www/html/multicom_cluster/work/$subdir";
	$weblink = "http://sysbio.rnet.missouri.edu/multicom_cluster/status.php?job_id=$jobid&job_name=$jobname&method=multicom&domain_class=full_length";


	$filepath='/var/www/html/multicom_cluster/dashboard/MULTICOM_Methods/multicom/prediction.summary';
	
	print "Processing $location\n";
	use HTTP::Request::Common qw( POST );
	$ua = LWP::UserAgent->new;
	$req = POST $server_endpoint, 
			Content_Type => 'form-data',
			Content => [
					submit  => 1,
					date  => "$currentdate",
					name  => "$jobname",
					location  => "$location",
					weblink  => "$weblink",
					filepath  => "$filepath",
			];
	print "\tSending request..\n";
	$resp = $ua->request($req);
	if ($resp->is_success) {
			$message = $resp->decoded_content;
			print "\tReceived reply: \n\t----------------------------\n$message\n";
	}
	else {
			print "HTTP POST error code: ", $resp->code, "\n";
			print "HTTP POST error message: ", $resp->message, "\n";
	}		

}




=pod
use Cwd;

use Carp;
use Cwd 'abs_path';
use File::Basename;
use Time::Local;
use LWP::UserAgent;
use lib dirname(abs_path($0));
use POSIX qw(strftime);

$num = @ARGV;
if($num != 1)
{
	die "The number of parameter is not correct!\n";
}
$file = $ARGV[0];


$create_time = strftime("%d %b %Y %H:%M", localtime((lstat($file))[9]));

printf "%s %s\n", $file, $create_time
=cut

