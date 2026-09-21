import datetime
from utils import db_helper, common
from typing import List, Dict, Optional
import importlib

session = common.create_session()

def create_refs(content: Dict[str, Optional[str]], aliases_only: bool, view_only: bool) -> None:
    try:
        for k, v in content.items():
            if k is None: continue
            if not view_only:
                db_helper.create_ref(f'{k}', 
                    v if v is not None else f'VREF{k}',
                    aliases_only,
                    session)
            else:
                db_helper.create_view_standalone(k, v, aliases_only, session)
            print(f'{k} done at {datetime.datetime.now()}')
    except Exception as e:
        print(f'fatal : {e}')
    print(f'{datetime.datetime.now()} : done create refs')
def check_etl_bot():
    db_helper.check_etl_bot(session)

def get_fact_table(period: str = 'AUTO', is_odinass = True) -> None:
    period_range = (
        common.get_rolling_window_standard(True) if period == 'AUTO' else common.parse_date_range(period, is_odinass)
    )
    session['command'] = 'START ETL'
    db_helper.get_fact_table(*period_range, session)
def check_updates() -> None:
    print('check done')
def start_etl() -> None:
    try:
        result = get_fact_table()
        result = check_updates()
        # commit log
    except Exception as e:
        print(f'exception : {e}')
def do_init(content: dict[str, str], aliases_only: bool) -> None:
    create_refs(content, aliases_only, False, session)
def perform_command(module_name: str, command: str, args: dict[str, str]) -> None:
    method = getattr(importlib.import_module(module_name), command, **args)
    if callable(method): method(**args)
def upload_docs() -> None:
    db_helper.upload_docs(*common.get_rolling_window_standard(True), session)
    
    

