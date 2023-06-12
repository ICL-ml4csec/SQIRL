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
    $conn = new mysqli($servername, $username, $password, $db);
                
    // Check connection
    if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
    }
    
    
    
    $name = 'invalid_user';
    
    $id = $_GET['id'];
    // $conn->quoteIde
    // $where_clause = " WHERE id = {$id} ";
    $sql = "UPDATE users SET name=$name WHERE id = $id";
    echo "Search: ". $name. ", ". $id. "<br>";

    // insert in database 
    $rs = mysqli_query($conn, $sql);
    if($rs)
    {   if(strpos($difficulty, 'feed') !== False)
        {
            echo "Query feedback: ";
            if (gettype($rs) != 'boolean')
            {
                $count = 0;
                while($row = mysqli_fetch_assoc($rs) and $count < 10) {
                    echo "ID: " . $row["id"]. " - Name: " . $row["name"]. " - Pass: " . $row["pass"]. "<br>";
                    $count += 1;
                }
                if(mysqli_num_rows($rs) == 0){
                   echo "<br>";
                }
            }else{
                echo $rs;
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