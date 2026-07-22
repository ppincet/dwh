import pyodbc

def get_data_chunks(cursor, batch_size=5000):
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows 

def transfer_data():
    
    
    src_cursor = src_conn.cursor()
    dst_cursor = dst_conn.cursor()
    dst_cursor.fast_executemany = True

    src_cursor.execute("SELECT col1, col2, col3 FROM dbo.SourceTable")

    
    for chunk in get_data_chunks(src_cursor, 5000):
        dst_cursor.executemany(
            "INSERT INTO dbo.TargetTable (col1, col2, col3) VALUES (?, ?, ?)", 
            chunk
        )
        dst_conn.commit()
    
#     conn_str_src = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=src_server;DATABASE=db_src;UID=user;PWD=pass"
# conn_str_dst = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=dst_server;DATABASE=db_dst;UID=user;PWD=pass"

# def transfer_data():
#     try:
#    
#         src_conn = pyodbc.connect(conn_str_src)
#         dst_conn = pyodbc.connect(conn_str_dst)
        
#         src_cursor = src_conn.cursor()
#         dst_cursor = dst_conn.cursor()

#    
#         dst_cursor.fast_executemany = True

#    
#         src_cursor.execute("SELECT col1, col2, col3 FROM dbo.SourceTable")
        
#         batch_size = 5000  # Оптимальный размер пакета
#         while True:
#             rows = src_cursor.fetchmany(batch_size)
#             if not rows:
#                 break
            
#         
#             dst_cursor.executemany(
#                 "INSERT INTO dbo.TargetTable (col1, col2, col3) VALUES (?, ?, ?)", 
#                 rows
#             )
#             dst_conn.commit()

#         print("success")

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         src_conn.close()
#         dst_conn.close()

# if __name__ == "__main__":
#     transfer_data()