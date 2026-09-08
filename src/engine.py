# main entry point
# from config import settings
import pyodbc
import typer
# from utils import db_helper
import process
from typing import Optional
from itertools import zip_longest


app = typer.Typer(
    help="CLI Engine ", add_completion=False
)

@app.command()
def manual(period: str = typer.Option(
        "--period",
        help="period_from(optional)  - period_to (optional)"
    ),
        is_odinass: bool = typer.Option(
            False,
            '--is-odinass',
            help = 'odinass date'
        )):
    process.get_fact_table(period, is_odinass)

@app.command()
def daily(log_type: Optional[str] = typer.Option(
        "full",
        "--log-type",
        help="Log type. Options: full, medium, successfull",
    ),
    ):
    process.start_etl()


@app.command()
def init(log_type: str = typer.Option(
        "full",
        "--log-type",
        help = "Log type. Options: full, medium, successfull",
    ),
    mode: str = typer.Option(
        "daily", "--mode", help = "Start mode. Options: daily, spec"
    ),
    ref_list: Optional[str] = typer.Option(
        None,
        "--ref-list",
        help = "Comma-separated list of references (e.g. 15,35,90)",
    ),
    view_list: Optional[str] = typer.Option(
        None,
        "--view-list",
        help = "Comma-separated list of views names (e.g. NOVIEW, SPEC)",
    ),
    aliases_only: bool = typer.Option(
        False,
        "--aliases-only",
        help="creates view if set",
    ),
    period: str = typer.Option(
        "--period",
        help="period_from(optional)  - period_to (optional)"
    )
    
):
    '''
        system init
    '''
    refs = []
    views = []
    if ref_list:
        refs = [item.strip() for item in ref_list.split(",") if item.strip()]
    if view_list:
        views = [item.strip() for item in view_list.split(",") if item.strip()]
    content = dict(zip_longest(refs, views, fillvalue=None))
    # 2do
    # create non REF
    # create view only
    # process.create_refs(content, aliases_only)
    #process.get_fact_table()

    print('done')
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

  
  
