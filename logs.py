import sqlite3
import os

def connect_db(db_file):
    """Connect to the database and return the connection and cursor."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor

def delete_records(cursor, resource_id):
    """Delete a record from the database."""
    cursor.execute('DELETE FROM logs WHERE resource_id = ?', (resource_id,))

def list_records(cursor):
    """List all records in the database."""
    cursor.execute('SELECT * FROM logs')
    print("[log ID], [resource ID], [timestamp], [IP address], [user agent], [referrer]")
    for row in cursor:
        print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}")

def identify_records(cursor, resource_id):
    """List records with given resource_id in the database."""
    cursor.execute('SELECT * FROM logs WHERE resource_id = ?', (resoruce_id,))
    print("[log ID], [resource ID], [timestamp], [IP address], [user agent], [referrer]")
    for row in cursor:
        print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}")

def reset_records(cursor):
    """Reset the database."""
    cursor.execute('DELETE FROM logs')

def main():
    db_file = 'logs.db'
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
            elif commands[0] == 'delete':
                delete_records(cursor, commands[1])
                conn.commit()
            elif commands[0] == 'reset':
                reset_records(cursor)
                conn.commit()
            elif commands[0] == 'list':
                list_records(cursor)
                conn.commit()
            elif commands[0] == 'identify':
                identify_records(cursor, commands[1])
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
                print("  identify [resource ID]")
                print("  delete [resource ID]")
                print("  list")
                print("  reset")
                print("  help")
                print("  exit")
            else:
                print("command not found")
        except:
            print("failed to execute command")

if __name__ == '__main__':
    main()
