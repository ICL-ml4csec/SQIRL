<?php
    $id = $_GET['id'];
    $difficulty = $_GET['difficulty'];
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

    echo "Search: ".$id."<br>";

    $id = str_replace("AND","",$id);
    $id = str_replace("and","",$id);
    $id = str_replace("SLEEP","",$id);
    $id = str_replace("sleep","",$id);
    $id = str_replace("UNION","",$id);

    $sql = "SELECT MIN(name) from users GROUP BY id HAVING id=('" .  $id. "')";

    // insert in database 
    $rs = mysqli_query($conn, $sql);
    if($rs)
    {   if(strpos($difficulty, 'feed') !== False)
        {
            echo "Query feedback: ";
            $count = 0;
            while($row = mysqli_fetch_assoc($rs)and $count < 10) {
                echo implode($row). "<br>";
                $count += 1;
            }
            if(mysqli_num_rows($rs) == 0){
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