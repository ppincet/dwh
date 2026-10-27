--- -- create part
drop table if exists ZLSF_OPERATION;
create table ZLSF_OPERATION (
	ZID bigint primary key,
	ZOPERATION nvarchar(100),
	ZROPERATION nvarchar(100),
	ZOPID nvarchar(100)
	)
;--- -- select part
select key0,
	operation_name_operation,
	operation_namereturn_operation,
	operation_id_operation
from operation_operation

;---  -- insert part
insert ZLSF_OPERATION (
    ZID,
    ZOPERATION,
    ZROPERATION,
    ZOPID 
	)
values (?, ?, ?, ?)