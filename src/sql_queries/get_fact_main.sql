select top (?)
    rg._period z_period,
    0x50000000 z_bk_dt_type,
    rg._accountdtrref z_bk_dt_ref,
    rg._fld617 z_amnt,
    rg._recordertref,
    rg._recorderrref,
    rg._lineno,

    dt_sk.sk00t ZSK00T,
    dt_sk.sk00r ZSK00R,
    dt_sk.sk01t ZSK01T,
    dt_sk.sk01r ZSK01R,
    dt_sk.sk02t ZSK02T,
    dt_sk.sk02r ZSK02R,
    dt_sk.sk03t ZSK03T,
    dt_sk.sk03r ZSK03R,
    dt_sk.sk10t ZSK10T,
    dt_sk.sk10r ZSK10R,
    dt_sk.sk11t ZSK11T,
    dt_sk.sk11r ZSK11R,
    dt_sk.sk12t ZSK12T,
    dt_sk.sk12r ZSK12R,
    dt_sk.sk13t ZSK13T,
    dt_sk.sk13r ZSK13R,
    dt_sk.sk20t ZSK20T,
    dt_sk.sk20r ZSK20R

from dbo._accrg614 rg 
join dbo._acc9 deb 
    on deb._idrref = rg._accountdtrref

outer apply (
    select 
        max(case when aeddt._keyfield = 0 and v.t = 0x00000020 then v.t end) sk00t,
        max(case when aeddt._keyfield = 0 and v.t = 0x00000020 then v.r end) sk00r,
        max(case when aeddt._keyfield = 0 and v.t = 0x0000006f then v.t end) sk01t,
        max(case when aeddt._keyfield = 0 and v.t = 0x0000006f then v.r end) sk01r,
        max(case when aeddt._keyfield = 0 and v.t = 0x00000085 then v.t end) sk02t,
        max(case when aeddt._keyfield = 0 and v.t = 0x00000085 then v.r end) sk02r,
        max(case when aeddt._keyfield = 0 and v.t = 0x000000a6 then v.t end) sk03t,
        max(case when aeddt._keyfield = 0 and v.t = 0x000000a6 then v.r end) sk03r,

        max(case when aeddt._keyfield = 1 and v.t = 0x00000016 then v.t end) sk10t,
        max(case when aeddt._keyfield = 1 and v.t = 0x00000016 then v.r end) sk10r,
        max(case when aeddt._keyfield = 1 and v.t = 0x00000057 then v.t end) sk11t,
        max(case when aeddt._keyfield = 1 and v.t = 0x00000057 then v.r end) sk11r,
        max(case when aeddt._keyfield = 1 and v.t = 0x00000071 then v.t end) sk12t,
        max(case when aeddt._keyfield = 1 and v.t = 0x00000071 then v.r end) sk12r,
        max(case when aeddt._keyfield = 1 and v.t = 0x0000008a then v.t end) sk13t,
        max(case when aeddt._keyfield = 1 and v.t = 0x0000008a then v.r end) sk13r,
        
        max(case when aeddt._keyfield = 0 and v.t = 0x0000001b then v.t end) sk20t,
        max(case when aeddt._keyfield = 0 and v.t = 0x0000001b then v.r end) sk20r

    from dbo._accrged639 ed 
    inner join dbo._acc9_extdim604 aeddt 
        on aeddt._acc9_idrref = rg._accountdtrref 
       and ed._kindrref = aeddt._dimkindrref
    cross apply (
        select 
            ed._value_rtref t,
            ed._value_rrref r
    ) v
    where ed._period = rg._period
      and ed._recordertref = rg._recordertref
      and ed._recorderrref = rg._recorderrref
      and ed._lineno = rg._lineno
) dt_sk

where 
    rg._period < ? -- must be start of next day
    and (
        (rg._period > ?) 
        or (rg._period = ? and rg._recordertref > ?)
        or (rg._period = ? and rg._recordertref = ? and rg._recorderrref > ?)
        or (rg._period = ? and rg._recordertref = ? and rg._recorderrref = ? and rg._lineno > ?)
    )
    and deb._code in (
        '20.1', '68.3.1', '73.2', '44.2', '44.3', 
        '90.10.1', '90.10.11', '90.7.1', '90.7.2', 
        '91.4.1', '91.4.11', '91.1.1'
    )

order by 
    rg._period asc,
    rg._recordertref asc,
    rg._recorderrref asc,
    rg._lineno asc;