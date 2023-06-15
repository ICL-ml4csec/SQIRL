# Diretory containing log files output from SQIRL

## actions_applied

actions_Applied files contain the actions that an agent has made and the payload it has attempted to execute at eaach timestep.

## all_inputs_found.stat

This contains the inputs found by SQIRL in the crawling phase of testing.

## log

This is a general log that contains the payload, executed SQL, avaliable actions, current game, and current input for each timestep.

## result_stats

Contains the number of steps of an episode, for each input. This will also contain any vulnerabilities that are found from testing.

## rewards

The reward that is achieved at each timestep.

## sql_statement

The sql statement that is executed at each timestep as recovered from the general log of the database by the SQL Proxy.

## timing

The time taken to execute each step.


