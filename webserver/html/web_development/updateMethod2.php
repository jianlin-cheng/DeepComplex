<?php
$method = $_GET['method'];
$path = 'MULTICOM_Methods/' . $method . '/';

if ($handle = opendir($path)) {
    $blacklist = array('.', '..','comments.txt');
    while (false !== ($directories = readdir($handle))) {
        $newDate = substr($directories, 0,  7);  
        if (!in_array($directories, $blacklist)) {
            $prevDate=$date;
            
            $file = rtrim($directories);
            echo "<option><button id=\"#$file\" type=\"button\"  value=\"$file\">$file</button></option>\n";
        }
        else if($prevDate != $date && !in_array($file, $blacklist)) {
            $prevDate=$date;
            echo "<li class='dropdown-submenu'><a tabindex="-1">New dropdown <span class='caret'></span></a>";
            echo "<ul class='dropdown-menu'>";
            $file = rtrim($file);
            echo "<option><button id=\"#$file\" type=\"button\"  value=\"$file\">$file</button></option>\n";
        }
    }
    closedir($handle);
}
?>