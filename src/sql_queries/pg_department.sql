--- -- create part
drop table if exists ZLSF_DPT;
create table ZLSF_DPT (
    ZID bigint not null,
    ZDEPID nvarchar(100),
    ZSTRID nvarchar(100),
    ZDEP nvarchar(150),
    ZDEPTYP bigint,
    ZDEPREG bigint,
    ZRET char(1),
    ZACT integer,
    primary key (ZID)
)
;--- -- select part
select 
    sds.key0 id,
	store_id_departmentstore dp,
	store_id_store storeid,
	store_name_departmentstore sn,
	store_storetype_store stype,
	store_region_store region,
	coalesce(store_retaildepartment_departmentstore::char(1), '') isretail,
	coalesce(store_inactive_departmentstore, 0) isinactive
from store_departmentstore sds
left join store_store ss
on sds.store_store_departmentstore = ss.key0

;--- -- insert part
insert ZLSF_DPT (
    ZID,
    ZDEPID,
    ZSTRID,
    ZDEP,
    ZDEPTYP,
    ZDEPREG,
    ZRET,
    ZACT
)
values (?, ?, ?, ?, ?, ?, ?, ?)