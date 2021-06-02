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
	if(!( isset($_POST['location']) )) #/var/www/html/casp13_dashboard/CASP13_dashboard/MULTICOM_Methods/dncon2/
	{
		
		echo 'location is not defined'; 
		exit; 
	}


	$upfilename = $_POST['upfilename'];
	$location = $_POST['location'];
	if (!file_exists($location)) {
		mkdir($location, 0777, true);
	}
	
	#$ext = $info['extension']; // get the extension of the file
	$target = $location."/".$upfilename; 

	#$target = '/var/www/html/DeepSF/results_3D/'.$newname;
	move_uploaded_file( $_FILES['upfile']['tmp_name'], $target);
	echo 'File is received, move to '.$target; 
?>