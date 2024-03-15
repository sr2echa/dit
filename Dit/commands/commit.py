import mysql.connector
from collections import defaultdict


def create_db_connection(database_name):
    return mysql.connector.connect(
        user='your_username', 
        password='your_password',
        host='127.0.0.1',
        database=database_name
    )

def fetch_all_tables(database_name):
    query = "SHOW TABLES;"
    cnx = create_db_connection(database_name)
    cursor = cnx.cursor()
    cursor.execute(query)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    cnx.close()
    return tables

def fetch_table_dependencies(database_name):
    query = """
    SELECT 
        REFERENCED_TABLE_NAME, TABLE_NAME
    FROM 
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE 
        REFERENCED_TABLE_SCHEMA = %s AND 
        REFERENCED_TABLE_NAME IS NOT NULL;
    """
    cnx = create_db_connection(database_name)
    cursor = cnx.cursor()
    cursor.execute(query, (database_name,))
    
    dependencies = defaultdict(set)
    for ref_table, table in cursor:
        dependencies[ref_table].add(table)
    
    cursor.close()
    cnx.close()
    return dict(dependencies)

def topological_sort(dependencies):
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

def escape_value(value):
    if value is None:
        return 'NULL'
    elif isinstance(value, str):
        return f"'{value.replace("'", "''")}'"
    elif isinstance(value, bool):
        return '1' if value else '0'
    else:
        return str(value)

def export_table_schema(cursor, table_name):
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    schema = cursor.fetchone()[1]
    print(f"{schema};\n")

def export_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    if not rows:
        return
    
    columns = [desc[0] for desc in cursor.description]
    for row in rows:
        formatted_row = [escape_value(value) for value in row]
        values_str = ', '.join(formatted_row)
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_str});"
        print(insert_stmt)

def export_database(database_name):
    all_tables = fetch_all_tables(database_name)
    dependencies = fetch_table_dependencies(database_name)
    
    # Generate a full list of tables, including those without dependencies
    full_dependency_graph = {table: set() for table in all_tables}
    for ref_table, dependent_tables in dependencies.items():
        for dep in dependent_tables:
            full_dependency_graph[dep].add(ref_table)

    sorted_tables = topological_sort(full_dependency_graph)
    
    cnx = create_db_connection(database_name)
    cursor = cnx.cursor()

    print("SET foreign_key_checks = 0;")
    for table in sorted_tables:
        export_table_schema(cursor, table)

    for table in sorted_tables:
        export_table_data(cursor, table)

    print("SET foreign_key_checks = 1;\n")
    
    cursor.close()
    cnx.close()

# Example Usage
database_name = 'your_database'
export_database(database_name)
