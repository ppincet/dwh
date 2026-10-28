with raw_chunk as (
select 
	*  
from ZLSF_FACT_STG)
,main_chunk as (
	select *,
		 ZBSUM - ZBSUM * ZP_VAT ZBSUMNET
	from raw_chunk
)
select
    mc.ZDS ds, 
	mc.ZSID,
    max(mc.ZBARCODE) barcode,
    cast(max(mc.ZBSUMNET / mc.ZB_COST) as numeric(18,4)) p_price,
    cast(sum(mc.ZB_COST) as numeric(16, 5)) qnt,
    cast(sum(mc.ZBSUM) as numeric(18,4)) r_sum,
    cast(sum(mc.ZBSUMNET) as numeric(18,4)) n_sum,
    cast(max(mc.ZVALUE_VAT) as numeric(4,2)) vat,
    cast(sum(mc.ZNETW) as numeric(16,5)) netw,
    cast(sum(mc.ZGROSSW) as numeric(16,5)) grossw,
    cast(sum(mc.ZVOL) as numeric(16,5)) vol,
    cast(sum(mc.ZB_REVENUEC) as numeric(18,4)) bn_sum,
    cast(sum(mc.ZBSUMNET - mc.ZB_REVENUEC) as numeric(18,4)) grossin,
	cast(sum(mc.ZBSUMNET - mc.ZB_REVENUEC) as  numeric(18,4)) / nullif(sum(mc.ZBSUMNET),0)  p_grossin,
    cast(sum((mc.ZBSUMNET / mc.ZB_COST - mc.Z_PRICE)) / sum(mc.Z_PRICE) as numeric(18,4)) markup,
    mc.ZDT_V _period
from main_chunk mc
group by mc.ZDT_V, 
	mc.ZDS,
	mc.ZSID,
	mc.op