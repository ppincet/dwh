import subprocess
import sys
from config import settings
import os


def run_bcp_import(
    csv_filepath: str,
    table_name: str,
    delimiter: str = "\t",
):
    cmd = [
        "bcp", table_name,
        "in", csv_filepath, # it's possible 2 hardcode it
        "-c", 
        "-t", delimiter, 
        "-F", "2",
        "-h", "TABLOCK",  
        "-u",
        "-S", settings.DST_SRV,  
        "-d", settings.DST_DB, 
        "-U", settings.DST_USR, 
        "-P", settings.DST_PWD,
    ]

    for i, arg in enumerate(cmd):
        if not isinstance(arg, (str, bytes, os.PathLike)):
            print(f"ОШИБКА: Элемент с индексом {i} имеет тип {type(arg)}: {arg}")
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        text=True,  
        encoding="cp866",  
    )

    # Проверяем результат выполнения
    if result.returncode == 0:
        print("Импорт через bcp успешно завершен!")
        print(result.stdout)
    else:
        print(
            f"Ошибка выполнения bcp! Код ошибки: {result.returncode}",
            file=sys.stderr,
        )
        print("STDOUT:\n", result.stdout, file=sys.stderr)
        print("STDERR:\n", result.stderr, file=sys.stderr)
        raise RuntimeError(f"bcp failed for file {csv_filepath}")