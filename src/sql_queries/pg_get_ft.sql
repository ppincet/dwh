--- -- select part
with main_chunk as (
    select 
        l.key0,
        lb.key1 batch_id,
        s.key0 ds, 
        lb.key1 sku,
        ssku.barcode_idbarcode_sku barcode,
        l.saleledger_quantity_saleledger qnt,
        l.saleledger_sum_saleledger revenue,
        l.saleledger_datetime_saleledger dt_vv,
        l.saleledger_stock_saleledger
    from saleledger_saleledger l
    join saleledger_saleledgerbatch lb on lb.key0 = l.key0
    join store_departmentstore s on l.saleledger_stock_saleledger = s.key0
    join stock_sku ssku on ssku.key0 = l.saleledger_sku_saleledger
    where l.saleledger_date_saleledger >= cast(? as timestamp)
      and l.saleledger_date_saleledger < cast(? as timestamp)
      and l.saleledger_isposted_saleledger is not null 
      and l.saleledger_skip_saleledger is null
      and (l.saleledger_datetime_saleledger >= s.cashregister_startdategroupcashregister_departmentstore 
           or s.cashregister_startdategroupcashregister_departmentstore is null)
        and (l.key0, lb.key1) > (?,?)
    order by l.key0, lb.key1, l.saleledger_stock_saleledger
    limit ?
)
select 
    mc.ds, 
    mc.sku,
    mc.barcode,
    mc.qnt,
    p.manufacturing_price, 
    mc.revenue,
    mc.dt_vv,
    mc.key0 id
from main_chunk mc
left join lateral (
    select pid.purchase_manufacturingprice_invoicedetail manufacturing_price
    from stock_batch b
    join purchase_shipmentdetail psd on b.key0 = psd.purchase_shipmentbatch_shipmentdetail
    join purchase_invoicedetail pid on psd.purchase_invoicedetail_shipmentdetail = pid.key0
    where b.key0 = mc.batch_id
      and pid.purchase_manufacturingprice_invoicedetail is not null
    limit 1
) p on true


;--- -- insert part
--truncate table ZLSF_FACT;
insert ZLSF_FACT (
	ZDSID,
	ZSKUID,
	ZBARCODE,
	ZAMNT,
	ZCOST,
	ZVAT,
	ZVOL,
	ZNETW,
	ZGROSSW,
	ZPERIOD
)	
values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
