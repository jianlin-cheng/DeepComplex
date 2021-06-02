<?php
#http://tulip.rnet.missouri.edu/deepcomplex/
#http://tulip.rnet.missouri.edu/deepcomplex/status.php?method=multicom&target_name=A0A0F6AZ77&domain_class=full_length
#http://tulip.rnet.missouri.edu/multicom_cluster/status.php?method=multicom&target_name=A0A0F6AZ77&domain_class=full_length
#http://tulip.rnet.missouri.edu/multicom_cluster/status.php?method=multicom&job_id=15451457358921&job_name=C0022&protein_id=C0022&domain_class=full_length
#http://tulip.rnet.missouri.edu/multicom_cluster/status.php?method=multicom&job_id=15451457358921&job_name=C0022&domain_class=full_length
#$job_id = $_REQUEST["job_id"];
#$job_name = $_REQUEST["job_name"];

$target_name = $_REQUEST["target_name"];
#$protein_id = $_REQUEST["protein_id"];
$pred_dir = $_REQUEST["domain_class"]; # full_length, domain1, domain2,...
$method_id = $_REQUEST["method"]; # multicom

if($method_id == 'multicom')
{
	$method_id='';
}else{
	$method_id='';
}

$full_length_seq = '';

if ($file = fopen("/var/www/html/deepcomplex/work_dimer/$target_name/$target_name.fasta", "r")) {
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
$done_file = "/var/www/html/deepcomplex/work_dimer/$target_name/.done";
$exec_file = "/var/www/html/deepcomplex/work_dimer/$target_name/.exec";
$queue_file = "/var/www/html/deepcomplex/work_dimer/$target_name/.queue";
$error_file = "/var/www/html/deepcomplex/work_dimer/$target_name/.error";


$$protein_template_dash = "/var/www/html/deepcomplex/work_dimer/$target_name/$pred_dir/full_length.dash.csv";
$protein_fasta_file = "/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.fasta";
$protein_ss_file = "/var/www/html/deepcomplex/work_dimer/$target_name/ss_sa/$protein_id.ss_sa";
$protein_disorder_file = "/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.fasta.disorder";
$protein_domain_list = "/var/www/html/deepcomplex/work_dimer/$target_name/domain_info";

$contact_stats_file="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.dncon2.rr.stats";
$contact_long_acc1_file="/var/www/html/deepcomplex/work_dimer/$target_name/long_Acc_formated.txt";
$contact_long_acc2_file="/var/www/html/deepcomplex/work_dimer/$target_name/long_Acc_formated.txt";
$contact_long_acc3_file="/var/www/html/deepcomplex/work_dimer/$target_name/long_Acc_formated.txt";
$contact_long_acc4_file="/var/www/html/deepcomplex/work_dimer/$target_name/long_Acc_formated.txt";
$contact_long_acc5_file="/var/www/html/deepcomplex/work_dimer/$target_name/long_Acc_formated.txt";

$avetm_model1_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id"."_GD.pdb";

$avetm_model2_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp2.avetm";
$avetm_model3_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp3.avetm";
$avetm_model4_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp4.avetm";
$avetm_model5_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp5.avetm";

$rank_model1_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id"."_GD.pdb";
$rank_model2_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp2.rank";
$rank_model3_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp3.rank";
$rank_model4_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp4.rank";
$rank_model5_file ="/var/www/html/deepcomplex/work_dimer/$target_name/$protein_id.casp5.rank";

$Rg_file ="/var/www/html/deepcomplex/work_dimer/$target_name/Rg.txt";

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
		<script>
		  window.dataLayer = window.dataLayer || [];
		  function gtag(){dataLayer.push(arguments);}
		  gtag('js', new Date());

		  gtag('config', 'UA-96943265-4');
		</script>
			<style>
			@media print  
			{
			a[href]:after {
			content: none !important;
			 }
			@page {
			margin-top: 0;
			margin-bottom: 0;
			}
			 body{
			padding-top: 72px;
			padding-bottom: 72px ;
			}
			}
			</style>

		<title>DeepComplex: Protein Quaternary Structure Modeling by Deep Learning</title>
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

	<body style="background-color:#000000;">
	   <!--	 <div id="header"> -->

			<table style="background-color:#000000;" width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#000000">
			  <tr>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
				<td bgcolor="#000000">&nbsp;</td>
			  </tr>
			</table>
			<table  style="background-color:#000000;" width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#000000">
			  <tr>
				<td bgcolor="#000000" width="240" rowspan="2"><img src="images/3.png" width="350" height="280" /></td>
				<td bgcolor="#000000" width="100%" height="100"><div align="center"><img src="images/DeepComplex_Logo_2.png" width="420" height="300" align="middle" /></div></td>
				<td bgcolor="#000000" width="240" rowspan="2"><div align="center"><img src="images/1a3n_screenshot.png" width="420" height="280" align="middle" /></div></td>
			  </tr>
			  <tr>
				<td bgcolor="#000000" width="100%"><div align="center"><img src="images/protein2.png" width="400" height="40" align="top" /></div></td>
			  </tr>
			  
			</table>contact_long_acc1_file
			<table  style="background-color:#000000;"width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#000000">
			  <tr>
				<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
			  </tr>

<table  style="background-color:black;" width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#000000">
  <tr>
	<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
  </tr>			  
			</table>
			

		<p id="targetname" style="display:none;" hidden><?php echo $target_name?></p>
		<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
		<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
		<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
							 
		<div style="background-color:black;" id="page" bordercolor="#000000">
			<div style="background-color:black;" id="navBarDiv" align="center" bordercolor="#000000">
				<ul id="navbar" style="background-color:black;">
				<li>
					<a href="http://tulip.rnet.missouri.edu/deepcomplex/chlamdimer_dimer_index.html">Home</a>
				</li>
				<li>
					<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
				</li>
				<li>
					<a href="http://tulip.rnet.missouri.edu/deepcomplex/dimer_status.php?target_name=FDX1&method=multicom&domain_class=full_length">Result Example</a>
				</li>
				</ul>
			</div>				
            <div id="content_success">
                <div class="post_success">
					   <p class="title"> JOB STATUS : FAILED</p>
					   <p style="text-align:center"> 
					   <img src='images/error.png' height=50px width=50px/>
					   </p>
					   <p class="title" style="text-align:center">Your job has failed during execution. Please consider resubmitting yor job with the correct input. Please note that DeepComplex accepts only 20 standard amino acids in the input pdb file. Please avoid any non-standard amino acids in your initial structures. Alternatively, contact us for help.</p>
					   
                </div>
            </div>  <!-- end #content -->
            <div style="clear: both;">&nbsp;</div>
        </div>  <!-- end #page -->
		<div class="headedBox" >
		<h1><b>References</b> </h1>
		<p align="left"><text style="font-size: 1.5em;color:grey">[1] Quadir, F., Roy, R., Halfmann, R., & Cheng, J. (2021). DNCON2_Inter: Predicting interchain contacts for homodimeric and homomultimeric protein complexes using multiple sequence alignments of monomers and deep learning. Scientific Reports, under review. (https://doi.org/10.21203/rs.3.rs-228041/v1) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[2] Hou, J., Wu, T., Guo, Z., Quadir, F. & Cheng, J. The MULTICOM Protein Structure Prediction Server Empowered by Deep Learning and Contact Distance Prediction. in Methods in Molecular Biology vol. 2165 13–26 (Humana Press Inc., 2020) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[3] Hou, J., Wu, T., Cao, R., & Cheng, J. (2019). Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13. Proteins, accepted. (https://doi.org/10.1002/prot.25697)</text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[4] Li, J., Deng, X., Eickholt, J., & Cheng, J. (2013). Designing and benchmarking the MULTICOM protein structure prediction system. BMC structural biology, 13(1), 2.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[5] Cheng, J., Li, J., Wang, Z., Eickholt, J., & Deng, X. (2012). The MULTICOM toolbox for protein structure prediction. BMC bioinformatics, 13(1), 65.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[6] Wang, Z., Eickholt, J., & Cheng, J. (2010). MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics, 26(7), 882-888.</text></p>
		</div>
		<div class="footer">
		<div align="center">
		<p align="center" style="text-align:center"><a href="http://people.cs.missouri.edu/~chengji/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a>, <a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
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
		<script>
		  window.dataLayer = window.dataLayer || [];
		  function gtag(){dataLayer.push(arguments);}
		  gtag('js', new Date());

		  gtag('config', 'UA-96943265-4');
		</script>
		<title>DeepComplex: Protein Quaternary Structure Modeling by Deep Learning</title>
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
				height: 350,
				serverURL: "http://chemapps.stolaf.edu/jmol/jsmol/jsmol.php ",
				use: "HTML5",
				j2sPath: "js/j2s"
			}
			


		</script>
			<style>
			@media print  
			{
			a[href]:after {
			content: none !important;
			 }
			@page {
			margin-top: 0;
			margin-bottom: 0;
			}
			 body{
			padding-top: 72px;
			padding-bottom: 72px ;
			}
			}
			</style>

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

		<table width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#000000">
		  <tr>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
			<td bgcolor="#000000">&nbsp;</td>
		  </tr>
		</table>
		<table style="background-color:black;" width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#000000">
		  <tr>
			<td bgcolor="#000000" width="240" rowspan="2"><img src="images/3.png" width="200" height="120" /></td>
			<td bgcolor="#000000" width="100%" height="100"><div align="center"><img src="images/DeepComplex_Logo_2.png" width="420" height="60" align="middle" /></div></td>
			<td bgcolor="#000000" width="240" rowspan="2"><div align="center"><img src="images/1a3n_screenshot.png" width="180" height="140" align="middle" /></div></td>
		  </tr>
		  <tr>
			<td bgcolor="#000000" width="100%"><div align="center"><img src="images/protein2.png" width="330" height="26" align="top" /></div></td>
		  </tr>
		  
		</table>
		<table style="background-color:black;" width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#000000">
		  <tr>
			<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
		  </tr>
		  
		</table>

		<p id="targetname" style="display:none;" hidden><?php echo $target_name?></p>
		<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
		<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
		<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
		<p id="p_id" style="display:none;" hidden><?php echo $protein_id?></p>

		<div id="navBarDiv" align="center" style="background-color:black;">
			<ul id="navbar" style="background-color:black;">
				<li>
					<a href="http://tulip.rnet.missouri.edu/deepcomplex/chlamdimer_index.html">Home</a>
				</li>
				<li>
					<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
				</li>
				<li>
					<a href="http://tulip.rnet.missouri.edu/deepcomplex/dimer_status.php?target_name=T1022s1&method=multicom&domain_class=full_length">Result Example</a>
				</li>
				
			</ul>
  <tr>
	<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
  </tr>			  

		</div>


		<div style="background-color:#000000;" id="mainSection">
		<div align="center">
		<p class="title"><b>Results of Complex Structure Prediction for Target Name: <?php echo $target_name?> (<u> <a style="color: #154360;" href = "./work_dimer/<?php echo "${target_name}"?>/multicom_results.tar.gz">Click <img src='images/download.png' height=20px width=20px/></a></u>)</b></p>
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
				<div id="rightColumn">
				
		<?php
			if(file_exists("./work_dimer/${target_name}/$protein_id.domain_info.marker.jpeg"))
			{
		?>
				<div class="headedBox">
				<h1><b> Domain Boundary prediction </b> (<u> <a href = "./work_dimer/<?php echo "${target_name}/$protein_id.domain_info.marker.jpeg"?>" style="font-weight: bold;color: #EEE;"> View <img src='images/download.png' height=20px width=20px/></a></u>)</h1>
				<img width="100%" height="100%" alt="./work_dimer/<?php echo "${target_name}/$protein_id.domain_info.marker.jpeg"?>" src="./work_dimer/<?php echo "${target_name}/$protein_id.domain_info.marker.jpeg"?>" />
				</div> 
		<?php
			}
		?>
				</div>  <!-- rightColumn -->
		<div class="headedBox" style="width:70%;overflow-wrap: break-word;word-wrap: break-word;">
		<h1><b><u> <a href = "./work_dimer/<?php echo "$target_name/$protein_id.fasta"?>" style="font-weight: bold;color: #EEE;">Protein sequence</a></u></b></h1>
		<table cellspacing="4" style="width: 100%;height: 100px;font-size: 15px;font-weight: bold;table-layout: fixed;">
		<!--<textarea  readonly="readonly" id="protein_sequence" style="width: 100%;height: 100px;font-size: 15px;font-weight: bold;">
		-->
		
		<?php
			$body = "";
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
							$body .= "<b style=\"font-size: 16px;color:grey;\">$line: $pos_start-$pos_end</b>\n"; 
							
						}else{
							$pieces = str_split($line);
							$body .= "<tr><td style=\"color:grey;\" width=\"80px\">1-60: </td>\n"; 
							for($x = 0; $x < strlen($line); $x++)
							{
								if($x % 60==0 and $x > 0)
								{
									$line_start = $x+1;
									$line_end = $x+60-1;
									if($line_end>strlen($line))
									{
										$line_end = strlen($line);
									}contact_long_acc1_file
									$body .= "\n</tr><tr><td style=\"color:grey;\"  width=\"80px\">$line_start-$line_end: </td>\n";
								}
								
								$body .= "<td style=\"color:grey;\">$pieces[$x]</td>"; 
							}
							$body .= "</tr>\n"; 
							
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
			echo $body;

		?>
		</table>
		<!--</textarea>--><br>
		</div>

		<div class="headedBox" style="width:70%">
		<h1><b><u> <a href = "./work_dimer/<?php echo "$target_name/ss_sa/$protein_id.ss_sa"?>" style="font-weight: bold;color: #EEE;">Secondary structure prediction (H: Helix   E: Strand   C: Coil)</a></u></b></h1>
		<!--<h1><b> Secondary structure prediction  <u>(H: Helix   E: Strand   C: Coil)</u> </b></h1>-->
		<table cellspacing="4" style="width: 100%;height: 100px;font-size: 15px;font-weight: bold;table-layout: fixed;">
		<!--<textarea  readonly="readonly"  id="protein_ss_sa" style="width: 100%;height: 70px;font-size: 15px;font-weight: bold;">-->
		<?php
			$body = "";
			$ss = "";
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
							$ss .= $line;
							$pieces = str_split($line);
							$body .= "<tr><td style=\"color:grey;\" width=\"80px\">1-60: </td>\n"; 
							for($x = 0; $x < strlen($line); $x++)
							{
								if($x % 60==0 and $x > 0)
								{
									$line_start = $x+1;
									$line_end = $x+60-1;
									if($line_end>strlen($line))
									{
										$line_end = strlen($line);
									}
									$body .= "\n</tr><tr><td style=\"color:grey;\" width=\"80px\">$line_start-$line_end: </td>\n";
								}
								
								$body .= "<td style=\"color:grey;\">".strtoupper($pieces[$x])."</td>"; 
							}
							$body .= "</tr>\n"; 
							#echo strtoupper($line)."\n";
						}
					}
				}
				fclose($file);
				$body .= "<td>  </td>";
			}
			echo $body;

		?>
		</table>
		<table cellspacing="4" style="width: 60%;height: 20px;font-size: 15px;font-weight: bold;table-layout: fixed;">
		<!--<textarea  readonly="readonly"  id="protein_ss_sa" style="width: 100%;height: 70px;font-size: 15px;font-weight: bold;">-->
		<?php
			$body = "";
			$ss = "";
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
							$ss .= $line;
						}
					}
				}
				fclose($file);
				$H_count = substr_count($ss, 'H');
				$H_percent = round(100 * $H_count/strlen($ss),2);
				$E_count = substr_count($ss, 'E');
				$E_percent = round(100 * $E_count/strlen($ss),2);
				$C_count = substr_count($ss, 'C');
				$C_percent = round(100 * $C_count/strlen($ss),2);
				$body .= "<td> </td>";
				$body .= "<td style=\"color:grey;\">H(Helix): ".$H_count."(".$H_percent."%)</td>";
				$body .= "<td style=\"color:grey;\">E(Strand): ".$E_count."(".$E_percent."%)</td>";
				$body .= "<td style=\"color:grey;\">C(Coil): ".$C_count."(".$C_percent."%)</td>";
			}
			echo $body;

		?>
		</table>
		
		<!--</textarea>--><br>
		</div>

