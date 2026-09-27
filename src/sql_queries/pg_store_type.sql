--- beware of the sequence - 
CREATE TABLE DBO.STORE_STORETYPE
(
    ZKEY0 BIGINT NOT NULL,
    ZSTORE_CHAINSTORES_STORETYPE BIGINT NULL,
    ZPRICELISTSTORE_RETAILCALCPRICELISTTYPE_STORETYPE BIGINT NULL,
    ZPRICELISTSTORE_RETAILPRICELISTTYPE_STORETYPE BIGINT NULL,
    ZSTORE_ID_STORETYPE NVARCHAR(100) NULL,
    ZSTORE_NAME_STORETYPE NVARCHAR(100) NULL,
    ZRANGE_USERANGE_STORETYPE INT NULL,
    ZSTORE_INACTIVE_STORETYPE INT NULL,
    ZPRICELIMIT_PRICELIMITPRICELISTTYPE_STORETYPE BIGINT NULL,
    ZPURCHASE_SKIPCHECKDAYSINVOICEORDERDETAIL_STORETYPE INT NULL,
    ZINVENTORYSANTA_INSTORETYPE_STORETYPE INT NULL,
    ZSTORE_STORETYPEGROUP_STORETYPE BIGINT NULL,
    CONSTRAINT STORE_STORETYPE_PKEY PRIMARY KEY CLUSTERED (ZKEY0 ASC)
);
CREATE NONCLUSTERED INDEX STORE_ID_STORETYPE_KEY0_IDX_STORE_STORETYPE
    ON DBO.STORE_STORETYPE (ZSTORE_ID_STORETYPE ASC, ZKEY0 ASC);
--- select section
select
    zkey0,
    zstore_chainstores_storetype,
    zpriceliststore_retailcalcpricelisttype_storetype,
    zpriceliststore_retailpricelisttype_storetype,
    zstore_id_storetype,
    zstore_name_storetype,
    zrange_userange_storetype,
    zstore_inactive_storetype,
    zpricelimit_pricelimitpricelisttype_storetype,
    zpurchase_skipcheckdaysinvoiceorderdetail_storetype,
    zinventorysanta_instoretype_storetype,
    zstore_storetypegroup_storetype
from store_storetype
