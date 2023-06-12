<?php
    // CVE-2020-8638
    $difficulty = $_GET['difficulty'];
    echo 'CVE-2020-8638<br>';

    // database insert SQL code
    $servername = "db";
    $username = "server";
    $password = "Qazwsxedcr12@";
    $db = "sqliDB";

    // Create connection
    $conn = new PDO('mysql:host=' . $servername.';dbname=' . $db.';charset=utf8', $username, $password, array(PDO::MYSQL_ATTR_FOUND_ROWS => true));
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $conn->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

    $name = isset($_GET['name']) ? trim($_GET['name']) : null;
    $name = !is_null($name) && strlen($name) > 0 ? trim($name) : null;

    $id = isset($_GET['id']) ? trim($_GET['id']) : null;
    $id = !is_null($id) && strlen($id) > 0 ? trim($id) : null;

    $id = $_GET['id'];
    $sql = "UPDATE users SET name=:name WHERE id = :id";

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
            if (gettype($rs) != 'boolean')
            {
                if (gettype($rs) != 'boolean')
                {
                    echo $data->rowCount(). '<br>';
                    
                }else{
                    echo $rs;
                    echo "<br>";
                }
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