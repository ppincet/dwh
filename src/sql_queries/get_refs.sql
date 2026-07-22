-- returns back list of subkonto referencies
SELECT 
	o.name
FROM sys.objects o

WHERE o.name LIKE '%Reference%'
	and o.name not like '%VT%'
	and o.name not like '%RefSinf%'
	and o.name not like '%chngr%'