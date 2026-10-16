--- -- create part
drop table if exists ZLSF_CITY;
create table ZLSF_CITY (
    ZID bigint not null,
    ZREG bigint,
    ZCITY nvarchar(100),
    primary key (ZID)
)
;--- -- select part
select 
    key0,
    stock_region_city,
    stock_name_city
from stock_city
;--- -- insert part
insert ZLSF_CITY (
    ZID,
    ZREG,
    ZCITY
) 
values (?, ?, ?)