import pyodbc
from config import settings
from pathlib import Path

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
        'src' :{
            'DRIVER' : settings.SRC_DRV,
            'PORT' : settings.SRC_PORT,
            'SERVER' : settings.SRC_SRV,
            'DATABASE' : settings.SRC_DB,
            'UID' : settings.SRC_USR,
            'PWD' : settings.SRC_PWD,
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
        'src' : ";".join([f"{k}={v}" for k, v in params['src'].items()]),
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

def create_table(name, metadata):
    '''
    
    '''
def upload_ref(name):
