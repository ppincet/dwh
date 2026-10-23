import subprocess
import sys
from config import settings
import os

def get_object_size_mb(obj):
    seen = set()
    
    def inner(o):
        o_id = id(o)
        if o_id in seen:
            return 0
        seen.add(o_id)
        
        size = sys.getsizeof(o)
        if isinstance(o, (list, tuple, set, frozenset)):
            size += sum(inner(item) for item in o)
        elif isinstance(o, dict):
            size += sum(inner(k) + inner(v) for k, v in o.items())
        return size
    return inner(obj) / (1024 * 1024)

def run_bcp_import(
    csv_filepath: str,
    table_name: str,
    delimiter: str = "\t",
):
    cmd = [
        "bcp", table_name,
        "in", csv_filepath,
        "-c", 
        "-t", delimiter, 
        "-r", "\n", # !!!!! \r\n for win 
        "-h", "TABLOCK",  
        "-u",
        "-S", settings.DST_SRV,  
        "-d", settings.DST_DB, 
        "-U", settings.DST_USR, 
        "-P", settings.DST_PWD,
        "-k",
        "-e", "./logs/bcp_error_rows.err"
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        text=True,  
        encoding="cp866",  
    )

    if result.returncode == 0:
    
        return result.stdout
    else:
        raise RuntimeError(f"bcp failed for file {csv_filepath}")