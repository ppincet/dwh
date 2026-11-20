insert into dbo.ETL_TEMPDB_LOG (
	RUN_ID, 
    STEP_NAME,
    DT_V,
    FILE_ID,
	TOTAL_MB, 
    FREE_MB, 
    USER_OBJ_MB, 
    INTERNAL_OBJ_MB, 
    VERSION_STORE_MB
)
select
	?,
    ?,
    ?,
    0,
    cast(coalesce(sum(total_page_count), 0) * 8.0 / 1024 as decimal(12, 2)),
    cast(coalesce(sum(unallocated_extent_page_count), 0) * 8.0 / 1024 as decimal(12, 2)),
    cast(coalesce(sum(user_object_reserved_page_count), 0) * 8.0 / 1024 as decimal(12, 2)),
    cast(coalesce(sum(internal_object_reserved_page_count), 0) * 8.0 / 1024 as decimal(12, 2)),
    cast(coalesce(sum(version_store_reserved_page_count), 0) * 8.0 / 1024 as decimal(12, 2))
from tempdb.sys.dm_db_file_space_usage;
