<?php

if ($_FILES['file']['size'] >= 4096) {
    die("Too big");
}

$uploads = '/var/www/html/uploads/';
$name = basename($_FILES['file']['name']);

if (move_uploaded_file($_FILES['file']['tmp_name'], $uploads . $name)) {
    header("Location: /uploads/$name");
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width" />
        <title>Transfer</title>
    </head>
    <body>
        <form enctype="multipart/form-data" method="POST">
            <input type="file" name="file" />
            <input type="submit" value="Submit" />
        </form>
    </body>
</html>
