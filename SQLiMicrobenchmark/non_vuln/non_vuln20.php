<?php
    // CVE-2020-8841
    $difficulty = $_GET['difficulty'];
    echo 'CVE-2020-8841<br>';

    // database insert SQL code
    $servername = "db";
    $username = "server";
    $password = "Qazwsxedcr12@";
    $db = "sqliDB";

    // Create connection
    $conn = new PDO('mysql:host=' . $servername.';dbname=' . $db.';charset=utf8', $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $conn->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

    
    $name = 'invalid_user';

    $id = isset($_GET['id']) ? trim($_GET['id']) : null;
    $id = !is_null($id) && strlen($id) > 0 ? trim($id) : null;


    $sql = "SELECT * FROM users WHERE (id=:id AND name=:name)";
    $data = $conn->prepare($sql);
    $data->bindParam( ':id', $id, PDO::PARAM_INT );
    $data->bindParam( ':name', $name, PDO::PARAM_STR );
    $data->execute();

    echo "Search: ".$name.", ".$id."<br>";

    // insert in database 
    $rs = $data;
    if($rs)
    {   if(strpos($difficulty, 'feed') !== False)
        {
            echo "Query feedback: ";
            $count = 0;
            while ($row = $data->fetch(PDO::FETCH_ASSOC) AND  $count < 10) {
                echo "ID: " . $row["id"]. " - Name: " . $row["name"]. " - Pass: " . $row["pass"]. "<br>";
                $count += 1;
            }
            if($data->rowCount()==0){
               echo "<br>";
            }
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