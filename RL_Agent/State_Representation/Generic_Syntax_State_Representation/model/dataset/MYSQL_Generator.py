from pypika import MySQLQuery as Query, Table, Field
from pypika import Order, Interval,Tuple,Case
from pypika import functions as fn
from pypika import JoinType
from nltk.corpus import words
import nltk
import random
class MYSQL_Generator:
    def remove_values_from_list(the_list, val):
        return [value for value in the_list if value.casefold() not in val]

    def __init__(self) -> None:
        functions = ["ABS","AVG","COUNT","FLOOR","MAX","BIN","MIN","STD","STDDEV","CONCAT","NOW","LIKE","REGEX"]
        self.reserved_keywords = "ACCESSIBLE,ACCOUNT,ACTION,ACTIVE,ADD,ADMIN,AFTER,AGAINST,AGGREGATE,ALGORITHM,ALL,ALTER,ALWAYS,ANALYSE,ANALYZE,AND,ANY,ARRAY,AS,ASC,ASCII,ASENSITIVE,AT,AUTOEXTEND_SIZE,AUTO_INCREMENT,AVG,AVG_ROW_LENGTH,BACKUP,BEFORE,BEGIN,BETWEEN,BIGINT,BINARY,BINLOG,BIT,BLOB,BLOCK,BOOL,BOOLEAN,BOTH,BTREE,BUCKETS,BY,BYTE,CACHE,CALL,CASCADE,CASCADED,CASE,CATALOG_NAME,CHAIN,CHANGE,CHANGED,CHANNEL,CHAR,CHARACTER,CHARSET,CHECK,CHECKSUM,CIPHER,CLASS_ORIGIN,CLIENT,CLONE,CLOSE,COALESCE,CODE,COLLATE,COLLATION,COLUMN,COLUMNS,COLUMN_FORMAT,COLUMN_NAME,COMMENT,COMMIT,COMMITTED,COMPACT,COMPLETION,COMPONENT,COMPRESSED,COMPRESSION,CONCURRENT,CONDITION,CONNECTION,CONSISTENT,CONSTRAINT,CONSTRAINT_CATALOG,CONSTRAINT_NAME,CONSTRAINT_SCHEMA,CONTAINS,CONTEXT,CONTINUE,CONVERT,CPU,CREATE,CROSS,CUBE,CUME_DIST,CURRENT,CURRENT_DATE,CURRENT_TIME,CURRENT_TIMESTAMP,CURRENT_USER,CURSOR,CURSOR_NAME,DATA,DATABASE,DATABASES,DATAFILE,DATE,DATETIME,DAY,DAY_HOUR,DAY_MICROSECOND,DAY_MINUTE,DAY_SECOND,DEALLOCATE,DEC,DECIMAL,DECLARE,DEFAULT,DEFAULT_AUTH,DEFINER,DEFINITION,DELAYED,DELAY_KEY_WRITE,DELETE,DENSE_RANK,DESC,DESCRIBE,DESCRIPTION,DES_KEY_FILE,DETERMINISTIC,DIAGNOSTICS,DIRECTORY,DISABLE,DISCARD,DISK,DISTINCT,DISTINCTROW,DIV,DO,DOUBLE,DROP,DUAL,DUMPFILE,DUPLICATE,DYNAMIC,EACH,ELSE,ELSEIF,EMPTY,ENABLE,ENCLOSED,ENCRYPTION,END,ENDS,ENFORCED,ENGINE,ENGINES,ENUM,ERROR,ERRORS,ESCAPE,ESCAPED,EVENT,EVENTS,EVERY,EXCEPT,EXCHANGE,EXCLUDE,EXECUTE,EXISTS,EXIT,EXPANSION,EXPIRE,EXPLAIN,EXPORT,EXTENDED,EXTENT_SIZE,FAILED_LOGIN_ATTEMPTS,FALSE,FAST,FAULTS,FETCH,FIELDS,FILE,FILE_BLOCK_SIZE,FILTER,FIRST,FIRST_VALUE,FIXED,FLOAT,FLOAT4,FLOAT8,FLUSH,FOLLOWING,FOLLOWS,FOR,FORCE,FOREIGN,FORMAT,FOUND,FROM,FULL,FULLTEXT,FUNCTION,GENERAL,GENERATED,GEOMCOLLECTION,GEOMETRY,GEOMETRYCOLLECTION,GET,GET_FORMAT,GET_MASTER_PUBLIC_KEY,GLOBAL,GRANT,GRANTS,GROUP,GROUPING,GROUPS,GROUP_REPLICATION,HANDLER,HASH,HAVING,HELP,HIGH_PRIORITY,HISTOGRAM,HISTORY,HOST,HOSTS,HOUR,HOUR_MICROSECOND,HOUR_MINUTE,HOUR_SECOND,IDENTIFIED,IF,IGNORE,IGNORE_SERVER_IDS,IMPORT,IN,INACTIVE,INDEX,INDEXES,INFILE,INITIAL_SIZE,INNER,INOUT,INSENSITIVE,INSERT,INSERT_METHOD,INSTALL,INSTANCE,INT,INT1,INT2,INT3,INT4,INT8,INTEGER,INTERVAL,INTO,INVISIBLE,INVOKER,IO,IO_AFTER_GTIDS,IO_BEFORE_GTIDS,IO_THREAD,IPC,IS,ISOLATION,ISSUER,ITERATE,JOIN,JSON,JSON_TABLE,JSON_VALUE,KEY,KEYS,KEY_BLOCK_SIZE,KILL,LAG,LANGUAGE,LAST,LAST_VALUE,LATERAL,LEAD,LEADING,LEAVE,LEAVES,LEFT,LESS,LEVEL,LIKE,LIMIT,LINEAR,LINES,LINESTRING,LIST,LOAD,LOCAL,LOCALTIME,LOCALTIMESTAMP,LOCK,LOCKED,LOCKS,LOGFILE,LOGS,LONG,LONGBLOB,LONGTEXT,LOOP,LOW_PRIORITY,MASTER,MASTER_AUTO_POSITION,MASTER_BIND,MASTER_COMPRESSION_ALGORITHMS,MASTER_CONNECT_RETRY,MASTER_DELAY,MASTER_HEARTBEAT_PERIOD,MASTER_HOST,MASTER_LOG_FILE,MASTER_LOG_POS,MASTER_PASSWORD,MASTER_PORT,MASTER_PUBLIC_KEY_PATH,MASTER_RETRY_COUNT,MASTER_SERVER_ID,MASTER_SSL,MASTER_SSL_CA,MASTER_SSL_CAPATH,MASTER_SSL_CERT,MASTER_SSL_CIPHER,MASTER_SSL_CRL,MASTER_SSL_CRLPATH,MASTER_SSL_KEY,MASTER_SSL_VERIFY_SERVER_CERT,MASTER_TLS_CIPHERSUITES,MASTER_TLS_VERSION,MASTER_USER,MASTER_ZSTD_COMPRESSION_LEVEL,MATCH,MAXVALUE,MAX_CONNECTIONS_PER_HOUR,MAX_QUERIES_PER_HOUR,MAX_ROWS,MAX_SIZE,MAX_UPDATES_PER_HOUR,MAX_USER_CONNECTIONS,MEDIUM,MEDIUMBLOB,MEDIUMINT,MEDIUMTEXT,MEMBER,MEMORY,MERGE,MESSAGE_TEXT,MICROSECOND,MIDDLEINT,MIGRATE,MINUTE,MINUTE_MICROSECOND,MINUTE_SECOND,MIN_ROWS,MOD,MODE,MODIFIES,MODIFY,MONTH,MULTILINESTRING,MULTIPOINT,MULTIPOLYGON,MUTEX,MYSQL_ERRNO,NAME,NAMES,NATIONAL,NATURAL,NCHAR,NDB,NDBCLUSTER,NESTED,NETWORK_NAMESPACE,NEVER,NEW,NEXT,NO,NODEGROUP,NONE,NOT,NOWAIT,NO_WAIT,NO_WRITE_TO_BINLOG,NTH_VALUE,NTILE,NULL,NULLS,NUMBER,NUMERIC,NVARCHAR,OF,OFF,OFFSET,OJ,OLD,ON,ONE,ONLY,OPEN,OPTIMIZE,OPTIMIZER_COSTS,OPTION,OPTIONAL,OPTIONALLY,OPTIONS,OR,ORDER,ORDINALITY,ORGANIZATION,OTHERS,OUT,OUTER,OUTFILE,OVER,OWNER,PACK_KEYS,PAGE,PARSER,PARTIAL,PARTITION,PARTITIONING,PARTITIONS,PASSWORD,PASSWORD_LOCK_TIME,PATH,PERCENT_RANK,PERSIST,PERSIST_ONLY,PHASE,PLUGIN,PLUGINS,PLUGIN_DIR,POINT,POLYGON,PORT,PRECEDES,PRECEDING,PRECISION,PREPARE,PRESERVE,PREV,PRIMARY,PRIVILEGES,PRIVILEGE_CHECKS_USER,PROCEDURE,PROCESS,PROCESSLIST,PROFILE,PROFILES,PROXY,PURGE,QUARTER,QUERY,QUICK,RANDOM,RANGE,RANK,READ,READS,READ_ONLY,READ_WRITE,REAL,REBUILD,RECOVER,RECURSIVE,REDOFILE,REDO_BUFFER_SIZE,REDUNDANT,REFERENCE,REFERENCES,REGEXP,RELAY,RELAYLOG,RELAY_LOG_FILE,RELAY_LOG_POS,RELAY_THREAD,RELEASE,RELOAD,REMOTE,REMOVE,RENAME,REORGANIZE,REPAIR,REPEAT,REPEATABLE,REPLACE,REPLICATE_DO_DB,REPLICATE_DO_TABLE,REPLICATE_IGNORE_DB,REPLICATE_IGNORE_TABLE,REPLICATE_REWRITE_DB,REPLICATE_WILD_DO_TABLE,REPLICATE_WILD_IGNORE_TABLE,REPLICATION,REQUIRE,REQUIRE_ROW_FORMAT,RESET,RESIGNAL,RESOURCE,RESPECT,RESTART,RESTORE,RESTRICT,RESUME,RETAIN,RETURN,RETURNED_SQLSTATE,RETURNING,RETURNS,REUSE,REVERSE,REVOKE,RIGHT,RLIKE,ROLE,ROLLBACK,ROLLUP,ROTATE,ROUTINE,ROW,ROWS,ROW_COUNT,ROW_FORMAT,ROW_NUMBER,RTREE,SAVEPOINT,SCHEDULE,SCHEMA,SCHEMAS,SCHEMA_NAME,SECOND,SECONDARY,SECONDARY_ENGINE,SECONDARY_LOAD,SECONDARY_UNLOAD,SECOND_MICROSECOND,SECURITY,SELECT,SENSITIVE,SEPARATOR,SERIAL,SERIALIZABLE,SERVER,SESSION,SET,SHARE,SHOW,SHUTDOWN,SIGNAL,SIGNED,SIMPLE,SKIP,SLAVE,SLOW,SMALLINT,SNAPSHOT,SOCKET,SOME,SONAME,SOUNDS,SOURCE,SPATIAL,SPECIFIC,SQL,SQLEXCEPTION,SQLSTATE,SQLWARNING,SQL_AFTER_GTIDS,SQL_AFTER_MTS_GAPS,SQL_BEFORE_GTIDS,SQL_BIG_RESULT,SQL_BUFFER_RESULT,SQL_CACHE,SQL_CALC_FOUND_ROWS,SQL_NO_CACHE,SQL_SMALL_RESULT,SQL_THREAD,SQL_TSI_DAY,SQL_TSI_HOUR,SQL_TSI_MINUTE,SQL_TSI_MONTH,SQL_TSI_QUARTER,SQL_TSI_SECOND,SQL_TSI_WEEK,SQL_TSI_YEAR,SRID,SSL,STACKED,START,STARTING,STARTS,STATS_AUTO_RECALC,STATS_PERSISTENT,STATS_SAMPLE_PAGES,STATUS,STOP,STORAGE,STORED,STRAIGHT_JOIN,STREAM,STRING,SUBCLASS_ORIGIN,SUBJECT,SUBPARTITION,SUBPARTITIONS,SUPER,SUSPEND,SWAPS,SWITCHES,SYSTEM,TABLE,TABLES,TABLESPACE,TABLE_CHECKSUM,TABLE_NAME,TEMPORARY,TEMPTABLE,TERMINATED,TEXT,THAN,THEN,THREAD_PRIORITY,TIES,TIME,TIMESTAMP,TIMESTAMPADD,TIMESTAMPDIFF,TINYBLOB,TINYINT,TINYTEXT,TLS,TO,TRAILING,TRANSACTION,TRIGGER,TRIGGERS,TRUE,TRUNCATE,TYPE,TYPES,UNBOUNDED,UNCOMMITTED,UNDEFINED,UNDO,UNDOFILE,UNDO_BUFFER_SIZE,UNICODE,UNINSTALL,UNION,UNIQUE,UNKNOWN,UNLOCK,UNSIGNED,UNTIL,UPDATE,UPGRADE,USAGE,USE,USER,USER_RESOURCES,USE_FRM,USING,UTC_DATE,UTC_TIME,UTC_TIMESTAMP,VALIDATION,VALUE,VALUES,VARBINARY,VARCHAR,VARCHARACTER,VARIABLES,VARYING,VCPU,VIEW,VIRTUAL,VISIBLE,WAIT,WARNINGS,WEEK,WEIGHT_STRING,WHEN,WHERE,WHILE,WINDOW,WITH,WITHOUT,WORK,WRAPPER,WRITE,X509,XA,XID,XML,XOR,YEAR,YEAR_MONTH,ZEROFILL".split(",")
        self.reserved_keywords.extend(functions)
        self.reserved_keywords = [w.casefold() for w in self.reserved_keywords]
        self.words = words.words()

        self.words = MYSQL_Generator.remove_values_from_list(self.words,self.reserved_keywords)
        self.column_limit = 10
        self.max_depth = 1
        self.max_join = 1
        self.max_sub_query = 2
        self.select_column_adders = 3
        self.max_number_of_cases = 2
        self.max_no_inserts = 3 
        pass

    def select(self,depth=0,column_size=None,query=None):
        '''
            # select statment
                - number of columns
                - order by
                - table arithmatic
                    -alias
                - filters (WHERE)
                    boolean operators
                        - ==
                        - !=
                        - IN
                        - BETWEEN
                    - connectors : &, |, ^
                    - tuples
                - grouping and aggregation
                    - aggregation functions
                        - abs
                        - avg
                        - count
                        - floor
                        - max
                        - Bin
                        - min
                        - std
                        - stdDev
                    - having clause
                        - contains possible from above aggregated
                          along with boolean operators and conected
                          with boolean connectors
                - join
                    - static table or dynamic sub query
                    -join types
                        - cross
                        - full_outer
                        - hash
                        - inner
                        - left
                        - left_outer
                        - outer
                        - right
                        - right_outer
                    - on or using
                -limit
                - correlated sub queries
                    -alias
                - union
                - intersect
                - minus
                - except
                - date, time, interval
                - string functions
                    - ascii
                    - like
                    - regex
                    - concat
                - outer comment
                - inner comment
                - case statments
                - with clause
        '''
        # counters
        no_sub_queries = 0
        no_columns_added = 0

        # table
        if query is None:
            table = Table(random.choice(self.words))
            query = Query.from_(table)
        else:
            table = Table(random.choice(self.words))
            query = query.from_(table)

        # normal columns
        if column_size is not None:
            no_columns = random.randint(1,column_size//self.select_column_adders)
        else:
            no_columns = random.randint(1,self.column_limit)
        no_columns_added += no_columns
        columns_names = random.choices(self.words,k=no_columns)
        column_fields = [Field(current_column_name) for current_column_name in columns_names]

        # concat columns
        if random.randint(0,1):
            chosen_column = random.randint(0,no_columns-1)
            if random.randint(0,1):
                # alias
                column_fields[chosen_column] = fn.Concat(column_fields[chosen_column], ' ', Field(random.choice(self.words))).as_(random.choice(self.words))
            else:
                # no alias
                column_fields[chosen_column] = fn.Concat(column_fields[chosen_column], ' ', Field(random.choice(self.words)))

        # case columns
        if random.randint(0,1):
            number_of_cases = random.randint(1,self.max_number_of_cases)
            chosen_column = random.randint(0,no_columns-1)
            case = Case()
            for current_case in range(number_of_cases):
                chosen_column = random.randint(0,no_columns-1)
                case = case.when(self.critertion_parameter(1,[Field(random.choice(self.words)),Field(random.choice(self.words))]),str(random.choice(self.words) + " " + random.choice(self.words)))
            column_fields[chosen_column] = case
        query = query.select(*tuple(column_fields))

        # order by
        if random.randint(0,1):
            if random.randint(0,1):
                query = query.orderby(random.choice(columns_names),Order.asc)
            else:
                query = query.orderby(random.choice(columns_names),Order.desc)

        # arithmatic columns
        if random.randint(0,1):
            # how many arithmatic columns
            if column_size is not None:
                no_columns = random.randint(1,(column_size//self.select_column_adders)//2) * 2
            else:
                no_columns = random.randint(1,self.column_limit//2) * 2
            # how many operations 
            no_operations = no_columns // 2
            no_columns_added += no_operations
            # fields
            columns_names = random.choices(self.words,k=no_columns)
            columns_fields = [Field(current_column) for current_column in columns_names]
            operations = []
            for current_operation in range(no_operations):
                random_oper = random.randint(1,4)
                current_operation_columns = [random.choice(columns_fields),random.choice(columns_fields)]
                if random_oper == 1:
                    # + operation
                    operations.append(current_operation_columns[0] + current_operation_columns[1])
                elif random_oper == 2:
                    # - operation
                    operations.append(current_operation_columns[0] - current_operation_columns[1])
                elif random_oper == 3:
                    # * operation
                    operations.append(current_operation_columns[0] * current_operation_columns[1])
                else:
                    # / operation
                    operations.append(current_operation_columns[0] / current_operation_columns[1])

            query = query.select(*tuple(operations))

        # filter
        if random.randint(0,1):
            # number of filters
            no_columns = random.randint(1,self.column_limit//2)*2
            columns_names = random.choices(self.words,k=no_columns)
            columns_fields = [Field(current_column) for current_column in columns_names]
            no_filters = no_columns // 2
            final_filters = self.critertion_parameter(no_filters,columns_fields)
            query = query.where(final_filters)

        # grouping and aggregated results
        if random.randint(0,1):
            if column_size is not None:
                no_columns = random.randint(0,column_size//self.select_column_adders)
            else:
                no_columns = random.randint(0,self.column_limit)
            no_columns_added += no_columns
            columns_names = random.choices(self.words,k=no_columns)
            columns_fields = [Field(current_column) for current_column in columns_names]
            result_aggerated_columns = []
            for current_aggregated_column in range(no_columns):
                random_oper = random.randint(1,9)
                if random_oper == 1:
                    # abs
                    result_aggerated_columns.append(fn.Abs(columns_fields[current_aggregated_column]))
                elif random_oper == 2:
                    # avg
                    result_aggerated_columns.append(fn.Avg(columns_fields[current_aggregated_column]))
                elif random_oper == 3:
                    # count
                    result_aggerated_columns.append(fn.Count(columns_fields[current_aggregated_column]))
                elif random_oper == 4:
                    # floor
                    result_aggerated_columns.append(fn.Floor(columns_fields[current_aggregated_column]))
                elif random_oper == 5:
                    # max
                    result_aggerated_columns.append(fn.Max(columns_fields[current_aggregated_column]))
                elif random_oper == 6:
                    # Bin
                    result_aggerated_columns.append(fn.Bin(columns_fields[current_aggregated_column]))
                elif random_oper == 7:
                    # min
                    result_aggerated_columns.append(fn.Min(columns_fields[current_aggregated_column]))
                elif random_oper == 8:
                    # std
                    result_aggerated_columns.append(fn.Std(columns_fields[current_aggregated_column]))
                else:
                    # stdDev
                    result_aggerated_columns.append(fn.StdDev(columns_fields[current_aggregated_column]))
            
            query = query.groupby(random.choice(self.words))
            if len(result_aggerated_columns) > 0:
                query = query.select(*tuple(result_aggerated_columns))
            
            # having 
            if random.randint(0,1):
                # number of criterias
                no_columns = random.randint(1,self.column_limit//2)*2
                columns_names = random.choices(self.words,k=no_columns)
                columns_fields = [Field(current_column) for current_column in columns_names]
                columns_fields.extend(result_aggerated_columns)
                no_filters = no_columns // 2
                final_criteria = self.critertion_parameter(no_filters,columns_fields)
                query = query.having(final_criteria)

        # join
        if random.randint(0,1):
            no_joins = random.randint(1,self.max_join)
            for current_join in range(no_joins):
                # static or dynamic table
                if depth  < self.max_depth and no_sub_queries < self.max_sub_query:
                    if random.randint(0,1):
                        # static table
                        join_table = Table(random.choice(self.words))
                    else:
                        # dynamic sub quiry table
                        join_table,_ = self.select(depth+1)
                        no_sub_queries = no_sub_queries + 1
                else:
                    # static table
                    join_table = Table(random.choice(self.words))

                # type of join
                random_join = random.randint(1,8)
                if random_join == 1:
                    # cross
                    query = query.join(join_table, JoinType.cross)
                elif random_join == 2:
                    # hash
                    query = query.join(join_table, JoinType.hash)
                elif random_join == 3:
                    # inner
                    query = query.join(join_table, JoinType.inner)
                elif random_join == 4:
                    # left
                    query = query.join(join_table, JoinType.left)
                elif random_join == 5:
                    # left_outer
                    query = query.join(join_table, JoinType.left_outer)
                elif random_join == 6:
                    # outer
                    query = query.join(join_table, JoinType.outer)
                elif random_join == 7:
                    # right
                    query = query.join(join_table, JoinType.right)
                else:
                    # right_outer
                    query = query.join(join_table, JoinType.right_outer)

                # on or using
                if random.randint(0,1):
                    # on
                    current_field_name = random.choice(self.words)
                    field_1 = table.field(current_field_name)
                    field_2 = join_table.field(current_field_name)
                    if random.randint(0,1):
                        # ==
                        query = query.on(field_1 == field_2)
                    else:
                        # !=
                        query = query.on(field_1 != field_2)
                else:
                    # using
                    current_field_name = random.choice(self.words)
                    query = query.using(current_field_name)

        # limit
        if random.randint(0,1):
             query = query.limit(random.randint(0,1000))

        # correlated queries 
        if random.randint(0,1) and depth < self.max_depth and no_sub_queries < self.max_sub_query\
            and ((column_size is not None and no_columns_added < column_size) or column_size is None):

            no_columns_added += 1
            column_sub_query,_ = self.select(depth+1)
            no_sub_queries = no_sub_queries + 1
            if random.randint(0,1):
                # alias
                query = query.select(column_sub_query).as_(random.choice(self.words))
            else:
                query = query.select(column_sub_query)


         # satisfy the column size if not None
        if column_size is not None and no_columns_added < column_size:
            difference = column_size - no_columns_added
            columns_names = random.choices(self.words,k=difference)
            query = query.select(*tuple(columns_names))
            no_columns_added += difference
            
        
        # union, intersection and minus
        if random.randint(0,1) and no_columns_added %2 ==0 and no_columns_added >8 and depth <self.max_depth:
            random_operation = random.randint(1,5)
            if random_operation == 1:
                # union
                if random.randint(0,1):
                    # union distinct
                    intersected_query,_ = self.select(depth+1,no_columns_added)
                    query = query.union(intersected_query)
                else:
                    # union all
                    intersected_query,_ = self.select(depth+1,no_columns_added)
                    query = query.union_all(intersected_query)
            elif random_operation == 2:
                # intersection
                intersected_query,_ = self.select(depth+1,no_columns_added)
                query = query.intersect(intersected_query)
            elif random_operation == 3:
                # minus
                intersected_query,_ = self.select(depth+1,no_columns_added)
                query = query.minus(intersected_query)
            elif random_operation == 4:
                # except
                intersected_query,_ = self.select(depth+1,no_columns_added)
                query = query.except_of(intersected_query)
            else:
                # with clause
                sub_query,_ =self.select()
                query = query.with_(sub_query,random.choice(self.words))

        return query,no_columns_added 

    def insert(self,depth=0):
        # table name
        table = Table(random.choice(self.words))
        query = Query.into(table)

        # into column names
        if random.randint(0,1):
            # insert column names
            no_columns = random.randint(1,self.column_limit)
            columns_names = [Field(random.choice(self.words)) for c in range(no_columns)]
            query = query.columns(*tuple(columns_names))
            
        # inserts
        random_inserts = random.randint(1,3)
        if random_inserts == 1:
            # multiple
            no_inserts = random.randint(2,self.max_no_inserts)
            number_columns = random.randint(1,self.column_limit)
            for current_insert in range(no_inserts):
                insert_data = [random.choice(self.words) for c in range(number_columns)]
                query =query.insert(*tuple(insert_data))

        elif random_inserts == 2:
            # single
            number_columns = random.randint(1,self.column_limit)
            insert_data = [random.choice(self.words) for c in range(number_columns)]
            query = query.insert(*tuple(insert_data))
        else:
            # sub select query
            query,_ = self.select(depth+1,query=query)

        return query
        
    def update(self,depth=0):
        no_sub_queries = 0
        # table name
        table = Table(random.choice(self.words))
        query = Query.update(table)
        
        # set
        query = query.set(random.choice(self.words),random.choice(self.words))

        # critertion paramter
        if random.randint(0,1):
            # number of filters
            no_columns = random.randint(1,self.column_limit//2)*2
            columns_names = random.choices(self.words,k=no_columns)
            columns_fields = [Field(current_column) for current_column in columns_names]
            no_filters = no_columns // 2
            final_filters = self.critertion_parameter(no_filters,columns_fields)
            query = query.where(final_filters)

        # limit
        if random.randint(0,1):
             query = query.limit(random.randint(0,1000))

        # join
        if random.randint(0,1):
            no_joins = random.randint(1,self.max_join)
            for current_join in range(no_joins):
                # static or dynamic table
                if depth  < self.max_depth and no_sub_queries < self.max_sub_query:
                    if random.randint(0,1):
                        # static table
                        join_table = Table(random.choice(self.words))
                    else:
                        # dynamic sub quiry table
                        join_table,_ = self.select(depth+1)
                        no_sub_queries = no_sub_queries + 1
                else:
                    # static table
                    join_table = Table(random.choice(self.words))
                # type of join
                random_join = random.randint(1,9)
                if random_join == 1:
                    # cross
                    query = query.join(join_table, JoinType.cross)
                elif random_join == 2:
                    # full_outer
                    query = query.join(join_table, JoinType.full_outer)
                elif random_join == 3:
                    # hash
                    query = query.join(join_table, JoinType.hash)
                elif random_join == 4:
                    # inner
                    query = query.join(join_table, JoinType.inner)
                elif random_join == 5:
                    # left
                    query = query.join(join_table, JoinType.left)
                elif random_join == 6:
                    # left_outer
                    query = query.join(join_table, JoinType.left_outer)
                elif random_join == 7:
                    # outer
                    query = query.join(join_table, JoinType.outer)
                elif random_join == 8:
                    # right
                    query = query.join(join_table, JoinType.right)
                else:
                    # right_outer
                    query = query.join(join_table, JoinType.right_outer)

              
                # using
                current_field_name = random.choice(self.words)
                query = query.using(current_field_name)
        return query

    def critertion_parameter(self,no_filters,columns_fields):
        '''
            - return a random critertion given the number of filters and columns fields
        '''
        final_filters = None
        for current_filter in range(no_filters):
            random_oper = random.randint(1,10)
            current_filter_columns_1 = [random.choice(columns_fields),random.choice(columns_fields),self.date_operands(False),self.date_operands(False)]
            current_filter_columns_2 = [random.choice(columns_fields),random.choice(columns_fields),self.date_operands(True),self.date_operands(True)]
            random_number_of_operands = random.randint(2,5)
            
            if random_number_of_operands == 2:
                # two operands
                operand_1 = random.choice(current_filter_columns_1)
                operand_2 = random.choice(current_filter_columns_2)
            elif random_number_of_operands == 3 :
                # three operands
                operand_1 = self.arithmatic_operation(random.choice(current_filter_columns_1),random.choice(current_filter_columns_2))
                operand_2 = random.choice(current_filter_columns_2)
            elif random_number_of_operands == 4 :
                # 4 operands
                operand_1 = self.arithmatic_operation(random.choice(current_filter_columns_1),random.choice(current_filter_columns_2))
                operand_1 = self.arithmatic_operation(operand_1,random.choice(current_filter_columns_1))
                operand_2 = random.choice(current_filter_columns_2)
            else:
                # tuples
                operand_1 = Tuple(random.choice(current_filter_columns_1),random.choice(current_filter_columns_1))
                operand_2 = Tuple(random.choice(current_filter_columns_2),random.choice(current_filter_columns_2))
            
            
            if random_oper == 1:
                # ==operation
                operation = operand_1 == operand_2
            elif random_oper == 2:
                # != operation
                operation = operand_1 != operand_2
            elif random_oper == 3:
                # > operation
                operation = operand_1 > operand_2
            elif random_oper == 4:
                # < operation
                operation = operand_1 < operand_2
            elif random_oper == 5:
                # <= operation
                operation = operand_1 <= operand_2
            elif random_oper == 6:
                # >= operation
                operation = operand_1 >= operand_2
            elif random_oper == 7:
                oper_columns_choices = random.choices(self.words,k=2)
                # IN operation
                if random.randint(0,1):
                    # with tuple
                    operation = Tuple(current_filter_columns_1[0],current_filter_columns_1[1]).isin([Tuple(oper_columns_choices[0],oper_columns_choices[1])])
                else:
                    # without tuple
                    operation = current_filter_columns_1[0].isin([oper_columns_choices[0],oper_columns_choices[1]])
            elif random_oper == 8:
                # BETWEEN operation
                # int or float betweens
                numbers_choosen = []
                if random.randint(0,1):
                    numbers_choosen.append(round(random.random() * random.randint(1,100),4))
                    numbers_choosen.append(round(random.random() * random.randint(1,100),4))
                else:
                    numbers_choosen.append(random.randint(1,100))
                    numbers_choosen.append(random.randint(1,100))

                operation= current_filter_columns_1[0][numbers_choosen[0]:numbers_choosen[1]]
            elif random_oper == 9:
                # like operation
                operation = current_filter_columns_1[0].like("MC%")
            else:
                # regex operation
                operation = current_filter_columns_1[0].regex(r'^[abc][a-zA-Z]+&')


            if final_filters is None:
                final_filters = operation
            else:
                random_filter = random.randint(1,3)
                if random_filter == 1:
                    # and
                    final_filters = final_filters & operation
                elif random_filter == 2:
                    # or
                    final_filters = final_filters | operation
                else:
                    # xor
                    final_filters = final_filters ^ operation
        return final_filters

    def arithmatic_operation(self,operand_1,operand_2):
        random_oper = random.randint(1,4)
        if random_oper == 1:
            # + operation
            return operand_1+ operand_2
        elif random_oper == 2:
            # - operation
            return operand_1 - operand_2
        elif random_oper == 3:
            # * operation
            return operand_1 * operand_2
        else:
            # / operation
            return operand_1 / operand_2

    def date_operands(self,interval):
        random_oper = random.randint(1,2)
        if random_oper == 1 and interval:
            # interval
            random_interval = random.randint(1,3)
            if random_interval == 1:
                # days
                return Interval(days=random.randint(0,31))
            elif random_interval == 2:
                # months
                return Interval(months=random.randint(0,12))
            else:
                return Interval(years=random.randint(0,10))
        else:
            # now fun
            return fn.Now()

