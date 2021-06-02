<?php
    $newComment = $_POST['newComment'];
    $method = $_POST['method'];
    $filepath = $_POST['filepath'];
    
    $newComment = date('Y/m/d h:i:a') . " : " .  $newComment . PHP_EOL;
    file_put_contents($filepath, $newComment, FILE_APPEND);
    echo file_get_contents($filepath, true);
?>