
with batchkeys as (
    select top (?) *
    from (

        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref  _accountdref,
            rg._accountctrref  _accountcref, 
            rg._fld617  z_amnt, 
            cast('D' as varchar(1))  d_c_flag,
            convert(char(8), rg._recordertref,2) recordertref,
            convert(char(32), rg._recorderrref,2) recorderrref
            
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period > ? and rg._period < ?

        union all

        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617 as z_amnt, cast('D' as varchar(1)) as d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period = ? and rg._recordertref > ?

        union all

  
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617  z_amnt, 
            cast('D' as varchar(1))  d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref > ?

        union all

        
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617  z_amnt, 
            cast('D' as varchar(1))  d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref = ? and rg._lineno > ?

     
        union all

       
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1))  d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period > ? and rg._period < ?

        union all

    
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1)) as d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period = ? and rg._recordertref > ?

        union all

        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1)) d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref > ?

        union all


        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._accountctrref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1))  d_c_flag,
            convert(char(8), rg._recordertref,2),
            convert(char(32), rg._recorderrref,2)
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref = ? and rg._lineno > ?

    )  combined
    order by
        _period asc,
        _recordertref asc,
        _recorderrref asc,
        _lineno asc,
        d_c_flag asc
)
select 
    k._period  z_period,
    --0x50000000  z_bk_dt_type,       
    k._accountdref  z_bk_accountd_ref, 
    k._accountcref  z_bk_accountc_ref, 
    k.z_amnt,
    k.d_c_flag,                      
    case when k.d_c_flag = 'D' then dt_sk.sk00t else ct_sk.sk00t end ZSK00T, 
    case when k.d_c_flag = 'D' then dt_sk.sk00r else ct_sk.sk00r end ZSK00R,
    case when k.d_c_flag = 'D' then dt_sk.sk01t else ct_sk.sk01t end ZSK01T, 
    case when k.d_c_flag = 'D' then dt_sk.sk01r else ct_sk.sk01r end ZSK01R,
    case when k.d_c_flag = 'D' then dt_sk.sk02t else ct_sk.sk02t end ZSK02T, 
    case when k.d_c_flag = 'D' then dt_sk.sk02r else ct_sk.sk02r end ZSK02R,
    case when k.d_c_flag = 'D' then dt_sk.sk03t else ct_sk.sk03t end ZSK03T, 
    case when k.d_c_flag = 'D' then dt_sk.sk03r else ct_sk.sk03r end ZSK03R,
    case when k.d_c_flag = 'D' then dt_sk.sk10t else ct_sk.sk10t end ZSK10T, 
    case when k.d_c_flag = 'D' then dt_sk.sk10r else ct_sk.sk10r end ZSK10R,
    case when k.d_c_flag = 'D' then dt_sk.sk11t else ct_sk.sk11t end ZSK11T, 
    case when k.d_c_flag = 'D' then dt_sk.sk11r else ct_sk.sk11r end ZSK11R,
    case when k.d_c_flag = 'D' then dt_sk.sk12t else ct_sk.sk12t end ZSK12T, 
    case when k.d_c_flag = 'D' then dt_sk.sk12r else ct_sk.sk12r end ZSK12R,
    case when k.d_c_flag = 'D' then dt_sk.sk13t else ct_sk.sk13t end ZSK13T, 
    case when k.d_c_flag = 'D' then dt_sk.sk13r else ct_sk.sk13r end ZSK13R,
    case when k.d_c_flag = 'D' then dt_sk.sk20t else ct_sk.sk20t end ZSK20T, 
    case when k.d_c_flag = 'D' then dt_sk.sk20r else ct_sk.sk20r end ZSK20R,
    k.recordertref,
    k.recorderrref,
    k._recordertref,
    k._recorderrref,
    k._lineno
from batchkeys k
outer apply (
    select
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000020 then ed._value_rtref end)  sk00t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000020 then ed._value_rrref end)  sk00r,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000006f then ed._value_rtref end)  sk01t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000006f then ed._value_rrref end)  sk01r,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000085 then ed._value_rtref end)  sk02t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000085 then ed._value_rrref end)  sk02r,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x000000a6 then ed._value_rtref end)  sk03t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x000000a6 then ed._value_rrref end)  sk03r,

        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000016 then ed._value_rtref end)  sk10t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000016 then ed._value_rrref end)  sk10r,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000057 then ed._value_rtref end)  sk11t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000057 then ed._value_rrref end)  sk11r,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000071 then ed._value_rtref end)  sk12t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000071 then ed._value_rrref end)  sk12r,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x0000008a then ed._value_rtref end)  sk13t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x0000008a then ed._value_rrref end)  sk13r,

        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000001b then ed._value_rtref end)  sk20t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000001b then ed._value_rrref end)  sk20r
    from dbo._accrged639 ed 
    inner join dbo._acc9_extdim604 aeddt 
        on aeddt._acc9_idrref = k._accountdref 
       and ed._kindrref = aeddt._dimkindrref
    where ed._period = k._period
      and ed._recordertref = k._recordertref
      and ed._recorderrref = k._recorderrref
      and ed._lineno = k._lineno
) dt_sk
outer apply (
select
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x00000020 then ed._value_rtref end)  sk00t,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x00000020 then ed._value_rrref end)  sk00r,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x0000006f then ed._value_rtref end)  sk01t,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x0000006f then ed._value_rrref end)  sk01r,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x00000085 then ed._value_rtref end)  sk02t,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x00000085 then ed._value_rrref end)  sk02r,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x000000a6 then ed._value_rtref end)  sk03t,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x000000a6 then ed._value_rrref end)  sk03r,

        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x00000016 then ed._value_rtref end)  sk10t,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x00000016 then ed._value_rrref end)  sk10r,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x00000057 then ed._value_rtref end)  sk11t,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x00000057 then ed._value_rrref end)  sk11r,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x00000071 then ed._value_rtref end)  sk12t,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x00000071 then ed._value_rrref end)  sk12r,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x0000008a then ed._value_rtref end)  sk13t,
        max(case when aedct._keyfield = 1 and ed._value_rtref = 0x0000008a then ed._value_rrref end)  sk13r,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x0000001b then ed._value_rtref end)  sk20t,
        max(case when aedct._keyfield = 0 and ed._value_rtref = 0x0000001b then ed._value_rrref end)  sk20r
 from dbo._accrged639 ed 
 inner join dbo._acc9_extdim604 aedct 
        on aedct._acc9_idrref = k._accountcref
       and ed._kindrref = aedct._dimkindrref
 where ed._period = k._period
      and ed._recordertref = k._recordertref
      and ed._recorderrref = k._recorderrref
      and ed._lineno = k._lineno
) ct_sk
order by
    k._period asc,
    k._recordertref asc,
    k._recorderrref asc,
    k._lineno asc,
    k.d_c_flag asc;
