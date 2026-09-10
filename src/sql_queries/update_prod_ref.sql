insert {prod_name} 
select *
from #tempo t
left join {stage_name} s
on t.IDRREF = s.IDRREF 
where t.VERSION != s.VERSION or s.IDRREF is null