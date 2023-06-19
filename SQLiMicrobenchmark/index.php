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
        <h4>A deliberately vulnerable web application containing 30 different examples of SQLI.</h4>
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
    <pre>
.-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
/ / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ 
`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'  `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
</pre>
        There are three vulnerable versions of this that provide different levels of feedback:
    <ul>
        <li>
            <a href="no_feedback.php"> No feedback of any Kind (Vulnerable)</a>
        </li> 
          <li>
            <a href="feedback.php"> Feedback on the SQL query (Vulnerable)</a>
        </li> 
        <li>
            <a href="exception.php"> Feedback on the Exception (Vulnerable)</a>
        </li> 

    </ul>
        There are three non-vulnerable versions of this that provide different levels of feedback:
    <ul>     
        <li>
            <a href="non_vuln_no_feedback.php"> No feedback of any Kind (Non-Vulnerable)</a>
        </li> 
          <li>
            <a href="non_vuln_feedback.php"> Feedback on the SQL query (Non-Vulnerable)</a>
        </li> 
        <li>
            <a href="non_vuln_exception.php"> Feedback on the Exception (Vulnerable)</a>
        </li> 
    </ul>
        Finally there is the vulnerable samples used in training:
    <ul>
        <li>
            <a href="non_vuln_exception.php"> Feedback on the Exception (Vulnerable)</a>
        </li> 
    </ul>

    </body>
</html>
