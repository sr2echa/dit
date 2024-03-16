# IMPORTSHEAD
import os
import pickle
import json
import mysql.connector
import shutil
import zlib
import hashlib
from collections import defaultdict


# CONSTANTS
home_directory = os.path.expanduser('~')
home_directory += r"\.dit"


# HELPERS
def generate_hash(data) -> str:
    return hashlib.sha1(data).hexdigest()

def compress_data(data) -> bytes:
    return zlib.compress(data)

def decompress_data(data) -> bytes:
    return zlib.decompress(data)

def save_compressed_data(compressed_data, filename) -> None:
    with open(filename, 'wb') as file:
        file.write(compressed_data)


def fetch_table_dependencies(database_name) -> dict:
    query = """
    SELECT 
        REFERENCED_TABLE_NAME, TABLE_NAME
    FROM 
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE 
        REFERENCED_TABLE_SCHEMA = %s AND 
        REFERENCED_TABLE_NAME IS NOT NULL;
    """
    config = get_config(database_name)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (database_name,))
    
    dependencies = defaultdict(set)
    for ref_table, table in cursor:
        dependencies[ref_table].add(table)
    
    cursor.close()
    cnx.close()
    return dict(dependencies)

def topological_sort(dependencies) -> list:
    visited = set()
    order = []
    
    def dfs(table):
        if table not in visited:
            visited.add(table)
            for dep in dependencies.get(table, []):
                dfs(dep)
            order.append(table)
    
    for table in dependencies:
        if table not in visited:
            dfs(table)
    
    return order[::-1]

def escape_value(value) -> str:
    if value is None:
        return 'NULL'
    elif isinstance(value, str):
        return f"""'{value.replace("'", "''")}'"""
    elif isinstance(value, bool):
        return '1' if value else '0'
    else:
        return str(value)

def export_table_schema(cursor, table_name) -> str:
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    schema = cursor.fetchone()[1]
    return f"{schema};\n\n"

def export_table_data(cursor, table_name) -> str:
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    if not rows:
        return ''
    
    columns = [desc[0] for desc in cursor.description]
    insert_statements = []
    for row in rows:
        formatted_row = [escape_value(value) for value in row]
        values_str = ', '.join(formatted_row)
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_str});\n"
        insert_statements.append(insert_stmt)
    
    return ''.join(insert_statements)

def get_database_state(database_name) -> str:
    all_tables = get_tables(database_name)
    dependencies = fetch_table_dependencies(database_name)
    
    # Generate a full list of tables, including those without dependencies
    full_dependency_graph = {table: set() for table in all_tables}
    for ref_table, dependent_tables in dependencies.items():
        for dep in dependent_tables:
            full_dependency_graph[dep].add(ref_table)

    sorted_tables = topological_sort(full_dependency_graph)
    
    config = get_config(database_name)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(f"USE {database_name}")

    output = "SET foreign_key_checks = 0;\n"
    for table in sorted_tables:
        output += export_table_schema(cursor, table)

    for table in sorted_tables:
        output += export_table_data(cursor, table)

    output += "SET foreign_key_checks = 1;"
    
    cursor.close()
    cnx.close()

    return output
        
def get_directory(db: str) -> str:
    return home_directory + r"\\" + db

def check_init(db: str) -> bool:
    return os.path.exists(get_directory(db))

def update_history(db: str, hash: str) -> None:
    history = pickle.load(open(get_directory(db) + r"\past.lore", "rb"))
    history.append(hash)
    pickle.dump(history, open(get_directory(db) + r"\past.lore", "wb"))

def execute_multi_commands(connection, multi_commands) -> None:
    try:
        cursor = connection.cursor()
        commands = multi_commands.split(';')
        
        for command in commands:
            if not command.strip():
                continue
            cursor.execute(command)
        
        connection.commit()
        print("Commands executed successfully.")
    except mysql.connector.Error as err:
        print("Error executing commands:", err)

def recreate(db: str, commands: str) -> None:
    config = get_config(db)
    # print(config)
    cnx = mysql.connector.connect(host=config['host'], port=config['port'], user=config['username'], password=config['password'])
    cursor = cnx.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {};".format(db)) 
    cursor.execute("CREATE DATABASE {};".format(db))
    cursor.execute("USE {};".format(db))
    # print(commands)
    execute_multi_commands(cnx, commands)
    cursor.execute(commands)
    cursor.close()
    cnx.close()

