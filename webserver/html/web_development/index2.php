<?php
#http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/index2.php?method=multicom&job_id=15451457358921&job_name=Hbx
#MULTICOM.Hbx.15451457358921
$job_id = $_REQUEST["job_id"];  #15451457358921
$job_name = $_REQUEST["job_name"]; #Hbx

$method_id = $_REQUEST["method"]; # multicom
$pred_dir = 'full_length'; # multicom

if($method_id == 'multicom')
{
	$method_id='multicom';
}else{
	echo '<script language="javascript">';
  echo "alert(\"Couldn\'t find predictions from MULTICOM server $method_id, please provide correct link!\")";
  echo '</script>';

	$method_id='none';
}

?>

<!DOCTYPE html>
<html>
<head>
    <title>MULTICOM dashboard</title>
    <meta charset="UTF-8">
    
  <!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

<!-- Latest compiled JavaScript -->
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
</head>

<script type="text/javascript">
	function openPopup(updateid) {
		var popup = window.open("", "", "width=1000,height=480,resizeable,scrollbars");
		var align_path = document.getElementById(updateid).value;
		//alert(align_path);
		var client = new XMLHttpRequest();
		client.open('GET', align_path);
		jQuery.get(align_path, function(data) {
			//alert(data);
			
			var lines = data.split('\n');
			var tableContent = '<h2>Multiple sequence alignment Alignment</h2>';
			for(var line = 0; line < lines.length; line++){

				tableContent += lines[line]+"</br>\n";
			}
					
			
			 popup.document.write(tableContent);
			  popup.document.close();
			  if (window.focus) 
				popup.focus();
		});
	 
	}

</script>

<?php
	## save the commentstarget
	if(!empty($_POST['data']) and !empty($_POST['filepath'])){
	$data = $_POST['data'];
	$fname = $_POST['filepath'];
	$file = fopen($fname, 'w');//creates new file
	$today = date("d/m/Y");
	fwrite($file, $data."\n");
	fclose($file);
	}
?>


<script type="text/javascript" src="js/JSmol.min.js"></script>
<script type="text/javascript">
	var Info = {
		width: 300,
		height: 300,
		serverURL: "http://chemapps.stolaf.edu/jmol/jsmol/jsmol.php ",
		use: "HTML5",
		j2sPath: "js/j2s"
	}
</script>
		
<body style="overflow-x=hidden">
    <div id="header">
<!--        <h1 id="title">CASP13</h1>-->
        <!--<h2 id="subtitle">Critical Assesment of Techniques for Protein Structure Prediction</h2>-->
<!--        <h2 id="subtitle">Central Web Portal of MULTICOM Predictors</h2>-->
    </div>
	        <p id="jobname" style="display:none;" hidden><?php echo $job_name?></p>
        	<p id="jobid" style="display:none;" hidden><?php echo $job_id?></p>
        	<p id="methodName" style="display:none;" hidden><?php echo $method_id?></p>
        	<p id="pred_dir" style="display:none;" hidden><?php echo $pred_dir?></p>
			
