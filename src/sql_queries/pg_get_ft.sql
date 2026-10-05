--- -- select part
SELECT 
            s.key0 ds, 
			lb.key1 sku,
			barcode_idbarcode_sku barcode,
			saleledger_quantity_saleledger qnt,
			CAST(lb.saleledger_cost_saleledger_batch AS numeric(17,3)) AS n_mat, 
			-- cast(CASE WHEN saleledger_quantity_saleledger = 0 
			-- 	THEN COALESCE(l.saleledger_sum_saleledger, 0) 
			-- 	ELSE lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * COALESCE(l.saleledger_sum_saleledger, 0) END AS numeric(17,2)) AS n_sum,
			COALESCE(l.SaleLedger_valueVAT_SaleLedger, b.Stock_valueVAT_Batch) AS value_vat,
            coalesce(stock_volume_sku, 0) vol,
			stock_netweight_sku,
			stock_grossweight_sku,
            l.saleledger_datetime_saleledger,
            l.key0 id

			FROM saleledger_saleledger l 
			JOIN saleledger_saleledgerbatch lb ON lb.key0 = l.key0 
			JOIN stock_batch b ON lb.key1 = b.key0 
			JOIN store_departmentstore s ON l.saleledger_stock_saleledger = s.key0 
			join stock_sku ssku on ssku.key0 = l.saleledger_sku_saleledger
			WHERE 1=1
				and l.saleledger_isposted_saleledger IS NOT NULL 
				AND lb.saleledger_cost_saleledger_batch IS NOT NULL 
				AND l.saleledger_skip_saleledger IS NULL 
				AND (l.saleledger_description_saleledger IN (
					'Продажа за день', 
					'Возврат за день') 
					or l.saleledger_operation_saleledger in (
						10138950, 101314170, 14213275406, 179455, 5105135458, 497186287, 580
					))
				AND (l.saleledger_date_saleledger >= s.cashregister_startdategroupcashregister_departmentstore 
					OR s.cashregister_startdategroupcashregister_departmentstore IS NULL) 
				AND l.saleledger_date_saleledger >= cast(? as timestamp)
				AND l.saleledger_date_saleledger < cast(? as timestamp)
				and (l.key0, lb.key1, s.key0) > (?, ?, ?)

order by  id, sku, ds
limit ?
;--- -- insert part
truncate table ZLSF_FACT;
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
