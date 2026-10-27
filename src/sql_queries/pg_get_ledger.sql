--- -- ledger region
select 
        ssku.key0 sid,
        s.key0 ds, 
        cast(saleledger_valuevat_saleledger as numeric(10,5)) value_vat,
        cast(saleledger_valuevat_saleledger / (100 + saleledger_valuevat_saleledger) as numeric(10,5)) p_vat,
        cast(stock_netweight_sku * saleledger_cost_saleledger_batch as numeric(18, 4)) netw,
        cast(saleledger_cost_saleledger_batch * stock_grossweight_sku as numeric(18, 4)) grossw,
        coalesce(cast(l.saleledger_quantity_saleledger * stock_volume_sku as numeric(18,4)),0) vol,
        l.saleledger_quantity_saleledger qnt,
        ssku.barcode_idbarcode_sku barcode,
        l.saleledger_costsum_saleledger revenuec,
        cast(lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * l.saleledger_costsum_saleledger as numeric(18,4)) b_revenuec,
        cast(l.saleledger_datetime_saleledger as date) dt_v,
        lb.saleledger_cost_saleledger_batch b_cost,
        cast(lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * l.saleledger_sum_saleledger as numeric(18, 4)) b_sum,
		    cast(sb.stock_cost_batch as decimal(18,4)) m_price,
        cast(case when l.saleledger_description_saleledger = 'Продажа за день'
				then 581 else 580
			end as bigint) op,
     lb.key1,
     l.key0 

    from saleledger_saleledger l
    join saleledger_saleledgerbatch lb on lb.key0 = l.key0
    join store_departmentstore s on l.saleledger_stock_saleledger = s.key0
    join stock_sku ssku on ssku.key0 = l.saleledger_sku_saleledger
	  join stock_batch sb on sb.key0 = lb.key1
	
	  join stock_stock ss on ss.key0 = s.key0
    where l.saleledger_date_saleledger >= ?::timestamp
      and l.saleledger_date_saleledger < ?::timestamp
      and l.saleledger_isposted_saleledger is not null 
      and l.saleledger_skip_saleledger is null
      and l.saleledger_description_saleledger in (
	  	  'Продажа за день',
		 'Возврат за день'
		)
      and (l.saleledger_datetime_saleledger >= s.cashregister_startdategroupcashregister_departmentstore 
           or s.cashregister_startdategroupcashregister_departmentstore is null)
      and (l.key0, lb.key1) > (?, ?)
    order by l.key0, lb.key1
    limit ?

;--- -- sku ledger region
  sku ledger