<!--->
		<div class="headedBox" style="width:70%">
		<h1><b><u> <a href = "./work_dimer/<?php echo "$target_name/$pred_dir/$protein_id.ss_sa"?>" style="font-weight: bold;color: #EEE;">Solvent accessibility prediction (e: Exposed   b: Buried)</a></u></b></h1>
		<!--<h1><b> Solvent accessibility prediction <u>(e: Exposed   b: Buried)</u>  </b></h1>-->
		
		<table cellspacing="4" style="width: 100%;height: 100px;font-size: 15px;font-weight: bold;table-layout: fixed;">
		<!--<textarea  readonly="readonly" id="protein_ss_sa" style="width: 100%;height: 70px;font-size: 15px;font-weight: bold;">-->
		<?php
			$body = "";
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
							$pieces = str_split($line);
							$body .= "<tr><td style=\"color:grey;\" width=\"80px\">1-60: </td>\n"; 
							for($x = 0; $x < strlen($line); $x++)
							{
								if($x % 60==0 and $x > 0)
								{
									$line_start = $x+1;
									$line_end = $x+60-1;
									if($line_end>strlen($line))
									{
										$line_end = strlen($line);
									}
									$body .= "\n</tr><tr><td style=\"color:grey;\" width=\"80px\">$line_start-$line_end: </td>\n";
								}
								
								$body .= "<td style=\"color:grey;\">".strtoupper($pieces[$x])."</td>"; 
							}
							$body .= "</tr>\n"; 
							#echo strtoupper($line)."\n";
						}
					}
				}
				fclose($file);
				$body .= "<td>  </td>";
			}
			echo $body;

		?>
		</table>

		<table cellspacing="4" style="width: 60%;height: 20px;font-size: 15px;font-weight: bold;table-layout: fixed;">
		<!--<textarea  readonly="readonly"  id="protein_ss_sa" style="width: 100%;height: 70px;font-size: 15px;font-weight: bold;">-->
		<?php
			$body = "";
			$ss = "";
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
							$ss .= $line;
						}
					}
				}
				fclose($file);
				$e_count = substr_count($ss, 'e');
				$e_percent = round(100 * $e_count/strlen($ss),2);
				$b_count = substr_count($ss, 'b');
				$b_percent = round(100 * $b_count/strlen($ss),2);
				$body .= "<td> </td>";
				$body .= "<td style=\"color:grey;\">e(Exposed): ".$e_count."(".$e_percent."%)</td>";
				$body .= "<td style=\"color:grey;\">b(Buried): ".$b_count."(".$b_percent."%)</td>";
			}
			echo $body;

		?>
		</table>

		<!--</textarea>--><br>
		</div>
		<?php
			if(file_exists($protein_disorder_file))
			{
		?>
		<div class="headedBox" style="width:70%">
		<h1><b><u> <a href = "./work_dimer/<?php echo "$target_name/$protein_id.fasta.disorder"?>" style="font-weight: bold;color: #EEE;">Disorder prediction (N: Normal   T: Disorder)</a></u></b></h1>
		<!--<h1><b> Disorder prediction <u>(N: Normal   T: Disorder)</u> </b></h1>-->
		<table cellspacing="4" style="width: 100%;height: 100px;font-size: 15px;font-weight: bold;table-layout: fixed;">

		<!--<textarea  readonly="readonly" id="protein_disorder" style="width: 100%;height: 70px;font-size: 15px;font-weight: bold;">-->
		<?php
			$body = "";
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
							$pieces = str_split($line);
							$body .= "<tr><td width=\"80px\">1-60: </td>\n"; 
							for($x = 0; $x < strlen($line); $x++)
							{
								if($x % 60==0 and $x > 0)
								{
									$line_start = $x+1;
									$line_end = $x+60-1;
									if($line_end>strlen($line))
									{
										$line_end = strlen($line);
									}
									$body .= "\n</tr><tr><td width=\"80px\">$line_start-$line_end: </td>\n";
								}
								
								$body .= "<td>$pieces[$x]</td>"; 
							}
							$body .= "</tr>\n"; 
						}
						
					}
				}
				$body .= "<td>  </td>";
				echo $body;
				fclose($file);
			}

		?>
		</table>

		<table cellspacing="4" style="width: 60%;height: 20px;font-size: 15px;font-weight: bold;table-layout: fixed;">
		<!--<textarea  readonly="readonly"  id="protein_ss_sa" style="width: 100%;height: 70px;font-size: 15px;font-weight: bold;">-->
		<?php
			$body = "";
			$disorder = "";
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
							$disorder .= $line;
						}
					}
				}
				fclose($file);
				$T_count = substr_count($disorder, 'T');
				$T_percent = round(100 * $T_count/strlen($disorder),2);
				$N_count = substr_count($disorder, 'N');
				$N_percent = round(100 * $N_count/strlen($disorder),2);
				$body .= "<td> </td>";
				$body .= "<td>N(Normal): ".$N_count."(".$N_percent."%)</td>";
				$body .= "<td>T(Disorder): ".$T_count."(".$T_percent."%)</td>";
			}
			echo $body;

		?>
		</table>

		<!--</textarea>--><br>

		</div>
		<?php
			}
		?>
