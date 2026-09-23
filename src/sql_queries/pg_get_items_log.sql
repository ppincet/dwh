-- gets changes
select * -- 2do filter field list
from stock_sku ss
where exists (
select 1
from item_itemlog il
where 1=1
	and il.item_item_itemlog = ss.key0
	and il.item_datetimesession_itemlog >= CURRENT_DATE - INTERVAL '1 day'
    and il.item_datetimesession_itemlog < CURRENT_DATE
)
and stock_inactive_sku is null

-- opt 1
-- WHERE i.item_datetimesession_itemlog >= CURRENT_DATE - INTERVAL '1 day'
--   AND i.item_datetimesession_itemlog < CURRENT_DATE

-- opt 2
-- WHERE i.item_datetimesession_itemlog BETWEEN 
--       (CURRENT_DATE - INTERVAL '1 day')::timestamp 
--   AND (CURRENT_DATE - INTERVAL '1 day' + INTERVAL '23 hours 59 minutes 59 seconds')::timestamp

