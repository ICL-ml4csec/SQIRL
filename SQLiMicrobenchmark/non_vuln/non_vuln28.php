<?php
		
    $name = $_POST['name'];
    $pass = 'password';
    $difficulty = $_POST['difficulty'];
    // database insert SQL code
    $servername = "db";
    $username = "server";
    $password = "Qazwsxedcr12@";
    $db = "sqliDB";
    
    // Create connection
    $conn = new PDO('mysql:host=' . $servername.';dbname=' . $db.';charset=utf8', $username, $password, array(PDO::MYSQL_ATTR_FOUND_ROWS => true));
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $conn->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);


    // database insert SQL code
    echo "Search: ".$name.", ".$pass."<br>";
    $pass = str_replace(" ","",$pass);
    $name = str_replace(" ","",$name);
    $sql = "INSERT INTO `users` (`name`, `pass`) VALUES (:name, :pass)"; 
    
    

    $data = $conn->prepare($sql);
    $data->bindParam( ':name', $name, PDO::PARAM_STR );
    $data->bindParam( ':pass', $pass, PDO::PARAM_STR );
    $data->execute();
    $rs = $data;
    
    if($rs)
    {   if(strpos($difficulty, 'feed') !== False)
        {
            echo "Query feedback: ";
            echo $data->rowCount(). "<br>";
            echo 'Exception feedback: NO<br>';

        }elseif(strpos($difficulty, 'exec') !== False){
            echo "Query feedback: NO<br>";
            echo 'Exception feedback: YES<br>';
        }
        else{
            echo "Query feedback: NO<br>";
            echo 'Exception feedback: NO<br>';
        }
        
    }else{
        if(strpos($difficulty, 'exec') !== False)
        {
            echo "Query feedback: NO<br>";
            echo "Exception feedback: ";
            if(mysqli_error($conn) !== Null){
                    echo mysqli_error($conn);
            }else{
                echo "YES";
            }
        }
        elseif(strpos($difficulty, 'feed') !== False)
        {
            echo "Query feedback: <br>";
            echo 'Exception feedback: NO<br>';

        }else{
            echo "Query feedback: NO<br>";
            echo 'Exception feedback: NO<br>';
        }

    }
			
	
?>