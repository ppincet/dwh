--- --create part
drop table if exists ZLSF_GRP;
create table ZLSF_GRP (
    ZID bigint not null,
    ZGRLVL integer,
    ZSGRP1 bigint,
    ZSGRP2 bigint,
    ZSGRP3 bigint,
    ZSGRP4 bigint,
    ZSGRP5 bigint,
    ZSGRP6 bigint,
    ZSGRPGRP nvarchar(250),
    primary key (ZID)
)
;--- --select part
select 
	key0,
	stock_level_group,
	stock_group1_group,
	stock_group2_group,
	stock_group3_group,
	stock_group4_group,
	stock_group5_group,
	stock_group6_group,
	stock_name_group
from stock_group
;--- --insert part
insert ZLSF_GRP (
    ZID,
    ZGRLVL,
    ZSGRP1,
    ZSGRP2,
    ZSGRP3,
    ZSGRP4,
    ZSGRP5,
    ZSGRP6,
    ZSGRPGRP
)
values (?, ?, ?, ?, ?, ?, ?, ?, ?)