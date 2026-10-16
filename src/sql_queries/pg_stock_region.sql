--- -- create part
drop table if exists ZLSF_REG;
create table ZLSF_REG (
    ZID bigint not null,
    ZRID bigint,
    ZREG nvarchar(100),
    primary key (ZID)
)
;--- -- select part
select 
    key0,
    stock_id_region,
    stock_name_region
from stock_region
;--- -- insert part
insert ZLSF_REG (
    ZID,
    ZRID,
    ZREG
) 
values (?, ?, ?)