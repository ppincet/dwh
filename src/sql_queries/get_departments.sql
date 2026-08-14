
select 
    0x00000057 IDTYPE,
    _IDRRef IDREF,
    0x00000057 PARENTTYPE,
    _ParentIDRRef PARENTREF,
    _code CODE,
    _description DESCR
from _reference113 p
union all
select 
    0x00000071,
    c._IDRRef,
    0x00000057,
    c._ParentIDRRef,
    c._code,
    c._description
from _reference87 c
join _reference113 p
on c._Fld1272RRef = p._IDRRef