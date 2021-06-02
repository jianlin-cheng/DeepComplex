<?php
#http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?method=multicom&job_id=15451457358921&job_name=Hbx&protein_id=Hbx&domain_class=full_length
#http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?method=multicom&job_id=15451457358921&job_name=C0022&protein_id=C0022&domain_class=full_length
#http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?method=multicom&job_id=15451457358921&job_name=C0022&domain_class=full_length
$job_id = $_REQUEST["job_id"];
$job_name = $_REQUEST["job_name"];
#$protein_id = $_REQUEST["protein_id"];
$pred_dir = $_REQUEST["domain_class"]; # full_length, domain1, domain2,...

$method_id = $_REQUEST["method"]; # multicom

if($method_id == 'multicom')
{
	$method_id='multicom';
}else{
	echo '<script language="javascript">';
  echo "alert(\"Couldn\'t find predictions from MULTICOM server $method_id, please provide correct link!\")";
  echo '</script>';

	$method_id='none';
}

$full_length_seq = '';

if ($file = fopen("/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/query.fasta", "r")) {
	$c=0;
	while(!feof($file)) {
		$line = trim(fgets($file));
		# do same stuff with the $line
		if($line  !="")
		{
			$c++;
			if($c == 1)
			{
				$protein_id = substr($line,1);
				
			}
			if($c == 2)
			{
				$full_length_seq = $line;
				
			}
		}
	}
	fclose($file);
}	
	
if($pred_dir != 'full_length')
{
	$protein_id = $pred_dir;
}





/* Set the path for different Status Files */
$done_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/.done";
$exec_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/.exec";
$queue_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/.queue";
$error_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/.error";


$$protein_template_dash = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/full_length.dash.csv";
$protein_fasta_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/$protein_id.fasta";
$protein_ss_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/$protein_id.ss_sa";
$protein_disorder_file = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/$protein_id.fasta.disorder";
$protein_domain_list = "/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/domain_info";

$contact_stats_file="/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/$protein_id.dncon2.rr.stats";
$contact_long_acc1_file="/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/deep1_contact/long_Acc_formated.txt";
$contact_long_acc2_file="/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/deep2_contact/long_Acc_formated.txt";
$contact_long_acc3_file="/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/deep3_contact/long_Acc_formated.txt";
$contact_long_acc4_file="/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/deep4_contact/long_Acc_formated.txt";
$contact_long_acc5_file="/var/www/html/multicom_cluster/web_development/work/multicom-$job_name-$job_id/$pred_dir/deep5_contact/long_Acc_formated.txt";


##### check the range of domain in original fasta

$target_seq = '';

if ($file = fopen("$protein_fasta_file", "r")) {
	$c=0;
	while(!feof($file)) {
		$line = trim(fgets($file));
		# do same stuff with the $line
		if($line  !="")
		{
			$c++;
			if($c == 2)
			{
				$target_seq = $line;
				
			}
		}
	}
	fclose($file);
}	

$pos_start = strpos($full_length_seq, $target_seq)+1;
$pos_end = $pos_start + strlen($target_seq)-1;


