<?php

if(!( isset($_POST['date']) )) 
{
     echo 'date is not defined';
	 exit;
}
if(!( isset($_POST['name']) )) 
{ 
	
	echo 'name is not defined'; 
	exit;
}
if(!( isset($_POST['location']) ))
{
	
	echo 'location is not defined'; 
	exit;
}
if(!( isset($_POST['weblink']) ))
{
	
	echo 'weblink is not defined'; 
	exit;
}
if(!( isset($_POST['filepath']) ))
{
	
	echo 'filepath is not defined'; 
	exit;
}


	$filepath = $_POST['filepath'];
	$location = $_POST['location'];
	$date = $_POST['date'];
	$name = $_POST['name'];
	$weblink = $_POST['weblink'];
	
	$txt = "$date\t$name\t$location\t$weblink";
	$myfile = file_put_contents($filepath, $txt.PHP_EOL , FILE_APPEND | LOCK_EX);

?>