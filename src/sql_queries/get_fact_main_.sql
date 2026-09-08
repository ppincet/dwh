 select
    rg.[_period] z_period,
    0x50000000 z_bk_dt_type,
    rg._AccountDtRRef  z_bk_dt_ref,
    rg._fld617 z_amnt,
    dt_sk.SK00T ZSK00T,
    dt_sk.SK00R ZSK00R,
    dt_sk.SK01T ZSK01T,
    dt_sk.SK01R ZSK01R,
    dt_sk.SK02T ZSK02T,
    dt_sk.SK02R ZSK02R,
    dt_sk.SK03T ZSK03T,
    dt_sk.SK03R ZSK03R,
    dt_sk.SK10T ZSK10T,
    dt_sk.SK10R ZSK10R,
    dt_sk.SK11T ZSK11T,
    dt_sk.SK11R ZSK11R,
    dt_sk.SK12T ZSK12T,
    dt_sk.SK12R ZSK12R,
    dt_sk.SK13T ZSK13T,
    dt_sk.SK13R ZSK13R,
    dt_sk.SK20T ZSK20T,
    dt_sk.SK20R ZSK20R


FROM _AccRg614 rg
JOIN _documentjournal13332 journ
    ON journ.[_documenttref] = rg.[_RecorderTRef]
    AND journ.[_documentrref] = rg.[_RecorderRRef]
JOIN _acc9 deb 
    ON deb.[_idrref] = rg._AccountDtRRef
JOIN _acc9 cred 
    ON cred.[_idrref] = rg._AccountCtRRef
OUTER APPLY (
    SELECT 
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x00000020 THEN v.t end), 0) SK00T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x00000020 THEN v.r end), 0) SK00R,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x0000006F THEN v.t end), 0) SK01T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x0000006F THEN v.r end), 0) SK01R,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x00000085 THEN v.t end), 0) SK02T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x00000085 THEN v.r end), 0) SK02R,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x000000A6 THEN v.t end), 0) SK03T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x000000A6 THEN v.r end), 0) SK03R,

        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x00000016 THEN v.t end), 0) SK10T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x00000016 THEN v.r end), 0) SK10R,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x00000057 THEN v.t end), 0) SK11T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x00000057 THEN v.r end), 0) SK11R,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x00000071 THEN v.t end), 0) SK12T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x00000071 THEN v.r end), 0) SK12R,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x0000008A THEN v.t end), 0) SK13T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 and v.t = 0x0000008A THEN v.r end), 0) SK13R,
        
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x0000001B THEN v.t end), 0) SK20T,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 and v.t = 0x0000001B THEN v.r end), 0) SK20R
        
        
    FROM _accrged639 ed
    INNER JOIN _Acc9_ExtDim604 aeddt
        ON aeddt._Acc9_IDRRef = rg._AccountDtRRef 
        AND ed._KindRRef = aeddt._DimKindRRef
    CROSS APPLY (
        SELECT 
             ed._Value_RTRef t,
             ed._Value_RRRef r
        
    ) v
    WHERE ed.[_period] = rg.[_period]
      AND ed.[_RecorderTRef] = rg._RecorderTRef
      AND ed.[_RecorderRRef] = rg._RecorderRRef
      AND ed.[_LineNo] = rg._LineNo
) dt_sk
where 
    rg._period < ? 
    AND (
        (rg._period > ?) 
        OR (rg._period = ? AND rg._RecorderTRef > ?)
        OR (rg._period = ? AND rg._RecorderTRef = ? AND rg._RecorderRRef > ?)
        OR (rg._period = ? AND rg._RecorderTRef = ? AND rg._RecorderRRef = ? AND rg._LineNo > ?)
    )

    AND deb._code IN (
        '20.1', '68.3.1', '73.2', '44.2', '44.3', 
        '90.10.1', '90.10.11', '90.7.1', '90.7.2', 
        '91.4.1', '91.4.11', '91.1.1'
    )

ORDER BY 
    rg._period ASC,
    rg._RecorderTRef ASC,
    rg._RecorderRRef ASC,
    rg._LineNo ASC