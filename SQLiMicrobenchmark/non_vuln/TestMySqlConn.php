<!DOCTYPE html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>SQL CON</title>
	</head>

	<body>
		<h1>TEST SQL CON</h1>
		
		<?php
            $servername = "localhost:3306";
            $username = "server";
            $password = "Qazwsxedcr12@";

            // Create connection
            $conn = new mysqli($servername, $username, $password);
            
            // Check connection
            if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
            }
            echo "Connected successfully";
        ?>
		

		
	</body>
</html>
