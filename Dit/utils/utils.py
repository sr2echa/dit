# IMPORTS
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

def fetch_all_tables(database_name) -> list:
    query = "SHOW TABLES;"
    config = get_config()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    cnx.close()
    return tables

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
    config = get_config()
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
    all_tables = fetch_all_tables(database_name)
    dependencies = fetch_table_dependencies(database_name)
    
    # Generate a full list of tables, including those without dependencies
    full_dependency_graph = {table: set() for table in all_tables}
    for ref_table, dependent_tables in dependencies.items():
        for dep in dependent_tables:
            full_dependency_graph[dep].add(ref_table)

    sorted_tables = topological_sort(full_dependency_graph)
    
    config = get_config()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

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
    history = pickle.load(open(get_directory(db) + r"\history.bin", "rb"))
    history.append(hash)
    pickle.dump(history, open(get_directory(db) + r"\history.bin", "wb"))

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
    config = get_config()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(db))
    cursor.execute("CREATE DATABASE {}".format(db))
    cursor.execute("USE {}".format(db))
    execute_multi_commands(cnx, commands)
    cursor.execute(commands)
    cursor.close()
    cnx.close()

def get_tables(db: str) -> list:
    config = get_config()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("USE {}".format(db))
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor]
    cursor.close()
    cnx.close()
    return tables

def get_schema(db: str) -> dict:
    config = get_config()
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
    config = get_config()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE {}".format(db))
    cursor.close()
    cnx.close()

def drop_db(db: str) -> None:
    config = get_config()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(db))
    cursor.close()
    cnx.close()

def get_config() -> dict:
    with open(home_directory + r"\config.json", "r") as f:
        return json.load(f)


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


def init(db: str) -> None:
    if check_init(db):
        raise Exception("dit already initialized")
    else:
        os.makedirs(get_directory(db))
        pickle.dump([], open(get_directory(db) + r"\history.bin", "wb"))

def commit(db: str, msg: str) -> None:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    commands = get_database_state(db)
    hash = generate_hash(commands.encode())
    history = pickle.load(open(get_directory(db) + r"\history.bin", "rb"))

    if not history or history[-1] != hash:
        data = [msg, commands]
        binary_data = pickle.dumps(data)
        compressed_data = compress_data(binary_data)
        save_compressed_data(compressed_data, get_directory(db) + r"\\" + hash + ".dbs")
        update_history(db, hash)
    else:
        print("No changes to commit")

def reset(db: str, hash: str) -> None:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    if not os.path.exists(get_directory(db) + r"\{}.dbs".format(hash)):
        raise Exception("commit does not exist")
    
    compressed_data = open(get_directory(db) + r"\{}.dbs".format(hash), 'rb').read()
    pickled_data = decompress_data(compressed_data)
    unpickled_data = pickle.loads(pickled_data)
    commands = unpickled_data[1]
    recreate(db, commands)

def discard_changes(db: str) -> None:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    history = pickle.load(open(get_directory(db) + r"\history.bin", "rb"))
    if not history:
        raise Exception("No changes to discard")
    else:
        recent_hash = history[-1]
        compressed_data = open(get_directory(db) + r"\{}.dbs".format(recent_hash), 'rb').read()
        pickled_data = decompress_data(compressed_data)
        unpickled_data = pickle.loads(pickled_data)
        commands = unpickled_data[1]
        recreate(db, commands)

def branch(db: str, branch_name: str) -> None:
    if not check_init(db):
        raise Exception("dit not initialized")
    
    shutil.copytree(get_directory(db), get_directory(branch_name))
    recreate(branch_name, get_database_state(db))

def merge(db1: str, db2: str) -> None:
    if not check_init(db1) or not check_init(db2):
        raise Exception("dit not initialized")
    
    history1 = pickle.load(open(get_directory(db1) + r"\history.bin", "rb"))
    history2 = pickle.load(open(get_directory(db2) + r"\history.bin", "rb"))
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