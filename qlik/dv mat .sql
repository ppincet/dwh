SELECT 
			CAST(lb.key0 AS character varying(20)) || '!' || CAST(lb.key1 AS character varying(20))  AS schz, 
			CAST(lb.key1 AS character varying(20)) AS k_mat, 
			CAST(s.stock_id_stock AS character(12)) AS k_skl, 
			l.stock_date_skuledger AS d_vv,
			l.stock_datetime_skuledger AS dt_vv, 
			CASE WHEN sl.SkuLedger_isReturn_SkuLedger = 1  THEN Operation_nameReturn_Operation ELSE Operation_name_Operation END AS k_op, 
			CAST(e.legalentity_id_legalentity AS character(12)) AS k_ana, 
			
			CAST(l_st.stock_id_stock AS character(12)) AS k_ana_stock, 
			
			CAST(d.stockdocument_number_stockdocumentledger || COALESCE(d.stockdocument_series_stockdocumentledger, '') AS character(48)) AS dok, 
			CAST((CASE WHEN NOT lb.stock_cost_skuledger_batch = lb.stock_signedquantityactive_skuledger_batch THEN -lb.stock_cost_skuledger_batch ELSE lb.stock_cost_skuledger_batch END) AS numeric(17,3)) AS n_mat, 
			CAST(CASE WHEN (l.stock_quantity_skuledger = 0 OR l.stock_quantity_skuledger IS NULL) THEN l.stock_signedsumactive_skuledger ELSE (CASE WHEN NOT lb.stock_cost_skuledger_batch = lb.stock_signedquantityactive_skuledger_batch THEN -lb.stock_cost_skuledger_batch ELSE lb.stock_cost_skuledger_batch END) / l.stock_quantity_skuledger * l.stock_sum_skuledger END AS numeric(17,2)) AS n_sum,
			COALESCE(pid.Purchase_valueRetailVAT_InvoiceDetail, sid.Sale_valueVAT_InvoiceDetail, b.Stock_valueVAT_Batch) AS value_vat, 		
	 		COALESCE(srid.SaleReturn_invoiceSum_invoiceDetail, sid.Sale_invoiceSum_InvoiceDetail, prid.PurchaseReturn_invoiceSum_invoiceDetail, pid.Purchase_invoiceSum_invoiceDetail) AS invoice_sum,
	 		pid.Purchase_manufacturingPrice_InvoiceDetail AS manufacturing_price,
	 		
	 		wr.WriteOff_name_Reason AS writeoff_reason,
			w.writeoff_createdtime_userwriteoff AS writeoff_dtime,
			wrt.writeoff_nametype_reasontype AS writeoff_namereasontype,
			
			sale_cust.stock_id_stock AS sale_customer_stock,
			sale_barc.Barcode_UOM_Barcode AS sale_UOM
			
			
			FROM stock_skuledgerbatch lb 
			JOIN stock_skuledger l ON lb.key0 = l.key0 
			JOIN stock_batch b ON lb.key1 = b.key0 
			JOIN stock_stock s ON l.stock_stock_skuledger = s.key0 
			JOIN stockdocument_stockdocumentledger d ON l.stock_stockdocumentledger_skuledger = d.key0 
			LEFT JOIN legalentity_legalentity e ON d.stockdocument_legalentity_stockdocumentledger = e.key0 
			
			LEFT JOIN stock_stock l_st ON d.stockdocument_legalentitystock_stockdocumentledger = l_st.key0
			
	 		JOIN Operation_operation o ON d.stockdocument_operation_stockdocumentledger = o.key0
	 		LEFT JOIN SkuLedger_sumSkuLedger sl ON l.key0 = sl.key0
	
	 		LEFT JOIN Purchase_shipmentDetail psd ON l.key0 = COALESCE(psd.Purchase_shipmentSkuLedger_ShipmentDetail, psd.Purchase_shipmentBatch_ShipmentDetail)
	 		LEFT JOIN Purchase_invoiceDetail pid ON psd.Purchase_invoiceDetail_ShipmentDetail = pid.key0
			LEFT JOIN Sale_shipmentDetail ssd ON l.key0 = ssd.key0
	  		LEFT JOIN Sale_invoiceDetail sid ON ssd.Sale_invoiceDetail_ShipmentDetail = sid.key0
			LEFT JOIN Sale_userInvoiceDetail suid ON ssd.Sale_invoiceDetail_ShipmentDetail = suid.key0
			LEFT JOIN Barcode_Barcode sale_barc ON suid.Sale_barcodePack_UserInvoiceDetail = sale_barc.key0
			LEFT JOIN stock_stock sale_cust ON ssd.Sale_customerStock_ShipmentDetail = sale_cust.key0 
	 		LEFT JOIN PurchaseReturn_shipmentDetail prsd ON l.key0 = prsd.key0
	  		LEFT JOIN PurchaseReturn_invoiceDetail prid ON prsd.PurchaseReturn_invoiceDetail_ShipmentDetail = prid.key0
	 		LEFT JOIN SaleReturn_shipmentDetail srsd ON l.key0 = srsd.key0
	  		LEFT JOIN SaleReturn_invoiceDetail srid ON srsd.SaleReturn_invoiceDetail_ShipmentDetail = srid.key0
	  		LEFT JOIN WriteOff_WriteOffDetail wd ON l.key0 = wd.key0
 			LEFT JOIN WriteOff_UserWriteOff w ON w.key0 = wd.WriteOff_writeOff_WriteOffDetail
 			LEFT JOIN WriteOff_Reason wr ON wr.key0 = w.WriteOff_reason_UserWriteOff
 			LEFT JOIN WriteOff_UserWriteOffDetail uwd ON l.key0 = uwd.key0 			
 			LEFT JOIN WriteOff_ReasonType wrt ON wrt.key0 = uwd.writeoff_reasontype_userwriteoffdetail
			
			WHERE l.stock_active_skuledger IS NOT NULL AND lb.stock_cost_skuledger_batch IS NOT NULL AND Operation_name_Operation != 'Ввод начальных остатков в магазине' AND Operation_name_Operation != 'Ввод начальных остатков склада' AND (l.stock_date_skuledger >= '$(vCurrDate)' AND l.stock_date_skuledger <= '$(vCurrDate)'))
	UNION (SELECT 
			CAST(lb.key0 AS character varying(20)) || '!' || CAST(lb.key1 AS character varying(20))  AS schz, 
			CAST(lb.key1 AS character varying(20)) AS k_mat, 
			CAST(s.store_id_departmentstore AS character(12)) AS k_skl, 
			l.saleledger_date_saleledger AS d_vv,
			l.saleledger_datetime_saleledger AS dt_vv, 
			l.saleledger_description_saleledger::character(100) AS k_op, 
			NULL::character(12) AS k_ana, 
			NULL::character(12) AS k_ana_stock,
			CAST(l.saleledger_date_saleledger AS character(48)) AS dok, 
			CAST(lb.saleledger_cost_saleledger_batch AS numeric(17,3)) AS n_mat, 
			CAST(CASE WHEN saleledger_quantity_saleledger = 0 THEN COALESCE(l.saleledger_sum_saleledger, 0) ELSE lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * COALESCE(l.saleledger_sum_saleledger, 0) END AS numeric(17,2)) AS n_sum,
			COALESCE(l.SaleLedger_valueVAT_SaleLedger, b.Stock_valueVAT_Batch) AS value_vat,
		    NULL AS invoice_sum,
		    NULL AS manufacturing_price,
		   	NULL AS writeoff_reason,
		   	NULL AS writeoff_dtime,
		   	NULL AS writeoff_namereasontype,
			NULL AS sale_customer_stock,  
			NULL AS sale_UOM
			
			FROM saleledger_saleledgerbatch lb 
			JOIN saleledger_saleledger l ON lb.key0 = l.key0 
			JOIN stock_batch b ON lb.key1 = b.key0 
			JOIN store_departmentstore s ON l.saleledger_stock_saleledger = s.key0 
	
			
			WHERE l.saleledger_isposted_saleledger IS NOT NULL AND lb.saleledger_cost_saleledger_batch IS NOT NULL AND l.saleledger_skip_saleledger IS NULL AND l.saleledger_description_saleledger IN ('Продажа за день', 'Возврат за день') AND (l.saleledger_date_saleledger >= s.cashregister_startdategroupcashregister_departmentstore OR s.cashregister_startdategroupcashregister_departmentstore IS NULL) AND (l.saleledger_date_saleledger >= '$(vCurrDate)' AND l.saleledger_date_saleledger <= '$(vCurrDate)'))
	UNION (SELECT 
			CAST(lb.key0 AS character varying(20)) || '!' || CAST(lb.key1 AS character varying(20))  AS schz, 
			CAST(lb.key1 AS character varying(20)) AS k_mat, 
			CAST(s.store_id_departmentstore AS character(12)) AS k_skl, 
			l.saleledger_date_saleledger AS d_vv,
			l.saleledger_datetime_saleledger AS dt_vv, 
			'Скидки'::character(100) AS k_op, 
			NULL::character(12) AS k_ana, 
			NULL::character(12) AS k_ana_stock,
			CAST(l.saleledger_date_saleledger AS character(48)) AS dok, 
			CAST(lb.saleledger_cost_saleledger_batch AS numeric(17,3)) AS n_mat, 
			CAST(CASE WHEN saleledger_quantity_saleledger = 0 THEN l.saleledger_discountsum_saleledger ELSE lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * l.saleledger_discountsum_saleledger END AS numeric(17,2)) AS n_sum,
			COALESCE(l.SaleLedger_valueVAT_SaleLedger, b.Stock_valueVAT_Batch) AS value_vat,
		    NULL AS invoice_sum,
		    NULL AS manufacturing_price,
		   	NULL AS writeoff_reason,
			NULL AS writeoff_dtime,
			NULL AS writeoff_namereasontype,
			NULL AS sale_customer_stock,  
			NULL AS sale_UOM
			
			FROM saleledger_saleledgerbatch lb 
			JOIN saleledger_saleledger l ON lb.key0 = l.key0 
			JOIN stock_batch b ON lb.key1 = b.key0 
			JOIN store_departmentstore s ON l.saleledger_stock_saleledger = s.key0 
			
			WHERE l.saleledger_isposted_saleledger IS NOT NULL AND lb.saleledger_cost_saleledger_batch IS NOT NULL AND l.saleledger_skip_saleledger IS NULL AND l.saleledger_description_saleledger IN ('Продажа за день', 'Возврат за день') AND (l.saleledger_date_saleledger >= s.cashregister_startdategroupcashregister_departmentstore OR s.cashregister_startdategroupcashregister_departmentstore IS NULL) AND l.saleledger_discountsum_saleledger IS NOT NULL AND (l.saleledger_date_saleledger >= '$(vCurrDate)' AND l.saleledger_date_saleledger <= '$(vCurrDate)'))
			;