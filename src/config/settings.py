import os
from pathlib import Path
from dotenv import load_dotenv

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
except ImportError:
    print('import error')
else:
    SRC_SRV = os.environ['SRC_SRVR']
    SRC_PORT = os.environ['SRC_PORT']
    SRC_USR = os.environ['SRC_USR']
    SRC_PWD = os.environ['SRC_PWD']
    SRC_DB = os.environ['SRC_DB']
    SRC_DRV = os.environ['SRC_DRV']
    DST_SRV = os.environ['DST_SRVR']
    DST_PORT = os.environ['DST_PORT']
    DST_USR = os.environ['DST_USR']
    DST_PWD = os.environ['DST_PWD']
    DST_DB = os.environ['DST_DB']
    DST_DRV = os.environ['DST_DRV']
   