<?php
$method_id = $_REQUEST["method"];

if($method_id == 'multicom')
{
	$method_id='multicom';
}else if($method_id == 'multicom_CAMEO')
{
	$method_id='multicom_CAMEO';
}else{
	echo '<script language="javascript">';
  echo 'alert("Wrong server name input, please input one of multicom")';
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

$(document).ready(function() {
   $("#title-menu").click(function() {
	   var target = String($(this).val());
	   $("#dropdown-description").html(target.toUpperCase() + '<span class="caret"></span>');
		$.get("updateMethod.php", {method:target}, function(response){
			$("#targetMenu").html(response);
			});
	   $(".comment_box").html(target.toUpperCase() + " Comments");
	   location.href = "http://sysbio.rnet.missouri.edu/multicom_cluster/dashboard//index.php?method=" + target;
		});
});


// Sort targets by decreasing date
$(document).ready(function() {
    var opt = $("#view_targets li").sort(function (a,b) { return b.innerText.toUpperCase().localeCompare(a.innerText.toUpperCase()) });
    var lastDate = "";
    $("#view_targets").html("");
//  console.log(opt);
  var html = "";
  var list = new Array();
    $.each(opt, function(index, value){
        var thisDate = opt[index].textContent.substr(0,10);
        var thisName = opt[index].textContent.substr(11);
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

var __target = "";
var __targetDate = "";
var __targetWeb = "";
function loadTarget(e){
	//    console.log(e);
	document.getElementById("targetMenu").innerHTML = e.attributes.value.textContent + "<span class='caret'></span>";
	$(".activeDropdown").hide();
	$(".activeDropdown").removeClass("activeDropdown");
	methodName = $("#dropdown-description").text();
	var target = e.name;
	target = target.replace(/\n/g, '');
	target_array = target.split('|');
	__targetDate = target_array[0];
	__targetName = target_array[1];
	__targetWeb = target_array[2];
	
};

function getTarget(){
	return __targetName;
}

function getTargetDate(){
	return __targetDate;
}

function getTargetWeb(){
	return __targetWeb;
}

   $(document).ready(function() {
      // Fills the table for each model. The View Model, Align, etc.
       $("#view_targets").click(function() {
           var methodName = $("#dropdown-description").text();
			var targetName = getTarget();
			var targetDate = getTargetDate();
			var targetWeb = getTargetWeb();
            $("#dropdownMenu1").html(targetName);
			targetName = targetName.replace(/\n/g, '');
			targetDate = targetDate.replace(/\n/g, '');
			targetWeb = targetWeb.replace(/\n/g, '');
		  
		   // update the multicom prediction link 
		   
		   //multicom_web_prediction
		   
		   document.getElementById('multicom_iframe').src = targetWeb;
		   document.getElementById('multicom_iframe').width = "100%";
		   document.getElementById('multicom_iframe').height = "100%";

		});	
			
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


<body style="overflow-x=hidden">
    <div id="header">
        <h1 id="title">MULTICOM</h1>
        <!--<h2 id="subtitle">Critical Assesment of Techniques for Protein Structure Prediction</h2>-->
        <h2 id="subtitle">Central Web Portal of MULTICOM Predictors</h2>
    </div>
	<div class="post_success">
        <div class="visualization-container">
			<div class="row"> <!-- row for visualization container -->
				<div class="col-md-5">
					<div class="dropdown col-md-3 text-left">
						<button id="dropdown-description" class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown"><?php echo strToUpper($method_id) ?><span class="caret"></span></button>
						<select  class="dropdown-menu" id="title-menu" multiple="multiple" aria-labelledby="targetMenu" style="left: 19px; min-width: 111px;">
								<?php
						
								if ($handle = opendir('MULTICOM_Methods/')) {
									$blacklist = array('.', '..','comments.txt');
									while (false !== ($file = readdir($handle))) {
										if (!in_array($file, $blacklist)) {
											$file = rtrim($file);
											$file_upper=strtoupper($file);
											echo "<option class='dropdown-menu-methods'><button id=\"#$file\" type=\"button\"  value=\"$file\">$file</button></option>\n";
										}
									}
									closedir($handle);
								}
								?>
							
						</select >
					</div>
					
					<div class="dropdown col-md-2 text-left">
						<button class="btn btn-default dropdown-toggle" type="button" id="targetMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
						
								Please select the target
								<span class="caret"></span>
						</button>
						
						<ul class="dropdown-menu" id="view_targets" multiple="multiple" aria-labelledby="targetMenu" size=20 style="left: 19px; font-size: 15px; min-width: 133px;">
								<?php
										$blacklist = array('.', '..','comments.txt');

										if(file_exists("MULTICOM_Methods/$method_id/prediction.summary"))
										{
											$c = 0;
											if ($file = fopen("MULTICOM_Methods/$method_id/prediction.summary", "r")) {
												while(!feof($file)) {
													$line = trim(fgets($file));
													# do same stuff with the $line
													if($line  !="")
													{
														$tmp_info = explode("\t", $line);
														$target_date = $tmp_info[0];
														$target_name = $tmp_info[1];
														$target_path = $tmp_info[2];
														$target_web = $tmp_info[3];
														$target_label = $target_date.'-'.$target_name;
														$target_info = $target_date.'|'.$target_name.'|'.$target_web;
														if(!in_array($target_name, $blacklist))
														{
															echo "<li><button id=\"#$target_label\" type=\"button\"  class='target-btns btn' style='margin-bottom: 4px;' value=\"$target_label\" name=\"$target_info\" onclick='loadTarget(this)' >$target_label</button></li>\n";
														}
													}
												}
												fclose($file);
											}
										}
									
									?>
						</ul>
					  <div class="loader" id="multi_confold_deep_loader" style="display:none;"></div>
					</div>
				   <!--save new comments -->
					<script>
						function saveNewComment(commentId, box, name, filepath) {
							var newComment = document.getElementById(commentId).value;
							var newName = document.getElementById(name).value;
							var method = $("#dropdown-description").text().toLowerCase();
							$.post("updateComments.php", {newComment: newComment, method: method, name: name, filepath: filepath}, function(response){
								document.getElementById(box).value = response;
								document.getElementById('newComment').value = '';
							});
						}
					</script>
				</div> <!-- end of col-md-5 -->				
	
			</div> <!-- end of row -->
			

			<div  align="center">
				<font size="5"><b>Comments<br></b></font>

				<textarea readonly id="comment_box" style="height:200px; width: 50%; overflow-y:auto; resize: none;" class="comment_content"><?php echo trim(file_get_contents("./MULTICOM_Methods/$method_id/comments.txt", true));?></textarea><br>
				<div style="margin-top: 5px; display: block; text-align:center;">
				<textarea id="newComment" name=newComment style="width:40%; height:30px; resize: none;" placeholder="New Comment"></textarea><br>
				<textarea id="name" name=name placeholder="Name"></textarea><br>
				
					<input type="button" class="btn" value="Save" style="vertical-align: 11px; padding: 5px;" id="<?php echo $method_id ?>_comment" onclick="saveNewComment('newComment','comment_box', 'name', ./MULTICOM_Methods/<?php echo $method_id ?>/comments.txt')"/>
				  </div>
			</div> 			
			
			<?php
			#if ($method_id == 'multicom')
			#{
			?>
				<div class="row">
					<h2 align="center"> MULTICOM prediction </h2>
					<div  style="height: 1000px; width: 1800px;border: 0px solid black;margin:0 auto;" align="center">
						<iframe id="multicom_iframe" src=""  width="100%"  height="10%" ></iframe><br/>					
					</div>
						
				</div>	
				</div> <!-- end of visualiation containter -->
			<?php
			#}
			?>	



		</div> <!-- end of visualiation containter -->
	</div> <!-- end of post_success -->

</body>
</html>



