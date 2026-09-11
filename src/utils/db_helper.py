import pyodbc
from config import settings
from pathlib import Path
import pandas as pd
import re
import csv
# import datetime
import time
# from sqlalchemy import create_engine, Table, MetaData

TASK_NAME = 'ZGETFACT'
BATCH_SIZE = 5000
cp_struct = {
    "task_name": None,
    "last_period": None,
    "last_tref": None,
    "last_rref": None,
    "last_lineno": None,
    "total_rows": None,
    "status": None
}
def get_conn_strings(): 
    params = {
        'src_1cb' :{
            'DRIVER' : settings.SRC_1CB_DRV,
            'PORT' : settings.SRC_1CB_PORT,
            'SERVER' : settings.SRC_1CB_SRV,
            'DATABASE' : settings.SRC_1CB_DB,
            'UID' : settings.SRC_1CB_USR,
            'PWD' : settings.SRC_1CB_PWD,
            'TrustServerCertificate' : 'yes'
            },
        'dst' : {
            'DRIVER' : settings.DST_DRV,
            'PORT' : settings.DST_PORT,
            'SERVER' : settings.DST_SRV,
            'DATABASE' : settings.DST_DB,
            'UID' : settings.DST_USR,
            'PWD' : settings.DST_PWD,
            }
    }    
    return {
        'src_1cb' : ";".join([f"{k}={v}" for k, v in params['src_1cb'].items()]),
        'dst' : ";".join([f"{k}={v}" for k, v in params['dst'].items()]),
    }


def get_sql_statements(file_name):
    SRC_DIR = Path(__file__).resolve().parent.parent
    filepath = f"{SRC_DIR}/sql_queries/{file_name}"
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    return [f'{cmd.strip()};' for cmd in sql_script.split(';') if cmd.strip()]

def get_data_chunks(cursor, batch_size=5000):
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

def execute_sql_script(cursor, statement):
    commands = [cmd.strip() for cmd in statement.split(';') if cmd.strip()]
    for command in commands:
        cursor.execute(command)

