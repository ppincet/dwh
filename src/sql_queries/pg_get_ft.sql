--- -- select part
with raw_chunk as (
    select 
        l.key0, 
        lb.key1 batch_id,
        ssku.key0 sid,
        s.key0 ds, 
        saleledger_valuevat_saleledger value_vat,
        saleledger_valuevat_saleledger / (100 + saleledger_valuevat_saleledger) p_vat,
        store_id_departmentstore,
        stock_name_sku ssku,
        stock_netweight_sku * saleledger_cost_saleledger_batch netw,
        stock_netweight_sku netws,
        saleledger_cost_saleledger_batch * stock_grossweight_sku grossw,
        l.saleledger_quantity_saleledger * stock_volume_sku vol,
        l.saleledger_quantity_saleledger qnt,
        ssku.barcode_idbarcode_sku barcode,
        l.saleledger_sum_saleledger revenue,
        l.saleledger_costsum_saleledger revenuec,
        lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * l.saleledger_costsum_saleledger b_revenuec,
        l.saleledger_datetime_saleledger dt_vv,
        l.saleledger_stock_saleledger,
        lb.saleledger_cost_saleledger_batch b_cost,
        lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * l.saleledger_sum_saleledger b_sum
    from saleledger_saleledger l
    join saleledger_saleledgerbatch lb on lb.key0 = l.key0
    join store_departmentstore s on l.saleledger_stock_saleledger = s.key0
    join stock_sku ssku on ssku.key0 = l.saleledger_sku_saleledger
    where l.saleledger_date_saleledger >= timestamp ?
      and l.saleledger_date_saleledger < timestamp ?
      and l.saleledger_isposted_saleledger is not null 
      and l.saleledger_skip_saleledger is null
      and l.saleledger_description_saleledger in ('Продажа за день', 'Возврат за день')
      and (l.saleledger_datetime_saleledger >= s.cashregister_startdategroupcashregister_departmentstore 
           or s.cashregister_startdategroupcashregister_departmentstore is null)
      and (l.key0, lb.key1) > (?, ?)
    order by l.key0, lb.key1
    limit ?
),
main_chunk as (
    select *,
           b_sum - b_sum * p_vat b_sum_net
    from raw_chunk
)
select 
    mc.ds ds, 
    mc.sid sku,
    max(mc.barcode) barcode,
    mc.ssku,
    cast(max(mc.b_sum_net / mc.b_cost) as numeric(18,4)) p_price,
    cast(sum(mc.b_cost) as numeric(16, 5)) qnt,
    cast(sum(mc.b_sum) as numeric(18,4)) r_sum,
    cast(sum(mc.b_sum_net) as numeric(18,4)) n_sum,
    cast(max(mc.value_vat) as numeric(4,2)) vat,
    cast(sum(mc.netw) as numeric(16,5)) netw,
    cast(sum(mc.grossw) as numeric(16,5)) grossw,
    cast(sum(mc.vol) as numeric(16,5)) vol,
    cast(sum(mc.b_revenuec) as numeric(18,4)) bn_sum,
    cast(sum(mc.b_sum_net - mc.b_revenuec) as numeric(18,4)) grossin,
    cast(sum(mc.b_sum_net - mc.b_revenuec) / sum(mc.b_sum_net) as numeric(18,4)) p_grossin,
    cast(sum((mc.b_sum_net / mc.b_cost - p.m_price)) / sum(p.m_price) as numeric(18,4)) markup,
    mc.dt_vv _period
from main_chunk mc
join lateral (
    select 
        stock_cost_batch m_price
    from stock_batch b
    where b.key0 = mc.batch_id
    limit 1
) p on true
group by mc.dt_vv, 
    mc.ds,
    mc.sid
   
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
