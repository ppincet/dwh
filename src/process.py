import datetime
import pyodbc
import csv
import psycopg2
#from config import settings
from utils import db_helper

def init_subkonto_():
    print(f'{datetime.datetime.now()} : start init skonto')
    conn_strings = db_helper.get_conn_strings()
    try:
        pg_connection = psycopg2.connect(
           dbname=settings.DST_DB, 
           user=settings.DST_USR, 
           password=settings.DST_PWD,
           host= settings.DST_SRV
        )
        pg_cursor = pg_connection.cursor()
        connection =  pyodbc.connect(conn_strings['src'])
        cursor = connection.cursor()
        cursor.execute(db_helper.get_sql_statements('get_refs.sql')[0])
        for row in cursor.fetchall():
            skonto_type = f'{int(row[0][10:]):08X}'
            statement = f"""
                select '{skonto_type}', 
                    convert(varchar(32),  _idrref, 2)_idrref
                from [{row[0]}] (nolock)
            """
            source_cursor = connection.cursor()
            source_cursor.execute(statement)
            # csv_file_path = './sources/tempo.csv'
            # with open(csv_file_path, mode="w", encoding="utf-8", newline="") as f:
            #     writer = csv.writer(f, delimiter=",")
            #     for chunk in db_helper.get_data_chunks(source_cursor, 5000):
            #         writer.writerows(chunk)
            # with open(csv_file_path, mode="r", encoding="utf-8") as f:
            #     pg_cursor.copy_expert(sql="COPY z_subkonto_all (z_subkonto_type, z_subkonto_ref) FROM STDIN WITH CSV", file=f)
            #     pg_connection.commit()
            print(f'{datetime.datetime.now()} : {row[0]} - done')
    except Exception as e:
        print(f'fatal: {e}')
        
    print(f'{datetime.datetime.now()} : done init skonto')
def init_subkonto():
    print(f'{datetime.datetime.now()} : start init skonto')
    conn_strings = db_helper.get_conn_strings()
    
    src_connection = None
    dst_connection = None
    try:
        src_connection = pyodbc.connect(conn_strings['src'])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        dst_connection.autocommit = False 
        dst_cursor = dst_connection.cursor()
        dst_cursor.fast_executemany = True 
        
        src_cursor = src_connection.cursor()
        src_cursor.execute(db_helper.get_sql_statements('get_refs.sql')[0])
        
        for row in src_cursor.fetchall():
            skonto_type = f'{int(row[0][10:]):08X}'
            
            try:
                statement = f"""
                    select '{skonto_type} ztype', 
                         _idrref zref
                    from [{row[0]}] (nolock)
                """
                
                source_cursor = src_connection.cursor()
                source_cursor.execute(statement)
                
                insert_query = "INSERT INTO z_subkonto (z_subkonto_type, z_subkonto_ref) VALUES (?, ?)"
                
                for chunk in db_helper.get_data_chunks(source_cursor, 5000):
                    dst_cursor.executemany(insert_query, chunk)

                dst_connection.commit()
                source_cursor.close()
                
                print(f'{datetime.datetime.now()} : {row[0]} - done')
                
            except Exception as table_err:
               
                dst_connection.rollback()
                print(f'error processing {row[0]} (rolled back): {table_err}')
               
                
    except Exception as e:
        print(f'fatal: {e}')
    finally:
        if src_connection:
            src_connection.close()
        if dst_connection:
            dst_connection.close()
            
    print(f'{datetime.datetime.now()} : done init skonto')
def create_refs():
    print(f'{datetime.datetime.now()} : start create refs')
    conn_strings = db_helper.get_conn_strings()
    try:
        src_connection = pyodbc.connect(conn_strings['src'])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        cursor = src_connection.cursor()
        cursor.execute(db_helper.get_sql_statements('get_tables_w_fields.sql')[0])
        current_row = cursor.fetchone()[0]

        for row in cursor.fetchall():
            if row[0] != current_row[0]:
                print('---------------')
                current_row = row
            print(row)
    except Exception as e:
        print(f'fatal : {e}')
    print(f'{datetime.datetime.now()} : done create refs')