<script>


      // Fills the table for each model. The View Model, Align, etc. #MULTICOM.Hbx.15451457358921
            var methodName = $("#methodName").text();
			var job = $("#jobname").text();
			var id = $("#jobid").text(); 
			var target = job+'-'+id;
			var pred_dir = $("#pred_dir").text();
			//  load the protein sequence
			var fasta_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir+'/'+target+ ".fasta";
			$.get(fasta_file)
			.done(function() { 
				// exists code 
					var client = new XMLHttpRequest();
					client.open('GET', fasta_file);
					jQuery.get(fasta_file, function(data) {
						document.getElementById('protein_sequence').value =data;
					});
			}).fail(function() { 
				// not exists code
				
			})
			

			// update the rank list 
			var dashfile = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir+'/full_length.dash.csv';
			
			
			//alert(dashfile);
			
			$.get(dashfile)
			.done(function() { 
				// exists code 
				var client = new XMLHttpRequest();
				client.open('GET', dashfile);
				jQuery.get(dashfile, function(data) {
					var lines = data.split('\n');
					var tableContent = '<tbody>';
					for(var line = 0; line < lines.length; line++){
					//for(var line = 0; line < 2; line++){
						var line_array = lines[line].split(',');
						tableContent += '<tr style="border: 1px solid black;">';
						for(var ind = 0; ind < line_array.length; ind++){
							tableContent += '<td style="border: 1px solid black;padding: 6px;">'+line_array[ind]+'</td>';
						}
						tableContent += '</tr>';
					}
					tableContent += '</tbody>';
					$('#template_rank').html(tableContent);
				});
			}).fail(function() { 
				// not exists code
			})
			
			
			
			
			//  load the protein sequence
			var model_aln1 = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir+'/'+target+ "_model1.pir";
			$.get(model_aln1)
			.done(function() { 
				// exists code 
					var client = new XMLHttpRequest();
					client.open('GET', model_aln1);
					jQuery.get(model_aln1, function(data) {
						document.getElementById('template_alignment').value =data;
					});
			}).fail(function() { 
				// not exists code
				
			})
		
