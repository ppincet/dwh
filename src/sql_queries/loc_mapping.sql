--- --[0] create region
create table dbo.ZLOCMAP (
    ZID bigint identity(1,1) not null,
    ZLID bigint null,
    ZOID bigint null,
    ZDPT nvarchar(20) null,
    constraint PK_ZLOCMAP primary key clustered (ZID asc)
);

create nonclustered index IX_ZLOCMAP_ZLID
    on dbo.ZLOCMAP (ZLID asc)
    include (ZDPT);

create nonclustered index IX_ZLOCMAP_ZOID
    on dbo.ZLOCMAP (ZOID asc)
    include (ZDPT);

;--- --[1] populate region
insert ZLOCMAP (
    ZLID,
    ZOID,
    ZDPT
)
select 
	ZID,
    coalesce(ZBGUID, 0),
	ZDEPID
from ZLSF_DPT d
left join ZBSTLOC l
on ZBGN042 = ZDEPID