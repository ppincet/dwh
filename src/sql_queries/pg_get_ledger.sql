--- -- ledger region
 select 
		s.key0 ds,
    ssku.key0 sid,
		ssku.barcode_idbarcode_sku barcode,  
		l.saleledger_quantity_saleledger n_mat,
		stock_netweight_sku * saleledger_cost_saleledger_batch netw, 
		saleledger_cost_saleledger_batch * stock_grossweight_sku grossw, 
		l.saleledger_quantity_saleledger * stock_volume_sku vol, 
		lb.saleledger_cost_saleledger_batch 
			/ l.saleledger_quantity_saleledger 
			* l.saleledger_sum_saleledger n_sum,
		saleledger_valuevat_saleledger r_vat, 
        stock_valuevat_batch b_vat,
		l.saleledger_quantity_saleledger * sb.stock_cost_batch base,
        l.saleledger_datetime_saleledger dt_v,
		cast(case when l.saleledger_description_saleledger = 'Возврат за день'
				then 1
				else 0
			end as integer) isret,
		cast(case when l.saleledger_description_saleledger = 'Возврат за день'
				then 581 
				else 580
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
--- -- sku region

with raw_chunk as(
SELECT 
	stock_netweight_sku,
	stock_grossweight_sku,
	stock_volume_sku, 
	stock_name_sku ssku,
	s.key0 ds,
	ssku.key0 sid,
	stockdocument_operation_stockdocumentledger op,
    l.stock_date_skuledger dt_v, 
	coalesce(sl.SkuLedger_isReturn_SkuLedger, 0) isret,
    CAST(- (CASE WHEN NOT lb.stock_cost_skuledger_batch = lb.stock_signedquantityactive_skuledger_batch 
				THEN -lb.stock_cost_skuledger_batch 
				ELSE lb.stock_cost_skuledger_batch 
			END) AS numeric(17,3)) n_mat, 
    CAST(- CASE WHEN (l.stock_quantity_skuledger = 0 
				OR l.stock_quantity_skuledger IS NULL) 
		THEN l.stock_signedsumactive_skuledger 
		ELSE (CASE WHEN NOT lb.stock_cost_skuledger_batch = lb.stock_signedquantityactive_skuledger_batch 
					THEN -lb.stock_cost_skuledger_batch 
					ELSE lb.stock_cost_skuledger_batch 
				END) / l.stock_quantity_skuledger * l.stock_sum_skuledger 
		END AS numeric(17,2)) AS n_summ,

    COALESCE(pid.Purchase_valueRetailVAT_InvoiceDetail, 
		sid.Sale_valueVAT_InvoiceDetail, 
		b.Stock_valueVAT_Batch)  b_vat, 		
		stock_valuevat_sku r_vat,
    - COALESCE(srid.SaleReturn_invoiceSum_invoiceDetail, 
			sid.Sale_invoiceSum_InvoiceDetail, 
			prid.PurchaseReturn_invoiceSum_invoiceDetail, 
			pid.Purchase_invoiceSum_invoiceDetail) 
				 invoice_sum,
    sale_barc.Barcode_UOM_Barcode AS sale_UOM,
	ssku.barcode_idbarcode_sku barcode,
	b.stock_cost_batch m_price,
	lb.key1,
	l.key0
FROM stock_skuledgerbatch lb 
JOIN stock_skuledger l ON lb.key0 = l.key0 
JOIN stock_batch b ON lb.key1 = b.key0 
JOIN stock_stock s ON l.stock_stock_skuledger = s.key0 
join stock_sku ssku on ssku.key0 = l.stock_sku_skuledger
JOIN stockdocument_stockdocumentledger d ON l.stock_stockdocumentledger_skuledger = d.key0 
LEFT JOIN Purchase_shipmentDetail psd 
    ON l.key0 = psd.Purchase_shipmentSkuLedger_ShipmentDetail 
    OR l.key0 = psd.Purchase_shipmentBatch_ShipmentDetail
LEFT JOIN Purchase_invoiceDetail pid ON psd.Purchase_invoiceDetail_ShipmentDetail = pid.key0
LEFT JOIN Sale_shipmentDetail ssd ON l.key0 = ssd.key0
LEFT JOIN Sale_invoiceDetail sid ON ssd.Sale_invoiceDetail_ShipmentDetail = sid.key0
LEFT JOIN Sale_userInvoiceDetail suid ON ssd.Sale_invoiceDetail_ShipmentDetail = suid.key0
LEFT JOIN Barcode_Barcode sale_barc ON suid.Sale_barcodePack_UserInvoiceDetail = sale_barc.key0
LEFT JOIN PurchaseReturn_shipmentDetail prsd ON l.key0 = prsd.key0
LEFT JOIN PurchaseReturn_invoiceDetail prid ON prsd.PurchaseReturn_invoiceDetail_ShipmentDetail = prid.key0
LEFT JOIN SaleReturn_shipmentDetail srsd ON l.key0 = srsd.key0
LEFT JOIN SaleReturn_invoiceDetail srid ON srsd.SaleReturn_invoiceDetail_ShipmentDetail = srid.key0
LEFT JOIN SkuLedger_sumSkuLedger sl ON l.key0 = sl.key0


WHERE l.stock_active_skuledger IS NOT NULL 
  AND lb.stock_cost_skuledger_batch IS NOT NULL 
  AND stockdocument_operation_stockdocumentledger IN ( 
  	  	10138950, 
	  	179455,
	  	5105135458,
		14213275406,
		101314170,
  		101314170 
  )
  AND l.stock_date_skuledger >= ?:: timestamp
  AND l.stock_date_skuledger < ?:: timestamp
  and (l.key0, lb.key1) > (?, ?)
order by l.key0, lb.key1
limit ?
  ),
sku_main_chunk as (
 select *,
 	cast(n_mat * m_price as numeric(18,4)) base,
	cast(stock_netweight_sku * n_mat as numeric(18, 4)) netw,
	cast(n_mat * stock_grossweight_sku as numeric(18,4)) grossw,
	cast(coalesce(n_mat * stock_volume_sku,0) as numeric(18, 4)) vol,
	cast(case when rc.op = 14213275406
	 	then rc.n_summ
	 	else case when sign(rc.n_summ) <> sign(rc.invoice_sum) 
				 	then -rc.invoice_sum
			 		else rc.invoice_sum
			end
	 end as numeric(18,3)) n_sum
 from raw_chunk rc)
	select
		mc.ds ZDS,
		mc.sid ZSID,
		barcode ZARC,
		n_mat ZMAT,
		netw ZNETW,
		grossw ZGROSSW,
		vol ZVOL,
		n_sum ZSUM,
		r_vat ZR_VAT,
		b_vat ZB_VAT,
		base ZBASE,
		dt_v ZDV_T,
		mc.isret ZISRET,
		op ZOP,
		key1 ZKEY1,
	  key0 ZKEY2	
	from sku_main_chunk mc
 