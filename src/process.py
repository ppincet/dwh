import datetime
from utils import db_helper, common
from typing import List, Dict, Optional


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

def create_refs(content: Dict[str, Optional[str]], aliases_only: str) -> None:
    try:
        for k, v in content.items():
            if k is None: continue
            db_helper.create_ref(f'{k}', 
                v if v is not None else f'VREF{k}',
                aliases_only)
    except Exception as e:
        print(f'fatal : {e}')
    print(f'{datetime.datetime.now()} : done create refs')

def get_fact_table(period: str = 'AUTO', is_odinass = True) -> None:
    period_range = (
        common.get_rolling_window_standard(True) if period == 'AUTO' else common.parse_date_range(period, is_odinass)
    )
    db_helper.get_fact_table(*period_range)
def check_updates() -> None:
    print('check done')
def start_etl() -> None:
    get_fact_table()
    check_updates()
    print(f'done: {datetime.datetime.now()}')
def do_init(content: dict[str, str], aliases_only: bool) -> None:
    create_refs(content, aliases_only)


    
    