<!---  --->


<!--- --->

<!--- --->


<!--- --->

		<div style="background-color:black;" class="headedBox">
		<h1><b>Predicted Top 1 Tertiary structure </b> </h1>
		<div align="left">
		&nbsp;&nbsp;&nbsp;

		<table style="background-color:black;" cellspacing="60" bgcolor="#000000" style="background-color:#000000;">
		<tr>
		<td align="left">
		<div class="carousel-inner" style="height:500px; margin-left: 0%;">
		<p class="title" style="font-size:22px;color:#154360"> <a style="font-size:22px;color:#154360" href = "./work_dimer/<?php echo "${target_name}/$protein_id"."_GD.pdb"?>"><u><b>Predicted Model 1</b></u> <img src='images/download.png' height=20px width=20px/> </a>
		<?php
		if(file_exists("./work_dimer/${target_name}/$protein_id.deep1.deeprank"))
		{
			if(file_exists("./work_dimer/${target_name}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
			}else
			{
				$c = 0;
				if ($file = fopen("./work_dimer/${target_name}/$protein_id.deep1.deeprank", "r")) {
					while(!feof($file)) {
						$line = trim(fgets($file));
						# do same stuff with the $line
						if($line  !="")
						{
							
							echo "<br><text class=\"title\" style=\"font-size:18px;color:#154360;\"><b>($line)<b></text>"; 
							$c +=1;
						}
					}
					fclose($file);
				}
			}
		}
		?>
		</p>
		<br>

		<script type="text/javascript">
			var target = $("#targetname").text();
			var protein_id = $("#protein_id").text();
			var methodName = $("#methodName").text();
			var pred_dir = $("#pred_dir").text();
			var rfile = 1;
			var model = 1;
			//var append = "APPEND";
			var append = "";
			var modelfile = "work_dimer/" + target+'/'+protein_id+"_GD.pdb";
			Jmol.getApplet("jsmolApplet_M23d1", Info);
			Jmol.script(jsmolApplet_M23d1,"background black; load work_dimer/" + target+"/"+protein_id+ "_GD.pdb;");
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
					<p class="title" style="font-size:22px;color:#154360;text-align:left;"><a style="font-size:22px;color:#154360;text-align:left;" href = "./work_dimer/<?php echo "${target_name}/$protein_id.png"?>"><u><b> Model 1 vs Contact (Top L/10)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<?php
					if(file_exists("./work_dimer/${target_name}/$protein_id.png"))
					{
					?>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" src="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" />
					</div>	
					<?php
					}else
					{
					?>
					<div style="width: 350px; height: 350px;">
							<text style="font-weight:bold;font-size:1.5em;"><u>Note: No long-range contacts in the model!</u></text>
					</div>	
					<?php
					}
					?>	
				
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work/<?php echo "${target_name}/$protein_id.png"?>"><u><b> Model 1 vs Contact (Top L/5)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" src="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" />
					</div>

					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;">  <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work_dimer/<?php echo "${target_name}/$protein_id.png"?>"><u><b> Model 1 vs Contact (Top L)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" src="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" />
					</div>	
					
				</div>
				
				
				<div class='carousel item'>	

					<p class="title" style="font-size:22px;color:#154360;text-align:left;"> <a style="font-size:22px;color:#154360;text-align:left;"  href = "./work_dimer/<?php echo "${target_name}/$protein_id.png"?>"><u><b> Model 1 vs Contact (Top 10)</b></u> <img src='images/download.png' height=20px width=20px/> </a></p>
					<div style="width: 350px; height: 350px;">
						<img style="width: 350px; height: 350px;" alt="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" src="./work_dimer/<?php echo "${target_name}/$protein_id.png"?>" />
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
		<h3 style="text-align: center;color:#154360"> <u><b>Predicted Contact Accuracy</u><br> <a style="text-align: center;color:#154360" href = "./work_dimer/<?php echo "${target_name}/$protein_id.rr"?>"> ( <u>Contact file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		<div align="center"> 
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;font-weight:bold;">
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
		  <h3 style="text-align: center;color:#154360"> <b><a style="text-align: center;color:#154360" href = "./work_dimer/<?php echo "${target_name}/$protein_id.aln"?>"> ( <u>Alignment file <img src='images/download.png' height=20px width=20px/></u> )</a></b></h3>  
		  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;font-weight:bold;">
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

		<td>


		<td style="padding: 0px 0px 0px 50px;">
		<div class="carousel-inner" style="width:400px;height:500px; margin-left: 0%;">
			<?php
			if(file_exists("./work_dimer/${target_name}/domain0/domain0.fasta") and ${pred_dir}=='full_length')
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:1.5em;\"><u>Note: This is multi-domain structure, check alignments and domain qualities in individual domains!</u></text>"; 

			}else if(!file_exists("./work_dimer/${target_name}/alignments/$protein_id.casp1.msa"))
			{
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<p>&nbsp;&nbsp;&nbsp;</p>";
					echo "<text style=\"font-weight:bold;font-size:1.5em;\"><u>Note: The model is built by ab initio method, no significant templates are found!</u></text>"; 

				
			}else{
			?>	
				<div class="carousel-inner" style="width:600px;height:500px; margin-left: 0%;">
				<h3 align="center" style="align:center;text-align: left;color:#154360;"> 
				<form action="" name="main_form" id="main_form_3d_1">
				<textarea rows="6" cols="61" style="display:none;">
			<?php
				$c = 0;
				if ($file = fopen("./work_dimer/${target_name}/alignments/$protein_id.a3m", "r")) {
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
				<input type="button" value="View multiple sequence alignment" name="main_submit" onclick="try{colorAlignProp(document,'main_form_3d_1')} catch(e) {alert('The following error was encountered: ' + e);}" /> <input type="button" value="Clear" onclick="document.forms[0].elements[0].value = ' '" style='display:none;' /> <input type="reset" value="Reset" / style='display:none;'>

				<select  style='display:none;'><option selected="selected" value="80">80</option></select> 
				<select  style='display:none;'><option selected="selected" value="100">100</option></select>
				<select  style='display:none;'><option selected="selected" value="background">backgrounds</option><option value="text">text</option></select> 
				<textarea rows="2" cols="61"  style='display:none;'></textarea>
				</form>
				<br>
				<!--<b><a style="align:center;text-align: center;color:#154360" href = "./work/<?php echo "${method_id}-${target_name}/${pred_dir}/Top5_aln/$protein_id.casp1.msa.marker.jpeg"?>"> ( <u>Click <img src='images/download.png' height=20px width=20px/></u> )</a></b>-->
				<b>(<a style="align:center;text-align: center;color:#154360" href = "./work_dimer/<?php echo "${target_name}/$protein_id.casp1.msa.marker.jpeg"?>">  <u>Image <img src='images/download.png' height=20px width=20px/></u></a><a style="align:center;text-align: center;color:#154360" href = "./work_dimer/<?php echo "${target_name}/alignments/$protein_id.a3m"?>">  <u>Alignment <img src='images/download.png' height=20px width=20px/></u></a>)</b>
				</h3>
				<img align="left" style="width: 80%; height: 50%; margin: 0 0 0 -50px;text-align: left;" alt="template_alignment" src=<?php echo "./work_dimer/${target_name}/alignments/Top5_aln/$protein_id.casp1.msa.marker.jpeg"?> />
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
<!--- --->




		</div> 
<!-- mainSection -->

		<div style="background-color:black;" class="headedBox" >
		<h1><b>References</b> </h1>
      <p align="left"><text style="font-size: 1.5em;color:grey">[1] Quadir, F., Roy, R., Halfmann, R., & Cheng, J. (2021). DNCON2_Inter: Predicting interchain contacts for homodimeric and homomultimeric protein complexes using multiple sequence alignments of monomers and deep learning. Scientific Reports, under review. (https://doi.org/10.21203/rs.3.rs-228041/v1) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[2] Hou, J., Wu, T., Guo, Z., Quadir, F. & Cheng, J. The MULTICOM Protein Structure Prediction Server Empowered by Deep Learning and Contact Distance Prediction. in Methods in Molecular Biology vol. 2165 13–26 (Humana Press Inc., 2020) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[3] Hou, J., Wu, T., Cao, R., & Cheng, J. (2019). Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13. Proteins, accepted. (https://doi.org/10.1002/prot.25697)</text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[4] Li, J., Deng, X., Eickholt, J., & Cheng, J. (2013). Designing and benchmarking the MULTICOM protein structure prediction system. BMC structural biology, 13(1), 2.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[5] Cheng, J., Li, J., Wang, Z., Eickholt, J., & Deng, X. (2012). The MULTICOM toolbox for protein structure prediction. BMC bioinformatics, 13(1), 65.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[6] Wang, Z., Eickholt, J., & Cheng, J. (2010). MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics, 26(7), 882-888.</text></p>

		</div>
		<div class="footer">
		<div align="center">
		<p align="center" style="text-align:center"><a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a>, <a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
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
			<script>
			  window.dataLayer = window.dataLayer || [];
			  function gtag(){dataLayer.push(arguments);}
			  gtag('js', new Date());

			  gtag('config', 'UA-96943265-4');
			</script>
			<style>
			@media print  
			{
			a[href]:after {
			content: none !important;
			 }
			@page {
			margin-top: 0;
			margin-bottom: 0;
			}
			 body{
			padding-top: 72px;
			padding-bottom: 72px ;
			}
			}
			</style>

			<title>DeepComplex: Protein Quaternary Structure Modeling by Deep Learning</title>
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

			<body style="background-color:black;">

					<table style="background-color:black;" width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#000000">
					  <tr>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
						<td bgcolor="#000000">&nbsp;</td>
					  </tr>
					</table>
					<table   width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#000000">
					  <tr>
						<td bgcolor="#000000" width="240" rowspan="2"><img src="images/3.png" width="350" height="280" /></td>
						<td bgcolor="#000000" width="100%" height="100"><div align="center"><img src="images/DeepComplex_Logo_2.png" width="420" height="300" align="middle" /></div></td>
						<td bgcolor="#000000" width="240" rowspan="2"><div align="center"><img src="images/1a3n_screenshot.png" width="420" height="280" align="middle" /></div></td>
					  </tr>
					  <tr>
						<td bgcolor="#000000" width="100%"><div align="center"><img src="images/protein2.png" width="400" height="40" align="top" /></div></td>
					  </tr>
					  
					</table>
					<table  width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#000000">
					  <tr>
						<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
					  </tr>
					  
					</table>
					

				<p id="targetname" style="display:none;" hidden><?php echo $target_name?></p>	
				<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
				<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
				<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
									 
				<div id="page">
					<div id="navBarDiv" align="center">
						<ul id="navbar">
						<li>
							<a href="http://tulip.rnet.missouri.edu/deepcomplex/index.html">Home</a>
						</li>
						<li>
							<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
						</li>
						<li>
							<a href="http://tulip.rnet.missouri.edu/deepcomplex/status.php?target_name=T1022s1&method=multicom&domain_class=full_length">Result Example</a>
						</li>
						
						<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
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
							   <p class="title">Your job is being executed by DeepComplex server. Results will be emailed once your job is finished.</p>
						</div>
					</div>  <!-- end #content -->
					<div style="clear: both;">&nbsp;</div>
				</div>  <!-- end #page -->
				<div class="headedBox" >
				<h1><b>References</b> </h1>
		<p align="left"><text style="font-size: 1.5em;color:grey">[1] Quadir, F., Roy, R., Halfmann, R., & Cheng, J. (2021). DNCON2_Inter: Predicting interchain contacts for homodimeric and homomultimeric protein complexes using multiple sequence alignments of monomers and deep learning. Scientific Reports, under review. (https://doi.org/10.21203/rs.3.rs-228041/v1) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[2] Hou, J., Wu, T., Guo, Z., Quadir, F. & Cheng, J. The MULTICOM Protein Structure Prediction Server Empowered by Deep Learning and Contact Distance Prediction. in Methods in Molecular Biology vol. 2165 13–26 (Humana Press Inc., 2020) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[3] Hou, J., Wu, T., Cao, R., & Cheng, J. (2019). Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13. Proteins, accepted. (https://doi.org/10.1002/prot.25697)</text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[4] Li, J., Deng, X., Eickholt, J., & Cheng, J. (2013). Designing and benchmarking the MULTICOM protein structure prediction system. BMC structural biology, 13(1), 2.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[5] Cheng, J., Li, J., Wang, Z., Eickholt, J., & Deng, X. (2012). The MULTICOM toolbox for protein structure prediction. BMC bioinformatics, 13(1), 65.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[6] Wang, Z., Eickholt, J., & Cheng, J. (2010). MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics, 26(7), 882-888.</text></p>
				</div>
				<div class="footer">
				<div align="center">
				<p align="center" style="text-align:center"><a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a>, <a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
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
			<script>
			  window.dataLayer = window.dataLayer || [];
			  function gtag(){dataLayer.push(arguments);}
			  gtag('js', new Date());

			  gtag('config', 'UA-96943265-4');
			</script>
			<style>
			@media print  
			{
			a[href]:after {
			content: none !important;
			 }
			@page {
			margin-top: 0;
			margin-bottom: 0;
			}
			 body{
			padding-top: 72px;
			padding-bottom: 72px ;
			}
			}
			</style>
			<title>DeepComplex: Protein Quaternary Structure Modeling by Deep Learning</title>
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

		<body style="background-color:black;">
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
				<table style="background-color:black;" width="100%" height="40" border="0" align="center" cellspacing="0" bordercolor="#000000">
				  <tr>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
					<td bgcolor="#000000">&nbsp;</td>
				  </tr>
				</table>
				<table style="background-color:black;"  width="100%" height="140" border="0" align="center" cellspacing="0" bordercolor="#000000">
				  <tr>
					<td bgcolor="#000000" width="240" rowspan="2"><img src="images/3.png" width="350" height="280" /></td>
					<td bgcolor="#000000" width="100%" height="100"><div align="center"><img src="images/DeepComplex_Logo_2.png" width="420" height="300" align="middle" /></div></td>
					<td bgcolor="#000000" width="240" rowspan="2"><div align="center"><img src="images/1a3n_screenshot.png" width="420" height="280" align="middle" /></div></td>
				  </tr>
				  <tr>
					<td bgcolor="#000000" width="100%"><div align="center"><img src="images/protein2.png" width="400" height="40" align="top" /></div></td>
				  </tr>
				  
				</table>
				<table  width="100%" height="60" border="0" align="center" cellspacing="0" bordercolor="#000000">
				  <tr>
					<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
				  </tr>
				  
				</table>
				

			<p id="targetname" style="display:none;" hidden><?php echo $target_name?></p>	
			<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
			<p id="protein_id" style="display:none;" hidden><?php echo $protein_id?></p>
			<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
								 
			<div id="page">
				<div style="background-color:black;" id="navBarDiv" align="center" bordercolor="#000000">
					<ul id="navbar">
					<li>
						<a href="http://tulip.rnet.missouri.edu/deepcomplex/web_index.html">Home</a>
					</li>
					<li>
						<a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">BDM Lab</a>
					</li>
					<li>
						<a href="http://tulip.rnet.missouri.edu/deepcomplex/status.php?target_name=T1022s1&method=multicom&domain_class=full_length">Result Example </a>
					</li>
					</ul>
<tr>
	<td bgcolor="#000000" width="100%"><div align="center"><p align="center"><img src="images/line_.png" width="100%" height="10" align="middle"/></p></div></td>
  </tr>

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
		<p align="left"><text style="font-size: 1.5em;color:grey">[1] Quadir, F., Roy, R., Halfmann, R., & Cheng, J. (2021). DNCON2_Inter: Predicting interchain contacts for homodimeric and homomultimeric protein complexes using multiple sequence alignments of monomers and deep learning. Scientific Reports, under review. (https://doi.org/10.21203/rs.3.rs-228041/v1) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[2] Hou, J., Wu, T., Guo, Z., Quadir, F. & Cheng, J. The MULTICOM Protein Structure Prediction Server Empowered by Deep Learning and Contact Distance Prediction. in Methods in Molecular Biology vol. 2165 13–26 (Humana Press Inc., 2020) </text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[3] Hou, J., Wu, T., Cao, R., & Cheng, J. (2019). Protein tertiary structure modeling driven by deep learning and contact distance prediction in CASP13. Proteins, accepted. (https://doi.org/10.1002/prot.25697)</text> </p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[4] Li, J., Deng, X., Eickholt, J., & Cheng, J. (2013). Designing and benchmarking the MULTICOM protein structure prediction system. BMC structural biology, 13(1), 2.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[5] Cheng, J., Li, J., Wang, Z., Eickholt, J., & Deng, X. (2012). The MULTICOM toolbox for protein structure prediction. BMC bioinformatics, 13(1), 65.</text></p>
      <p align="left"><text style="font-size: 1.5em;color:grey">[6] Wang, Z., Eickholt, J., & Cheng, J. (2010). MULTICOM: a multi-level combination approach to protein structure prediction and its assessments in CASP8. Bioinformatics, 26(7), 882-888.</text></p>
			</div>
			<div class="footer">
			<div align="center">
			<p align="center" style="text-align:center"><a href="http://calla.rnet.missouri.edu/cheng/cheng_research.html">Dr. Jianlin Cheng's Bioinformatics, Data Mining, Machine Learning Laboratory (BDM) Laboratory</a>, <a href="http://www.cs.missouri.edu">Department of Computer Science</a>,  <a href="http://www.missouri.edu/">University of Missouri-Columbia</a></p>
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
