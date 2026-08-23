import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
except ImportError:
    print('import error')
else:
    SRC_1CB_SRV = os.environ['SRC_1CB_SRVR']
    SRC_1CB_PORT = os.environ['SRC_1CB_PORT']
    SRC_1CB_USR = os.environ['SRC_1CB_USR']
    SRC_1CB_PWD = os.environ['SRC_1CB_PWD']
    SRC_1CB_DB = os.environ['SRC_1CB_DB']
    SRC_1CB_DRV = f"{{{os.environ['SRC_1CB_DRV']}}}"
    DST_SRV = os.environ['DST_SRVR']
    DST_PORT = os.environ['DST_PORT']
    DST_USR = os.environ['DST_USR']
    DST_PWD = os.environ['DST_PWD']
    DST_DB = os.environ['DST_DB']
    DST_DRV = f"{{{os.environ['DST_DRV']}}}"
   