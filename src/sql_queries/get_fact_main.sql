with batchkeys as (
    select top (?) *
    from (
        select top (?)
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, rg._fld617 as z_amnt
        from dbo._accrg614 rg 
        where rg._period > ?
          and rg._period < ?
          and rg._accountdtrref in (
                0xBF8A3C0B880CCCE14300B5657383E5B5,
                0x9E81AA3F75D9FC81403229609193FADA,
                0x8F62AD919A7699C04D146BB85F217614,
                0xBD10E98B2639DC05495199B0ED8A4C2D,
                0x830C72D2D0665D0D4CED1913F66F2A7A,
                0x8372AEE2AF96125B4E2EFE7948660BA7,
                0x843A00505683949511EBD908F48F3006,
                0xBAC64B1A7A9143CD42095CCEE0A12C4E,
                0x9238B79EF2F846C04060AC09498F4B9E,
                0x8D0D0D5528A9770F4E3E2BC7EFF35167,
                0x9422850C6E2C51EE48DF8E69CB67A861,
                0x843A00505683949511EBD908F48F3005
          )

        union all

        select top (?)
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, rg._fld617 as z_amnt
        from dbo._accrg614 rg 
        where rg._period = ?
          and rg._recordertref > ?
        --  and rg._recordertref <> 0x00000000
          and rg._accountdtrref in (
                0xBF8A3C0B880CCCE14300B5657383E5B5,
                0x9E81AA3F75D9FC81403229609193FADA,
                0x8F62AD919A7699C04D146BB85F217614,
                0xBD10E98B2639DC05495199B0ED8A4C2D,
                0x830C72D2D0665D0D4CED1913F66F2A7A,
                0x8372AEE2AF96125B4E2EFE7948660BA7,
                0x843A00505683949511EBD908F48F3006,
                0xBAC64B1A7A9143CD42095CCEE0A12C4E,
                0x9238B79EF2F846C04060AC09498F4B9E,
                0x8D0D0D5528A9770F4E3E2BC7EFF35167,
                0x9422850C6E2C51EE48DF8E69CB67A861,
                0x843A00505683949511EBD908F48F3005
          )

        union all

        select top (?)
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, rg._fld617 as z_amnt
        from dbo._accrg614 rg 
        where rg._period = ?
          and rg._recordertref = ?
          and rg._recorderrref > ?
        --  and rg._recorderrref <> 0x0000000000000000
          and rg._accountdtrref in ( 
                0xBF8A3C0B880CCCE14300B5657383E5B5,
                0x9E81AA3F75D9FC81403229609193FADA,
                0x8F62AD919A7699C04D146BB85F217614,
                0xBD10E98B2639DC05495199B0ED8A4C2D,
                0x830C72D2D0665D0D4CED1913F66F2A7A,
                0x8372AEE2AF96125B4E2EFE7948660BA7,
                0x843A00505683949511EBD908F48F3006,
                0xBAC64B1A7A9143CD42095CCEE0A12C4E,
                0x9238B79EF2F846C04060AC09498F4B9E,
                0x8D0D0D5528A9770F4E3E2BC7EFF35167,
                0x9422850C6E2C51EE48DF8E69CB67A861,
                0x843A00505683949511EBD908F48F3005
          )

        union all

        select top (?)
            rg._period, rg._recordertref, rg._recorderrref, rg._lineno,
            rg._accountdtrref, rg._fld617 as z_amnt
        from dbo._accrg614 rg 
        where rg._period = ?
          and rg._recordertref = ?
          and rg._recorderrref = ?
          and rg._lineno > ?
          and rg._accountdtrref in (
                0xBF8A3C0B880CCCE14300B5657383E5B5,
                0x9E81AA3F75D9FC81403229609193FADA,
                0x8F62AD919A7699C04D146BB85F217614,
                0xBD10E98B2639DC05495199B0ED8A4C2D,
                0x830C72D2D0665D0D4CED1913F66F2A7A,
                0x8372AEE2AF96125B4E2EFE7948660BA7,
                0x843A00505683949511EBD908F48F3006,
                0xBAC64B1A7A9143CD42095CCEE0A12C4E,
                0x9238B79EF2F846C04060AC09498F4B9E,
                0x8D0D0D5528A9770F4E3E2BC7EFF35167,
                0x9422850C6E2C51EE48DF8E69CB67A861,
                0x843A00505683949511EBD908F48F3005
          )
    ) as combined
    order by
        _period asc,
        _recordertref asc,
        _recorderrref asc,
        _lineno asc
)
select 
    k._period as z_period,
    0x50000000 as z_bk_dt_type,       
    k._accountdtrref as z_bk_dt_ref, 
    k.z_amnt,
    
    dt_sk.sk00t as ZSK00T, dt_sk.sk00r as ZSK00R,
    dt_sk.sk01t as ZSK01T, dt_sk.sk01r as ZSK01R,
    dt_sk.sk02t as ZSK02T, dt_sk.sk02r as ZSK02R,
    dt_sk.sk03t as ZSK03T, dt_sk.sk03r as ZSK03R,
    dt_sk.sk10t as ZSK10T, dt_sk.sk10r as ZSK10R,
    dt_sk.sk11t as ZSK11T, dt_sk.sk11r as ZSK11R,
    dt_sk.sk12t as ZSK12T, dt_sk.sk12r as ZSK12R,
    dt_sk.sk13t as ZSK13T, dt_sk.sk13r as ZSK13R,
    dt_sk.sk20t as ZSK20T, dt_sk.sk20r as ZSK20R,
    k._recordertref,
    k._recorderrref,
    k._lineno
from batchkeys k
outer apply (
    select
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000020 then ed._value_rtref end) as sk00t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000020 then ed._value_rrref end) as sk00r,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000006f then ed._value_rtref end) as sk01t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000006f then ed._value_rrref end) as sk01r,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000085 then ed._value_rtref end) as sk02t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x00000085 then ed._value_rrref end) as sk02r,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x000000a6 then ed._value_rtref end) as sk03t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x000000a6 then ed._value_rrref end) as sk03r,

        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000016 then ed._value_rtref end) as sk10t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000016 then ed._value_rrref end) as sk10r,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000057 then ed._value_rtref end) as sk11t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000057 then ed._value_rrref end) as sk11r,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000071 then ed._value_rtref end) as sk12t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x00000071 then ed._value_rrref end) as sk12r,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x0000008a then ed._value_rtref end) as sk13t,
        max(case when aeddt._keyfield = 1 and ed._value_rtref = 0x0000008a then ed._value_rrref end) as sk13r,

        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000001b then ed._value_rtref end) as sk20t,
        max(case when aeddt._keyfield = 0 and ed._value_rtref = 0x0000001b then ed._value_rrref end) as sk20r
    from dbo._accrged639 ed 
    inner join dbo._acc9_extdim604 aeddt 
        on aeddt._acc9_idrref = k._accountdtrref
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
    k._lineno asc;