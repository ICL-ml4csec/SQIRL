from copy import deepcopy
import os
import socket
import struct
import time
from Environment.Environment import Game_Type, SQLI_Environment
from Manual_Agent.Agent_Random import Agent_Random
from RL_Agent.Agents.DQN_Agent.Agent_2 import Agent_2
from RL_Agent.Agents.DQN_RND_Agent.Agent_6 import Agent_6
from RL_Agent.Agents.One_Hot_Encoder_DQN_Agent.Agent_8 import Agent_8
from RL_Agent.Agents.Worker_DQN_RND_Client.Agent_11 import Agent_11
import numpy as np


def sqirl_cli(print_func,target_url, max_depth, verbose, db_type,log_file, model_dir, is_learning, no_episodes, max_timestamp, win_criteria, loss_criteria, crawler_input, sql_proxy_input, agent_unique_id, input_selection, agent_type, login_module):

    if print_func == print:
    	add_logo(print)
    	print("Initialise Environment...\n")
    else:
    	print_func.clear()
    	print_func.refresh()
    	add_logo(print_func.addstr)
    	print_func.addstr("Initialise Environment...\n")
    	print_func.refresh()

    # create instance of env
    is_federated = True if agent_type == 4 else False
    env = SQLI_Environment(False, is_federated, crawler_input, sql_proxy_input, input_selection, login_module,verbose)
    env.reset(change_input=False)
    num_inputs = deepcopy(env.total_inputs)
    no_episodes = int(no_episodes) * num_inputs
    if print_func == print:
    	print("Initialise Agent...")
    else:
    	print_func.addstr("Initialise Agent...")
    	print_func.refresh()
    
    save_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    domain = env.current_input_entry.input.action.split('/')[2]
    log_location = f'./stats_logs/{domain}_{save_time}'
    if agent_type != 4:
        os.makedirs(f'./stats_logs/{domain}_{save_time}')
        os.rename("./stats_logs/all_inputs_found.stat",f"{log_location}/all_inputs_found.stat")
   
    
    # create instance of agent based on supplied agent type
    if agent_type == 0: #Random
        agent = Agent_Random(agent_unique_id)
    elif agent_type == 1 or (model_dir is not None and 'DQN_Agent' in model_dir):#DQN
        if model_dir is None:
            model_dir = os.path.join("/RL_Agent","pretrained_agents","DQN_Agent")
            model_dir = os.path.abspath(os.getcwd() + model_dir)
        model_checkpoint_file = os.path.join(os.getcwd(), log_location,"DQN_Agent_Checkpoint")
        model_checkpoint_file = os.path.abspath(model_checkpoint_file)
        agent = Agent_2(agent_unique_id,model_checkpoint_file,learning=is_learning, load=model_dir)
    elif agent_type == 2 or (model_dir is not None and 'DQN_RND_Agent' in model_dir):#DQN_RND
        if model_dir is None:
            model_dir = os.path.join("/RL_Agent","pretrained_agents","DQN_RND_Agent")
            model_dir = os.path.abspath(os.getcwd() + model_dir)
        model_checkpoint_file = os.path.join(os.getcwd(), log_location,"DQN_RND_Agent_Checkpoint")
        model_checkpoint_file = os.path.abspath(model_checkpoint_file)
        agent = Agent_6(agent_unique_id,model_checkpoint_file,learning=is_learning, load=model_dir)
    elif agent_type == 3 or (model_dir is not None and 'One_Hot_Encoder_DQN_Agent' in model_dir):#One_Hot_Encoder_DQN_RND
        if model_dir is None:
            model_dir = os.path.join("/RL_Agent","pretrained_agents","One_Hot_Encoder_DQN_Agent")
            model_dir = os.path.abspath(os.getcwd() + model_dir)
        model_checkpoint_file = os.path.join(os.getcwd(), log_location,"One_Hot_Encoder_DQN_Agent_Checkpoint")
        model_checkpoint_file = os.path.abspath(model_checkpoint_file)
        agent = Agent_8(agent_unique_id,model_checkpoint_file,learning=is_learning, load=model_dir)
    elif agent_type == 4 or (model_dir is not None and 'Worker_DQN_RND_Client 'in model_dir):#Worker_DQN_RND
        agent = Agent_11(agent_unique_id,learning=is_learning, domain=domain)
        log_location = agent.syntax_fixing_agent.action_Q_value.save_dir_mem.split('/Checkpoint')[0]
        os.rename("./stats_logs/all_inputs_found.stat",f"./{log_location}/all_inputs_found.stat")
    else:
        if model_dir is None:
            model_dir = os.path.join("/RL_Agent","pretrained_agents","DQN_Agent")
            model_dir = os.path.abspath(s.getcwd() + model_dir)
        model_checkpoint_file = os.path.join(os.getcwd(), log_location,"DQN_Agent_Checkpoint")
        model_checkpoint_file = os.path.abspath(model_checkpoint_file)
        agent = Agent_2(agent_unique_id,model_checkpoint_file,learning=is_learning, load=model_dir)
    if print_func == print:
    	print(f"Log output location: {os.path.abspath(os.path.join(os.getcwd(), log_location))}")
    else:
        print_func.addstr(f"Log output location: {os.path.abspath(os.path.join(os.getcwd(), log_location))}")
        print_func.refresh()
        
   

    # get all_actions_dic
    all_actions = None
    q_value_all_actions = None

    stat_report = []

    reached_win_criteria = False
    reached_loss_criteria = False
    current_wins = 0
    current_losses = 0
    total_no_wins = 0
    total_no_losses = 0
    trials = 0
    last_injection_win = None

    results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "w+")
    results_file.close()

    results_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "w+")
    results_file.close()

    total_wins = []

    training_loss = {Game_Type.BEHAVIOR_CHANGING: {"action": [], "range": [], "type": []},
                     Game_Type.SANITIZATION_ESCAPING: {"action": [], "range": [], "type": []},
                     Game_Type.SYNTAX_FIXING: {"action": [], "range": [], "type": []}}

    results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
    results_file.write(f"---------------------Training-----------------\n")
    results_file.close()

    results_file = open(os.path.join(log_location, f"timing_{agent_unique_id}.stats"), "a+")
    results_file.close()

    results_file = open(os.path.join(log_location, f"actions_Applied_{agent_unique_id}.stats"), "w+")
    results_file.close()

    sql_statment_file = open(os.path.join(log_location, f"sql_statment_{agent_unique_id}.stats"), "w+")
    sql_statment_file.close()

    results_file = open(os.path.join(log_location, f"rewards_{agent_unique_id}.stats"), "w+")
    results_file.close()
    avg_time_taken = 0

    seen_pairs = {}
    # playing loop
    for current_episode in range(no_episodes):

        sql_statment_file = open(os.path.join(log_location, f"sql_statment_{agent_unique_id}.stats"), "a")
        sql_statment_file.write(f"---------------------ep{current_episode}-----------------\n")
        sql_statment_file.write(f"\n")
        sql_statment_file.close()

        # reset the environment to initialise to next input
        current_game, current_state = env.reset(change_input=reached_win_criteria or reached_loss_criteria)

        stat_log_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "a")
        stat_log_file.write(f"\n\n---------------------ep{current_episode}-----------------\n")
        stat_log_file.write(f"[!] Input: {env.current_input_entry.input.action}\n")
        stat_log_file.close()

        results_file = open(os.path.join(log_location, f"actions_Applied_{agent_unique_id}.stats"), "a")
        results_file.write(f"---------------------ep{current_episode}-----------------\n")
        results_file.close()
        if current_episode == 0:
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            results_file.write(
                f"[!] Starting to input {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]},{env.current_input_entry.input.action}\n")
            results_file.close()
            seen_pairs[env.current_input_entry.input.action] = [param['name'] for param in
                                                                env.current_input_entry.input.inputs if
                                                                param['input_use'] == 'injection_point']

        elif (reached_win_criteria or reached_loss_criteria):
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            results_file.write(
                f"[!] Changing to input {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]},{env.current_input_entry.input.action}\n")
            results_file.close()
            stat_log_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "a")
            stat_log_file.write(
                f"[!] CHANGING TO: {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]},{env.current_input_entry.input.action}\n")
            stat_log_file.close()
            if env.current_input_entry.input.action in seen_pairs:
                if [param['name'] for param in env.current_input_entry.input.inputs if
                    param['input_use'] == 'injection_point'][0] in seen_pairs[env.current_input_entry.input.action]:
                     continue
                seen_pairs[env.current_input_entry.input.action].append(
                    [param['name'] for param in env.current_input_entry.input.inputs if
                     param['input_use'] == 'injection_point'][0])
            else:
                print(
                    f"Testing: {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]}, {env.current_input_entry.input.action}")
                seen_pairs[env.current_input_entry.input.action] = [param['name'] for param in
                                                                    env.current_input_entry.input.inputs if
                                                                    param['input_use'] == 'injection_point']

        sql_statment_file = open(os.path.join(log_location, f"sql_statment_{agent_unique_id}.stats"), "a")
        if current_state['error']:
            sql_statment_file.write(f"Base: None\n")
        else:
            sql_statment_file.write(f"Base: {current_state['sql']}\n")
        sql_statment_file.write(f"\n")
        sql_statment_file.close()

        if all_actions is None:
            all_actions = env.get_all_actions(max_timestamp)
            q_value_all_actions = deepcopy(all_actions)

        # reset env to for next targeted input state
        if reached_win_criteria or reached_loss_criteria:
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            reached_win_criteria = False
            reached_loss_criteria = False
            current_wins = 0
            current_losses = 0
            trials = 0

        # apply policy until goal reached (terminate state) or max timestamp
        max_timestamp_reached = False
        game_done = False
        current_time_stamp = 0
        last_state = current_state
        current_time = time.time()

        while (not game_done and not max_timestamp_reached):
            # get next action
            # print(current_state)

            selected_action, q_value = agent.get_next_action(current_state)

            # increment counter of visiting the state
            all_actions[str([selected_action["action"], selected_action["range"][0], selected_action["type"]])][
                current_time_stamp] += 1

            # add q_value
            if q_value is not None:
                q_value_all_actions[
                    str([selected_action["action"], selected_action["range"][0], selected_action["type"]])][
                    current_time_stamp] += q_value

            # perform action and get next state and reward
            current_game, current_state, reward, game_done = env.step(selected_action)
            results_file = open(os.path.join(log_location, f"actions_Applied_{agent_unique_id}.stats"), "a")
            results_file.write(f'{current_time_stamp}: {current_state["payload"]}\n')
            results_file.write(f"\n")
            results_file.close()

            stat_log_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "a")
            stat_log_file.write(f"{current_time_stamp}:Payload: {current_state['payload']}\n")
            stat_log_file.write(f"{current_time_stamp}:Available actions: {current_state['actions']}\n")
            stat_log_file.write(f"{current_time_stamp}:CURRENT GAME: {current_state['game']}\n")
            stat_log_file.close()

            sql_statment_file = open(os.path.join(log_location, f"sql_statment_{agent_unique_id}.stats"), "a")
            if current_state['error']:
                sql_statment_file.write(f"{current_time_stamp}: None\n")
            else:
                sql_statment_file.write(f"{current_time_stamp}: {current_state['sql']}\n")
            sql_statment_file.write(f"\n")
            sql_statment_file.close()

            stat_log_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "a")
            if current_state['error']:
                stat_log_file.write(f"SQL EXECUTED: None\n")
            else:
                stat_log_file.write(f"SQL EXECUTED: {current_state['sql']}\n")
            stat_log_file.close()

            # send reward to agent
            loss = agent.reward(reward, current_state)
            for key in loss.keys():
                if loss[key][0]:
                    training_loss[key]["action"].append(loss[key][0])
                    training_loss[key]["range"].append(loss[key][1])
                    training_loss[key]["type"].append(loss[key][2])
            # update state and action
            last_state = current_state

            # increment timestamp
            current_time_stamp += 1

            if current_time_stamp >= max_timestamp:
                max_timestamp_reached = True
        if current_episode % 10 == 0 and print_func == print:

            print("Summary:\n")
            if is_learning:
                print(
                    f"Running episode: {current_episode + 1}, average time taken: {round(avg_time_taken, 2)} sec, total number of wins: {total_no_wins}, total number of losses: {total_no_losses}")
            else:
                print(
                    f"Running episode: {current_episode + 1}, average time taken: {round(avg_time_taken, 2)} sec, total number of wins: {total_no_wins}, total number of losses: {total_no_losses}")
            if last_injection_win:
                print("Last Successfull Injection:")
                print(f"{last_injection_win}")

            print("Current Run Details:")
            print(
                f"Input parameter: {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]}")
            print(f"URL of input: {env.current_input_entry.input.action}")

            print(f"current timestamp: {current_time_stamp}")

            print(f"current payload: {current_state['payload']}")

            sql_text = current_state['sql'] if not current_state['error'] else "No SQL Executed"
            print(f"current SQL: {sql_text}")
        elif print_func != print:
                print_func.clear()
                add_logo(print_func.addstr)
                print_func.addstr("Summary:\n")
                print_func.addstr(f"Log output location: {os.path.abspath(os.path.join(os.getcwd(), log_location))}\n")
                if is_learning:
                    print_func.addstr(f"Running episode: {current_episode+1}, average time taken: {round(avg_time_taken,2)} sec, total number of wins: {total_no_wins}, total number of losses: {total_no_losses}\n")
                else:
                    print_func.addstr(f"Running episode: {current_episode + 1}, average time taken: {round(avg_time_taken, 2)} sec, total number of wins: {total_no_wins}, total number of losses: {total_no_losses}\n")
                print_func.addstr(" \n")
                if last_injection_win:
                    print_func.addstr("Last Successfull Injection:\n")
                    print_func.addstr(f"{last_injection_win}\n")
                    print_func.addstr(" \n")

                print_func.addstr(
                "  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-\n"+
                "/ / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\\n"+
                "`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'\n"
                )
                print_func.addstr("Current Run Details:\n")
                print_func.addstr(f"Input parameter: {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]}\n")
                print_func.addstr(f"URL of input: {env.current_input_entry.input.action}\n")
                print_func.addstr(" \n")

                print_func.addstr(f"current timestamp: {current_time_stamp}\n")
                print_func.addstr(" \n")

                print_func.addstr(f"current payload: {current_state['payload']}\n")
                print_func.addstr(" \n")

                sql_text = current_state['sql'] if not current_state['error'] else "No SQL Executed"
                print_func.addstr(f"current SQL: {sql_text}\n")
                print_func.addstr(
                "  .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-\n"+
                "/ / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\ \\ / / \\\n"+
                "`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'\n"
                )
                print_func.refresh()

        # time interval
        time_taken = time.time() - current_time
        if avg_time_taken == 0:
            avg_time_taken = time_taken
        else:
            avg_time_taken += time_taken
            avg_time_taken /= 2
        results_file = open(os.path.join(log_location, f"timing_{agent_unique_id}.stats"), "a")
        results_file.write(f"{time_taken}\n")
        results_file.close()

        # update win and loss criteria and trials
        results_file = open(os.path.join(log_location, f"rewards_{agent_unique_id}.stats"), "a")
        results_file.write(f"{np.sum(agent.reward_value)}\n")
        results_file.close()

        # check if win
        if game_done:
            last_injection_win = current_state['sql']
            current_wins += 1
            total_no_wins += 1
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            results_file.write(
                f"ep {current_episode}: current game wins {current_wins} with {current_time_stamp} timestamps and reward {agent.reward_value} = {np.sum(agent.reward_value)}\n")
            results_file.write(f"sql {current_state['sql']}\n")

            results_file.close()
            print(30 * '*')
            print(
                f"SQLi Found: {env.current_input_entry.input.action}, {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]}")
            print(f'Payload: {current_state["payload"]}')
            print(30 * '*')
            total_wins.append(1)
            agent.reward_value = []

        # check if lost
        if max_timestamp_reached and not game_done:
            current_losses += 1
            total_no_losses += 1
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            results_file.write(
                f"ep {current_episode}: current game lost {current_losses} with {current_time_stamp} timestamps\n")
            results_file.close()
            total_wins.append(0)
            agent.reward_value = []
        trials += 1

        # check if win criteria reached
        if current_wins >= win_criteria:
            reached_win_criteria = True
            # state reporting
            stat_report.append({"reached_win": True, "reached_loss": False, "trials": trials, "wins": current_wins,
                                "losses": current_losses})
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            results_file.write(f"[!] reached win criteria\n")
            results_file.write(f"[!] payload: {current_state['payload']}\n")
            results_file.write(f"[!] URL: {env.current_input_entry.input.action}\n")
            results_file.write(
                f"[!] Parameter: {[param['name'] for param in env.current_input_entry.input.inputs if param['input_use'] == 'injection_point'][0]}\n\n")
            results_file.close()
            stat_log_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "a")
            stat_log_file.write(f"[!] WIN CRITERA\n")
            stat_log_file.close()

        # check if loss criteria reached
        if current_losses + current_wins >= loss_criteria:
            reached_loss_criteria = True
            # state reporting
            stat_report.append({"reached_win": False, "reached_loss": True, "trials": trials, "wins": current_wins,
                                "losses": current_losses})
            results_file = open(os.path.join(log_location, f"result_stats_{agent_unique_id}.stats"), "a")
            results_file.write(f"[!] reached loss criteria\n\n")
            results_file.close()
            stat_log_file = open(os.path.join(log_location, f"log_{agent_unique_id}.stats"), "a")
            stat_log_file.write(f"[!] LOSS CRITERA\n")
            stat_log_file.close()

    # check if federated then exit
    if is_federated:
        # exit client from server
        if agent_type == 4:
            # exit from server
            server_host = '127.0.0.1'
            server_port = 1234
            # connect to server
            ClientSocket = socket.socket()
            try:
                ClientSocket.connect((server_host, server_port))
            except socket.error as e:
                print(str(e))

            # get ack
            ack = recv_msg(ClientSocket)
            ack = ack.decode('utf-8')
            if ack != "ACK":
                raise Exception(f"got responce {ack} FROM SERVER, should be ACK")

            # send init command
            send_msg(ClientSocket, str.encode("EXIT"))

            # get ack
            ack = recv_msg(ClientSocket)
            ack = ack.decode('utf-8')
            if ack != "ACK":
                raise Exception(f"got responce {ack} FROM SERVER, should be ACK")

    return log_location

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def add_logo(print_func):
    print_func(
        "                                                    _ _\n" +
        "                                         |\__/|  .~    ~.\n" +
        "░██████╗░██████╗░██╗██████╗░██╗░░░░░    /  o `./      .'\n" +
        "██╔════╝██╔═══██╗██║██╔══██╗██║░░░░░   {o__,   \    {\n" +
        "╚█████╗░██║██╗██║██║██████╔╝██║░░░░░     / .  . )    \ \n" +
        "░╚═══██╗╚██████╔╝██║██╔══██╗██║░░░░░     `-` '-' \    }\n" +
        "██████╔╝░╚═██╔═╝░██║██║░░██║███████╗    .(   _(   )_.'\n" +
        "╚═════╝░░░░╚═╝░░░╚═╝╚═╝░░╚═╝╚══════╝   '---.~_ _ _|\n" +
        "-----------------------------------------------------\n")


