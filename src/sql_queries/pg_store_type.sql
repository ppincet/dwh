--- -- create part
drop table if exists ZLSF_STRTYP;
CREATE TABLE ZLSF_STRTYP
(
    ZKEY0 BIGINT NOT NULL,
    ZSTR_CSTOR BIGINT NULL,
    ZPRCL_CALC BIGINT NULL,
    ZPRCL BIGINT NULL,
    ZSTR_ID NVARCHAR(100) NULL,
    ZSTR_TYP NVARCHAR(100) NULL,

    PRIMARY KEY (ZKEY0 ASC)
)
;--- --select section
select
    key0,
    store_chainstores_storetype,
    priceliststore_retailcalcpricelisttype_storetype,
    priceliststore_retailpricelisttype_storetype,
    store_id_storetype,
    store_name_storetype
    -- range_userange_storetype,
    --store_inactive_storetype,
    -- pricelimit_pricelimitpricelisttype_storetype,
    -- purchase_skipcheckdaysinvoiceorderdetail_storetype,
    -- inventorysanta_instoretype_storetype,
    -- store_storetypegroup_storetype
from store_storetype
;--- -- insert part
insert ZLSF_STRTYP (
    ZKEY0,
    ZSTR_CSTOR,
    ZPRCL_CALC,
    ZPRCL,
    ZSTR_ID,
    ZSTR_TYP
)
values (?, ?, ?, ?, ?, ?)
