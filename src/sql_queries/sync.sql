
TRUNCATE TABLE {stage_stock};
INSERT INTO {stage_stock} 
SELECT *
FROM #temp t
LEFT JOIN {stage_buffer} b ON t.ID = b.ID
WHERE b.ID IS NULL              
   OR t.VERSION <> b.VERSION;   
TRUNCATE TABLE {stage_buffer};
INSERT INTO {stage_buffer} SELECT * FROM #temp;