--- -- create part
drop table if exists ZLSF_DPT;
create table ZLSF_DPT (
    ZID bigint not null,
    ZDEPID nvarchar(100),
    ZSTRID nvarchar(100),
    ZDEP nvarchar(150),
    ZDEPTYP bigint,
    ZADDR nvarchar(150),
    ZDEPCITY bigint,
    ZDEPDITR bigint,
    ZDEPREG bigint,
    ZOPND date,
    ZRENTSQ numeric(10, 2),
    ZTOTSQ numeric(10, 2),
    ZTMPCLD tinyint,
    ZRENT tinyint,
    ZIANCT tinyint,
    ZRET char(1),
    primary key (ZID)
)
;--- -- select part
-- with filtered as (
-- 	select
-- 		row_number() over (partition by key0 order by key1 desc) rn,
-- 		key0,
-- 		store_datatradingsquare_departmentstore_date tr_square
-- 	from store_departmentstoredate
-- 	where store_datatradingsquare_departmentstore_date is not null
-- )
-- select 
	
-- 	tr_square
-- from store_departmentstore ds
-- left join filtered f on ds.key0 = f.key0
-- where 1=1 
-- and rn = 1
select 
	sds.key0,
	store_id_departmentstore dp,
	store_id_store,
	store_name_departmentstore sn,
	store_storetype_store,
	ss.store_address_store,
	store_city_store,
	store_district_store,
	store_region_store,
	store_opendate_store,
	coalesce(store_rentsquare_store, 0),
	store_totalsquare_store,
	coalesce(store_temporaryclosed_store, 0),
	coalesce(store_rent_store, 0),
	coalesce(store_inactive_departmentstore, 0),
	coalesce(store_retaildepartment_departmentstore::char(1), '')
	
from store_departmentstore sds
join store_store ss on sds.store_store_departmentstore = ss.key0

;--- -- insert part
insert ZLSF_DPT (
    ZID, ZDEPID, ZSTRID, ZDEP, ZDEPTYP, ZADDR, 
    ZDEPCITY, ZDEPDITR, ZDEPREG, ZOPND, 
    ZRENTSQ, ZTOTSQ, ZTMPCLD, ZRENT, ZIANCT, ZRET
)
values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);