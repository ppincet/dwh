SELECT 
    lb.key0 id,
    ss.key0,
    saleledger_quantity_saleledger qnt,
    lb.key1 k_mat, 
    s.store_id_departmentstore k_skl, 
    store_id_store,
    l.saleledger_date_saleledger AS d_vv,
    l.saleledger_datetime_saleledger AS dt_vv,
    saleledger_operation_saleledger op,
    l.saleledger_description_saleledger k_op, 
    l.saleledger_date_saleledger dok,
    l.saleledger_sku_saleledger,
    saleledger_quantity_saleledger qnt,
    operation_name_operation,
    operation_id_operation,
    CAST(lb.saleledger_cost_saleledger_batch AS numeric(17,3)) AS n_mat, 
    cast(CASE WHEN saleledger_quantity_saleledger = 0 
        THEN COALESCE(l.saleledger_sum_saleledger, 0) 
        ELSE lb.saleledger_cost_saleledger_batch / l.saleledger_quantity_saleledger * COALESCE(l.saleledger_sum_saleledger, 0) END AS numeric(17,2)) AS n_sum,
    COALESCE(l.SaleLedger_valueVAT_SaleLedger, b.Stock_valueVAT_Batch) AS value_vat
FROM saleledger_saleledgerbatch lb 
JOIN saleledger_saleledger l ON lb.key0 = l.key0 
JOIN stock_batch b ON lb.key1 = b.key0 
JOIN store_departmentstore s ON l.saleledger_stock_saleledger = s.key0 
join store_store ss on ss.key0 = s.store_store_departmentstore
left join operation_operation oo on oo.key0 = l.saleledger_operation_saleledger
join stock_sku ssku on ssku.key0 = l.saleledger_sku_saleledger
WHERE 1=1
    and l.saleledger_isposted_saleledger IS NOT NULL 
    AND lb.saleledger_cost_saleledger_batch IS NOT NULL 
    AND l.saleledger_skip_saleledger IS NULL 
    AND l.saleledger_description_saleledger IN (
        'Продажа за день', 
        'Возврат за день') 
    AND (l.saleledger_date_saleledger >= s.cashregister_startdategroupcashregister_departmentstore 
        OR s.cashregister_startdategroupcashregister_departmentstore IS NULL) 
    AND (l.saleledger_date_saleledger >= '20261001') 
        --AND l.saleledger_date_saleledger <= '202690930')
order by   id, k_mat