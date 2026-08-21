# main entry point
# from config import settings
import pyodbc
import typer
from utils import db_helper
import process

app = typer.Typer(
    help="Утилита управления движком (Engine CLI)", add_completion=False
)

@app.command()
def init():
    '''
        system init
    '''
    # process.init_subkonto()
    # db_helper.create_table('_Reference133')
    print(f'initial: {0xBFE2F6CAE319E4354248DB8359EFE3E6}')
    print(db_helper.get_next_id(1))
@app.command()
def upd():
    '''
        system update
    '''
    typer.echo('upd done')

# def get_data_chunks(cursor, batch_size=5000):
#     while True:
#         rows = cursor.fetchmany(batch_size)
#         if not rows:
#             break
#         yield rows 
if __name__ == "__main__":
  app()
# driver = '{ODBC Driver 18 for SQL Server}'
# src_params = {
#     'DRIVER' : '{ODBC Driver 18 for SQL Server}',
#     'PORT' : settings.SRC_PORT,
#     'SERVER' : settings.SRC_SRV,
#     'DATABASE' : settings.SRC_DB,
#     'UID' : settings.SRC_USR,
#     'PWD' : settings.SRC_PWD,
#     'TrustServerCertificate' : 'yes'
# }
# dst_params = {
#     'DRIVER' : '{PostgreSQL Unicode}',
#     'PORT' : settings.DST_PORT,
#     'SERVER' : settings.DST_SRV,
#     'DATABASE' : settings.DST_DB,
#     'UID' : settings.DST_USR,
#     'PWD' : settings.DST_PWD,
    
# }

# conn_str_src = ";".join([f"{k}={v}" for k, v in src_params.items()])
# conn_str_dst = ";".join([f"{k}={v}" for k, v in dst_params.items()])
# try:
#     src_conn = pyodbc.connect(conn_str_src)
#     dst_conn = pyodbc.connect(conn_str_dst)


# except Exception as e:
#     print(f'fatal: {e}')
# finally:
#     src_conn.close()
#     dst_conn.close()
#     print ('hello, world!')