def create_schema(name: str, view_name: str, aliases_only: bool) -> dict[str, str]:
    EXCLUDED = {
                'PREDEFINEDID',
              
                }
    try:
        real_name = f'_Reference{name}'
        stage_stock_name = f'ZSREF{name}'
        stage_buffer_name = f'ZBREF{name}'
        tempo_name = f'ZTREF{name}'
        sql_select_statement = 'SELECT '
        sql_insert_statement = f'insert {tempo_name} ('
        sql_create_buffer_statement = f'''
            DROP TABLE IF EXISTS {stage_buffer_name} ;
            create table {stage_buffer_name} (
        '''
        sql_create_statement = f'''
            DROP TABLE IF EXISTS {stage_stock_name};
            create table {stage_stock_name} (
        '''
        sql_create_tempo_statement = f'''
            create table {tempo_name} (
        '''
        view_name = view_name.upper()
        sql_view_create_statement = f'drop view if exists {view_name};\n create view {view_name} as \n select \n\t'
        df = pd.read_excel('./vcb v1.xlsx', 
            sheet_name='fields',
            header=None)
        result = df[df[3] == real_name]
        
        if not result.empty:
            src_cnt = 0
            lines = []
            pk_s = ''
            pk_b = ''
            idx_p = []
            idx_b = []
            select_lines = []
            insert_lines = []
            view_select_lines = []
            view_join_lines = []
            spec_idx = set()
            for _, row in result.iterrows():
                data_type = str(row[10]).strip().lower() 
                
                col_name = row[4].upper()[1:]
                if col_name in EXCLUDED: continue 
                if 'TYPE' not in col_name: 
                    # if data_type == 'binary':
                    if data_type == 'binary' and row[11] == 1: fld = f'\n\tcast(cast({row[4]} as int) as char(1)) {col_name}'
                    elif data_type == 'timestamp': fld = f'convert(varchar(18), convert(binary(8), {row[4]}), 1) {col_name}'
                    else: fld = row[4]
                    select_lines.append(f'\n\t{fld}') 
                
                match = re.match(r"(FLD(\d+))", col_name)
                if match:
                    col_name_pure, field_n = match.groups()
                else:
                    col_name_pure = col_name
                    field_n = None
                col_name_field_n = re.search(r"d+", col_name)
                if re.search(r"(RRREF|RTREF)$", col_name):
                    ref_type = 2
                    spec_idx.add(col_name_pure)
                elif (re.search(r"RREF$", col_name) 
                        and col_name != 'IDRREF' 
                        and 'PARENT' not in col_name):
                    ref_type = 1
                    ref_ref = '10000000' if 'Перечисление' in str(row[7]) else row[8]
                elif col_name == 'IDRREF':
                    ref_type = 3
                    ref_ref = row[0]

                elif 'PARENT' in col_name:
                    ref_type = 4
                    ref_ref = row[0]
                else: 
                    ref_type = 0
                    ref_ref = ''
                p1 = int(float(row[11])) if pd.notna(row[11]) else None
                if p1 == -1: p1 = 'max'
                p2 = int(float(row[12])) if pd.notna(row[12]) else None
                p3 = int(float(row[13])) if pd.notna(row[13]) else None
                if data_type.startswith(('decimal', 'numeric')):
                    args_str = f"({p2}, {p3})"
                elif data_type.startswith('timestamp'):
                    data_type = 'char(18)'
                    args_str = ''
                else:
                    args_str = f"({p1})"
                args_isnull = f' not null' if row[14] == 0 else ''
                
                # skip TYPE (common, binary(1) field)
                if 'TYPE' in col_name: continue
                alias = row[15] if pd.notna(row[15]) else ''
                src_cnt += 1
                if ref_type == 1 :
                    lines.append(f"\t{col_name_pure}RTREF\tbinary(4) default 0x{ref_ref}{args_isnull}")
                    lines.append(f"\t{col_name_pure}RRREF\tbinary(16){args_isnull}")
                    insert_lines.append(f"\t{col_name_pure}RRREF")
                    if not aliases_only or pd.notna(row[15]):
                        view_select_lines.append(f'\tisnull(Z{field_n}.ID, 0) {alias if alias else "Z" + field_n + "ID"}')
                        view_join_lines.append(f'left join ZSUBKONTO Z{field_n} on Z{field_n}.Z_TYPE = ref.{col_name_pure}RTREF and Z{field_n}.Z_REF = ref.{col_name_pure}RRREF')
                    idx_p.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref ON {stage_stock_name} ({col_name_pure}RTREF, {col_name_pure}RRREF);''')
                    idx_b.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref ON {stage_buffer_name} ({col_name_pure}RTREF, {col_name_pure}RRREF);''')
                if ref_type == 3 :
                    lines.append(f"\tIDTREF\tbinary(4) default 0x{ref_ref} not null")
                    lines.append(f"\tIDRREF\tbinary(16) not null")
                    insert_lines.append(f"\tIDRREF")
                    view_select_lines.append(f'zid.ID {alias}')
                    view_join_lines.append(f'inner join ZSUBKONTO zid on zid.Z_TYPE = ref.IDTREF and zid.Z_REF = ref.IDRREF')
                if ref_type == 4:
                    lines.append(f"\tPARENTIDRTREF\tbinary(4) default 0x{ref_ref} not null")
                    lines.append(f"\tPARENTIDRRREF\tbinary(16) not null")
                    insert_lines.append(f"\tPARENTIDRRREF")
                    view_select_lines.append(f'\tisnull(zpid.ID, 0) {alias if alias else "ZPID"}')
                    view_join_lines.append(f'left join ZSUBKONTO zpid on zpid.Z_TYPE = ref.PARENTIDRTREF and zpid.Z_REF = ref.PARENTIDRRREF')
                    idx_p.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref ON {stage_stock_name} (PARENTIDRTREF, PARENTIDRRREF);''')
                    idx_b.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref ON {stage_buffer_name} (PARENTIDRTREF, PARENTIDRRREF);''')

                if ref_type in [0, 2]:
                    
                    match = re.search(r'_(.*)$', col_name)
                    cname = col_name_pure + (match.group(1) if match else "")
                    lines.append(f"\t{cname}\t{'char' if data_type == 'binary' and row[11] == 1 else data_type}  {args_str} {args_isnull}")
                    insert_lines.append(f"\t{cname}")
                    if not aliases_only or pd.notna(row[15]):
                        default_val = "''" if 'char' in data_type else 0
                        col_alias = alias if alias else cname
                        view_select_lines.append(f"\tisnull({cname}, {default_val}) {col_alias}")
            for item in spec_idx:
                print(f'idx item:{item}')
                idx_p.append(f'''CREATE NONCLUSTERED INDEX UIX_{item}_Type_Ref 
                            ON {stage_stock_name} ({item}RTREF, {item}RRREF);''')
                idx_b.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref 
                            ON {stage_buffer_name} ({col_name_pure}RTREF, {col_name_pure}RRREF);''')
                
            # lines.append(f'\tCONSTRAINT PK_{stage_stock_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF));\n')
            pk_s = f'\n\tCONSTRAINT PK_{stage_stock_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF));\n'
            pk_b = f'\n\tCONSTRAINT PK_{stage_buffer_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF));\n'
            pk_t = f'\n\tCONSTRAINT PK_{tempo_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF));\n'
            sql_create_statement += ',\n'.join(lines) + '\n' + pk_s + '\n\n' + '\n'.join(idx_p)
            sql_create_buffer_statement += ',\n'.join(lines) + '\n' + pk_b + '\n\n' + '\n'.join(idx_b)
            sql_create_tempo_statement += ',\n'.join(lines) + '\n' + pk_t
            sql_select_statement += ','.join(select_lines) +f'\nfrom {real_name}'
            sql_view_create_statement += ',\n'.join(view_select_lines) + f'\nfrom {stage_stock_name} ref\n' + '\n'.join(view_join_lines)
            sql_insert_statement += ',\n'.join(insert_lines) + f") VALUES ({', '.join(['?'] * src_cnt)})"
    except Exception as e:
            print(f'exception: {e}')
    return {
        'sql_create': sql_create_statement,
        'sql_buffer_create': sql_create_buffer_statement,
        'sql_create_tempo': sql_create_tempo_statement,
        'sql_select': sql_select_statement,
        'sql_view_create': sql_view_create_statement,
        'sql_insert': sql_insert_statement,
    }
def update_ref(src_cursor: pyodbc.Cursor, dst_cursor: pyodbc.Cursor, ref_name: str,statements: dict[str,str]) -> None:
    try:
        stmnt = 'TRUNCATE TABLE Z{0}REF{1}'.format
        dst_cursor.execute(stmnt('S', ref_name))
        src_cursor.execute(statements['sql_select'])
        for chunk in get_data_chunks(src_cursor, 5000):
            dst_cursor.executemany(statements['sql_insert'], chunk)
        dst_cursor.execute(f'''
                            insert ZSREF{ref_name}
                            select t.* 
                            from ZTREF{ref_name} t
                            left join ZBREF{ref_name} b
                            on t.IDRREF = b.IDRREF
                            where t.VERSION<>b.VERSION
                            or b.IDRREF is null
                        ''')
        dst_cursor.execute(stmnt('B', ref_name))
        dst_cursor.execute(f'''insert into ZBREF{ref_name}
                            select * from ZTREF{ref_name}
                            ''')
        dst_cursor.execute(f'drop table ZTREF{ref_name}')
    except Exception as e:
        print(f'update ref exception {e}')
        raise

def create_view(dst_cursor: pyodbc.Cursor, statement: str) -> None:
    try:
        print('inside create view')
        print(statement)
        execute_sql_script(dst_cursor, statement)
    except Exception as e:
        print(f'create view exception: {e}')
        raise

def create_ref(name: str, view_name: str, aliases_only : bool) -> bool:
    status = True
    try:
        statements = create_schema(name, view_name, aliases_only)      
        conn_strings = get_conn_strings()
        src_connection = pyodbc.connect(conn_strings['src_1cb'])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        dst_connection.autocommit = False 
        source_cursor = src_connection.cursor()
        create_cursor = dst_connection.cursor()
        insert_cursor = dst_connection.cursor()
        # insert_cursor.fast_executemany = True
        create_cursor.execute(statements['sql_create'])
        create_cursor.execute(statements['sql_buffer_create'])
        create_cursor.execute(statements['sql_create_tempo'])
        create_view(create_cursor, statements['sql_view_create'])
        update_ref(source_cursor, insert_cursor, name, statements)
        dst_connection.commit()
        source_cursor.close()
    except Exception as e:
        print(f'create ref  exception: {e}')
        dst_connection.rollback()
        status = False
        raise
    finally:
        if src_connection: src_connection.close()
        if dst_connection: dst_connection.close()
        return status


# initial and replication 
def populate_enums():   
    server = f"{settings.DST_SRV},{settings.DST_PORT}"
    database = settings.DST_DB
    username = settings.DST_USR
    password = settings.DST_PWD
    connection_string = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"    
    )
  
    try:
        engine = create_engine(connection_string)
        df = pd.read_csv('./enums.csv', 
            sep=';', 
            encoding='utf-8',
            header=None,  
            names=['ZREF', 'ZSYN', 'ZDESCR'])
        
        if 'ZREF' in df.columns:
            df['ZREF'] = df['ZREF'].apply(convert_hex_to_bytes)
        df.to_sql(
            name='ZENUM',
            con=engine,
            if_exists='append',  
            index=False,         
            chunksize=1000,
            dtype={
            'ZREF': BINARY(16),  
            'ZSYN': NVARCHAR(128),    
            'ZDESCR': NVARCHAR(255)  
        }
        )
        
    except Exception as e:
        print(f"Exception: {e}")
    
def read_csv_chunks(file_path, chunk_size=200):
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        chunk = []
        
        for row in reader:
            processed_row = {
                'ZREF': convert_hex_to_bytes(row.get('ZREF')),
                'ZSYN': row.get('ZSYN'),
                'ZDESCR': row.get('ZDESCR')
            }
            chunk.append(processed_row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    metadata = MetaData()
    zenum_table = Table('ZENUM', metadata, autoload_with=engine)
    try:
        with engine.begin() as connection:
            for chunk in read_csv_chunks('./enums.csv', chunk_size=200):
                connection.execute(zenum_table.insert(), chunk)
    except Exception as e:
        print(f"Exception: {e}")

# 2do : add period
# !!! deprecated !!!
def get_fact_table_(period_from :str, period_to :str) -> None:
    try:
        conn_strings = get_conn_strings()
        src_conn = pyodbc.connect(conn_strings['src_1cb'])
        dst_conn = pyodbc.connect(conn_strings['dst'])
        dst_conn.autocommit = False
        src_cursor = src_conn.cursor()
        src_cursor.fast_executemany = True
        dst_cursor = dst_conn.cursor()
        dst_cursor.execute(get_sql_statements('create_tempo.sql')[0])
        src_cursor.execute(get_sql_statements('get_fact_main.sql')[0](period_from, period_to))
        chunkn = 0
        for chunk in get_data_chunks(src_cursor, BATCH_SIZE):
            dst_cursor.executemany(get_sql_statements('insert_fact_table.sql')[0], chunk)
        dst_cursor.execute("""
            CREATE NONCLUSTERED INDEX IX_ZFACT_Base 
            ON #ZFACT (ZPERIOD, ZBDACCT, ZBDACCR);

            CREATE NONCLUSTERED INDEX IX_ZFACT_SK_Group1 
            ON #ZFACT (ZSK00T, ZSK00R, ZSK01T, ZSK01R, ZSK02T, ZSK02R);

            CREATE NONCLUSTERED INDEX IX_ZFACT_SK_Group2 
            ON #ZFACT (ZSK03T, ZSK03R, ZSK10T, ZSK10R, ZSK11T, ZSK11R);
    
            CREATE NONCLUSTERED INDEX IX_ZFACT_SK_Group3 
            ON #ZFACT (ZSK12T, ZSK12R, ZSK13T, ZSK13R, ZSK20T, ZSK20R);
        """)
        dst_cursor.execute("DROP TABLE IF EXISTS ZFACT;")
        dst_cursor.execute(get_sql_statements('insert_fact_table_bw.sql')[0])
        dst_cursor.commit()
    except Exception as e:
        dst_cursor.rollback()
        print(f'exception {e}')
    finally:
        if src_conn: src_conn.close()
        if src_conn: dst_conn.close()

def get_or_create_checkpoint(dst_cursor, 
                             dst_conn, 
                             task_name, 
                             start_window, 
                             end_window):
    dst_cursor.execute(get_sql_statements('get_cp.sql')[0], 
                       (task_name,))
    row = dst_cursor.fetchone()

    if row and row[0] == start_window and row[1] == end_window:
         
         return {
            "last_period": row[2],
            "last_tref": row[3],
            "last_rref": row[4],
            "last_lineno": row[5],
            "total_rows": row[6],
            "is_resume": True
        }    
    dst_cursor.execute("truncate table ZFACT;") # fact table
    dst_cursor.execute("truncate table ZFACTSTG;") # batch table
    init_tref = b'\x00' * 4
    init_rref = b'\x00' * 16
    print('phase : truncate, upsert log')  
    print(get_sql_statements('upsert_log.sql')[0])
    dst_cursor.execute(get_sql_statements('upsert_log.sql')[0], (
        task_name, start_window, end_window, start_window, init_tref, init_rref, -1,
        task_name, start_window, end_window, start_window, init_tref, init_rref, -1
    ))
    dst_conn.commit()

    return {
        "last_period": start_window,
        "last_tref": init_tref,
        "last_rref": init_rref,
        "last_lineno": -1,
        "total_rows": 0,
        "is_resume": False
    }
def update_checkpoint(dst_cursor, dst_conn, task_name, last_period, last_tref, last_rref, last_lineno, total_rows, status='IN_PROGRESS'):   
    dst_cursor.execute(get_sql_statements('checkpoint_upd.sql')[0], 
                       (last_period, last_tref, last_rref, last_lineno, total_rows, status, task_name))
    dst_conn.commit()

# wo nolock (pagination)
def get_fact_table(period_from :str, period_to :str) -> None:
    # print(f'from : {period_from} to: {period_to}')
    upd_cp = cp_struct.clone()
    # return True
    try:
        conn_strings = get_conn_strings()
        src_conn = pyodbc.connect(conn_strings['src_1cb'])
        dst_conn = pyodbc.connect(conn_strings['dst'])
        dst_conn.autocommit = False
        src_cursor = src_conn.cursor()
        src_cursor.fast_executemany = True
        dst_cursor = dst_conn.cursor()
        cp = get_or_create_checkpoint(dst_cursor, 
                                      dst_conn, 
                                      TASK_NAME, 
                                      period_from, 
                                      period_to)
                
        last_period = cp["last_period"]
        last_tref = cp["last_tref"]
        last_rref = cp["last_rref"]
        last_lineno = cp["last_lineno"]
        total_rows = cp["total_rows"]
        
        #return 
        batch_num = 0
        start_time = time.time()

        while True:
            batch_num += 1
            params = (
                BATCH_SIZE,
                BATCH_SIZE,
                last_period,
                period_to,
                BATCH_SIZE,
                last_period, 
                last_tref,
                BATCH_SIZE,
                last_period, 
                last_tref, 
                last_rref,
                BATCH_SIZE,
                last_period, 
                last_tref, 
                last_rref, 
                last_lineno
            )
            src_cursor.execute(get_sql_statements('get_fact_main.sql')[0], params)
            rows = src_cursor.fetchall()
            if not rows:
                update_checkpoint(dst_cursor, 
                                  dst_conn, 
                                  TASK_NAME, 
                                  last_period, 
                                  last_tref, 
                                  last_rref, 
                                  last_lineno, 
                                  total_rows, 
                                  status='SUCCESS')
                break
            
            dst_cursor.fast_executemany = True
            dst_cursor.executemany(get_sql_statements('insert_fact_table.sql')[0], 
                                   [row[:-3] for row in rows])
            
          
            last_row = rows[-1]
            last_period = last_row[0]
            last_tref, last_rref, last_lineno = last_row[-3:]
            total_rows += len(rows)
            
            print('update checkpoint')
            upd_cp['task_name'] = TASK_NAME, 
            upd_cp['last_period'] =last_period, 
            upd_cp['last_tref'] = last_tref, 
            upd_cp['last_rref'] = last_rref, 
            upd_cp['last_lineno'] = last_lineno, 
            upd_cp['total_rows'] = total_rows, 
            upd_cp['status'] = 'IN_PROGRESS'
            update_checkpoint(dst_cursor, dst_conn, upd_cp)
        # это здесь специально!
        return            
        dst_cursor.execute(get_sql_statements('create_tempo.sql')[0])
        src_cursor.execute(get_sql_statements('get_fact_main.sql')[0](period_from, period_to))
        chunkn = 0
        for chunk in get_data_chunks(src_cursor, BATCH_SIZE):
            dst_cursor.executemany(get_sql_statements('insert_fact_table.sql')[0], chunk)
        
        dst_cursor.execute("DROP TABLE IF EXISTS ZFACT;")
        dst_cursor.execute(get_sql_statements('insert_fact_table_bw.sql')[0])
        dst_cursor.commit()
    except Exception as e:
        dst_cursor.rollback()
        print(f'exception {e}')
    finally:
        if src_conn: src_conn.close()
        if src_conn: dst_conn.close()

def init_subkonto():
   
    conn_strings = get_conn_strings()
    
    src_connection = None
    dst_connection = None
    try:
        src_connection = pyodbc.connect(conn_strings['src_1cb'])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        dst_connection.autocommit = False 
        dst_cursor = dst_connection.cursor()
        dst_cursor.fast_executemany = True 
        
        src_cursor = src_connection.cursor()
        src_cursor.execute(get_sql_statements('get_refs.sql')[0])
        
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
                
                for chunk in get_data_chunks(source_cursor, 5000):
                    dst_cursor.executemany(insert_query, chunk)

                dst_connection.commit()
                source_cursor.close()    
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

def create_acc() -> None:
    try:
        conn_strings = get_conn_strings()
        src_connection = pyodbc.connect(conn_strings['src_1cb'])
        dst_connection = pyodbc.connect(conn_strings['dst'])
        dst_connection.autocommit = False 
        source_cursor = src_connection.cursor()
        create_cursor = dst_connection.cursor()
        source_cursor.execute('''
                               SELECT [_IDRRef]
                                    ,convert(varchar(18), convert(binary(8), [_Version]) ,1) VERSION
                                    ,cast(cast([_Marked] as int) as char(1)) [Marked]
                                    ,[_ParentIDRRef]
                                    ,[_Code]
                                    ,[_Description]
                                    ,[_OrderField]
                                    ,[_Kind]
                                    ,cast(cast([_OffBalance] as int) as char(1)) Offbalance
                                    ,[_Fld599]
                                    ,[_Fld600]
                                    ,[_Fld601RRef]
                                    ,cast(cast([_Fld602] as int) as char(1)) [_Fld602]
                                    ,cast(cast([_Fld603] as int) as char(1)) [_Fld603]
                                FROM [HSRet].[dbo].[_Acc9]
                                ''')
        batch_size = 2000
        rows = source_cursor.fetchmany(batch_size)
        create_cursor.executemany('''
                                    insert ZACC (
                                        [IDRREF]
                                        ,[VERSION]
                                        ,[MARKED]
                                        ,[PARENTIDRRREF]
                                        ,[CODE]
                                        ,[DESCRIPTION]
                                        ,[ORDERFIELD]
                                        ,[KIND]
                                        ,[OFFBALANCE]
                                        ,[FLD599]
                                        ,[FLD600]
                                        ,[FLD601RRREF]
                                        ,[FLD602]
                                        ,[FLD603])
                                        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    ''', 
                                  rows)
        dst_connection.commit()
    except Exception as e:
        src_connection.rollback()
        print(f'create acc exc:{e}')
        raise
    finally:
        if src_connection: src_connection.close()
        if dst_connection: dst_connection.close()

