<?php

if(!( isset($_FILES['upfile']) )) 
{
     echo 'upfile is not defined';
	 exit;
}
if(!( isset($_POST['upfilename']) )) 
{ 
	
	echo 'upfilename is not defined'; 
	exit;
}
if(!( isset($_POST['location']) ))
{
	
	echo 'location is not defined'; 
	exit;
}



	
	$info = pathinfo($_FILES['upfile']['name']);
	$upfilename = $_POST['upfilename']; #
	$location = $_POST['location'];
	

	$target = $location."/".$upfilename;  #/var/www/cgi-bin/multicom/work/multicom-banana-152411071925346/${jobid}_3D.tar.gz


	if (move_uploaded_file( $_FILES['upfile']['tmp_name'], $target)) {
		echo "\t\t",$_FILES['upfile']['tmp_name']," Uploaded\n\n";
	} else {
	   echo "\t\t",$_FILES['upfile']['tmp_name']," is not uploaded\n\n";
	}

	echo "\t\t",'File is received, move to '.$target,"\n"; 
	 
	echo 'Current PHP version: ' . phpversion();
	system('touch '.$location.'/testfile'); 
	chdir ($location); 
	system('tar -zxvf '.$upfilename); 
	system('cp -ar multicom_results/* '.$location); 
	system('rm -rf multicom_results/'); 
	system('touch .done'); 


?>