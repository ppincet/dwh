import pyodbc
from config import settings
from pathlib import Path
import pandas as pd
import re
import csv
# from sqlalchemy import create_engine, Table, MetaData
SQL_SERVER_TO_PG_MAP = {
    "bigint": "BIGINT",
    "binary": "BYTEA",
    "bit": "BOOLEAN",
    "char": "CHAR",
    "date": "DATE",
    "datetime": "TIMESTAMP",
    "datetime2": "TIMESTAMP",
    "datetimeoffset": "TIMESTAMP WITH TIME ZONE",
    "decimal": "DECIMAL",
    "float": "DOUBLE PRECISION",
    "geography": "GEOGRAPHY",
    "geometry": "GEOMETRY",
    "hierarchyid": "TEXT",
    "image": "BYTEA",
    "int": "INTEGER",
    "money": "NUMERIC(19,4)",
    "nchar": "CHAR",
    "ntext": "TEXT",
    "numeric": "NUMERIC",
    "nvarchar": "VARCHAR",
    "real": "REAL",
    "smalldatetime": "TIMESTAMP(0)",
    "smallint": "SMALLINT",
    "smallmoney": "NUMERIC(10,4)",
    "sql_variant": "TEXT",
    "sysname": "VARCHAR(128)",
    "text": "TEXT",
    "time": "TIME",
    "timestamp": "BYTEA",  # rowversion
    "tinyint": "SMALLINT",
    "uniqueidentifier": "UUID",
    "varbinary": "BYTEA",
    "varchar": "VARCHAR",
    "xml": "XML",
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
    return [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

def get_data_chunks(cursor, batch_size=5000):
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows 


# def upload_ref(name):

def create_table(name: str) -> bool:
    EXCLUDED = {
        'PREDEFINEDID',
        'VERSION',
    }
    real_name = name[1:].upper()
    sql_statement = f'''
        DROP TABLE IF EXISTS {real_name};
        create table {real_name} (
    '''
    
    df = pd.read_excel('./vcb v1.xlsx', 
        sheet_name='fields',
        header=None)
    result = df[df[3] == name]
    
    if not result.empty:
        lines = []
        for _, row in result.iterrows():
            col_name = row[4].upper()[1:]
            if col_name in EXCLUDED: 
                continue
            
            # Пропускаем вторую часть ссылки (RRREF), так как мы обрабатываем их парами
            if col_name.endswith('RRREF'):
                continue

            col_name_pure_ = re.search(r"^FLD\d+", col_name)
            col_name_pure = col_name_pure_.group(0) if col_name_pure_ else col_name
            
            if re.search(r"(RRREF|RTREF)$", col_name):
                ref_type = 2
                # Берем дефолтное значение для ссылки из 7-й или 8-й колонки Excel
                ref_ref = '10000000' if 'Перечисление' in str(row[7]) else (row[8] if pd.notna(row[8]) else '10000000')
            elif (re.search(r"RREF$", col_name) 
                    and col_name != 'IDRREF' 
                    and 'PARENT' not in col_name):
                ref_type = 1
                ref_ref = '10000000' if 'Перечисление' in str(row[7]) else (row[8] if pd.notna(row[8]) else '10000000')
            elif col_name == 'IDRREF':
                ref_type = 3
                ref_ref = row[0]
            elif 'PARENT' in col_name:
                ref_type = 4
                ref_ref = row[0]
            else: 
                ref_type = 0
                ref_ref = ''
                
            data_type = str(row[10]).strip().lower()
            p1 = int(float(row[11])) if pd.notna(row[11]) else None
            if p1 == -1:
                p1 = 'max'
            p2 = int(float(row[12])) if pd.notna(row[12]) else None
            
            if data_type.startswith(('decimal', 'numeric')):
                args_str = f"{p1}, {p2}"
            else:
                args_str = f"{p1}"
                
            # skip TYPE (common, binary(1) field)
            if 'TYPE' in col_name: 
                continue
                
            # Обработка типов полей
            if ref_type in (1, 2):
                # Очищаем суффиксы RTREF/RRREF, чтобы получить чистое имя поля для пары
                base_col = re.sub(r'(RTREF|RRREF)$', '', col_name)
                lines.append(f"\t{base_col}RTREF\tbinary(4) default 0x{ref_ref} not null")
                lines.append(f"\t{base_col}RRREF\tbinary(16) not null")
            elif ref_type == 3:
                lines.append(f"\tIDTREF\tbinary(4) default 0x{ref_ref} not null")
                lines.append(f"\tIDRREF\tbinary(16) not null")
            elif ref_type == 4:
                lines.append(f"\tPARENTIDRTREF\tbinary(4) default 0x{ref_ref} not null")
                lines.append(f"\tPARENTIDRRREF\tbinary(16) not null")
            elif ref_type == 0:
                lines.append(f"\t{col_name_pure} \t{data_type} ({args_str})")
                
        lines.append(f'\tCONSTRAINT PK_{real_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF)')
        sql_statement += ",\n".join(lines)    
        
    sql_statement += "\n);"
    print(sql_statement)
def create_table_(name: str) -> bool:
    EXCLUDED = {
        'PREDEFINEDID',
        'VERSION',
        }
    real_name = name[1:].upper()
    sql_statement = f'''
        DROP TABLE IF EXISTS {real_name};
        create table {real_name} (
    '''
    
    df = pd.read_excel('./vcb v1.xlsx', 
        sheet_name='fields',
        header=None)
    result = df[df[3] == name]
    
    if not result.empty:
        lines = []
        idx = []
        for _, row in result.iterrows():
            col_name = row[4].upper()[1:]
            if col_name in EXCLUDED: 
                continue
            col_name_pure_ = re.search(r"^FLD\d+", col_name)
            col_name_pure = col_name_pure_.group(0) if col_name_pure_ else col_name
            if re.search(r"(RRREF|RTREF)$", col_name):
                ref_type = 2
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
            data_type = str(row[10]).strip().lower()
            p1 = int(float(row[11])) if pd.notna(row[11]) else None
            if p1 == -1:
                p1 = 'max'
            p2 = int(float(row[12])) if pd.notna(row[12]) else None
            if data_type.startswith(('decimal', 'numeric')):
                args_str = f"{p1}, {p2}"
            else:
                args_str = f"{p1}"
            # skip TYPE (common, binary(1) field)
            if 'TYPE' in col_name: continue
            # lines.append(f"\t{col_name_pure} \t{data_type} ({args_str})")
            if ref_type == 1 :
                lines.append(f"\t{col_name_pure}RTREF\tbinary(4) default 0x{ref_ref} not null")
                lines.append(f"\t{col_name_pure}RRREF\tbinary(16) not null")
            if ref_type == 3 :
                lines.append(f"\tIDTREF\tbinary(4) default 0x{ref_ref} not null")
                lines.append(f"\tIDRREF\tbinary(16) not null")
            if ref_type == 4:
                lines.append(f"\tPARENTIDRTREF\tbinary(4) default 0x{ref_ref} not null")
                lines.append(f"\tPARENTIDRRREF\tbinary(16) not null")
            if ref_type == 0:
                lines.append(f"\t{col_name_pure} \t{data_type} ({args_str})")
        lines.append(f'\tCONSTRAINT PK_{real_name} PRIMARY KEY CLUSTERED (IDTREF, IDRREF)')

        sql_statement += ",\n".join(lines)    
    sql_statement += "\n);"
    print(sql_statement)
    return True
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
        # Указываем разделитель ';'
        reader = csv.DictReader(f, delimiter=';')
        chunk = []
        
        for row in reader:
            processed_row = {
                'ZREF': convert_hex_to_bytes(row.get('ZREF')),
                'ZSYN': row.get('ZSYN'),
                'ZDESCR': row.get('ZDESCR')
                # 'ZTYPE' не берем, если в БД срабатывает DEFAULT
            }
            chunk.append(processed_row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    # ... (здесь ваше создание engine) ...


    metadata = MetaData()
    zenum_table = Table('ZENUM', metadata, autoload_with=engine)

    try:
        with engine.begin() as connection:
            for chunk in read_csv_chunks('./enums.csv', chunk_size=200):
                connection.execute(zenum_table.insert(), chunk)
                
        print("Все данные успешно загружены порциями без Pandas!")

    except Exception as e:
        print(f"Произошла ошибка, всё откачено: {e}")