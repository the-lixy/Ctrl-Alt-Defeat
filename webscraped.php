<html>
<body>

<?php
$script = __DIR__ . DIRECTORY_SEPARATOR . "fbwebscraper5.py";
$data = array($_GET["page1"], $_GET["page2"], $_GET["page3"]);
$result = shell_exec("python $script 2>&1".escapeshellarg(json_encode($data)));
var_dump($result);
?>

</body>
</html>