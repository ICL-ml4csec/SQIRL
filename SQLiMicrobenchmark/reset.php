<?php
    // database insert SQL code
    $servername = "db";
    $username = "server";
    $password = "Qazwsxedcr12@";
    $db = "sqliDB";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $db);
                
    // Check connection
    if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
    }

    $sql = "DROP TABLE `users`;";


    // insert in database 
    $rs = mysqli_query($conn, $sql);

    $sql = "CREATE TABLE `users` (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(500) DEFAULT NULL, `pass` varchar(500) DEFAULT NULL, PRIMARY KEY (`id`), UNIQUE KEY `id_UNIQUE` (`id`));";

    $rs = mysqli_query($conn, $sql);

    $sql ="INSERT INTO users (name, pass, id) VALUES ('user', 'password', 1);";

    $rs = mysqli_query($conn, $sql);

    $sql = "INSERT INTO users (name, pass, id) VALUES ('user2', 'password2', 2);";

    $rs = mysqli_query($conn, $sql);
    
?>