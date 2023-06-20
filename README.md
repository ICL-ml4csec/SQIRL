
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
chmod +rw /path/to/general_log_dir/general.log
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
- (4) Worker_DQN_RND - SQIRL

SQIRL has several command line arguments to alter its behaviour:
```
# Crawling flags
--url (-u) 					# Start URL
--level						# Depth for the crawler to traverse
--login_function_name				# Function name for the authentication module in --auth_file_path
--auth_file_path				# Path to the .py file used for authentication

# Database flags
--log_file					# Path to the log file of the SQL database
--db_type					# Type of Database e.g. mysql

# Agent Flags 
--agent 					# SQIRL Variant: 0 for Random, 1 for DQN, 2 for DQN_RND, 3 for One_Hot_Encoder_DQN_RND, 4 for Worker_DQN_RND. Must be set if --model_dir is not.
--model_dir 					# Directory containing model checkpoints, SQIRL will detect the type of agent from the directory it is saved in. Must be set if --agent is not. 
--num_agents (-i)				# Number of agents to be used for testing, this is always 1 for agents 1-3, but can be more for agent type 4
--learning					# Boolean to set if SQIRL is in learning mode


# Environment Flags 
--episodes (-e)					# Maximum number of episodes per input found
--max_timestamp					# Maximum timesteps per episode
--win_criteria					# Minimum number of vulnerabilities found before switching inputs
--loss_criteria					# Maximum number of episodes before switching inputs
--input_selection				# Method to select next input: 1 FIFO queue, 2 is random
--verbose (-v)			 		# Set verbose level 0, 1, 2
--gui						# Set flag to enable GUI mode in the terminal, default is off, not used for agent type 4
```

### Authentication
SQIRL can be authenticated with a web application using a user defined python module. Examples are shown in `Envrionment/logins/login_examples.py`. These modules must take as input a requests.Session object and also return a requests.Session object. SQIRL loads the module using the following parameters:
```
--auth_file_path			# Path to the .py file used for authentication
--log_file					# Path to the log file of the SQL database
```

### Invoking Agents (1-4)
The centrlized agents can simply run by navigating to Code, then run:
```
python3 sqirl.py -i 1 URL -v 2 --log_file LOG_FILE_POINTER --agent AGENT_TYPE
```
example:
```
python3 sqirl.py -i 1 -u http://localhost:8000/no_feedback.php -v 2 --log_file ./SQLiMicrobenchmark/mysql/general.log --agent 2
```
#### Agent 4 - SQIRL 
SQIRL is also designed to run with a number of worker agents with a centralised agent. This can be run in the same way as the decentralised agents: 
```
python3 sqirl.py -i 2 -u http://localhost:8000/no_feedback.php -v 2 --log_file ./SQLiMicrobenchmark/mysql/general.log --agent 4 
```
This will start python subprocesses for the centralised agent server by calling:
```
python3 Worker_DQN_RND_Server.py -u 2 
```
Then each of the worker agents will be started as subprocesses via the following commands:
```
python3 sqirl_subprocess.py -u http://localhost:8000/no_feedback.php --log_file ./SQLiMicrobenchmark/mysql/general.log --agent 4 -i 1
python3 sqirl_subprocess.py -u http://localhost:8000/no_feedback.php --log_file ./SQLiMicrobenchmark/mysql/general.log --agent 4 -i 2
```         
Note that the main file `sqirl.py` will do this in the background, requiring no additonal commands to be run by the user.

## Log files

During each run the agent will produce and save details of its generation including the payload, sql, reward etc for analysis, all of the log files are named based on the agent id supplied (--agent). All of the logs are available at stats_log.

## Pretrained models

Pretrained models can be found in the directory `RL_Agents/pretrained_agents`. SQIRL will try by default to load agents from this directory.

## Training SQIRL 
To train the variants of sqirl 
```
# DQN agent
python3 sqirl.py -u http://localhost:8000/training.php -v 2 --log_file ./SQLiMicrobenchmark/mysql/general.log --loss_criteria 9999999 --win_criteria 14 --agent 1
# DQN agent using RND
python3 sqirl.py -u http://localhost:8000/training.php -v 2 --log_file ./SQLiMicrobenchmark/mysql/general.log --loss_criteria 9999999 --win_criteria 14 --agent 2
# DQN agent using a one-hot-encoded input space 
python3 sqirl.py -u http://localhost:8000/training.php -v 2 --log_file ./SQLiMicrobenchmark/mysql/general.log --loss_criteria 9999999 --win_criteria 14 --agent 3
python3 sqirl.py -u http://localhost:8000/training.php -v 2 --log_file ./SQLiMicrobenchmark/mysql/general.log --loss_criteria 9999999 --win_criteria 14 --agent 4
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
