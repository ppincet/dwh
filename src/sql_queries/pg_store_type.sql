--- beware of the sequence - 
CREATE TABLE DBO.STORE_STORETYPE
(
    ZKEY0 BIGINT NOT NULL,
    ZSTR_CSTOR BIGINT NULL,
    ZPRCL_CALC BIGINT NULL,
    ZPRCL BIGINT NULL,
    ZSTR_ID NVARCHAR(100) NULL,
    ZSTR_NAME NVARCHAR(100) NULL,
    -- ZRANGE_USERANGE_STORETYPE INT NULL,
    -- ZSTORE_INACTIVE_STORETYPE INT NULL,
    -- ZPRICELIMIT_PRICELIMITPRICELISTTYPE_STORETYPE BIGINT NULL,
    -- ZPURCHASE_SKIPCHECKDAYSINVOICEORDERDETAIL_STORETYPE INT NULL,
    -- ZINVENTORYSANTA_INSTORETYPE_STORETYPE INT NULL,
    -- ZSTORE_STORETYPEGROUP_STORETYPE BIGINT NULL,
    CONSTRAINT STORE_STORETYPE_PKEY PRIMARY KEY CLUSTERED (ZKEY0 ASC)
);
CREATE NONCLUSTERED INDEX STORE_ID_STORETYPE_KEY0_IDX_STORE_STORETYPE
    ON DBO.STORE_STORETYPE (ZSTORE_ID_STORETYPE ASC, ZKEY0 ASC);
--- select section
select
    key0,
    store_chainstores_storetype,
    priceliststore_retailcalcpricelisttype_storetype,
    priceliststore_retailpricelisttype_storetype,
    store_id_storetype,
    store_name_storetype
    -- range_userange_storetype,
    -- store_inactive_storetype,
    -- pricelimit_pricelimitpricelisttype_storetype,
    -- purchase_skipcheckdaysinvoiceorderdetail_storetype,
    -- inventorysanta_instoretype_storetype,
    -- store_storetypegroup_storetype
from store_storetype
