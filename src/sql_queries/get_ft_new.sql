create table #Accounts (
    _accountref varbinary(8) primary key
);

insert into #Accounts (_accountref) values 
    (0xBF8A3C0B880CCCE14300B5657383E5B5),
    (0x9E81AA3F75D9FC81403229609193FADA),
    (0x8F62AD919A7699C04D146BB85F217614),
    (0xBD10E98B2639DC05495199B0ED8A4C2D),
    (0x830C72D2D0665D0D4CED1913F66F2A7A),
    (0x8372AEE2AF96125B4E2EFE7948660BA7),
    (0x843A00505683949511EBD908F48F3006),
    (0xBAC64B1A7A9143CD42095CCEE0A12C4E),
    (0x9238B79EF2F846C04060AC09498F4B9E),
    (0x8D0D0D5528A9770F4E3E2BC7EFF35167),
    (0x9422850C6E2C51EE48DF8E69CB67A861),
    (0x843A00505683949511EBD908F48F3005);

with batchkeys as (
    select top (?) *
    from (

        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref  _accountref, 
            rg._fld617  z_amnt, 
            cast('D' as varchar(1))  d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period >= ? and rg._period < ?

        union all

        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, rg._fld617 as z_amnt, cast('D' as varchar(1)) as d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period = ? and rg._recordertref > ?

        union all

  
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._fld617  z_amnt, 
            cast('D' as varchar(1))  d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref > ?

        union all

        
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, 
            rg._fld617  z_amnt, 
            cast('D' as varchar(1))  d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountdtrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref = ? and rg._lineno > ?

     
        union all

       
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountctrref  _accountref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1))  d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period >= ? and rg._period < ?

        union all

    
        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountctrref  _accountref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1)) as d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period = ? and rg._recordertref > ?

        union all

        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountctrref  _accountref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1)) d_c_flag
        from dbo._accrg614 rg 
        inner join #Accounts a on rg._accountctrref = a._accountref
        where rg._period = ? and rg._recordertref = ? and rg._recorderrref > ?

        union all


        select top (?) 
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountctrref  _accountref, 
            rg._fld617  z_amnt, 
            cast('C' as varchar(1))  d_c_flag
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
    0x50000000  z_bk_dt_type,       
    k._accountref  z_bk_account_ref, 
    k.z_amnt,
    k.d_c_flag,                       
    
    dt_sk.sk00t  ZSK00T, dt_sk.sk00r  ZSK00R,
    dt_sk.sk01t  ZSK01T, dt_sk.sk01r  ZSK01R,
    dt_sk.sk02t  ZSK02T, dt_sk.sk02r  ZSK02R,
    dt_sk.sk03t  ZSK03T, dt_sk.sk03r  ZSK03R,
    dt_sk.sk10t  ZSK10T, dt_sk.sk10r  ZSK10R,
    dt_sk.sk11t  ZSK11T, dt_sk.sk11r  ZSK11R,
    dt_sk.sk12t  ZSK12T, dt_sk.sk12r  ZSK12R,
    dt_sk.sk13t  ZSK13T, dt_sk.sk13r  ZSK13R,
    dt_sk.sk20t  ZSK20T, dt_sk.sk20r  ZSK20R,
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
        on aeddt._acc9_idrref = k._accountref -- привязка идет к тому счету, который сработал в пачке
       and ed._kindrref = aeddt._dimkindrref
    where ed._period = k._period
      and ed._recordertref = k._recordertref
      and ed._recorderrref = k._recorderrref
      and ed._lineno = k._lineno
) dt_sk
order by
    k._period asc,
    k._recordertref asc,
    k._recorderrref asc,
    k._lineno asc,
    k.d_c_flag asc;

drop table #Accounts;