def get_tables(db: str) -> list:
    config = get_config(db)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("USE {}".format(db))
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor]
    cursor.close()
    cnx.close()
    return tables

def get_schema(db: str) -> dict:
    config = get_config(db)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("USE {}".format(db))
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor]
    schema = {}
    for table in tables:
        cursor.execute(f"SHOW CREATE TABLE {table}")
        schema[table] = cursor.fetchone()[1]
    cursor.close()
    cnx.close()
    return schema

def create_db(db: str) -> None:
    config = get_config(db)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE {}".format(db))
    cursor.close()
    cnx.close()

def drop_db(db: str) -> None:
    config = get_config(db)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(db))
    cursor.close()
    cnx.close()
    part = get_directory(db)
    shutil.rmtree(part)

def get_config(db:str) -> dict:
    with open(home_directory + r"\\" + db + r"\HEAD", "rb") as f:
        return pickle.load(f)

def get_recent_hash(db: str) -> str:
    history = pickle.load(open(get_directory(db) + r"\past.lore", "rb"))
    return history[-1]

def get_table_data(db: str, table: str) -> list:
    config = get_config(db)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("USE {}".format(db))
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return data

# def get_databases() -> list:
#     config = get_config()
#     cnx = mysql.connector.connect(**config)
#     cursor = cnx.cursor()
#     cursor.execute("SHOW DATABASES")
#     databases = [db[0] for db in cursor]
#     cursor.close()
#     cnx.close()
#     return databases


# COMMANDS
def setup(user: str = "root", pwd: str = "root", host: str = "127.0.0.1", port: str = "3306") -> None:
    config = {
        "user": user,
        "password": pwd,
        "host": host,
        "port": port
    }

    with open(home_directory + r"\config.json", "w") as f:
        json.dump(config, f, indent=4)


def init(data: dict) -> None:
    if check_init(data['database']):
        raise Exception("dit already initialized")
    else:
        os.makedirs(get_directory(data['database']), exist_ok=True)
        pickle.dump(data, open(get_directory(data['database']) + r"\HEAD", "wb"))
        pickle.dump([], open(get_directory(data["database"]) + r"\past.lore", "wb"))

def commit(db: str, msg: str) -> int:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    try:
        commands = get_database_state(db)
        hash = generate_hash(commands.encode())
        history = pickle.load(open(get_directory(db) + r"\past.lore", "rb"))

        if not history or history[-1] != hash:
            data = [msg, commands]
            binary_data = pickle.dumps(data)
            compressed_data = compress_data(binary_data)
            save_compressed_data(compressed_data, get_directory(db) + r"\\" + hash + ".rarc")
            update_history(db, hash)
            return 1
        else:
            return 0
   
    except Exception as e:
        raise Exception(e)

    
def log(db: str) -> list:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    history = pickle.load(open(get_directory(db) + r"\past.lore", "rb"))
    history = history[::-1]

    logs = []

    for hash in history:
        compressed_data = open(get_directory(db) + r"\{}.rarc".format(hash), 'rb').read()
        pickled_data = decompress_data(compressed_data)
        unpickled_data = pickle.loads(pickled_data)
        logs.append({
            "hash": hash,
            "message": unpickled_data[0]
        })
    
    return logs


def reset(db: str, hash: str = None) -> None:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    elif hash is None:
        hash = get_recent_hash(db)
    
    elif not os.path.exists(get_directory(db) + r"\{}.rarc".format(hash)):
        raise Exception("commit does not exist")
    
    compressed_data = open(get_directory(db) + r"\{}.rarc".format(hash), 'rb').read()
    pickled_data = decompress_data(compressed_data)
    unpickled_data = pickle.loads(pickled_data)
    commands = unpickled_data[1]
    print(commands)
    recreate(db, commands)




def discard_changes(db: str) -> int:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    history = pickle.load(open(get_directory(db) + r"\past.lore", "rb"))
    if not history:
        return 0 # No changes to discard
    else:
        recent_hash = history[-1]
        hdir = get_directory(db) + r"\{}.rarc".format(recent_hash)
        # print(hdir)
        compressed_data = open(hdir, 'rb').read()
        pickled_data = decompress_data(compressed_data)
        unpickled_data = pickle.loads(pickled_data)
        commands = unpickled_data[1]
        recreate(db, commands)
        return 1 # Changes discarded




