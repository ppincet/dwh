import subprocess
import sys


def run_bcp_import(
    csv_filepath: str,
    table_name: str,
    server: str,
    database: str,
    user: str,
    password: str,
    delimiter: str = "\t",
):
    """Вызывает утилиту bcp для заливки CSV-файла в MS SQL Server."""

    # Формируем команду bcp со всеми нужными флагами
    cmd = [
        "bcp",
        table_name,
        "in",
        csv_filepath,
        "-c",  # Символьный режим (для текстовых/CSV файлов)
        "-t",
        delimiter,  
        "-h",
        "TABLOCK",  
        "-S",
        server,  
        "-d",
        database, 
        "-U",
        user,  
        "-P",
        password,  
    ]

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