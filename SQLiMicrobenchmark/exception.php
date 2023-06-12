<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <title>SQLI web server</title>
    </head>

    <body>
        <pre> 
    (           (                             (         (                 (     
 )\ )   (    )\ )      (  (            (   )\ )      )\ )              )\ )  
(()/( ( )\  (()/( (    )\))(   ' (   ( )\ (()/( (   (()/( (   (   (   (()/(  
 /(_)))((_)  /(_)))\  ((_)()\ )  )\  )((_) /(_)))\   /(_)))\  )\  )\   /(_)) 
(_)) ((_)_  (_)) ((_) _(())\_)()((_)((_)_ (_)) ((_) (_)) ((_)((_)((_) (_))   
/ __| / _ \ | |   (_) \ \((_)/ /| __|| _ )/ __|| __|| _ \\ \ / / | __|| _ \  
\__ \| (_) || |__ | |  \ \/\/ / | _| | _ \\__ \| _| |   / \ V /  | _| |   /  
|___/ \__\_\|____||_|   \_/\_/  |___||___/|___/|___||_|_\  \_/   |___||_|_\  
        </pre>
        <h4>A deliberately vulnerable web application containing 15 different examples of SQLI.</h4>
        <!-- <pre>
                             .-"""""-.
                            /\ /\ /\ /\
                           (  _ ._. _  )
                            '. V   V .'
                             | >===< |
                             | >===< |
                           __| >===< |__
                     _..-"X, | >===< | ,X"-.._ 
                _.-"`Xx,   'X; >===< ;X'   ,xX`"-._
            _.'`X.    'Xx.  'X,>===<,X'  .xX'    .X`._
          .'X    `X,   'Xx   'X === X'   xX'   ,X'   X'.
        .xXXXXx,   'X    'Xx  'X = X'  xX'    X'   ,xXXXXx.
      .'       'X.   'X   'Xx  'X X'  xX'   X'   .X'       '.
    .xXXXXXXXXXXXXX,  `Xx. 'Xx, .X. ,xX' .xX'  ,XXXXXXXXXXXXXx.
   /               `X   XX  'XX//^\\XX'  XX   X`               \
  /XXXXXXXXXXXXXXXXXXX   XX  'X\\_//X'  XX   XXXXXXXXXXXXXXXXXXX\
 /                    X_.XX___XX'='XX___XX._X                    \
 |XXXXXXXXXXXXXXXXXXX.'                     '.XXXXXXXXXXXXXXXXXXX|
 |                  /                         \                  |
 |XXXXXXXXXXXXXXXXX/   ..::::.       .::::..   \XXXXXXXXXXXXXXXXX|
 |                /  .'       '     '       '.  \                |
 /XXXXXXXXXXXXXXXX|  _.-"```"-.     .-"```"-._  |XXXXXXXXXXXXXXXX\
|             .==.;   '._(')_.'\   /'._(')_.'   ;.==.             |
|XXXXXXXXXXX.'.-, |            |   |            | ,-.'.XXXXXXXXXXX|
|           |; (               |   |               ) ;|           |
|XXXXXXXXXXX|;  `,            /    .\            ,'  ;|XXXXXXXXXXX|
|           ;;'--            ( _   _ )            --';;           |
|XXXXXXXXXXXX\' o             `"`-`"`             o '/XXXXXXXXXXXX|
|             '-J-'|            : :            |'-L-'             |
|XXXXXXXXXXXXXX(_)X\          __   __          /X(_)XXXXXXXXXXXXXX|
|                   \      .-'  `'`  '-.      /                   |
|XXXXXXXXXXXXXXXXXXXX\    `-:""""""""":-`    /XXXXXXXXXXXXXXXXXXXX|
|                     \      `-.....-'      /                     |
|XXXXXXXXXXXXXXXXXXXXXX'.                 .'XXXXXXXXXXXXXXXXXXXXXX|
 \                       `;-._       _.-;`                       /
  \XXXXXXXXXXXXXXXXXXXXXXX|   `}}}}}`   |XXXXXXXXXXXXXXXXXXXXXXX/
   '.                     |    {{{{{    |                     .'
     '.XXXJGSXXXXXXXXXXXXX|     }}}     |XXXXXXXXXXXXXXXXXXX.'
       \                  |      }      |                  /
        'XXXXXXXXXXXXXXXXX|      }      |XXXXXXXXXXXXXXXXX'
         \                |             |                /
          'XXXXXXXXXXXXXXX|             |XXXXXXXXXXXXXXX'
           \              |             |              /
            \XXXXXXXXXXXXX|             |XXXXXXXXXXXXX/
            |             |             |             |
            |XXXXXXXXXXXXX|             |XXXXXXXXXXXXX|
            |             |             |             |
            |XXXXXXXXXXXXX|             |XXXXXXXXXXXXX|
            \             |             |             /
             'XXXXXXXXXXXX|             |XXXXXXXXXXXX'
               `-.________/             \________.-`
</pre> -->
        <?php
            
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
        ?>
        <!--  -->
        <!-- inputs to be inserted -->
        <!--  -->
    <pre>
.-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
/ / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ 
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'  `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
</pre>
<h2>Test Context Escape - Query Feedback</h2>
<h3>Tasks 1 - 10. These input fields include a variety of different SQL statements to exploit, without any sanitation to user inputs. </h3>

<pre>
.-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
/ / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ 
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'  `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
</pre>
<h2> Task 1</h2>

<!-- select -->
 <form action="functions_external/sqli1.php" method="get">
  ID <input type="text" name="id"></br></br>
              <input type="hidden" name="difficulty" id="difficulty" value="exec">

              Feedback
  Submit Request: <button type="submit">Go</button>
</form>

    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>



    <h2> Task 2</h2>


        <!-- select -->
        <form action="functions_external/sqli2.php" method="get">
            Name <input type="text" name="name"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Go</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 3</h2>

        <!-- update statement -->
    <form action="functions_external/sqli3.php" method="post">
            Password <input type="text" name="pass"></br></br>
              <input type="hidden" name="difficulty" id="difficulty" value="exec">

            Feedback
            Submit Request: <button type="submit">Update</button>
        </form> 
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 4</h2>


        <!-- insert -->
         <form action="functions_external/sqli4.php" method="post">
            Name <input type="text" name="name"></br></br>
            
            <input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Create</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
  </pre>
  <h2> Task 5</h2>


<!-- select -->
 <form action="functions_external/sqli5.php" method="get">
  Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
        Feedback
  Submit Request: <button type="submit">Go</button>
</form>


<pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
  </pre>
  <h2> Task 6</h2>


<!-- select -->
 <form action="functions_external/sqli6.php" method="get">
  Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
  Submit Request: <button type="submit">Go</button>
</form>

  <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
  </pre>
  <h2> Task 7 </h2>


  <!-- select -->
   <form action="functions_external/sqli7.php" method="get">
    Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
    Submit Request: <button type="submit">Go</button>
  </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 8</h2>


<!-- select -->
 <form action="functions_external/sqli8.php" method="get">
  Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
  Submit Request: <button type="submit">Go</button>
</form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
  <h2> Task 9</h2>


  <!-- select -->
   <form action="functions_external/sqli9.php" method="get">
    Name <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
    Submit Request: <button type="submit">Go</button>
  </form>
  <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
  </pre>
  <h2> Task 10</h2>


  <!-- select -->
   <form action="functions_external/sqli10.php" method="get">
    Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
    Submit Request: <button type="submit">Go</button>
  </form>
<pre>


.-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
/ / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ 
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'  `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
</pre>
<h1>Test Sanitisation</h2>
    <h3>Tasks 11 - 15. These input fields include a variety of different SQL statements to exploit, with sanitation to user inputs. </h3>
<pre>
.-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
/ / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ 
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'  `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
</pre>
    <h2> Task 11 </h2>

        <!-- select with mysqli escape and no quotes -->
         <form action="functions_external/sqli11.php" method="get">
            ID <input type="text" name="id"></br></br>
            <input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 12 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli12.php" method="get">
            ID <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 13 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli13.php" method="get">
            ID <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 14 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli14.php" method="get">
            ID <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
    <h2> Task 15 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli15.php" method="get">
            Name <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
            <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 16 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli16.php" method="get">
            Name <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 17 </h2>


         <form action="functions_external/sqli17.php" method="get">
            Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get Name</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 18 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli18.php" method="get">
            Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 19 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli19.php" method="get">
            
</br>            Name2 <input type="text" name="name2">

</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 20 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli20.php" method="get">
</br>            ID <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 21 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli21.php" method="get">

         ID <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 22 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli22.php" method="get">
</br>            ID <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 23 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli23.php" method="get">
            Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 24 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli24.php" method="get">
            Name <input type="text" name="name">
</br></br>   
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
             </form><pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 25 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli25.php" method="get">
            Name <input type="text" name="name">
</br></br>   
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
            </form> <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        
        <h2> Task 26 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli26.php" method="get">
            Name <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 27 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli27.php" method="get">
            Name <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 28 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli28.php" method="post">

            Name <input type="text" name="name"></br>
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
                <h2> Task 29 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli29.php" method="get">
            Name <input type="text" name="name">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>    <pre>
    .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
 / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
    </pre>
        <h2> Task 30 </h2>


        <!-- select with special escape keywords-->
         <form action="functions_external/sqli30.php" method="get">
            Name <input type="text" name="id">
</br></br>
<input type="hidden" name="difficulty" id="difficulty" value="exec">
            Feedback
            Submit Request: <button type="submit">Get ID</button>
        </form>
    </body>
</html>