def branch(db: str, branch_name: str) -> None:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    shutil.copytree(get_directory(db), get_directory(branch_name))
    recreate(branch_name, get_database_state(db))




def merge(db1: str, db2: str) -> None:
    if not check_init(db1) or not check_init(db2):
        raise Exception("dit not initialized")
    
    history1 = pickle.load(open(get_directory(db1) + r"\past.lore", "rb"))
    history2 = pickle.load(open(get_directory(db2) + r"\past.lore", "rb"))
    recent1 = history1[-1]
    recent2 = history2[-1]
    
    if recent1 == recent2:
        raise Exception("No changes to merge")
    else:
        tables1 = set(get_tables(db1))
        tables2 = set(get_tables(db2))
        common_tables = tables1.intersection(tables2)

        schema1 = get_schema(db1)
        schema2 = get_schema(db2)

        db1_ignore = set()
        db2_ignore = set()

        for table in common_tables:
            if schema1[table] != schema2[table]:
                ignore = input(f"""Merge Conflict! Press Enter to resolve the conflict
Database 1: {db1}
Database 2: {db2}
Enter 1 to keep changes from Database 1
Enter 2 to keep changes from Database 2
[1/2]: """)

                if ignore == "1":
                    db2_ignore.add(table)
                elif ignore == "2":
                    db1_ignore.add(table)
                else:
                    raise Exception("Invalid input")
            
        db1_commands = get_database_state(db1)
        db2_commands = get_database_state(db2)

        db1_commands = db1_commands.split(";")
        db2_commands = db2_commands.split(";")

        final = []
        for command in db1_commands:
            if command.strip() and command.split("`")[2] not in db1_ignore:
                final.append(command)
        
        for command in db2_commands:
            if command.strip() and command.split("`")[2] not in db2_ignore:
                final.append(command)
        
        final = ";\n".join(final)
        recreate(db1, final)
        commit(db1, f"Merged {db2} into {db1}")
        os.remove(get_directory(db2))

def diff(db: str, hash: str = "recent") -> dict:
    '''Prints the difference between the current state of the database and the state at the given hash'''
    if not check_init(db):
        raise Exception("dit not initialized")
    
    if hash == "recent":
        hash = get_recent_hash(db)

    if not os.path.exists(get_directory(db) + r"\{}.rarc".format(hash)):
        raise Exception("commit does not exist")
    
    # Create new temp database using hash
    directory = get_directory(db) + r"\{}.rarc".format(hash)
    compressed_data = open(directory, 'rb').read()
    pickled_data = decompress_data(compressed_data)
    unpickled_data = pickle.loads(pickled_data)
    commands = unpickled_data[1]
    shutil.copytree(get_directory(db), get_directory(f"__temp__{db}"))
    recreate(f"__temp__{db}", commands)

    # Get the schema of the current database
    current_schema = get_schema(db)
    # print(current_schema)

    # Get the schema of the temp database
    temp_schema = get_schema(f"__temp__{db}")
    # print(temp_schema)

    minus_tables = []
    plus_tables = []
    minus_rows = defaultdict(list)
    plus_rows = defaultdict(list)

    all_tables = set(current_schema.keys()).union(set(temp_schema.keys()))
    for table in all_tables:
        if table not in current_schema:
            minus_tables.append(table)
        elif table not in temp_schema:
            plus_tables.append(table)
        
        # Compare schema of the tables if they exist in both databases
        # If the schema is different, add the table to the modified_tables list
        elif current_schema[table] != temp_schema[table]:
            minus_tables.append(table)
            plus_tables.append(table)
        
        # If the schema is the same, compare the data in the tables
        else:
            current_data = get_table_data(db, table)
            temp_data = get_table_data(f"__temp__{db}", table)

            # Convert data to set for O(1) lookup
            current_data = set([tuple(row) for row in current_data])
            temp_data = set([tuple(row) for row in temp_data])

            new_rows = current_data - temp_data
            removed_rows = temp_data - current_data

            if new_rows:
                plus_rows[table] = list(new_rows)

            if removed_rows:
                minus_rows[table] = list(removed_rows)
        
    # Drop the temp database
    drop_db(f"__temp__{db}")

    return {
        "minus_tables": minus_tables,
        "plus_tables": plus_tables,
        "minus_rows": dict(minus_rows),
        "plus_rows": dict(plus_rows)
    }

if __name__ == "__main__":
    reset("tempppp", "d8b61a1035933a45bdad47b1d5d2bf413d6c13c0")