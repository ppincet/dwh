select
	o.name t,
	c.name col,
	t.name _type,
	c.max_length,
	c.precision,
	c.scale,
	c.is_nullable
from sys.tables o
join sys.columns c on o.object_id = c.object_id
join sys.types t on c.user_type_id = t.user_type_id

where 1 = 1
	and (o.name like '%Reference%' or o.name like '%Reference%VT%')
	and o.name not like '%RefSinf%'
	and o.name not like '%chngr%'
	and (c.name like '_Fld%Ref' or c.name like '%TYPE')
order by o.name, c.name