/* When the job encounters some error*/
$error = fopen($error_file, 'r');
if($error)
{
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<title>MULTICOM: Protein Tertiary Structure Modeling by Deep Learning</title>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<link rel="stylesheet" type="text/css" href="./css/mirna_base.css" media="all"/>
		<link rel="stylesheet" type="text/css" href="./css/mirna_entry.css" media="all"/>
		<meta name="keywords" content="" />
		<meta name="description" content="" />
		<link href="status.css" rel="stylesheet" type="text/css" />
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
		<script type="text/javascript" src="sms2/scripts/sms_common.js"></script>
		<script type="text/javascript" src="sms2/scripts/color_align_prop.js"></script>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
		<link rel="stylesheet" href="style/style.css">
		<link rel="Shortcut Icon" href="http://www.missouri.edu/favicon.ico" type="image/x-icon" />
		</head>

	<body>
	   <!--	 <div id="header"> -->

			<table width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
			  <tr>
				<td bgcolor="#C9E4FC">&nbsp;</td>
				<td bgcolor="#BCDEFA">&nbsp;</td>
				<td bgcolor="#9BCEF9">&nbsp;</td>
				<td bgcolor="#7EC0F5">&nbsp;</td>
				<td bgcolor="#61B1F3">&nbsp;</td>
				<td bgcolor="#4BA7F1">&nbsp;</td>
				<td bgcolor="#339BF0">&nbsp;</td>
				<td bgcolor="#2896F0">&nbsp;</td>
				<td bgcolor="#1187E8">&nbsp;</td>
				<td bgcolor="#0F78CE">&nbsp;</td>
				<td bgcolor="#0F70BF">&nbsp;</td>
				<td bgcolor="#0C5A9A">&nbsp;</td>
				<td bgcolor="#0C5694">&nbsp;</td>
				<td bgcolor="#0A477A">&nbsp;</td>
				<td bgcolor="#07355A">&nbsp;</td>
			  </tr>
			</table>
			<table   width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
			  <tr>
				<td bgcolor="#FFFFFF" width="240" rowspan="2"><img src="images/3.png" width="200" height="120" /></td>
				<td bgcolor="#FFFFFF" width="100%" height="100"><div align="center"><img src="images/MULTICOM.jpg" width="420" height="60" align="middle" /></div></td>
				<td bgcolor="#FFFFFF" width="240" rowspan="2"><div align="center"><img src="images/2.jpg" width="180" height="140" align="middle" /></div></td>
			  </tr>
			  <tr>
				<td bgcolor="#FFFFFF" width="100%"><div align="center"><img src="images/protein.jpg" width="330" height="26" align="top" /></div></td>
			  </tr>
			  
			</table>
			<table  width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
			  <tr>
				<td bgcolor="#FFFFFF" width="100%"><div align="center"><p align="center"><img src="images/line.jpg" width="100%" height="10" align="middle"/></p></div></td>
			  </tr>
			  
			</table>
			

		
		<p id="jobname" style="display:none;" hidden><?php echo $job_name?></p>
		<p id="jobid" style="display:none;" hidden><?php echo $job_id?></p>
		<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
		<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
		<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
							 
		<div id="page">
			<div id="navBarDiv">
				<ul id="navbar">
				<li>
					<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/index.html">Home</a>
				</li>
				<li>
					<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/contact.html">Contact</a>
				</li>
				<li>
					<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
				</li>
				<li>
					<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15505775833645&job_name=T1022s1&method=multicom&domain_class=full_length">Result Example (Multi-domain)</a>
				</li>
				<li>
					<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15506444111896&job_name=T0993s2&method=multicom&domain_class=full_length">Result Example (TBM)</a>
				</li>
				</ul>
			</div>				
            <div id="content_success">
                <div class="post_success">
					   <p class="title"> JOB STATUS : FAILED</p>
					   <p style="text-align:center"> 
					   <img src='images/error.png' height=50px width=50px/>
					   </p>
					   <p class="title" style="text-align:center">Your job has failed during execution. Please consider resubmitting yor job with the correct input. Please note that MULTICOM accepts only 20 standard amino acids in the input pdb file. Please avoid any non-standard amino acids in your initial structures. Alternatively, contact us for help.</p>
					   
                </div>
            </div>  <!-- end #content -->
            <div style="clear: both;">&nbsp;</div>
        </div>  <!-- end #page -->
		<div class="headedBox" >
		<h1><b>References</b> </h1>
		<b><text style="font-size: 1.2em;">[1] Hou, Jie, Tianqi Wu, Renzhi Cao, and Jianlin Cheng. "Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13." bioRxiv (2019): 552422.</text></b><br>
		<b><text style="font-size: 1.2em;">[2] Li J, Deng X, Eickholt J, Cheng J: Li J, Deng X, Eickholt J, Cheng J: Designing and Benchmarking the MULTICOM Protein Structure Prediction System. BMC Structural Biology 2013, 13(1):2.</text></b><br>
		<b><text style="font-size: 1.2em;">[3] Cheng J, Li J, Wang Z, Eickholt J, Deng X: The MULTICOM toolbox for protein structure prediction. BMC bioinformatics 2012, 13(1):65.</text></b><br>
		<b><text style="font-size: 1.2em;">[4] Wang Z, Eickholt J, Cheng J: MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics 2010, 26(7):882-888.</text></b><br>

		</div>
		<div class="footer">
		<div align="center">
		<p align="center" style="text-align:center"><a href="http://people.cs.missouri.edu/~chengji/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a><a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
		<p align="center">&nbsp;</p>
		</div>
		</div>
    </body>
</html>
<?php	
}
else
{
	/* When the job is finished*/
	$done = fopen($done_file, 'r');
	if($done)
	{
?>

		<!DOCTYPE html
				PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
						 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
		<title>MULTICOM: Protein Tertiary Structure Modeling by Deep Learning</title>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<link rel="stylesheet" type="text/css" href="./css/mirna_base.css" media="all"/>
		<link rel="stylesheet" type="text/css" href="./css/mirna_entry.css" media="all"/>
		<meta name="keywords" content="" />
		<meta name="description" content="" />
		<link href="status.css" rel="stylesheet" type="text/css" />
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
		<script type="text/javascript" src="sms2/scripts/sms_common.js"></script>
		<script type="text/javascript" src="sms2/scripts/color_align_prop.js"></script>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
		<link rel="stylesheet" href="style/style.css">
		 <style>
			.caret {
			  margin-left: 8px;
			}
			
			.target-btns:hover.btn:hover {
			  background-color: whitesmoke;
			}
			
			.target-btns {
			  background-color: white;
			}
			
			.dropdown-submenu:hover {
			  cursor: pointer;
			}
			
			.dropdown-menu-methods {
			  padding: 5px;
			}
			.dropdown-menu-methods:hover {
			  cursor: pointer;
			  background-color: whitesmoke;
			}
			.dropdown-menu {
			  overflow: inherit;
			}
			
			.loader {
			  border: 5px solid lightgray; /* Light grey */
			  border-top: 5px solid #3498db; /* Blue */
			  border-radius: 50%;
			  width: 20px;
			  height: 20px;
			  animation: spin 2s linear infinite;
			}

			@keyframes spin {
			  0% { transform: rotate(0deg); }
			  100% { transform: rotate(360deg); }
			}
			
			.carousel-control.left {
			  background-image: none;
			}

			.carousel-control.right {
			  background-image: none;
			}
		  </style>
		<link rel="Shortcut Icon" href="http://www.missouri.edu/favicon.ico" type="image/x-icon" />
		<script type="text/javascript" src="sorttable.js"></script>
		<script type="text/javascript" src="js/JSmol.min.js"></script>
		<script type="text/javascript">
			var Info = {
				width: 500,
				height: 400,
				serverURL: "http://chemapps.stolaf.edu/jmol/jsmol/jsmol.php ",
				use: "HTML5",
				j2sPath: "js/j2s"
			}
			


		</script>
		</head>
		<style>
			.select-style {
				border: 1px solid #ccc;
				width: 120px;
				border-radius: 3px;
				overflow: hidden;
				background: #fafafa url("img/icon-select.png") no-repeat 90% 50%;
			}

			.select-style select {
				padding: 5px 8px;
				width: 130%;
				border: none;
				box-shadow: none;
				background: transparent;
				background-image: none;
				-webkit-appearance: none;
			}

			.select-style select:focus {
				outline: none;
			}

		</style>
		<body>

		<table width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
		  <tr>
			<td bgcolor="#C9E4FC">&nbsp;</td>
			<td bgcolor="#BCDEFA">&nbsp;</td>
			<td bgcolor="#9BCEF9">&nbsp;</td>
			<td bgcolor="#7EC0F5">&nbsp;</td>
			<td bgcolor="#61B1F3">&nbsp;</td>
			<td bgcolor="#4BA7F1">&nbsp;</td>
			<td bgcolor="#339BF0">&nbsp;</td>
			<td bgcolor="#2896F0">&nbsp;</td>
			<td bgcolor="#1187E8">&nbsp;</td>
			<td bgcolor="#0F78CE">&nbsp;</td>
			<td bgcolor="#0F70BF">&nbsp;</td>
			<td bgcolor="#0C5A9A">&nbsp;</td>
			<td bgcolor="#0C5694">&nbsp;</td>
			<td bgcolor="#0A477A">&nbsp;</td>
			<td bgcolor="#07355A">&nbsp;</td>
		  </tr>
		</table>
		<table   width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
		  <tr>
			<td bgcolor="#FFFFFF" width="240" rowspan="2"><img src="images/3.png" width="200" height="120" /></td>
			<td bgcolor="#FFFFFF" width="100%" height="100"><div align="center"><img src="images/MULTICOM.jpg" width="420" height="60" align="middle" /></div></td>
			<td bgcolor="#FFFFFF" width="240" rowspan="2"><div align="center"><img src="images/2.jpg" width="180" height="140" align="middle" /></div></td>
		  </tr>
		  <tr>
			<td bgcolor="#FFFFFF" width="100%"><div align="center"><img src="images/protein.jpg" width="330" height="26" align="top" /></div></td>
		  </tr>
		  
		</table>
		<table  width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
		  <tr>
			<td bgcolor="#FFFFFF" width="100%"><div align="center"><p align="center"><img src="images/line.jpg" width="100%" height="10" align="middle"/></p></div></td>
		  </tr>
		  
		</table>

		<p id="jobname" style="display:none;" hidden><?php echo $job_name?></p>
		<p id="jobid" style="display:none;" hidden><?php echo $job_id?></p>
		<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
		<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
		<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
		<p id="p_id" style="display:none;" hidden><?php echo $protein_id?></p>

		<div id="navBarDiv">
			<ul id="navbar">
			<li>
				<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/index.html">Home</a>
			</li>
			<li>
				<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/contact.html">Contact</a>
			</li>
			<li>
				<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
			</li>
			<li>
				<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15505775833645&job_name=T1022s1&method=multicom&domain_class=full_length">Result Example (Multi-domain)</a>
			</li>
			<li>
				<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15506444111896&job_name=T0993s2&method=multicom&domain_class=full_length">Result Example (TBM)</a>
			</li>
			</ul>
		</div>


		<div id="mainSection">
		<div align="center">
		<p class="title"><b>Results of Structure Prediction for Job Name: <?php echo $job_name?> (<u> <a style="color: #154360;" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}"?>/multicom_results.tar.gz">Click <img src='images/download.png' height=20px width=20px/></a></u>)</b></p>
		</div>
		<!--
		<div id="releaseWarning" style="margin:0.5em; padding:0.5em; width: 80%; background: #ECC; border: 1px solid #500">
		<h2 style="font-size:1.0em; color:#500; padding:0; margin:0;">At risk time</h2>
		<p style="font-size:0.8em; color:#500; padding:0; margin:0;">
		miRBase release 10.0 is being rolled out on 2nd Aug.  Results from 
		searches on this page may be unstable during this time.
		</p>
		</div>
		-->
		<?php
			if(file_exists("./work/${method_id}-${job_name}-${job_id}/$protein_id.domain_info.marker.jpeg"))
			{
		?>
				<div id="rightColumn">
				<div class="headedBox">
				<h1><b> Domain Boundary prediction </b> (<u> <a href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$protein_id.domain_info.marker.jpeg"?>" style="font-weight: bold;color: #EEE;"> View <img src='images/download.png' height=20px width=20px/></a></u>)</h1>
				<img width="100%" height="100%" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/$protein_id.domain_info.marker.jpeg"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/$protein_id.domain_info.marker.jpeg"?>" />
				</div>  
				</div>  <!-- rightColumn -->
		<?php
			}
		?>
		<div class="headedBox" style="width:70%">
		<h1><b> Protein sequence </b></h1>
		<textarea  readonly="readonly" id="protein_sequence" style="width: 100%;height: 60px;font-size: 12px;font-weight: bold;"><?php
			if ($file = fopen($protein_fasta_file, "r")) {
				$c=0;
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c++;
						if($c==1)
						{
							echo "$line: $pos_start-$pos_end\n"; 
							
						}else{
							echo "$line\n"; 
						}
						#$parts = preg_split('/\s+/', $line);
						#if($parts[0] == ">$protein_id")
						#{
						#	echo "\n$parts[0]\n$parts[1]\n"; 
						#}
						
						
					}
				}
				fclose($file);
			}

		?></textarea><br>
		</div>

		<div class="headedBox" style="width:70%">
		<h1><b> Secondary structure prediction  <u>(H: Helix   E: Strand   C: Coil)</u> </b></h1>
		<textarea  readonly="readonly"  id="protein_ss_sa" style="width: 100%;height: 60px;font-size: 12px;font-weight: bold;"><?php
			if ($file = fopen($protein_ss_file, "r")) {
				$c=0;
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c++;
						#$parts = preg_split('/\s+/', $line);
						if($line != ">$protein_id" and $c!=2 and $c!=4)
						{
							echo strtoupper($line)."\n";
						}
					}
				}
				fclose($file);
			}

		?></textarea><br>
		</div>


		<div class="headedBox" style="width:70%">
		<h1><b> Solvent accessibility prediction <u>(e: Exposed   b: Buried)</u>  </b></h1>
		<textarea  readonly="readonly" id="protein_ss_sa" style="width: 100%;height: 60px;font-size: 12px;font-weight: bold;"><?php
			if ($file = fopen($protein_ss_file, "r")) {
				$c=0;
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c++;
						#$parts = preg_split('/\s+/', $line);
						if($line != ">$protein_id" and $c!=3 and $c!=2)
						{
							echo strtoupper($line)."\n";
						}
					}
				}
				fclose($file);
			}

		?></textarea><br>
		</div>
		<?php
			if(file_exists($protein_disorder_file))
			{
		?>
		<div class="headedBox" style="width:70%">
		<h1><b> Disorder prediction <u>(N: Normal   T: Disorder)</u> </b></h1>	
		<textarea  readonly="readonly" id="protein_disorder" style="width: 100%;height: 60px;font-size: 12px;font-weight: bold;"><?php
			if ($file = fopen($protein_disorder_file, "r")) {
				$c=0;
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c++;
						#$parts = preg_split('/\s+/', $line);
						if($line != ">$protein_id" and $c!=3 and $c!=1)
						{
							echo "$line\n";
						}
						
					}
				}
				fclose($file);
			}

		?></textarea><br>

		</div>
		<?php
			}
		?>


		<div align="center">
			<p class="title"><b> Select domain </b></p>
			<form action="status.php" id="carform" style="align:center;">
			<input name="job_id"  type="hidden" value="<?php echo $job_id?>">
			<input  name="job_name"  type="hidden" value="<?php echo $job_name?>">
			<input  name="method"  type="hidden" value="<?php echo $method_id?>">
			<select name="domain_class" style="font-size: 150%; text-align: center;align:center;">
					<option value="full_length">Select domain (<?php echo $protein_id?>)</option>
					<option value="full_length">full_length</option>
					<!--<option value="" disabled="disabled" selected="selected">Please select target</option>-->
					<?php
							$c = 0;
							if ($file = fopen($protein_domain_list, "r")) {
								while(!feof($file)) {
									$line = trim(fgets($file));
									# do same stuff with the $line
									if($line  !="")
									{
										
										echo "<option value=\"domain$c\">$line</option>"; 
										$c +=1;
									}
								}
								fclose($file);
							}
					
					?>
				
			</select>	
			<input style="font-size: 150%; text-align: center;" type="submit">
			</form>	
		</div>	



		<div class="headedBox">
		<h1><b>Predicted Top 1 Tertiary structure </b> </h1>
		<div align="left">
		&nbsp;&nbsp;&nbsp;

		<table cellspacing="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
		<tr>
		<td align="left">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
		<p class="title" style="font-size:22px;color:#154360"> <a style="font-size:22px;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/$protein_id.deep1.pdb"?>"><u><b>Predicted Model 1</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>

		<script type="text/javascript">
			var job = $("#jobname").text();
			var id = $("#jobid").text();
			var protein_id = $("#protein_id").text();
			var methodName = $("#methodName").text();
			var target = job+'-'+id;
			var pred_dir = $("#pred_dir").text();
			var rfile = 1;
			var model = 1;
			//var append = "APPEND";
			var append = "";
			var modelfile = "work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb";
			Jmol.getApplet("jsmolApplet_M23d1", Info);
			Jmol.script(jsmolApplet_M23d1,"background black; load work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb;");
			Jmol.script(jsmolApplet_M23d1, "spin on; cartoon only; color {file="+ rfile+"} group;");
		</script>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:500px; height:500px; margin-left: 0%;">
		<div id="displayTableCarousel1" class="carousel slide" data-ride="carousel" data-interval="false" style="width:500px; height:500px; margin-left: 0%;">
			<ol class="carousel-indicators">
				<li data-target="#displayTableCarousel1" data-slide-to="0" class="active"></li>
				<li data-target="#displayTableCarousel1" data-slide-to="1"></li>
				<li data-target="#displayTableCarousel1" data-slide-to="2"></li>
				<li data-target="#displayTableCarousel1" data-slide-to="3"></li>
			</ol>
			<div class="carousel-inner" style="height:500px; margin-left: 15%;">
				<div class="item active">		
					<p class="title" style="font-size:22px;color:#154360;text-align:left;"><a style="font-size:22px;color:#154360;text-align:left;" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep1_contact/L5_long.png"?>"><u><b> Model 1 vs Contact (Top L/5)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/L5_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/L5_long.png"?>" />
					</div>			
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep1_contact/L2_long.png"?>"><u><b> Model 1 vs Contact (Top L/2)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/L2_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/L2_long.png"?>" />
					</div>

					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;">  <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep1_contact/L_long.png"?>"><u><b> Model 1 vs Contact (Top L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/L_long.png"?>" />
					</div>	
					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep1_contact/2L_long.png"?>"><u><b> Model 1 vs Contact (Top 2L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/2L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/2L_long.png"?>" />
					</div>	
				</div>
				
				
			</div>
			<a class="left carousel-control" href="#displayTableCarousel1" data-slide="prev">
				<span class="glyphicon glyphicon-chevron-left" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Previous</span>
			  </a>
			  <a class="right carousel-control" href="#displayTableCarousel1" data-slide="next">
				<span class="glyphicon glyphicon-chevron-right" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Next</span>
			  </a>
		</div>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:220px;height:500px; margin-left: 0%;">
		<h3 style="text-align: center;color:#154360"> <u><b>Contact Accuracy</u><br> <a style="text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep1_contact/$protein_id.dncon2.rr"?>"> ( <u>Contact file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		<div align="center"> 
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_long_acc1_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		  <p>&nbsp;&nbsp;&nbsp;</p>
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_stats_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		</div>
		</div>
		</td>

		<td style="padding: 0px 0px 0px 50px;">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
			<?php
			if(file_exists("./work/${method_id}-${job_name}-${job_id}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is multi-domain domain, check alignments in individual domains!</u></text>"; 

			}else if(!file_exists("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep1.msa") and ${pred_dir}!='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is ab initio domain, no significant templates are found!</u></text>"; 

				
			}else{
			?>	
				<div class="carousel-inner" style="width:600px;height:500px; margin-left: 0%;">
				<h3 align="center" style="align:center;text-align: left;color:#154360;"> 
				<form action="" name="main_form" id="main_form_3d">
				<textarea rows="6" cols="61" style="display:none;">
			<?php
				$c = 0;
				if ($file = fopen("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep1.msa", "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c +=1;
						echo "$line\n"; 
					}
				}
				fclose($file);
				}
			?>	 
				</textarea>
				<input type="button" value="View multiple sequence alignment" name="main_submit" onclick="try{colorAlignProp(document,'main_form_3d')} catch(e) {alert('The following error was encountered: ' + e);}" /> <input type="button" value="Clear" onclick="document.forms[0].elements[0].value = ' '" style='display:none;' /> <input type="reset" value="Reset" / style='display:none;'>

				<select  style='display:none;'><option selected="selected" value="80">80</option></select> 
				<select  style='display:none;'><option selected="selected" value="100">100</option></select>
				<select  style='display:none;'><option selected="selected" value="background">backgrounds</option><option value="text">text</option></select> 
				<textarea rows="2" cols="61"  style='display:none;'></textarea>
				</form>
				<br>
				<b><a style="align:center;text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep1.msa.marker.jpeg"?>"> ( <u>Click <img src='images/download.png' height=20px width=20px/></u> )</a></b>
				</h3>
				<img align="left" style="width: 80%; height: 50%; margin: 0 0 0 -50px;text-align: left;" alt="template_alignment" src=<?php echo "./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep1.msa.marker.jpeg"?> />
				</div>
			<?php
			}
			?>
		</div>
		</td>
		</tr>


		</table>
		</div>
		</div>



		<div class="headedBox">
		<h1><b>Predicted Top 2 Tertiary structure </b> </h1>
		<div align="left">
		&nbsp;&nbsp;&nbsp;

		<table cellspacing="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
		<tr>
		<td align="left">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
		<p class="title" style="font-size:22px;color:#154360"> <a style="font-size:22px;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/$protein_id.deep2.pdb"?>"><u><b>Predicted Model 2</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>

		<script type="text/javascript">
			var job = $("#jobname").text();
			var id = $("#jobid").text();
			var methodName = $("#methodName").text();
			var target = job+'-'+id;
			var pred_dir = $("#pred_dir").text();
			var rfile = 1;
			var model = 2;
			//var append = "APPEND";
			var append = "";
			var modelfile = "work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb";
			Jmol.getApplet("jsmolApplet_M23d2", Info);
			Jmol.script(jsmolApplet_M23d2,"background black; load work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb;");
			Jmol.script(jsmolApplet_M23d2, "spin on; cartoon only; color {file="+ rfile+"} group;");
		</script>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:500px; height:500px; margin-left: 0%;">
		<div id="displayTableCarousel2" class="carousel slide" data-ride="carousel" data-interval="false" style="width:500px; height:500px; margin-left: 0%;">
			<ol class="carousel-indicators">
				<li data-target="#displayTableCarousel2" data-slide-to="0" class="active"></li>
				<li data-target="#displayTableCarousel2" data-slide-to="1"></li>
				<li data-target="#displayTableCarousel2" data-slide-to="2"></li>
				<li data-target="#displayTableCarousel2" data-slide-to="3"></li>
			</ol>
			<div class="carousel-inner" style="height:500px; margin-left: 15%;">
				<div class="item active">		
					<p class="title" style="font-size:22px;color:#154360;text-align:left;"><a style="font-size:22px;color:#154360;text-align:left;" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep2_contact/L5_long.png"?>"><u><b> Model 2 vs Contact (Top L/5)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/L5_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/L5_long.png"?>" />
					</div>			
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep2_contact/L2_long.png"?>"><u><b> Model 2 vs Contact (Top L/2)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/L2_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/L2_long.png"?>" />
					</div>

					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;">  <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep2_contact/L_long.png"?>"><u><b> Model 2 vs Contact (Top L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/L_long.png"?>" />
					</div>	
					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep2_contact/2L_long.png"?>"><u><b> Model 2 vs Contact (Top 2L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/2L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/2L_long.png"?>" />
					</div>	
				</div>
				
				
			</div>
			<a class="left carousel-control" href="#displayTableCarousel2" data-slide="prev">
				<span class="glyphicon glyphicon-chevron-left" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Previous</span>
			  </a>
			  <a class="right carousel-control" href="#displayTableCarousel2" data-slide="next">
				<span class="glyphicon glyphicon-chevron-right" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Next</span>
			</a>
		</div>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:220px;height:500px; margin-left: 0%;">
		<h3 style="text-align: center;color:#154360"> <u><b>Contact Accuracy</u><br> <a style="text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep2_contact/$protein_id.dncon2.rr"?>"> ( <u>Contact file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		<div align="center"> 
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_long_acc2_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		  <p>&nbsp;&nbsp;&nbsp;</p>
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_stats_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		</div>
		</div>
		</td>

		<td style="padding: 0px 0px 0px 50px;">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
			<?php
			if(file_exists("./work/${method_id}-${job_name}-${job_id}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is multi-domain domain, check alignments in individual domains!</u></text>"; 
			}else if(!file_exists("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep2.msa") and ${pred_dir}!='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is ab initio domain, no significant templates are found!</u></text>"; 

				
			}else{
			?>	
				<div class="carousel-inner" style="width:600px;height:500px; margin-left: 0%;">
				<h3 align="center" style="align:center;text-align: left;color:#154360;"> 
				<form action="" name="main_form" id="main_form_3d">
				<textarea rows="6" cols="61" style="display:none;">
			<?php
				$c = 0;
				if ($file = fopen("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep2.msa", "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c +=1;
						echo "$line\n"; 
					}
				}
				fclose($file);
				}
			?>	 
				</textarea>
				<input type="button" value="View multiple sequence alignment" name="main_submit" onclick="try{colorAlignProp(document,'main_form_3d')} catch(e) {alert('The following error was encountered: ' + e);}" /> <input type="button" value="Clear" onclick="document.forms[0].elements[0].value = ' '" style='display:none;' /> <input type="reset" value="Reset" / style='display:none;'>

				<select  style='display:none;'><option selected="selected" value="80">80</option></select> 
				<select  style='display:none;'><option selected="selected" value="100">100</option></select>
				<select  style='display:none;'><option selected="selected" value="background">backgrounds</option><option value="text">text</option></select> 
				<textarea rows="2" cols="61"  style='display:none;'></textarea>
				</form>
				<br>
				<b><a style="align:center;text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep2.msa.marker.jpeg"?>"> ( <u>Click <img src='images/download.png' height=20px width=20px/></u> )</a></b>
				</h3>
				<img align="left" style="width: 80%; height: 50%; margin: 0 0 0 -50px;text-align: left;" alt="template_alignment" src=<?php echo "./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep2.msa.marker.jpeg"?> />
				</div>
			<?php
			}
			?>
		</div>
		</td>
		</tr>


		</table>
		</div>
		</div>



		<div class="headedBox">
		<h1><b>Predicted Top 3 Tertiary structure </b> </h1>
		<div align="left">
		&nbsp;&nbsp;&nbsp;

		<table cellspacing="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
		<tr>
		<td align="left">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
		<p class="title" style="font-size:22px;color:#154360"> <a style="font-size:22px;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/$protein_id.deep3.pdb"?>"><u><b>Predicted Model 3</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>

			<script type="text/javascript">
				var job = $("#jobname").text();
				var id = $("#jobid").text();
				var methodName = $("#methodName").text();
				var target = job+'-'+id;
				var pred_dir = $("#pred_dir").text();
				var rfile = 1;
				var model = 3;
				//var append = "APPEND";
				var append = "";
				var modelfile = "work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb";
				Jmol.getApplet("jsmolApplet_M23d3", Info);
				Jmol.script(jsmolApplet_M23d3,"background black; load work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb;");
				Jmol.script(jsmolApplet_M23d3, "spin on; cartoon only; color {file="+ rfile+"} group;");
			</script>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:500px; height:500px; margin-left: 0%;">
		<div id="displayTableCarousel3" class="carousel slide" data-ride="carousel" data-interval="false" style="width:500px; height:500px; margin-left: 0%;">
			<ol class="carousel-indicators">
				<li data-target="#displayTableCarousel3" data-slide-to="0" class="active"></li>
				<li data-target="#displayTableCarousel3" data-slide-to="1"></li>
				<li data-target="#displayTableCarousel3" data-slide-to="2"></li>
				<li data-target="#displayTableCarousel3" data-slide-to="3"></li>
			</ol>
			<div class="carousel-inner" style="height:500px; margin-left: 15%;">
				<div class="item active">		
					<p class="title" style="font-size:22px;color:#154360;text-align:left;"><a style="font-size:22px;color:#154360;text-align:left;" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep3_contact/L5_long.png"?>"><u><b> Model 3 vs Contact (Top L/5)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/L5_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/L5_long.png"?>" />
					</div>			
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep3_contact/L2_long.png"?>"><u><b> Model 3 vs Contact (Top L/2)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/L2_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/L2_long.png"?>" />
					</div>

					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;">  <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep3_contact/L_long.png"?>"><u><b> Model 3 vs Contact (Top L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/L_long.png"?>" />
					</div>	
					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep3_contact/2L_long.png"?>"><u><b> Model 3 vs Contact (Top 2L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/2L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/2L_long.png"?>" />
					</div>	
				</div>
				
				
			</div>
			<a class="left carousel-control" href="#displayTableCarousel3" data-slide="prev">
				<span class="glyphicon glyphicon-chevron-left" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Previous</span>
			  </a>
			  <a class="right carousel-control" href="#displayTableCarousel3" data-slide="next">
				<span class="glyphicon glyphicon-chevron-right" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Next</span>
			  </a>
		</div>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:220px;height:500px; margin-left: 0%;">
		<h3 style="text-align: center;color:#154360"> <u><b>Contact Accuracy</u><br> <a style="text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep3_contact/$protein_id.dncon2.rr"?>"> ( <u>Contact file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		<div align="center"> 
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_long_acc3_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		  <p>&nbsp;&nbsp;&nbsp;</p>
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_stats_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		</div>
		</div>
		</td>

		<td style="padding: 0px 0px 0px 50px;">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
			<?php
			if(file_exists("./work/${method_id}-${job_name}-${job_id}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
				
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is multi-domain domain, check alignments in individual domains!</u></text>"; 
				
			}else if(!file_exists("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep3.msa") and ${pred_dir}!='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is ab initio domain, no significant templates are found!</u></text>"; 

				
			}else{
			?>	
				<div class="carousel-inner" style="width:600px;height:500px; margin-left: 0%;">
				<h3 align="center" style="align:center;text-align: left;color:#154360;"> 
				<form action="" name="main_form" id="main_form_3d">
				<textarea rows="6" cols="61" style="display:none;">
			<?php
				$c = 0;
				if ($file = fopen("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep3.msa", "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c +=1;
						echo "$line\n"; 
					}
				}
				fclose($file);
				}
			?>	 
				</textarea>
				<input type="button" value="View multiple sequence alignment" name="main_submit" onclick="try{colorAlignProp(document,'main_form_3d')} catch(e) {alert('The following error was encountered: ' + e);}" /> <input type="button" value="Clear" onclick="document.forms[0].elements[0].value = ' '" style='display:none;' /> <input type="reset" value="Reset" / style='display:none;'>

				<select  style='display:none;'><option selected="selected" value="80">80</option></select> 
				<select  style='display:none;'><option selected="selected" value="100">100</option></select>
				<select  style='display:none;'><option selected="selected" value="background">backgrounds</option><option value="text">text</option></select> 
				<textarea rows="2" cols="61"  style='display:none;'></textarea>
				</form>
				<br>
				<b><a style="align:center;text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep3.msa.marker.jpeg"?>"> ( <u>Click <img src='images/download.png' height=20px width=20px/></u> )</a></b>
				</h3>
				<img align="left" style="width: 80%; height: 50%; margin: 0 0 0 -50px;text-align: left;" alt="template_alignment" src=<?php echo "./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep3.msa.marker.jpeg"?> />
				</div>
			<?php
			}
			?>
		</div>
		</td>
		</tr>


		</table>
		</div>
		</div>




		<div class="headedBox">
		<h1><b>Predicted Top 4 Tertiary structure </b> </h1>
		<div align="left">
		&nbsp;&nbsp;&nbsp;

		<table cellspacing="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
		<tr>
		<td align="left">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
		<p class="title" style="font-size:22px;color:#154360"> <a style="font-size:22px;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/$protein_id.deep4.pdb"?>"><u><b>Predicted Model 4</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>

			<script type="text/javascript">
				var job = $("#jobname").text();
				var id = $("#jobid").text();
				var methodName = $("#methodName").text();
				var target = job+'-'+id;
				var pred_dir = $("#pred_dir").text();
				var rfile = 1;
				var model = 4;
				//var append = "APPEND";
				var append = "";
				var modelfile = "work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb";
				Jmol.getApplet("jsmolApplet_M23d4", Info);
				Jmol.script(jsmolApplet_M23d4,"background black; load work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb;");
				Jmol.script(jsmolApplet_M23d4, "spin on; cartoon only; color {file="+ rfile+"} group;");
			</script>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:500px; height:500px; margin-left: 0%;">
		<div id="displayTableCarousel4" class="carousel slide" data-ride="carousel" data-interval="false" style="width:500px; height:500px; margin-left: 0%;">
			<ol class="carousel-indicators">
				<li data-target="#displayTableCarousel4" data-slide-to="0" class="active"></li>
				<li data-target="#displayTableCarousel4" data-slide-to="1"></li>
				<li data-target="#displayTableCarousel4" data-slide-to="2"></li>
				<li data-target="#displayTableCarousel4" data-slide-to="3"></li>
			</ol>
			<div class="carousel-inner" style="height:500px; margin-left: 15%;">
				<div class="item active">		
					<p class="title" style="font-size:22px;color:#154360;text-align:left;"><a style="font-size:22px;color:#154360;text-align:left;" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep4_contact/L5_long.png"?>"><u><b> Model 4 vs Contact (Top L/5)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/L5_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/L5_long.png"?>" />
					</div>			
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep4_contact/L2_long.png"?>"><u><b> Model 4 vs Contact (Top L/2)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/L2_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/L2_long.png"?>" />
					</div>

					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;">  <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep4_contact/L_long.png"?>"><u><b> Model 4 vs Contact (Top L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/L_long.png"?>" />
					</div>	
					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep4_contact/2L_long.png"?>"><u><b> Model 4 vs Contact (Top 2L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/2L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/2L_long.png"?>" />
					</div>	
				</div>
				
				
			</div>
			<a class="left carousel-control" href="#displayTableCarousel4" data-slide="prev">
				<span class="glyphicon glyphicon-chevron-left" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Previous</span>
			  </a>
			  <a class="right carousel-control" href="#displayTableCarousel4" data-slide="next">
				<span class="glyphicon glyphicon-chevron-right" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Next</span>
			  </a>
		</div>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:220px;height:500px; margin-left: 0%;">
		<h3 style="text-align: center;color:#154360"> <u><b>Contact Accuracy</u><br> <a style="text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep4_contact/$protein_id.dncon2.rr"?>"> ( <u>Contact file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		<div align="center"> 
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_long_acc4_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		  <p>&nbsp;&nbsp;&nbsp;</p>
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_stats_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		</div>
		</div>
		</td>

		<td style="padding: 0px 0px 0px 50px;">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
			<?php
			if(file_exists("./work/${method_id}-${job_name}-${job_id}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
				
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is multi-domain domain, check alignments in individual domains!</u></text>"; 
				
			}else if(!file_exists("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep4.msa") and ${pred_dir}!='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is ab initio domain, no significant templates are found!</u></text>"; 

				
			}else{
			?>	
				<div class="carousel-inner" style="width:600px;height:500px; margin-left: 0%;">
				<h3 align="center" style="align:center;text-align: left;color:#154360;"> 
				<form action="" name="main_form" id="main_form_3d">
				<textarea rows="6" cols="61" style="display:none;">
			<?php
				$c = 0;
				if ($file = fopen("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep4.msa", "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c +=1;
						echo "$line\n"; 
					}
				}
				fclose($file);
				}
			?>	 
				</textarea>
				<input type="button" value="View multiple sequence alignment" name="main_submit" onclick="try{colorAlignProp(document,'main_form_3d')} catch(e) {alert('The following error was encountered: ' + e);}" /> <input type="button" value="Clear" onclick="document.forms[0].elements[0].value = ' '" style='display:none;' /> <input type="reset" value="Reset" / style='display:none;'>

				<select  style='display:none;'><option selected="selected" value="80">80</option></select> 
				<select  style='display:none;'><option selected="selected" value="100">100</option></select>
				<select  style='display:none;'><option selected="selected" value="background">backgrounds</option><option value="text">text</option></select> 
				<textarea rows="2" cols="61"  style='display:none;'></textarea>
				</form>
				<br>
				<b><a style="align:center;text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep4.msa.marker.jpeg"?>"> ( <u>Click <img src='images/download.png' height=20px width=20px/></u> )</a></b>
				</h3>
				<img align="left" style="width: 80%; height: 50%; margin: 0 0 0 -50px;text-align: left;" alt="template_alignment" src=<?php echo "./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep4.msa.marker.jpeg"?> />
				</div>
			<?php
			}
			?>
		</div>
		</td>
		</tr>


		</table>
		</div>
		</div>




		<div class="headedBox">
		<h1><b>Predicted Top 5 Tertiary structure </b> </h1>
		<div align="left">
		&nbsp;&nbsp;&nbsp;

		<table cellspacing="60" bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
		<tr>
		<td align="left">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
		<p class="title" style="font-size:22px;color:#154360"> <a style="font-size:22px;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/$protein_id.deep5.pdb"?>"><u><b>Predicted Model 5</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>

			<script type="text/javascript">
				var job = $("#jobname").text();
				var id = $("#jobid").text();
				var methodName = $("#methodName").text();
				var target = job+'-'+id;
				var pred_dir = $("#pred_dir").text();
				var rfile = 1;
				var model = 5;
				//var append = "APPEND";
				var append = "";
				var modelfile = "work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb";
				Jmol.getApplet("jsmolApplet_M23d5", Info);
				Jmol.script(jsmolApplet_M23d5,"background black; load work/" + methodName.toLowerCase() + "-"+target+'/'+pred_dir + "/"+protein_id+'.deep'+model+ ".pdb;");
				Jmol.script(jsmolApplet_M23d5, "spin on; cartoon only; color {file="+ rfile+"} group;");
			</script>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:500px; height:500px; margin-left: 0%;">
		<div id="displayTableCarousel5" class="carousel slide" data-ride="carousel" data-interval="false" style="width:500px; height:500px; margin-left: 0%;">
			<ol class="carousel-indicators">
				<li data-target="#displayTableCarousel5" data-slide-to="0" class="active"></li>
				<li data-target="#displayTableCarousel5" data-slide-to="1"></li>
				<li data-target="#displayTableCarousel5" data-slide-to="2"></li>
				<li data-target="#displayTableCarousel5" data-slide-to="3"></li>
			</ol>
			<div class="carousel-inner" style="height:500px; margin-left: 15%;">
				<div class="item active">		
					<p class="title" style="font-size:22px;color:#154360;text-align:left;"><a style="font-size:22px;color:#154360;text-align:left;" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep5_contact/L5_long.png"?>"><u><b> Model 5 vs Contact (Top L/5)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/L5_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/L5_long.png"?>" />
					</div>			
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep5_contact/L2_long.png"?>"><u><b> Model 5 vs Contact (Top L/2)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/L2_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/L2_long.png"?>" />
					</div>

					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;">  <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep5_contact/L_long.png"?>"><u><b> Model 5 vs Contact (Top L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/L_long.png"?>" />
					</div>	
					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/$pred_dir/deep5_contact/2L_long.png"?>"><u><b> Model 5 vs Contact (Top 2L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/2L_long.png"?>" src="./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/2L_long.png"?>" />
					</div>	
				</div>
				
				
			</div>
			<a class="left carousel-control" href="#displayTableCarousel5" data-slide="prev">
				<span class="glyphicon glyphicon-chevron-left" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Previous</span>
			  </a>
			  <a class="right carousel-control" href="#displayTableCarousel5" data-slide="next">
				<span class="glyphicon glyphicon-chevron-right" style="color:red" aria-hidden="true"></span>
				<span class="sr-only">Next</span>
			  </a>
		</div>
		</div>
		</td>

		<td>
		<div class="carousel-inner" style="width:220px;height:500px; margin-left: 0%;">
		<h3 style="text-align: center;color:#154360"> <u><b>Contact Accuracy</u><br> <a style="text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/deep5_contact/$protein_id.dncon2.rr"?>"> ( <u>Contact file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		<div align="center"> 
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_long_acc5_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		  <p>&nbsp;&nbsp;&nbsp;</p>
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;">
			<tbody>
			<?php
			if ($file = fopen($contact_stats_file, "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$parts = preg_split('/\s+/', $line);
						echo "\n<tr style=\"border: 1px solid black;\">\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[0]</td>\n";
						echo "<td style=\"border: 1px solid black;padding: 6px;\">$parts[1]</td>\n";
						echo "\n</tr>\n";
					}
				}
				fclose($file);
			}

			?>	
			</tbody>
		  </table>
		</div>
		</div>
		</td>

		<td style="padding: 0px 0px 0px 50px;">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
			<?php
			if(file_exists("./work/${method_id}-${job_name}-${job_id}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
				
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is multi-domain domain, check alignments in individual domains!</u></text>"; 
				
			}else if(!file_exists("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep5.msa") and ${pred_dir}!='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:2em;\"><u>Note: This is ab initio domain, no significant templates are found!</u></text>"; 

				
			}else{
			?>	
				<div class="carousel-inner" style="width:600px;height:500px; margin-left: 0%;">
				<h3 align="center" style="align:center;text-align: left;color:#154360;"> 
				<form action="" name="main_form" id="main_form_3d">
				<textarea rows="6" cols="61" style="display:none;">
			<?php
				$c = 0;
				if ($file = fopen("./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep5.msa", "r")) {
				while(!feof($file)) {
					$line = trim(fgets($file));
					# do same stuff with the $line
					if($line  !="")
					{
						$c +=1;
						echo "$line\n"; 
					}
				}
				fclose($file);
				}
			?>	 
				</textarea>
				<input type="button" value="View multiple sequence alignment" name="main_submit" onclick="try{colorAlignProp(document,'main_form_3d')} catch(e) {alert('The following error was encountered: ' + e);}" /> <input type="button" value="Clear" onclick="document.forms[0].elements[0].value = ' '" style='display:none;' /> <input type="reset" value="Reset" / style='display:none;'>

				<select  style='display:none;'><option selected="selected" value="80">80</option></select> 
				<select  style='display:none;'><option selected="selected" value="100">100</option></select>
				<select  style='display:none;'><option selected="selected" value="background">backgrounds</option><option value="text">text</option></select> 
				<textarea rows="2" cols="61"  style='display:none;'></textarea>
				</form>
				<br>
				<b><a style="align:center;text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep5.msa.marker.jpeg"?>"> ( <u>Click <img src='images/download.png' height=20px width=20px/></u> )</a></b>
				</h3>
				<img align="left" style="width: 80%; height: 50%; margin: 0 0 0 -50px;text-align: left;" alt="template_alignment" src=<?php echo "./work/${method_id}-${job_name}-${job_id}/${pred_dir}/Top5_aln/$protein_id.deep5.msa.marker.jpeg"?> />
				</div>
			<?php
			}
			?>
		</div>
		</td>
		</tr>


		</table>
		</div>
		</div>



		</div> <!-- mainSection -->

		<div class="headedBox" >
		<h1><b>References</b> </h1>
		<b><text style="font-size: 1.2em;">[1] Hou, Jie, Tianqi Wu, Renzhi Cao, and Jianlin Cheng. "Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13." bioRxiv (2019): 552422.</text></b><br>
		<b><text style="font-size: 1.2em;">[2] Li J, Deng X, Eickholt J, Cheng J: Li J, Deng X, Eickholt J, Cheng J: Designing and Benchmarking the MULTICOM Protein Structure Prediction System. BMC Structural Biology 2013, 13(1):2.</text></b><br>
		<b><text style="font-size: 1.2em;">[3] Cheng J, Li J, Wang Z, Eickholt J, Deng X: The MULTICOM toolbox for protein structure prediction. BMC bioinformatics 2012, 13(1):65.</text></b><br>
		<b><text style="font-size: 1.2em;">[4] Wang Z, Eickholt J, Cheng J: MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics 2010, 26(7):882-888.</text></b><br>

		</div>
		<div class="footer">
		<div align="center">
		<p align="center" style="text-align:center"><a href="http://people.cs.missouri.edu/~chengji/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a><a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
		<p align="center">&nbsp;</p>
		</div>
		</div>
		</body>
	</html>
<?php
	}
	else
	{
		/* When the job is executing*/
		$exec = fopen($exec_file, 'r');
		if($exec)
		{
		?>
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<title>MULTICOM: Protein Tertiary Structure Modeling by Deep Learning</title>
			<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
			<link rel="stylesheet" type="text/css" href="./css/mirna_base.css" media="all"/>
			<link rel="stylesheet" type="text/css" href="./css/mirna_entry.css" media="all"/>
			<meta name="keywords" content="" />
			<meta name="description" content="" />
			<link href="status.css" rel="stylesheet" type="text/css" />
			<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
			<script type="text/javascript" src="sms2/scripts/sms_common.js"></script>
			<script type="text/javascript" src="sms2/scripts/color_align_prop.js"></script>
			<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
			<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
			<link rel="stylesheet" href="style/style.css">
			<link rel="Shortcut Icon" href="http://www.missouri.edu/favicon.ico" type="image/x-icon" />
			</head>

			<body>

					<table width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
					  <tr>
						<td bgcolor="#C9E4FC">&nbsp;</td>
						<td bgcolor="#BCDEFA">&nbsp;</td>
						<td bgcolor="#9BCEF9">&nbsp;</td>
						<td bgcolor="#7EC0F5">&nbsp;</td>
						<td bgcolor="#61B1F3">&nbsp;</td>
						<td bgcolor="#4BA7F1">&nbsp;</td>
						<td bgcolor="#339BF0">&nbsp;</td>
						<td bgcolor="#2896F0">&nbsp;</td>
						<td bgcolor="#1187E8">&nbsp;</td>
						<td bgcolor="#0F78CE">&nbsp;</td>
						<td bgcolor="#0F70BF">&nbsp;</td>
						<td bgcolor="#0C5A9A">&nbsp;</td>
						<td bgcolor="#0C5694">&nbsp;</td>
						<td bgcolor="#0A477A">&nbsp;</td>
						<td bgcolor="#07355A">&nbsp;</td>
					  </tr>
					</table>
					<table   width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
					  <tr>
						<td bgcolor="#FFFFFF" width="240" rowspan="2"><img src="images/3.png" width="200" height="120" /></td>
						<td bgcolor="#FFFFFF" width="100%" height="100"><div align="center"><img src="images/MULTICOM.jpg" width="420" height="60" align="middle" /></div></td>
						<td bgcolor="#FFFFFF" width="240" rowspan="2"><div align="center"><img src="images/2.jpg" width="180" height="140" align="middle" /></div></td>
					  </tr>
					  <tr>
						<td bgcolor="#FFFFFF" width="100%"><div align="center"><img src="images/protein.jpg" width="330" height="26" align="top" /></div></td>
					  </tr>
					  
					</table>
					<table  width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
					  <tr>
						<td bgcolor="#FFFFFF" width="100%"><div align="center"><p align="center"><img src="images/line.jpg" width="100%" height="10" align="middle"/></p></div></td>
					  </tr>
					  
					</table>
					

					
				<p id="jobname" style="display:none;" hidden><?php echo $job_name?></p>
				<p id="jobid" style="display:none;" hidden><?php echo $job_id?></p>
				<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
				<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
				<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
									 
				<div id="page">
					<div id="navBarDiv">
						<ul id="navbar">
						<li>
							<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/index.html">Home</a>
						</li>
						<li>
							<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/contact.html">Contact</a>
						</li>
						<li>
							<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
						</li>
						<li>
							<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15505775833645&job_name=T1022s1&method=multicom&domain_class=full_length">Result Example (Multi-domain)</a>
						</li>
						<li>
							<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15506444111896&job_name=T0993s2&method=multicom&domain_class=full_length">Result Example (TBM)</a>
						</li>
						</ul>
					</div>				
					<div id="content_success">
						<div class="post_success">
							   <p class="title"> JOB STATUS : EXECUTING</p>
							   <p style="text-align:center">
							   <img src='images/executing.gif' height=30px width=150px/>
							   </p>
							   <!--<p class='subtitle'>This page will be automatically refreshed every 10 seconds</p>-->
							   <!--<p class="text-steps">Your job is being executed by MULTICOM server. You will be redirected to the results page once your job is finished.</p>-->
							   <p class="title">Your job is being executed by MULTICOM server. Results will be emailed once your job is finished.</p>
						</div>
					</div>  <!-- end #content -->
					<div style="clear: both;">&nbsp;</div>
				</div>  <!-- end #page -->
				<div class="headedBox" >
				<h1><b>References</b> </h1>
				<b><text style="font-size: 1.2em;">[1] Hou, Jie, Tianqi Wu, Renzhi Cao, and Jianlin Cheng. "Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13." bioRxiv (2019): 552422.</text></b><br>
				<b><text style="font-size: 1.2em;">[2] Li J, Deng X, Eickholt J, Cheng J: Li J, Deng X, Eickholt J, Cheng J: Designing and Benchmarking the MULTICOM Protein Structure Prediction System. BMC Structural Biology 2013, 13(1):2.</text></b><br>
				<b><text style="font-size: 1.2em;">[3] Cheng J, Li J, Wang Z, Eickholt J, Deng X: The MULTICOM toolbox for protein structure prediction. BMC bioinformatics 2012, 13(1):65.</text></b><br>
				<b><text style="font-size: 1.2em;">[4] Wang Z, Eickholt J, Cheng J: MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics 2010, 26(7):882-888.</text></b><br>

				</div>
				<div class="footer">
				<div align="center">
				<p align="center" style="text-align:center"><a href="http://people.cs.missouri.edu/~chengji/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a><a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
				<p align="center">&nbsp;</p>
				</div>
				</div>
			</body>
		</html>
	<?php	
		}
		else
		{
	/* When the job is queued*/
	?>
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<title>MULTICOM: Protein Tertiary Structure Modeling by Deep Learning</title>
			<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
			<link rel="stylesheet" type="text/css" href="./css/mirna_base.css" media="all"/>
			<link rel="stylesheet" type="text/css" href="./css/mirna_entry.css" media="all"/>
			<meta name="keywords" content="" />
			<meta name="description" content="" />
			<link href="status.css" rel="stylesheet" type="text/css" />
			<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
			<script type="text/javascript" src="sms2/scripts/sms_common.js"></script>
			<script type="text/javascript" src="sms2/scripts/color_align_prop.js"></script>
			<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
			<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
			<link rel="stylesheet" href="style/style.css">
			<link rel="Shortcut Icon" href="http://www.missouri.edu/favicon.ico" type="image/x-icon" />
			</head>

		<body>
		   <!--	 <div id="header"> -->
			   <!--	 <div id="logo">
				<div > -->
					<!--	  <h1><a style="margin-left: 15%" href="./">Deep<sup style='text-transform: lowercase'>SF</sup></a></h1> -->
					<!---<h1><a style="margin-left: 35%" href="./">Deep<sup>SF</sup></a></h1>
						<a style="margin-left: 35%">Deep Convolutional neural network for large-scale mapping protein sequence space to fold space</a>
					
					<h4 >
					</h4>
					<div style="width: 100%; height: 100%; float:left;"><a href="./"><img style="width: 100%; height: 100%; margin: 0 auto;text-align: center;" alt="MULTICOM" src="./style/multicom_header2.png" /></a></div>
				</div> <!-- end of #logo -->
				<table width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
				  <tr>
					<td bgcolor="#C9E4FC">&nbsp;</td>
					<td bgcolor="#BCDEFA">&nbsp;</td>
					<td bgcolor="#9BCEF9">&nbsp;</td>
					<td bgcolor="#7EC0F5">&nbsp;</td>
					<td bgcolor="#61B1F3">&nbsp;</td>
					<td bgcolor="#4BA7F1">&nbsp;</td>
					<td bgcolor="#339BF0">&nbsp;</td>
					<td bgcolor="#2896F0">&nbsp;</td>
					<td bgcolor="#1187E8">&nbsp;</td>
					<td bgcolor="#0F78CE">&nbsp;</td>
					<td bgcolor="#0F70BF">&nbsp;</td>
					<td bgcolor="#0C5A9A">&nbsp;</td>
					<td bgcolor="#0C5694">&nbsp;</td>
					<td bgcolor="#0A477A">&nbsp;</td>
					<td bgcolor="#07355A">&nbsp;</td>
				  </tr>
				</table>
				<table   width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
				  <tr>
					<td bgcolor="#FFFFFF" width="240" rowspan="2"><img src="images/3.png" width="200" height="120" /></td>
					<td bgcolor="#FFFFFF" width="100%" height="100"><div align="center"><img src="images/MULTICOM.jpg" width="420" height="60" align="middle" /></div></td>
					<td bgcolor="#FFFFFF" width="240" rowspan="2"><div align="center"><img src="images/2.jpg" width="180" height="140" align="middle" /></div></td>
				  </tr>
				  <tr>
					<td bgcolor="#FFFFFF" width="100%"><div align="center"><img src="images/protein.jpg" width="330" height="26" align="top" /></div></td>
				  </tr>
				  
				</table>
				<table  width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#F0F0F0">
				  <tr>
					<td bgcolor="#FFFFFF" width="100%"><div align="center"><p align="center"><img src="images/line.jpg" width="100%" height="10" align="middle"/></p></div></td>
				  </tr>
				  
				</table>
				

			<p id="jobname" style="display:none;" hidden><?php echo $job_name?></p>
			<p id="jobid" style="display:none;" hidden><?php echo $job_id?></p>
			<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
			<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
			<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
								 
			<div id="page">
				<div id="navBarDiv">
					<ul id="navbar">
					<li>
						<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/index.html">Home</a>
					</li>
					<li>
						<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/contact.html">Contact</a>
					</li>
					<li>
						<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
					</li>
					<li>
						<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15505775833645&job_name=T1022s1&method=multicom&domain_class=full_length">Result Example (Multi-domain)</a>
					</li>
					<li>
						<a href="http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/status.php?job_id=15506444111896&job_name=T0993s2&method=multicom&domain_class=full_length">Result Example (TBM)</a>
					</li>
					</ul>
				</div>		
					<div id="content_success">
						<div class="post_success">
							   <p class="title"> JOB STATUS : QUEUED</p>
							   <p style="text-align:center">
							   <img src='images/loading.gif' height=100px width=100px/>
							   </p>
							   <!--<p class='subtitle'>This page will be automatically refreshed every 10 seconds</p>-->
							   <!--<p class="text-steps">Your input file has been uploaded into MULTICOM server and your job is currently in QUEUE. This page will be automatically updated to show you the job status. You will be redirected to the results page once your job is finished.</p>-->
							    <p class="title">Your job is being queued by MULTICOM server. Results will be emailed once your job is finished.</p>
						</div>
					</div>  <!-- end #content -->
					<div style="clear: both;">&nbsp;</div>
				</div>  <!-- end #page -->
			<div class="headedBox" >
			<h1><b>References</b> </h1>
			<b><text style="font-size: 1.2em;">[1] Hou, Jie, Tianqi Wu, Renzhi Cao, and Jianlin Cheng. "Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13." bioRxiv (2019): 552422.</text></b><br>
			<b><text style="font-size: 1.2em;">[2] Li J, Deng X, Eickholt J, Cheng J: Li J, Deng X, Eickholt J, Cheng J: Designing and Benchmarking the MULTICOM Protein Structure Prediction System. BMC Structural Biology 2013, 13(1):2.</text></b><br>
			<b><text style="font-size: 1.2em;">[3] Cheng J, Li J, Wang Z, Eickholt J, Deng X: The MULTICOM toolbox for protein structure prediction. BMC bioinformatics 2012, 13(1):65.</text></b><br>
			<b><text style="font-size: 1.2em;">[4] Wang Z, Eickholt J, Cheng J: MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics 2010, 26(7):882-888.</text></b><br>

			</div>
			<div class="footer">
			<div align="center">
			<p align="center" style="text-align:center"><a href="http://people.cs.missouri.edu/~chengji/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a><a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
			<p align="center">&nbsp;</p>
			</div>
			</div>

			</body>
		</html>
	<?php	
		}
	}
}
?>
