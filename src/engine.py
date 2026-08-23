# main entry point
# from config import settings
import pyodbc
import typer
from utils import db_helper
import process


app = typer.Typer(
    help="CLI Engine ", add_completion=False
)

@app.command()
def daily(log_type: str = typer.Option(
        "full",
        "--log-type",
        help="Log type. Options: full, medium, successfull",
    ),):


    for k,i in db_helper.get_conn_strings().items():
        print(f'who:{k}')
        print(f'item:{i}')
    print(f'log: {log_type}')

@app.command()
def init(log_type: str = typer.Option(
        "full",
        "--log-type",
        help="Log type. Options: full, medium, successfull",
    ),
    mode: str = typer.Option(
        "daily", "--mode", help="Start mode. Options: daily, spec"
    ),
):
    '''
        system init
    '''
    db_helper.create_table('_Reference133')
@app.command()
def upd():
    '''
        system update
    '''
    typer.echo('upd done')
if __name__ == "__main__":
    try:
        app()  
    except Exception as critical:
        print(critical)

  
  
