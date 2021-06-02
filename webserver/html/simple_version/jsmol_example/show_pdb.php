

<!DOCTYPE html
		PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
				 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
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
<body>




<script type="text/javascript">
	var rfile = 1;
	var model = 1;
	//var append = "APPEND";
	var append = "";
	var modelfile = "./chr11_10kb_gm12878_list_125mb_135mb_1473188895655.pdb";
	Jmol.getApplet("jsmolApplet_M23d1", Info);
	Jmol.script(jsmolApplet_M23d1,"background black; load http://sysbio.rnet.missouri.edu/3dgenome/GSDB/structures/IFList_Chr_20_1mb_1450749845157.pdb;");
	Jmol.script(jsmolApplet_M23d1, "spin on; cartoon only; color {file="+ rfile+"} group;");
</script>

</body>
</html>
