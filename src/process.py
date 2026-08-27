import datetime
import pyodbc
import csv
import psycopg2
#from config import settings
from utils import db_helper

def get_ds_core(step, src, s_statement_file, i_statement):
    print(f'{datetime.datetime.now()} : start {step}')
    print(f'{datetime.datetime.now()} : {step} done')
    conn_strings = db_helper.get_conn_strings()
    src_connection = None
    dst_connection = None
    try:
        src_connection = pyodbc.connect(conn_strings[src])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        dst_connection.autocommit = False 
        dst_cursor = dst_connection.cursor()
        dst_cursor.fast_executemany = True     
        src_cursor = src_connection.cursor()
        src_cursor.execute(db_helper.get_sql_statements(s_statement)[0])


    except Exception as e:
        print(f'fatal : {e}')

def get_fact():
    print(f'{datetime.datetime.now()} : start getting fact table')
    conn_strings = db_helper.get_conn_strings()
    src_connection = None
    dst_connection = None
    try:
        src_connection = pyodbc.connect(conn_strings['src_1cb'])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        dst_connection.autocommit = False 
        dst_cursor = dst_connection.cursor()
        dst_cursor.fast_executemany = True 
        
        src_cursor = src_connection.cursor()
        src_cursor.execute(db_helper.get_sql_statements('get_fact_main.sql')[0])
    except Exception as fact_exc:
        print(f'fatal : {fact_exc}')

    print(f'{datetime.datetime.now()} : done')
def init_subkonto():
    print(f'{datetime.datetime.now()} : start init skonto')
    conn_strings = db_helper.get_conn_strings()
    
    src_connection = None
    dst_connection = None
    try:
        src_connection = pyodbc.connect(conn_strings['src_1cb'])
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
                    select 0x{skonto_type} ztype, 
                         _idrref zref
                    from [{row[0]}] (nolock)
                """
                source_cursor = src_connection.cursor()
                source_cursor.execute(statement)
                
                insert_query = "INSERT INTO Z_SUBKONTO(Z_TYPE, Z_REF) VALUES (?, ?)"
                
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
