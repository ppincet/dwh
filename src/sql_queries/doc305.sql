select 
    convert(char(32), _idrref,2),
	dateadd(year, -2000, j._Date_Time),
    case when _number_type = 0x03 then cast(_number_n as varchar(40)) else _number_s end docno,
    _Fld8989_RTRef, 
    _Fld8989_RRRef,
    _Fld8990_RTRef,
    _Fld8990_RRRef,
    --left(_Fld9007, 255) _Fld9007
    _Fld9007
from _documentjournal13332 j
join _document305 d
on j._DocumentRRef = d._IDRRef and j._Date_Time = d._Date_Time
join #Accounts a
on a._accountref = d._Fld8996RRef
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
    ZSUBJ)
values (?,?,?,?,?,?,?,?)


