create table ETL_TEMPDB_LOG (
	LOG_ID bigint identity(1,1) not null primary key,
	RUN_ID uniqueidentifier not null,
	STEP_NAME sysname not null,
	DT_V date null,
	CAPTURED_AT datetime2(3) not null default sysdatetime(),
	FILE_ID int not null,
	TOTAL_MB decimal(12,2) not null,
	FREE_MB decimal(12,2) not null,
	USER_OBJ_MB decimal(12,2) not null,
	INTERNAL_OBJ_MB decimal(12,2) not null,
	VERSION_STORE_MB decimal(12,2) not null
);

create index IX_ETL_TEMPDB_LOG_RUN
on ETL_TEMPDB_LOG (RUN_ID, LOG_ID);