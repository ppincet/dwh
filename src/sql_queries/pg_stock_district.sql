--- -- create part
drop table if exists ZLSF_DISTR;
create table ZLSF_DISTR (
    ZID bigint not null,
    ZDISTR nvarchar(100),
    primary key (ZID)
)
;--- -- select part
select 
    key0,
    stock_name_district
from stock_district
;--- -- insert part
insert ZLSF_DISTR (
    ZID,
    ZDISTR
) 
values (?, ?)