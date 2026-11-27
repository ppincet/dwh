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

def run_bcp_bin(
    file_path: str,
    batch_size: int,
    mode: str,
    table_name:str | None = None,
    sql_statement: str | None = None
):
    if mode == "in":
        target = table_name
        direction = "in"
        extra_flags = ["-E", "-h", "TABLOCK"]
    else:
        target = sql_statement
        direction = "queryout"
        extra_flags = []

    
    cmd = [
        "bcp", 
        target,
        direction,
        file_path,
        "-S", settings.DST_SRV,  
        "-d", settings.DST_DB, 
        "-U", settings.DST_USR, 
        "-P", settings.DST_PWD,
        "-n",
        "-b", str(batch_size),
        "-a", "65535",
        "-e", "./logs/bcp_error_rows.err",
        *extra_flags
    ] 
    return
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
        error_msg = (
            f"bcp failed for file {file_path}\n"
            f"STDERR: {result.stderr}\n"
            f"STDOUT: {result.stdout}"
        )
        raise RuntimeError(error_msg)

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
        error_msg = (
            f"bcp failed for file {csv_filepath}\n"
            f"STDERR: {result.stderr}\n"
            f"STDOUT: {result.stdout}"
        )
        raise RuntimeError(error_msg)
    