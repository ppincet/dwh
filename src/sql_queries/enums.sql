--- -- region create
drop table if exists ZENUM;
create table ZENUM (
    ZTYPE binary(4) not null default 0x10000000,
    ZREF binary(16) not null,
    ZSYN nvarchar(128),
    ZDESCR nvarchar(255),
    ZIOBJECT bigint,
    primary key clustered ([ZTYPE] asc, [ZREF] asc)
)
;--- -- region populate
insert ZENUM (
    ZTYPE,
    ZREF,
    ZSYN,
    ZDESCR,
    ZIOBJECT) 
values (?, ?, ?, ?, ?)
;--- -- region create view
DROP VIEW IF EXISTS [dbo].[ZVENUM];

create view [dbo].[ZVENUM] as
select 
	ZSYN,
	ZDESCR,
	ID,
	ZIOBJECT
from ZENUM ze
join ZSUBKONTO zs
on ze.ZTYPE = zs.Z_TYPE and ze.ZREF = zs.Z_REF