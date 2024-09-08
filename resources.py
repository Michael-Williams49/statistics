import sqlite3
import os

def connect_db(db_file):
    """Connect to the database and return the connection and cursor."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor

def add_record(cursor, resource_id, description, path):
    """Add a new record to the database."""
    cursor.execute('INSERT INTO resources VALUES (?, ?, ?)', (resource_id, description, path))

def edit_record(cursor, resource_id, new_description, new_path):
    """Edit an existing record in the database."""
    cursor.execute('UPDATE resources SET description = ? WHERE id = ?', (new_description, resource_id))
    cursor.execute('UPDATE resources SET path = ? WHERE id = ?', (new_path, resource_id))

def delete_record(cursor, resource_id):
    """Delete a record from the database."""
    cursor.execute('DELETE FROM resources WHERE id = ?', (resource_id,))

def list_records(cursor):
    """List all records in the database."""
    cursor.execute('SELECT * FROM resources')
    print("[ID], [description], [path]")
    for row in cursor:
        print(f"{row[0]}, {row[1]}, {row[2]}")

def main():
    db_file = 'resources.db'
    conn, cursor = connect_db(db_file)
    prompt = f"{db_file} $ "
    while True:
        command = input(prompt)
        commands = command.split()
        try:
            if commands[0] == 'connect':
                assert os.path.exists(commands[1])
                db_file = commands[1]
                conn, cursor = connect_db(db_file)
                conn.commit()
                prompt = f"{db_file} $ "
            elif commands[0] == 'add':
                add_record(cursor, commands[1], commands[2], commands[3])
                conn.commit()
            elif commands[0] == 'edit':
                edit_record(cursor, commands[1], commands[2], commands[3])
                conn.commit()
            elif commands[0] == 'delete':
                delete_record(cursor, commands[1])
                conn.commit()
            elif commands[0] == 'list':
                list_records(cursor)
                conn.commit()
            elif commands[0] == 'exit':
                try:
                    conn.commit()
                    conn.close()
                finally:
                    break
            elif commands[0] == 'help':
                print("available commands:")
                print("  connect [DB file]")
                print("  add [ID] [description] [path]")
                print("  edit [ID] [description] [path]")
                print("  delete [ID]")
                print("  list")
                print("  help")
                print("  exit")
            else:
                print("command not found")
        except:
            print("failed to execute command")

if __name__ == '__main__':
    main()