</script>			
        <div class="row"> <!-- row for visualization container -->
		  <div  style="height:300px; margin-left: 8%;">
				<div class="col-md-5">
						<div class="item" style="height:200px;">       
							<div style="text-align:center;">
							  <h3 > Protein sequence </h3>
							  <textarea  readonly="readonly" cols="100" rows="10" id="protein_sequence"></textarea>
							</div>
						</div> 
				</div> 
				<div class="col-md-5">
						<div style="display: inline-block; margin-left: 0%;">
							<h3 > Template Rank list </h3>
							<div style="height:205px;border-style: solid;border-width: medium; width: fit-content; overflow-y: auto; overflow-x: auto;"> 
							  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;" id="template_rank" >
							  </table>
							</div>
						</div> <!-- end row -->
				</div> <!-- end row -->
			</div> <!-- end row -->
		</div> <!-- end row -->
				

		<div class="row">
			<hr style="height:1px;border:none;color:#333;background-color:#333;" />
			<h3 align="center">Top 1 Predicted Tertiary Structure</h3>
			
			<div class="carousel-inner" style="height:450px; margin-left: 8%;">
				<div class="col-md-2">			
					<div id="visualization">
						<div class="col-md-2 method_box">
							 <h3 id="modelTitle" style="text-align:center"> Model </h3>

							<script type="text/javascript">
								var job = $("#jobname").text();
								var id = $("#jobid").text();
								var methodName = $("#methodName").text();
								var target = job+'-'+id;
								var pred_dir = $("#pred_dir").text();
								var rfile = 1;
								var model = 1;
								//var append = "APPEND";
								var append = "";
								var modelfile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb";
								Jmol.getApplet("jsmolApplet_M23d1", Info);
								Jmol.script(jsmolApplet_M23d1,"background black; load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb;");
								Jmol.script(jsmolApplet_M23d1, "spin on; cartoon only; color {file="+ rfile+"} group;");
							</script>
						</div> <!-- end of col-md-5 --> 
					</div> <!-- end of col-md-5 --> 
				</div> <!-- end of col-md-5 --> 
				<div class="col-md-3">
					<div id="displayTableCarousel1" class="carousel slide" data-ride="carousel" data-interval="false">
						<ol class="carousel-indicators">
							<li data-target="#displayTableCarousel1" data-slide-to="0" class="active"></li>
							<li data-target="#displayTableCarousel1" data-slide-to="1"></li>
							<li data-target="#displayTableCarousel1" data-slide-to="2"></li>
							<li data-target="#displayTableCarousel1" data-slide-to="3"></li>
						</ol>
						<div class="carousel-inner" style="height:500px; margin-left: 8%;">
							<div class="item active" style="height:502px;">		

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/5) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/2) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top 2L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
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
				<div class="col-md-5">
						<div class="item" style="height:200px;">       
							<div style="text-align:center;">
							  <h3 > Target-template alignment </h3>
							  <textarea  readonly="readonly" cols="100" rows="10" id="template_alignment"></textarea>
							</div>
						</div> 
				</div> 
			</div> <!-- end of carousel item 1 --> 
			
			<hr style="height:1px;border:none;color:#333;background-color:#333;" />
			<h3 align="center">Top 2 Predicted Tertiary Structure</h3>
		
			<div class="carousel-inner" style="height:400px; margin-left: 8%;">
				<div class="col-md-2">	
					<div id="visualization">
						<div class="col-md-2 method_box">
							 <h3 id="modelTitle" style="text-align:center"> Top 2 Tertiary structure</h3>

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
								var modelfile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb";
								Jmol.getApplet("jsmolApplet_M23d2", Info);
								Jmol.script(jsmolApplet_M23d2,"background black; load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb;");
								Jmol.script(jsmolApplet_M23d2, "spin on; cartoon only; color {file="+ rfile+"} group;");
							</script>
						</div> <!-- end of col-md-5 --> 
					</div> <!-- end of col-md-5 --> 
				</div> <!-- end of col-md-5 --> 
				<div class="col-md-3">
					<div id="displayTableCarousel2" class="carousel slide" data-ride="carousel" data-interval="false">
						<ol class="carousel-indicators">
							<li data-target="#displayTableCarousel2" data-slide-to="0" class="active"></li>
							<li data-target="#displayTableCarousel2" data-slide-to="1"></li>
							<li data-target="#displayTableCarousel2" data-slide-to="2"></li>
							<li data-target="#displayTableCarousel2" data-slide-to="3"></li>
						</ol>
						<div class="carousel-inner" style="height:500px; margin-left: 8%;">
							<div class="item active" style="height:502px;">		

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/5) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/2) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top 2L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
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
			</div> <!-- end of col-md-5 --> 
			
			<hr style="height:1px;border:none;color:#333;background-color:#333;" />
			<h3 align="center">Top 3 Predicted Tertiary Structure</h3>
		
			<div class="carousel-inner" style="height:400px; margin-left: 8%;">
				<div class="col-md-2">	
					<div id="visualization">
						<div class="col-md-2 method_box">
							 <h3 id="modelTitle" style="text-align:center"> Top 3 Tertiary structure</h3>

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
								var modelfile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb";
								Jmol.getApplet("jsmolApplet_M23d3", Info);
								Jmol.script(jsmolApplet_M23d3,"background black; load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb;");
								Jmol.script(jsmolApplet_M23d3, "spin on; cartoon only; color {file="+ rfile+"} group;");
							</script>
						</div> <!-- end of col-md-5 --> 
					</div> <!-- end of col-md-5 --> 
				</div> <!-- end of col-md-5 --> 
				<div class="col-md-3">
					<div id="displayTableCarousel3" class="carousel slide" data-ride="carousel" data-interval="false">
						<ol class="carousel-indicators">
							<li data-target="#displayTableCarousel3" data-slide-to="0" class="active"></li>
							<li data-target="#displayTableCarousel3" data-slide-to="1"></li>
							<li data-target="#displayTableCarousel3" data-slide-to="2"></li>
							<li data-target="#displayTableCarousel3" data-slide-to="3"></li>
						</ol>
						<div class="carousel-inner" style="height:500px; margin-left: 8%;">
							<div class="item active" style="height:502px;">		

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/5) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/2) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top 2L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
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
			</div> <!-- end of col-md-5 --> 
			
			<hr style="height:1px;border:none;color:#333;background-color:#333;" />
			<h3 align="center">Top 4 Predicted Tertiary Structure</h3>
		
			<div class="carousel-inner" style="height:400px; margin-left: 8%;">
				<div class="col-md-2">	
					<div id="visualization">
						<div class="col-md-2 method_box">
							 <h3 id="modelTitle" style="text-align:center"> Top 4 Tertiary structure</h3>

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
								var modelfile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb";
								Jmol.getApplet("jsmolApplet_M23d4", Info);
								Jmol.script(jsmolApplet_M23d4,"background black; load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb;");
								Jmol.script(jsmolApplet_M23d4, "spin on; cartoon only; color {file="+ rfile+"} group;");
							</script>
						</div> <!-- end of col-md-5 --> 
					</div> <!-- end of col-md-5 --> 
				</div> <!-- end of col-md-5 --> 
				<div class="col-md-3">
					<div id="displayTableCarousel4" class="carousel slide" data-ride="carousel" data-interval="false">
						<ol class="carousel-indicators">
							<li data-target="#displayTableCarousel4" data-slide-to="0" class="active"></li>
							<li data-target="#displayTableCarousel4" data-slide-to="1"></li>
							<li data-target="#displayTableCarousel4" data-slide-to="2"></li>
							<li data-target="#displayTableCarousel4" data-slide-to="3"></li>
						</ol>
						<div class="carousel-inner" style="height:500px; margin-left: 8%;">
							<div class="item active" style="height:502px;">		

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/5) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/2) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top 2L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
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
			</div> <!-- end of col-md-5 --> 
			
			<hr style="height:1px;border:none;color:#333;background-color:#333;" />
			<h3 align="center">Top 5 Predicted Tertiary Structure</h3>
		
			<div class="carousel-inner" style="height:400px; margin-left: 8%;">
				<div class="col-md-2">	
					<div id="visualization">
						<div class="col-md-2 method_box">
							 <h3 id="modelTitle" style="text-align:center"> Top 5 Tertiary structure</h3>

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
								var modelfile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb";
								Jmol.getApplet("jsmolApplet_M23d5", Info);
								Jmol.script(jsmolApplet_M23d5,"background black; load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+pred_dir + "/"+target+'_model'+model+ ".pdb;");
								Jmol.script(jsmolApplet_M23d5, "spin on; cartoon only; color {file="+ rfile+"} group;");
							</script>
						</div> <!-- end of col-md-5 --> 
					</div> <!-- end of col-md-5 --> 
				</div> <!-- end of col-md-5 --> 
				<div class="col-md-3">
					<div id="displayTableCarousel5" class="carousel slide" data-ride="carousel" data-interval="false">
						<ol class="carousel-indicators">
							<li data-target="#displayTableCarousel5" data-slide-to="0" class="active"></li>
							<li data-target="#displayTableCarousel5" data-slide-to="1"></li>
							<li data-target="#displayTableCarousel5" data-slide-to="2"></li>
							<li data-target="#displayTableCarousel5" data-slide-to="3"></li>
						</ol>
						<div class="carousel-inner" style="height:500px; margin-left: 8%;">
							<div class="item active" style="height:502px;">		

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/5) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top L/2) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
								</div>
								
							</div>
							
							
							<div class='carousel item'>	

								<div class="col-md-3">	
									<div id="visualization">
										<div class="col-md-3 method_box">
											<h3 style="text-align: center;"> Model 1 vs Contact (Top 2L) </h3>
											<div style="width: 350px; height: 300px;">
												<img style="width: 300px; height: 300px; margin: 0 auto;text-align: center;" alt="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" src="./MULTICOM_Methods/<?php echo "${method_id}/${job_name}-${job_id}/${job_name}-${job_id}_1.cmap-topL.png"?>" />
											</div>			
											<h4 style="text-align: center;"> Accuracy: <input type="text" name="confold_contact_map_topL_acc"  id="confold_contact_map_topL_acc" value="0.9" disabled><br></h3>
										</div>
									</div>
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

			</div> <!-- end of carousel item 1 --> 
		</div> <!-- end of carousel item 1 --> 
			
				
				
		<hr style="height:1px;border:none;color:#333;background-color:#333;" />
		

			<h3 align="center"> Domain Boundary & domain-based models</h3>
		

	



</body>
</html>