<?php
$method = $_GET['method'];
$path = 'MULTICOM_Methods/' . $method . '/';

if ($handle = opendir($path)) {
    $blacklist = array('.', '..','comments.txt');
    while (false !== ($file = readdir($handle))) {
        if (!in_array($file, $blacklist)) {
            $file = rtrim($file);
            echo "<option><button id=\"#$file\" type=\"button\"  value=\"$file\">$file</button></option>\n";
        }
    }
    closedir($handle);
}
?>