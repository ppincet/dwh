with services as (
select 0x000000a6 tref,
	c._idrref rref
from _reference166 c
join _reference166 p
on c._parentidrref = p._IDRRef
	where 1=1 
	and p._code in (244, 47, 553))
select 
    convert(char(32), _idrref,2),
	dateadd(year, -2000, j._Date_Time),
    case when _number_type = 0x03 then cast(_number_n as varchar(40)) else _number_s end docno,
    _Fld8989_RTRef, 
    _Fld8989_RRRef,
    _Fld8990_RTRef,
    _Fld8990_RRRef,
    --left(_Fld9007, 255) _Fld9007
    _Fld9007,
    _Fld18638,
    _Fld18639,
    _lineno9038
from _documentjournal13332 j
join _document305 d
on j._DocumentRRef = d._IDRRef and j._Date_Time = d._Date_Time
join #Accounts a
on a._accountref = d._Fld8996RRef
join _Document305_VT9037 dvt
on d._IDRRef = dvt._Document305_IDRRef 
join services s on s.tref = dvt._Fld9041_RTRef and s.rref = dvt._Fld9041_RRRef
where 1=1 
    and j._date_time between ? and ?;
--- insert part
 insert ZDOC305
    (ZIDRREF,
    ZPERIOD,
    ZDOCNO,
    ZCAGNTTREF,
    ZCAGNTRREF,
    ZAGRMNTTREF,
    ZAGRMNTRREF,
    ZSUBJ,
    ZAMNT,
    ZPRICE,
    ZLNNO)
values (?,?,?,?,?,?,?,?,?,?,?)



