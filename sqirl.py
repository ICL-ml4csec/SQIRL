import os
os.environ["NLTK_DATA"] = 'SQIRL/nltk_data'
import signal
import sys
import optparse
import time
import traceback
from RL_Agent.sqirl_core import sqirl_cli as sqril_cmd
import subprocess
import threading
from curses import wrapper, endwin


class sqirl_subprocess(object):
    def __init__(self, args, name):
        self.thread = threading.Thread(target=sqril_cmd, args=args, name=name)
        self.thread.daemon = True
        self.thread.start()


if __name__ == '__main__':
    '''
        main execution of the tool
    '''
    if len(sys.argv) < 2:
        print("You need to specify a URL to scan. Use --help for all options.")
        sys.exit()
    else:
        parser = optparse.OptionParser()

        parser.add_option('-u', '--url',
                          action="store", dest="url",
                          help="Full URL to crawl", default=None)

        parser.add_option('--gui',
                          action="store_false", dest="gui",
                          help="Use the SQIRL gui if the flag is set")

        parser.add_option('-i', '--num_agents',
                          action="store", dest="num_agents",
                          help="Number of agents to run with SQIRL is 1 unless Worker structure invoked", default=1)

        parser.add_option('--level',
                          action="store", dest="level",
                          help="Depth for the crawler to traverse", default="0")

        parser.add_option('--db_type',
                          action="store", dest="db_type",
                          help="Type of Database e.g. mysql", default="mysql")

        parser.add_option('--log_file',
                          action="store", dest="log_file",
                          help="Path to the log file of the SQL database", default=None)

        parser.add_option('--learning',
                          action="store", dest="learning",
                          help="does the agent learn", default=True)

        parser.add_option('-e', '--episodes',
                          action="store", dest="episodes",
                          help="Maximum number of episodes per input found", default=10)

        parser.add_option('--max_timestamp',
                          action="store", dest="max_timestamp",
                          help="Maximum timesteps per episode", default=10)

        parser.add_option('--win_criteria',
                          action="store", dest="win_criteria",
                          help="Minimum number of vulnerabilities found before switching inputs", default=1)

        parser.add_option('--loss_criteria',
                          action="store", dest="loss_criteria",
                          help="Maximum number of episodes before switching inputs", default=10)

        parser.add_option('-v', '--verbose',
                          action="store", dest="verbose",
                          help="Set verbose level 0, 1, 2", default="0")

        parser.add_option('--input_selection',
                          action="store", dest="input_selection",
                          help="Method to select next input: 1 FIFO queue, 2 is random", default=2)

        parser.add_option('--agent',
                          action="store", dest="agent_type",
                          help="SQIRL Variant: 0 for Random, 1 for DQN (DEFAULT), 2 for DQN_RND, 3 for One_Hot_Encoder_DQN_RND, 4 for Worker_DQN_RND.",
                          default=None)
        
        parser.add_option( '--model_dir',
                            action="store", dest="model_dir",
                            help="Directory containing model checkpoints, if not set a new agent will begin training", default=None)
        
        parser.add_option('--login_function_name',
                          action="store", dest="login_function",
                          help="Function name for the authentication module in --auth_file_path",
                          default=None)
        parser.add_option('--auth_file_path',
                          action="store", dest="module_path",
                          help="Path to the .py file used for authentication",
                          default=None)
        
        options, args = parser.parse_args()
        if options.url == None:
            raise Exception("--url cannot be None")
        target_url = str(options.url)
        max_depth = str(options.level)
        verbose = int(options.verbose)
        db_type = str(options.db_type)
        if options.log_file == None:
            raise Exception("--log_file file cant be None")
        if options.login_function != None and options.module_path == None or \
            options.login_function == None and options.module_path != None:
            raise Exception("If using authentication both --login_function_name and --auth_file_path must be set.")
        else:
            login_module = {'module_path':options.module_path, 'function':options.login_function }

        if options.model_dir != None and options.agent_type != None or \
            options.model_dir == None and options.agent_type == None:
            raise Exception("Please set only one of --model_dir (if you want to load a previous model), or '--agent if you wish to train a new agent")
        
        log_file = str(options.log_file)
        model_dir = options.model_dir
        is_learning = bool(options.learning)
        no_episodes = int(options.episodes)
        max_timestamp = int(options.max_timestamp)
        win_criteria = int(options.win_criteria)
        loss_criteria = int(options.loss_criteria)
        crawler_input = (target_url, max_depth)
        sql_proxy_input = (db_type, log_file)
        num_agents = str(options.num_agents)
        input_selection = int(options.input_selection)
        agent_type = int(options.agent_type) if options.agent_type != None else -1
        if agent_type == 4 or (model_dir is not None and 'Worker_DQN_RND_Client 'in model_dir):
            try:
                print('starting worker server')
                if model_dir is not None:
                    sub_pro = subprocess.Popen(['python3', 'Worker_DQN_RND_Server.py', '-u', num_agents, '--model_dir', model_dir])
                else:
                    sub_pro = subprocess.Popen(['python3', 'Worker_DQN_RND_Server.py', '-u', num_agents])
                    time.sleep(2)
                for agent_id in range(1, int(num_agents)+1):
                    call = ['python3', 'sqirl_subprocess.py', '-u', str(target_url), '-i', str(agent_id), '--level', str(max_depth), '--db_type', str(db_type), '--log_file', str(log_file), '--learning', str(is_learning), '-e', str(no_episodes), '--max_timestamp', str(max_timestamp), '--win_criteria', str(win_criteria), '--loss_criteria', str(loss_criteria), '-v', str(verbose), '--input_selection', str(input_selection)]
                    if options.login_function is not None:
                        call.extend(['--login_function_name', str(options.login_function), '--auth_file_path', str(options.module_path)])
                    if model_dir is not None:
                        call.extend(['--model_dir', str(model_dir)])
                    else:
                        call.extend(['--agent', '4'])
                    subprocess.call(call)

                
                os.killpg(os.getpgid(sub_pro.pid), signal.SIGTERM)
            except Exception as e:
                print(e)
                traceback.print_exc()
                os.killpg(os.getpgid(sub_pro.pid), signal.SIGTERM)

        elif options.gui:
            if int(num_agents) > 1:
                print(f'Setting --num_agents to 1')
                num_agents = 1
            log_output = sqril_cmd(print,target_url, max_depth, verbose, db_type,log_file, model_dir, is_learning, no_episodes, max_timestamp, win_criteria, loss_criteria, crawler_input, sql_proxy_input, num_agents, input_selection, agent_type, login_module)
            print(f'SQIRL RUN COMPLETE, PLEASE CONSULT DIRECTORY: {log_output}')
        else:
            try:
                if int(num_agents) > 1:
                    print(f'Setting --num_agents to 1')
                    num_agents = 1
                log_output = wrapper(sqril_cmd, target_url, max_depth, verbose, db_type,log_file, model_dir, is_learning, no_episodes, max_timestamp, win_criteria, loss_criteria, crawler_input, sql_proxy_input, num_agents, input_selection, agent_type, login_module)
                print(f'SQIRL RUN COMPLETE, PLEASE CONSULT DIRECTORY: {log_output}')
            except Exception as e:
                endwin()
                print(e)
                traceback.print_exc()


