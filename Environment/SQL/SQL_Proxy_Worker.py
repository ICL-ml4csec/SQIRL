from operator import index
from pprint import PrettyPrinter, pprint
import re

from Environment.Input.Input import Input


class SQL_Proxy_Worker:
    def __init__(self,file_name,db_type) -> None:
        self.file_name = file_name
        self.db_type = db_type
        # self.clear_log()

    def get_all_sql_statments(self,data_input):
        '''
            get all available sql statments in the logs related to the input
        '''
        with open(self.file_name, 'r',errors='ignore') as content_file:
            content = content_file.read()
            contents_split = content.splitlines()
            #contents_split = SQL_Proxy_Worker.fix_mysql_file_lines(contents_split)

            #possible_sql = [(re.search(r'\S*\s*\S*\s*\S*\s*(.*)', currentline).group(1),currentline) for currentline in contents_split if data_input.token in currentline]
            #possible_sql = [x[0] for x in possible_sql]
            possible_sql = []
            for line in contents_split:
                if data_input.token in line:
                    possible_sql += [re.search(r'\S*\s*\S*\s*\S*\s*(.*)', line).group(1)]

            starting_idx = 1
            final_idx = len(possible_sql)-1
            while starting_idx < final_idx:
                if possible_sql[starting_idx] == possible_sql[starting_idx-1]:
                    possible_sql.pop(starting_idx-1)
                    final_idx -= 1
                starting_idx += 1
            pp = PrettyPrinter(indent=4)



            if len(possible_sql) > 0:
                return possible_sql
            else:
                return None

    def get_new_sql(self,sql_input:Input):
        with open(self.file_name, 'r',errors='ignore') as content_file:
            content = content_file.read()
            contents_split = content.splitlines()
            #contents_split = SQL_Proxy_Worker.fix_mysql_file_lines(contents_split)

            # filter 1 by unique key
            #possible_sql = [(re.search(r'\S*\s*\S*\s*\S*\s*(.*)', currentline).group(1),currentline) for currentline in contents_split if sql_input.token in currentline]
            #possible_sql = [x[0] for x in possible_sql]
            #pp = PrettyPrinter(indent=4)
            possible_sql = []
            for line in contents_split:
                if sql_input.token in line:
                    possible_sql += [re.search(r'\S*\s*\S*\s*\S*\s*(.*)', line).group(1)]

            # filter 2: remove dublicates
            starting_idx = 1
            final_idx = len(possible_sql)-1
            while starting_idx < final_idx:
                if possible_sql[starting_idx] == possible_sql[starting_idx-1]:
                    possible_sql.pop(starting_idx-1)
                    final_idx -= 1
                starting_idx += 1


            if sql_input.seen_responce < len(possible_sql):
                if possible_sql[-1] != "":
                    return possible_sql[-1]
                else:
                    return None
            else:
                return None

    def fix_mysql_file_lines(lines:list):
        index = 0
        while index < len(lines):
            if re.search(f"[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+.[0-9]+Z",lines[index]) or "mysqld, Version: 5.6.51 (MySQL Community Server (GPL)). started with:" in lines[index] or re.search('\x00', lines[index]):
                index+=1
            else:
                if index - 1 < 0:

                    assert(False) 
                lines[index-1] = lines[index-1].strip()+ " " +lines[index].strip()
                lines.pop(index)
            # print(f"[SQL Proxy -> fix mysql lines] index {index} and lines length {len(lines)}")
        return lines

    def LCSubStr(X, Y, m, n):
        '''
            ack to geeks for geeks
        '''
    
        # Create a table to store lengths of
        # longest common suffixes of substrings.
        # Note that LCSuff[i][j] contains the
        # length of longest common suffix of
        # X[0...i-1] and Y[0...j-1]. The first
        # row and first column entries have no
        # logical meaning, they are used only
        # for simplicity of the program.
    
        # LCSuff is the table with zero
        # value initially in each cell
        LCSuff = [[0 for k in range(n+1)] for l in range(m+1)]
    
        # To store the length of
        # longest common substring
        result = 0
    
        # Following steps to build
        # LCSuff[m+1][n+1] in bottom up fashion
        for i in range(m + 1):
            for j in range(n + 1):
                if (i == 0 or j == 0):
                    LCSuff[i][j] = 0
                elif (X[i-1] == Y[j-1]):
                    LCSuff[i][j] = LCSuff[i-1][j-1] + 1
                    result = max(result, LCSuff[i][j])
                else:
                    LCSuff[i][j] = 0
        return result/m

    def clear_log(self):
        '''
            function used to clear logs to speed up
        '''
        with open(self.file_name, 'r+') as f:
            f.truncate(0)