<?php
$method_id = $_REQUEST["method"];

if($method_id == 'multicom')
{
	$method_id='multicom';
}else{
	echo '<script language="javascript">';
  echo 'alert("Couldn\'t find predictions from MULTICOM server, please provide correct link!")';
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
  var __target = "";
  function loadTarget(e){
//    console.log(e);
    document.getElementById("targetMenu").innerHTML = e.attributes.value.textContent + "<span class='caret'></span>";
    $(".activeDropdown").hide();
    $(".activeDropdown").removeClass("activeDropdown");
    methodName = $("#dropdown-description").text();
    var target = e.value;
    target = target.replace(/\n/g, '');
    __target = target;
	model = 1;
    if ($("#refinedCheck").prop("checked")) {
      Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
      if (!$("#initialCheck").prop("checked")) append = "";
      rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
      jmol_filepath = "load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;", "frame ALL; spin on; cartoon only; color {file=1} group;";
      jmol_frame_instructions = "frame ALL; spin on; cartoon only; color {file=1} group;";
    }
	else {
      $("#refinedCheck").prop("checked", true);
      rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
      jmol_filepath = "load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;";
      jmol_frame_instructions = "frame ALL; spin on; cartoon only; color {file=1} group;";
	}
    append = "APPEND";
    $("#modelTitle").html("Predicted Model 1");
  };
  
  function getTarget(){
    return __target;
  }
    $(document).ready(function() {
       $("#title-menu").click(function() {
           var target = String($(this).val());
           $("#dropdown-description").html(target.toUpperCase() + '<span class="caret"></span>');
            $.get("updateMethod.php", {method:target}, function(response){
                $("#targetMenu").html(response);
                });
           $(".comment_box").html(target.toUpperCase() + " Comments");
           location.href = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/index.php?method=" + target;
            });
    });
	
    $(document).ready(function() {
      // Fills the table for each model. The View Model, Align, etc.
       $("#view_targets").click(function() {
           var methodName = $("#dropdown-description").text();
			var target = getTarget();
            $("#dropdownMenu1").html(target);
			target = target.replace(/\n/g, '');
			model = 1;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
			document.getElementById('view_model_1').href =model_file;
			document.getElementById('viewButton1').value =target;
			document.getElementById('pdb_contact_analysis1').value =target+'.1';
			document.getElementById('viewAlign1').value =aln_file;
			model = 2;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
			document.getElementById('view_model_2').href =model_file;
			document.getElementById('viewButton2').value =target;
			document.getElementById('pdb_contact_analysis2').value =target+'.2';
			document.getElementById('viewAlign2').value =aln_file;
          
		  
			model = 3;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
            document.getElementById('view_model_3').href =model_file;
			document.getElementById('viewButton3').value =target;
			document.getElementById('pdb_contact_analysis3').value =target+'.3';
			document.getElementById('viewAlign3').value =aln_file;
          
		  
			model = 4;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
		    document.getElementById('view_model_4').href =model_file;
			document.getElementById('viewButton4').value =target;
			document.getElementById('pdb_contact_analysis4').value =target+'.4';
			document.getElementById('viewAlign4').value =aln_file;
          
		  
		  
			model = 5;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
            document.getElementById('view_model_5').href =model_file;
			document.getElementById('viewButton5').value =target;
			document.getElementById('pdb_contact_analysis5').value =target+'.5';
			document.getElementById('viewAlign5').value =aln_file;
			
			//  load the protein sequence
			var fasta_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+ ".fasta";
			
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
			
			
          
			//  load the protein template rank
			var fasta_rank = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/full_length.dash';
			$.get(fasta_rank)
			.done(function() { 
				// exists code 
				var client = new XMLHttpRequest();
					client.open('GET', fasta_rank);
                    
					jQuery.get(fasta_rank, function(data) {
						if(document.getElementById('template_rank'))
						{
							document.getElementById('template_rank').value =data;
						}
					});
		
			}).fail(function() { 
				// not exists code
			})

		   	
			//alert('here');
			//  load the protein predicted contact
			var contact_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'.rr';

			$.get(contact_file)
			.done(function() { 
				// exists code 
				client = new XMLHttpRequest();
				client.open('GET', contact_file);
					jQuery.get(contact_file, function(data) {
						if(document.getElementById('confold_contact'))
						{
							document.getElementById('confold_contact').value =data;
						}
					});
			}).fail(function() { 
				// not exists code
			})

		
			
			//load contact map
			var contact_file_map = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'.cmap.png';
			if(document.getElementById('confold_contact_map'))
			{
				document.getElementById('confold_contact_map').src =contact_file_map;
			}
		  
			
			// update the rank list 
			var dashfile = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/full_length.dash.csv';
			
			
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
		
		});	
			
    });


// Sort targets by increasing date
$(document).ready(function() {
    var opt = $("#view_targets li").sort(function (a,b) { return a.innerText.toUpperCase().localeCompare(b.innerText.toUpperCase()) });
    var lastDate = "";
    $("#view_targets").html("");
//  console.log(opt);
  var html = "";
  var list = new Array();
    $.each(opt, function(index, value){
        var thisDate = opt[index].textContent.substr(0,10);
//      console.log(value);
        //the first date
        if(lastDate === ""){
          html += "<li class='dropdown-submenu'>";
          html += "<a class='test'>";
          html += thisDate;
          html += "<b class='caret'></b></a>";
          html += "<ul class='dropdown-menu' id="+thisDate+" style='padding: 5px 5px 1px 5px;'>";
          html += "<li>";
          html += value.innerHTML;
          html += "</li>";
          list.push(value);
          lastDate = thisDate;
        }
        else if (lastDate !== thisDate){
          html += "</ul>";
          $("#view_targets").append(html);
          list=[];
          html="";
          html += "<li class='dropdown-submenu'>";
          html += "<a class='test'>" + thisDate + "<b class='caret'></b></a>";
          html += "<ul class='dropdown-menu'  id="+thisDate+" style='padding: 5px 5px 1px 5px;'>";
          html += "<li>";
          html += value.innerHTML;
          html += "</li>";
          list.push(value);
          lastDate = thisDate;
        }
        else if(lastDate === thisDate){
          html += "<li>";
          html += value.innerHTML;
          html += "</li>";
          list.push(value);
          lastDate = thisDate;
        }
        else {
          console.log("Test a failure");
        }
    });
  html += "</div>";
  $("#view_targets").append(html);
  
  // Toggle and show the submenus for the targets which are sorted by date
  $('#view_targets .dropdown-submenu a.test').on("click", function(e){
    $('.activeDropdown').hide();
    $('.activeDropdown').removeClass('activeDropdown');
    $(this).next('ul').toggle();
    $(this).next('ul').addClass('activeDropdown');
    e.stopPropagation();
    e.preventDefault();
  });
});

$(document).ready(function() {
    var opt = $("#viewButton1 option").sort(function (a,b) { return a.value.toUpperCase().localeCompare(b.value.toUpperCase()) });
    $("#viewButton1").append(opt);
});

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
		width: 500,
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
    <div class="post_success">
        <div class="visualization-container">
          <div class="row"> <!-- row for visualization container -->
            <div class="col-md-5">
		
				<div class="col-md-4 method_box">
					<div class="item" style="height:300px;">       
						<div style="text-align:center;">
						  <h3 > Protein sequence: </h3>
						  <textarea  readonly="readonly" cols="80" rows="10" id="protein_sequence"></textarea>
						</div>
					</div> 
					
				</div> 
				
				<hr>
			
                <div id="visualization">
				    <div class="col-md-4 method_box">
                        <!--   script to load visualization  -->
					   <script type="text/javascript">
								var model = 1;
								var rfile = 1;
								var ifile = 2;
								var append = "APPEND";
								Jmol.getApplet("jsmolAppletM1", Info);
						
								Jmol.script(jsmolAppletM1,"background black;");
								Jmol.script(jsmolAppletM1, "spin on; cartoon only; color {file=1} group;");
								Jmol.jmolCheckbox(jsmolAppletM1,"","","Top1 Structure", false, "initialCheck");
								Jmol.jmolCheckbox(jsmolAppletM1,"","","Selected Structure", true, "refinedCheck");
								var methodName="";
								var target="";
								$(document).ready(function() {
									$("#view_targets").click(function() {
                                        document.getElementById("multi_confold_deep_loader").style.display = "inline-block";
										methodName = $("#dropdown-description").text();
                                        target = getTarget();
										target = target.replace(/\n/g, '');
                                        
										model = 1;
										if ($("#refinedCheck").prop("checked")) {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file=1} group;");
										}
										else {
											$("#refinedCheck").prop("checked", true);
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file=1} group;");
										}
										append = "APPEND";
										$("#modelTitle").html("Predicted Model 1");
                                      hideLoader();
									});
                                  
                                    function hideLoader(){
                                      document.getElementById("multi_confold_deep_loader").style.display = "none";
                                    }
                                  
									$("#viewButton1").click(function() {
										methodName = $("#dropdown-description").text();
										target = String($(this).val());
										target = target.replace(/\n/g, '');
										model = 1;
										if ($("#refinedCheck").prop("checked")) {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										else {
											$("#refinedCheck").prop("checked", true);
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										append = "APPEND";
										$("#modelTitle").html("Predicted Model 1");
									});
									$("#viewButton2").click(function() {
										methodName = $("#dropdown-description").text();
										target = String($(this).val());
										target = target.replace(/\n/g, '');
										model = 2;
										if ($("#refinedCheck").prop("checked")) {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										else {
											$("#refinedCheck").prop("checked", true);
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										append = "APPEND";
										$("#modelTitle").html("Predicted Model 2");
									});
									$("#viewButton3").click(function() {
										methodName = $("#dropdown-description").text();
										target = String($(this).val());
										target = target.replace(/\n/g, '');
										model = 3;
										if ($("#refinedCheck").prop("checked")) {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										else {
											$("#refinedCheck").prop("checked", true);
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										append = "APPEND";
										$("#modelTitle").html("Predicted Model 3");
									});
									$("#viewButton4").click(function() {
										methodName = $("#dropdown-description").text();
										target = String($(this).val());
										target = target.replace(/\n/g, '');
										model = 4;
										if ($("#refinedCheck").prop("checked")) {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										else {
											$("#refinedCheck").prop("checked", true);
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										append = "APPEND";
										$("#modelTitle").html("Predicted Model 4");
									});
									$("#viewButton5").click(function() {
										methodName = $("#dropdown-description").text();
										target = String($(this).val());
										target = target.replace(/\n/g, '');
										model = 5;
										if ($("#refinedCheck").prop("checked")) {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										else {
											$("#refinedCheck").prop("checked", true);
											rfile = $("#initialCheck").prop("checked") ? ifile+1: 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
										}
										append = "APPEND";
										$("#modelTitle").html("Predicted Model 5");
									});
									
									$("#refinedCheck").click(function() {
										if(this.checked) {
											rfile = $("#initialCheck").prop("checked") ? ifile+1 : 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb;");
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ rfile+"} group;");
											append = "APPEND";
										}
										else {
											Jmol.script(jsmolAppletM1, "zap file=" + rfile + ";");
											if (!$("#initialCheck").prop("checked")) append = "";
										}
									});
									$("#initialCheck").click(function() {
										if(this.checked) {
											ifile = $("#refinedCheck").prop("checked") ? rfile+1 : 1;
											Jmol.script(jsmolAppletM1,"load "+append+" MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model1.pdb;');
											Jmol.script(jsmolAppletM1, "frame ALL; spin on; cartoon only; color {file="+ ifile+"} white;");
											append = "APPEND";
										}
										else {
											Jmol.script(jsmolAppletM1, "zap file=" + ifile + ";");
											if (!$("#refinedCheck").prop("checked")) append = "";
										}
									});
									
									//presort table
									var thID = 0;
									<?php if ($rwp && $molp) { ?> thID = 6;
									<?php } else if ($rwp) { ?> thID = 5;
									<?php } else if ($molp) { ?> thID = 5;
									<?php } else { ?> thID = 1; <?php } ?> 
									var myTH = document.getElementsByTagName("th")[thID];
									sorttable.innerSortFunction.apply(myTH, []);	
								});
							</script>
                  </div>
                </div> <!-- end of visualization -->
			</div> <!-- end of col-md-5 --> 

        <div class="col-md-5 update-box">

            <div class="item active" style="height:352px; margin-left: 12%;">
					
							
				<div class="col-md-4 method_box">
					<div style="display: inline-block; margin-left: 0%;">
						<h3 > Template Rank list: </h3>
						<div style="height:200px;border-style: solid;border-width: medium; width: fit-content; overflow-y: auto; overflow-x: auto;"> 
						  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;" id="template_rank" >
						  </table>
						</div>
					  </div>
				</div> <!-- end row -->
		  
  
                <div id="visualization">
				    <div class="col-md-4 method_box">
						<table id="myTable" class="" style="margin-top:13px;">
							<thead>
							<tr>
								<th style="border: 1px solid black;padding: 6px;" class="sorttable_nosort">Model #</th>
								<th style="border: 1px solid black;padding: 6px;" class="sorttable_nosort">View Model</th>
								<th style="border: 1px solid black;padding: 6px;" class="sorttable_nosort">Align</th>
								<th style="border: 1px solid black;padding: 6px;" class="sorttable_nosort">Contact</th>
							</tr>
							</thead>
							<tbody>
							<tr>
								<td style="border: 1px solid black;padding: 6px;"><h4><a class="view_model" id="view_model_1" href="">Top_1</a></h4></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewButton1" value="">View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewAlign1" value="" onclick="openPopup('viewAlign1');" >View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="pdb_contact_analysis1" value="" >Run</button></td>
							
							</tr>
							<tr>	
								<td style="border: 1px solid black;padding: 6px;"><h4><a class="view_model" id="view_model_2" href="">Top_2</a></h4></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewButton2" value="">View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewAlign2" value="" onclick="openPopup('viewAlign2');" >View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="pdb_contact_analysis2" value="" >Run</button></td>
						
							</tr>
							<tr>
								<td style="border: 1px solid black;padding: 6px;"><h4><a class=" view_model" id="view_model_3" href="">Top_3</a></h4></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewButton3" value="">View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewAlign3" value="" onclick="openPopup('viewAlign3');" >View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="pdb_contact_analysis3" value=""  >Run</button></td>
							
							</tr>
							<tr>
								<td style="border: 1px solid black;padding: 6px;"><h4><a class="view_model" id="view_model_4" href="">Top_4</a></h4></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewButton4" value="">View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewAlign4" value="" onclick="openPopup('viewAlign4');" >View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="pdb_contact_analysis4" value="" >Run</button></td>
							
							</tr>
							<tr>
								<td style="border: 1px solid black;padding: 6px;"><h4><a class=" view_model" id="view_model_5" href="">Top_5</a></h4></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewButton5" value="">View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="viewAlign5" value="" onclick="openPopup('viewAlign5');" >View</button></td>
								<td style="border: 1px solid black;padding: 6px;"><button type="button" class="btn btn-table" id="pdb_contact_analysis5" value="" >Run</button></td>
							</tr>
							</tbody>
						</table>
					</div>

					<div class="col-md-5">
						<h3> Model evaluation: </h3>
						<div style="height:auto; border-style: solid; border-width: medium; width: fit-content; overflow-y: auto; overflow-x: auto;"> 
						  <table style="border-collapse: collapse; border: 1px solid black;text-align:center;font-family: arial;" id="model_evaluation" ></table>
						</div>
					</div>
					 

				</div> <!-- end of carousel item 1 --> 
			</div> <!-- end of carousel item 1 --> 


                    
<?php
if ($method_id == 'confold2')
{
?>
             <div class="col-md-7 update-box">
               <div id="displayTableCarousel" class="carousel slide" data-ride="carousel" data-interval="false">
                 <ol class="carousel-indicators">
                  <li data-target="#displayTableCarousel" data-slide-to="0" class="active"></li>
                  <li data-target="#displayTableCarousel" data-slide-to="1"></li>
                 </ol>
                 <div class="carousel-inner" style="height:600px; margin-left: 12%;">
                   <div class="item active" style="height:502px;">
                     <div class="col-md-3" style="margin-top: 10%;">
						<div class="col-md-5">
                        <h3> Predicted Contacts: </h3>
				        <div style="width:fit-content;"> 
				            <textarea style="height:480px; overflow-y:auto; border: solid black medium;" readonly rows="150" cols="50" id="confold_contact" ></textarea>
                        </div>
                      </div>	
				    </div> <!-- end of carousel item-->
                    <div class='carousel item'>
                      <div style="width:fit-content; margin-left: 10%; ">
				        <h3 style="text-align: center;"> Predicted Contact Map: </h3>
				        <div style="width: 480px; height: auto;">
                          <img style="width: 480px; height: 480px; margin: 0 auto;text-align: center;" alt="DeepSF" src="" id="confold_contact_map"/>
                        </div>
                     </div>
				  </div> <!-- end of carousel item 2-->
              </div> <!--  end of carousel-inner role listbox -->
              <!--
			  <a class="left carousel-control" href="#displayTableCarousel" data-slide="prev">
                <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
              </a>
              <a class="right carousel-control" href="#displayTableCarousel" data-slide="next">
                <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                <span class="sr-only">Next</span>
              </a>
			  -->
        </div> <!-- end of carousel -->
    </div> <!-- end of update-box -->

<?php
}
?>
			
		</div> <!-- end of the row with the visualization container -->		


<?php
if ($method_id == 'multicom')
{ ?>
<script type="text/javascript">
    // this must be in the last, otherwise, the document won't be load
	function intial_load() {
           var methodName = 'multicom';
			var target = '2017-11-04_00000042_1_50';
			target = target.replace(/\n/g, '');
			model = 1;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
			
			document.getElementById('view_model_1').href =model_file;
			document.getElementById('viewButton1').value =target;
			document.getElementById('pdb_contact_analysis1').value =target+'.1';
			document.getElementById('viewAlign1').value =aln_file;
		  
			model = 2;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
			document.getElementById('view_model_2').href =model_file;
			document.getElementById('viewButton2').value =target;
			document.getElementById('pdb_contact_analysis2').value =target+'.2';
			document.getElementById('viewAlign2').value =aln_file;
          
		  
			model = 3;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
            document.getElementById('view_model_3').href =model_file;
			document.getElementById('viewButton3').value =target;
			document.getElementById('pdb_contact_analysis3').value =target+'.3';
			document.getElementById('viewAlign3').value =aln_file;
          
		  
			model = 4;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
		    document.getElementById('view_model_4').href =model_file;
			document.getElementById('viewButton4').value =target;
			document.getElementById('pdb_contact_analysis4').value =target+'.4';
			document.getElementById('viewAlign4').value =aln_file;
          
		  
		  
			model = 5;
			model_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pdb";
			aln_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+'_model'+model+ ".pir";
            document.getElementById('view_model_5').href =model_file;
			document.getElementById('viewButton5').value =target;
			document.getElementById('pdb_contact_analysis5').value =target+'.5';
			document.getElementById('viewAlign5').value =aln_file;
			
			
			//  load the protein sequence
			var fasta_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/'+target+ ".fasta";
			var client = new XMLHttpRequest();
			client.open('GET', fasta_file);
			jQuery.get(fasta_file, function(data) {
				document.getElementById('protein_sequence').value = data;
			});
          
			//  load the protein template rank
			var fasta_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/full_length.dash';
            console.log(methodName.toLocaleLowerCase());
			var client = new XMLHttpRequest();
			client.open('GET', fasta_file);
			jQuery.get(fasta_file, function(data) {
                console.log("This was the data ; " + data);
				document.getElementById('template_rank').value =data;
			});
			
//          
//		   //alert(document.getElementById('multicom_comment').onclick);
//		   document.getElementById('multicom_comment').setAttribute( "onClick", "saveEdits('edit_comment2','update2','" + "./MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/comments.txt'+"')");
//		   document.getElementById('multicom_comment_add').setAttribute( "onClick", "addEdits('edit_comment2','update2','" + "./MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/comments.txt'+"')");
//		   document.getElementById('multicom_comment_refresh').setAttribute( "onClick", "refreshEdits('edit_comment2','update2','" + "./MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/comments.txt'+"')");
//		   
		   
		   
		    var comment_file = "http://sysbio.rnet.missouri.edu/multicom_cluster/web_development/MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/comments.txt';
			var client = new XMLHttpRequest();
			client.open('GET', comment_file);
			jQuery.get(comment_file, function(data) {
				document.getElementById("edit_comment2").readOnly = true;
				document.getElementById('edit_comment2').value =data;
				document.getElementById('edit_comment2').scrollTop=document.getElementById('edit_comment2').scrollHeight;
			});
			
			
			
			// update the rank list 
			var dashfile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/full_length.dash.csv';
			
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
      
      
		// update the rank list 
		var modelevafile = "MULTICOM_Methods/" + methodName.toLowerCase() + "/"+target+'/model.evaluation';
      
        $.get(modelevafile)
			.done(function() { 
				// exists code 
				var client = new XMLHttpRequest();
				client.open('GET', modelevafile);
				jQuery.get(modelevafile, function(data) {
					var lines = data.split('\n');
					var tableContent = '<tbody>';
					for(var line = 0; line < lines.length; line++){
					//for(var line = 0; line < 2; line++){
						var line_array = lines[line].split('\t');
						tableContent += '<tr style="border: 1px solid black;">';
						for(var ind = 1; ind < line_array.length; ind++){
							tableContent += '<td style="border: 1px solid black;padding: 6px;">'+line_array[ind]+'</td>';
						}
						tableContent += '</tr>';
					}
					tableContent += '</tbody>';
					$('#model_evaluation').html(tableContent);
				});
			}).fail(function() {
                console.log(modelevafile);
                console.log("THIS WAS A FAILURE");
				// not exists code
			});
		}
	window.onload = intial_load();	
</script>

<?php
}
?>	


</body>
</html>