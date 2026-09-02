import pyodbc
from config import settings
from pathlib import Path
import pandas as pd
import re
import csv
# from sqlalchemy import create_engine, Table, MetaData

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
    return [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

def get_data_chunks(cursor, batch_size=5000):
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows


def create_ref(name: str, view_name: str, aliases_only : bool) -> bool:
    print(f'{name}:{view_name}')
    try:
        conn_strings = get_conn_strings()
        EXCLUDED = {
            'PREDEFINEDID',
            'VERSION',
            }
        real_name = name[1:].upper()
        sql_select_statement = 'SELECT '
        sql_insert_statement = f'insert {real_name} ('
        sql_create_statement = f'''
            DROP TABLE IF EXISTS {real_name};
            create table {real_name} (
        '''
        sql_view_create_statement = f'drop view {view_name} if exists; create view {view_name} as \n select \n\t'
        df = pd.read_excel('./vcb v1.xlsx', 
            sheet_name='fields',
            header=None)
        result = df[df[3] == name]
        
        if not result.empty:
            src_cnt = 0
            lines = []
            idx = []
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
                    if data_type == 'binary':
                        select_lines.append(f'\n\tcast(cast({row[4]} as int) as char(1)) {col_name}' if data_type == 'binary' and row[11] == 1 else f'\n\t{row[4]}') 
               
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
                        # alias = row[15] if pd.notna(row[15]) else '---'
                        view_select_lines.append(f'\tz{field_n}.ID {alias}' if row[14] == 0 else f'isnull(z{field_n}.ID, 0) {alias}')
                        view_join_lines.append(f'left join ZSUBKONTO z{field_n} on z{field_n}.Z_TYPE = ref.{col_name_pure}RTREF and z{field_n}.Z_REF = ref.{col_name_pure}RRREF')
                    idx.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref 
                                ON {real_name} ({col_name_pure}RTREF, {col_name_pure}RRREF);''')
                if ref_type == 3 :
                    lines.append(f"\tIDTREF\tbinary(4) default 0x{ref_ref} not null")
                    lines.append(f"\tIDRREF\tbinary(16) not null")
                    insert_lines.append(f"\tIDRREF")
                    view_select_lines.append(f'zid.ID {row[15]}')
                    view_join_lines.append(f'inner join ZSUBKONTO zid on zid.Z_TYPE = ref.IDTREF and zid.Z_REF = ref.IDRREF')
                if ref_type == 4:
                    lines.append(f"\tPARENTIDRTREF\tbinary(4) default 0x{ref_ref} not null")
                    lines.append(f"\tPARENTIDRRREF\tbinary(16) not null")
                    insert_lines.append(f"\tPARENTIDRRREF")
                    view_select_lines.append(f'\tisnull(zpid.ID, 0) {row[15]}')
                    view_join_lines.append(f'left join ZSUBKONTO zpid on zpid.Z_TYPE = ref.PARENTIDRTREF and zpid.Z_REF = ref.PARENTIDRRREF')
                    idx.append(f'''CREATE NONCLUSTERED INDEX UIX_{col_name_pure}_Type_Ref 
                                    ON {real_name} (PARENTIDRTREF, PARENTIDRRREF);''')

                if ref_type in [0, 2]:
                    
                    match = re.search(r'_(.*)$', col_name)
                    cname = col_name_pure + (match.group(1) if match else "")
                    lines.append(f"\t{cname}\t{'char' if data_type == 'binary' and row[11] == 1 else data_type}  {args_str} {args_isnull}")
                    insert_lines.append(f"\t{cname}")
                    if not aliases_only or pd.notna(row[15]):
                        view_select_lines.append(f"\t{cname} {row[15]}" if row[14] == 0 else f"\tisnull({cname}, {'""' if 'char' in data_type else 0}) {row[15]}")
                    # if data_type.startswith
                    # view_select_lines.append()
                
            for item in spec_idx:
                idx.append(f'''CREATE NONCLUSTERED INDEX UIX_{item}_Type_Ref 
                            ON {real_name} ({item}RTREF, {item}RRREF);''')
            lines.append(f'\tCONSTRAINT PK_{real_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF));\n')
            
        sql_create_statement += ',\n'.join(lines)    
        sql_create_statement += '\n\n' + '\n'.join(idx)
        sql_select_statement += ','.join(select_lines) +f'\nfrom {name}'
        sql_view_create_statement += ',\n'.join(view_select_lines) + '\n' + '\n'.join(view_join_lines)
        sql_insert_statement += ',\n'.join(insert_lines) + f") VALUES ({', '.join(['?'] * src_cnt)})"
        print(sql_create_statement)
        print(sql_select_statement)
        print(sql_insert_statement)
        print(sql_view_create_statement)
        return True
        try:
            src_connection = pyodbc.connect(conn_strings['src_1cb'])
            dst_connection = pyodbc.connect(conn_strings['dst'])
            dst_connection.autocommit = False 
            source_cursor = src_connection.cursor()
            create_cursor = dst_connection.cursor()
            insert_cursor = dst_connection.cursor()
            insert_cursor.fast_executemany = True
            create_cursor.execute(sql_create_statement)
            dst_connection.commit()
            source_cursor.execute(sql_select_statement)
            for chunk in get_data_chunks(source_cursor, 5000):
                insert_cursor.executemany(sql_insert_statement, chunk)
            dst_connection.commit()
            source_cursor.close()
        except pyodbc.Error as e:
            print(f'odbc exception: {e}')
            dst_connection.rollback()
        finally:
            src_connection.close()
            dst_connection.close()
        return True
    except Exception as e:
        print('stage: create table')
        print(f'Exception: {e}')
        return False 

def get_next_id(max_bytes: bytes) -> bytes:
    if not max_bytes:
        current_int = 0
    else:
        current_int = int.from_bytes(max_bytes, byteorder='big')
    
    next_int = current_int + 1
    return next_int.to_bytes(16, byteorder='big')
'''
    converts hex from ms sql like 0x into bytes for SQLAlchemy
'''
def convert_hex_to_bytes(val: str) -> bytes:
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    if val_str.startswith('0x') or val_str.startswith('0X'):
        val_str = val_str[2:]
    return bytes.fromhex(val_str)

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

def register_refs(refs: list[str]) -> None:
    try:
        connection  = pyodbc.connect(get_conn_strings['dst'])
        cursor = connection.cursor()
        insert_statement = 'insert REFS_REG values (?)'
        data = [(ref,) for ref in refs]
        cursor.execute(insert_statement, data)
        connection.commit()
    except Exception as e:
        print(f'Exception:{e}')
    finally:
        if connection is not None: connection.close()