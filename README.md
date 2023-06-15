

# SQIRL: Grey-Box Detection of SQL Injection Vulnerabilities Using Reinforcement Learning

Web security scanners are commonly used to discover SQL injection vulnerabilities in deployed web applications. Scanners tend to use static sets of rules to cover the most common injection cases, missing diversity in their payloads leading to a high volume of requests and false negatives. Moreover, in order to detect web application vulnerabilities, scanners often rely on error messages or other significant feedback on the web application pages, which are the result of additional insecure programming practices by web developers. In this paper, we develop SQIRL, a novel approach to detecting SQL injection vulnerabilities based on deep reinforcement learning, using multiple worker agents. Each worker intelligently fuzzes the input fields discovered by an automated crawling component. This approach generates a more varied set of payloads than existing scanners, leading to the discovery of more vulnerabilities. Moreover, SQIRL attempts fewer payloads, because they are generated in a targeted fashion. SQIRL finds all vulnerabilities in our novel SQLi MicroBenchmark for SQL injection, with substantially fewer requests than most of the state-of-the-art scanners compared with. We further run SQIRL on a set of production grade web applications and discover 33 vulnerabilities, with zero false positives, in 14 websites. We have responsibly disclosed the novel vulnerabilities and currently obtained 6 CVEs for them.




## Initial Setup - mysql
First, a web application and database need to be setup, which requires php and mysql.

Currently the tool has drivers to mysql, to allow the tool to connect to the mysql db logs, the general mysql logs need to be enabled, see:
```
 https://dev.mysql.com/doc/refman/8.0/en/query-log.html#:~:text=To%20disable%20or%20enable%20the,or%20ON%20)%20to%20enable%20it.
```
This can generally be achieved by running the flowing in mySQL:
```bash
SET GLOBAL general_log = 'ON';
```
The log file location can then be found by running:
```
mysql -se "SHOW VARIABLES" -u root -p | grep -e general_log
```

Alter the permissions of the general log 
```
chmod 755 /path/to/general_log_dir
chmod 755 /path/to/general_log_dir/general.log
```

For the given web application, create the associated user and table in mySQL:

```bash
CREATE USER 'server'@'localhost' IDENTIFIED BY 'Qazwsxedcr12@';
CREATE DATABASE sqliDB;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(500) DEFAULT NULL,
  `pass` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
);
GRANT ALL PRIVILEGES ON sqliDB.users TO 'server'@'localhost';
```

## Inital Setup - SQLiMicroBenchmark

To run the SQLiMicroBenchmark first install the [docker](https://docs.docker.com/engine/install/) engine, then run the following from the SQLiMicrobenchmark directory.
```
docker compose up -d 
```
This will create the SQLiMicrobenchmark which can be accessed from [http:localhost:8000](http:localhost:8000). The first time this runs it will create new files in the `SQLiMicrobenchmark/mysql` directory. It may be required to change the permissions of the `general.log` in this directory the first time this is created which can be done as:
```
chmod +777 general.log
```

## Inital Setup - SQIRL

SQIRL runs using python Python 3.8.16, and the requirements can be installed from root directory using pip:
```
pip3 install -r requirements.txt
```

### Note:
SQIRL uses curses for the GUI, for linux no installation needed but for windows some installation of curses is needed, please look at:
```
pip3 install windows-curses
```


## Running SQIRL
The code contains the four variants SQIRL in addition to its random equivalent :
- (0) Random 
- (1) DQN
- (2) DQN_RND
- (3) One_Hot_Encoder_DQN
- (4) Worker_DQN_RND

SQIRL has several command line arguments to alter its behaviour:
```
# Crawling flags
--url (-u) 							# Start URL
--level									# Depth for the crawler to traverse
--login_function_name		# Function name for the authentication module in --auth_file_path
--auth_file_path				# Path to the .py file used for authentication

# Database flags
--log_file							# Path to the log file of the SQL database
--db_type								# Type of Database e.g. mysql

# Agent Flags 
--agent_unique_id (-i)	# ID of the agent used for logging
--agent 								# SQIRL Variant: 0 for Random, 1 for DQN, 2 for DQN_RND, 3 for One_Hot_Encoder_DQN_RND, 4 for Worker_DQN_RND
--learning							# Boolean to set if SQIRL is in learning mode

# Environment Flags 
--episodes (-e)					# Maximum number of episodes per input found
--max_timestamp					# Maximum timesteps per episode
--win_criteria					# Minimum number of vulnerabilities found before switching inputs
--loss_criteria					# Maximum number of episodes before switching inputs
--input_selection				# Method to select next input: 1 FIFO queue, 2 is random
--verbose (-v)			 		# Set verbose level 0, 1, 2
```

### Authentication
SQIRL can be authenticated with a web application using a user defined python module. Examples are shown in `Envrionment/logins/login_examples.py`. These modules must take as input a requests.Session object and also return a requests.Session object. SQIRL loads the module using the following parameters:
```
--auth_file_path			# Path to the .py file used for authentication
--log_file					# Path to the log file of the SQL database
```

### Centralised Agents (1-3)
The centrlized agents can simply run by navigating to Code, then run:
```
python3 sqirl.py -i 1 URL -v 2 --log_file LOG_FILE_POINTER --agent AGENT_TYPE
```
example:
```
python3 sqirl.py -i 1 -u http://localhost:8000/no_feedback.php -v 2 --log_file /path/to/mysql/log.log --agent 2
```
### Non-Centralised Agents (4)
SQIRL is also designed to run with a number of worker agents with a centralised agent. The sever with the centralised agent needs to be run first. The federation server has one parameter:
- -u | --users: number of clients/workers


```
python3 Worker_DQN_RND_Server.py -u NUMBER_OF_CLIENTS
```
Each of the worker agents can then be run from an alternative terminal following the instructions for the Centralised Agents:
```
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --agent 2 --loss_critera 9999999 --win_criteria 14 --agent 4 -i 1
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --agent 2 --loss_critera 9999999 --win_criteria 14 --agent 4 -i 2
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --agent 2 --loss_critera 9999999 --win_criteria 14 --agent 4 -i 3
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --agent 2 --loss_critera 9999999 --win_criteria 14 --agent 4 -i 4
```         

## Log files

During each run the agent will produce and save details of its generation including the payload, sql, reward etc for analysis, all of the log files are named based on the agent id supplied (--agent). All of the logs are available at stats_log.

## Pretrained models

We include the DQN and Worker_DQN Agent models.

## Training SQIRL 
To train the variants of sqirl 
```
# DQN agent
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --loss_critera 9999999 --win_criteria 14 --agent 1
# DQN agent using RND
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --loss_critera 9999999 --win_criteria 14 --agent 2
# DQN agent using a one-hot-encoded input space 
python3 sqirl.py -i 1 -u http://localhost:8000/training.php -v 2 --log_file /path/to/mysql/log.log --loss_critera 9999999 --win_criteria 14 --agent 3

```

Please cite this work as:
```

@inproceedings{sqirl_2023,
	title = {{SQIRL}: {Grey}-{Box} {Detection} of {SQL} {Injection} {Vulnerabilities} {Using} {Reinforcement} {Learning}},
	language = {en},
	booktitle = {Proceedings of the 32nd {USENIX} {Security} {Symposium}},
	author = {Al-Wahaibi, Salim and Foley, Myles and Maffeis, Sergio},
	month = aug,
	year = {2023},
	pages = {18},
}

```

