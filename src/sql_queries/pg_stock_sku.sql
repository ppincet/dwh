--- --create part
drop table if exists ZLSF_SKU;
create table ZLSF_SKU
(
    ZID bigint not null,
    ZSTKGRP bigint not null,
    ZSTKCODE nvarchar(100),
    ZBARCODE varchar(15),
    ZNETW numeric(12, 6),
    ZGROSSW numeric(12, 6),
    ZVOL numeric (10, 4),
    ZSKU nvarchar(255),
    primary key (ZID, ZSTKGRP)
);--- --select part
select 
	key0 id,
    stock_skugroup_sku,
	stock_id_sku code,
	barcode_idbarcode_sku barcode,
	stock_netweight_sku weight,
	stock_grossweight_sku grossw,
	stock_volume_sku vol,
	stock_name_sku sku
from stock_sku
;--- -- insert part
insert ZLSF_SKU (
    ZID,
    ZSTKGRP,
    ZSTKCODE,
    ZBARCODE,
    ZNETW,
    ZGROSSW,
    ZVOL,
    ZSKU
) 
values (?, ?, ?, ?, ?, ?, ?, ?)