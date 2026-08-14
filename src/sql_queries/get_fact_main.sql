#########
# 2do:
# - insert into #tempo
# - join z_subkonto
# - join account mapping
# - insert fact
#
#
########
SELECT 
    DATEADD(year, -2000, rg.[_period]) z_period,
    0x00000009 z_bk_dt_type,
    rg._AccountDtRRef  z_bk_dt_ref,
    '00.00' z_mng_dt,
    1 z_qnt,
    1 z_trf,
    rg._fld617 z_amnt,

    dt_sk.sk0_t z_dt_sk1_type,
    dt_sk.sk0_r z_dt_sk1_ref,
    dt_sk.sk1_t z_dt_sk2_type,
    dt_sk.sk1_r z_dt_sk2_ref,
    dt_sk.sk2_t z_dt_sk3_type,
    dt_sk.sk2_r z_dt_sk3_ref,
    dt_sk.sk3_t z_dt_sk4_type,
    dt_sk.sk3_r z_dt_sk4_ref,

    0x00000009 z_bk_ct_type,
    rg._AccountCtRRef  z_bk_ct_ref,
    '99.99' z_mng_ct,
    
 
    ct_sk.sk0_t z_ct_sk0_type,
    ct_sk.sk0_r z_ct_sk1_ref,
    ct_sk.sk1_t z_ct_sk1_type,
    ct_sk.sk1_r z_ct_sk2_ref,
    ct_sk.sk2_t z_ct_sk3_type,
    ct_sk.sk2_r z_ct_sk3_ref,
    ct_sk.sk3_t z_ct_sk4_type,
    ct_sk.sk3_r z_ct_sk4_ref

FROM _AccRg614 rg WITH (NOLOCK)
JOIN _documentjournal13332 journ WITH (NOLOCK)
    ON journ.[_documenttref] = rg.[_RecorderTRef]
    AND journ.[_documentrref] = rg.[_RecorderRRef]
JOIN _acc9 deb WITH (NOLOCK)
    ON deb.[_idrref] = rg._AccountDtRRef
JOIN _acc9 cred WITH (NOLOCK)
    ON cred.[_idrref] = rg._AccountCtRRef
OUTER APPLY (
    SELECT 
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 THEN v.t end),-1) sk0_t,
        isnull(MAX(CASE WHEN aeddt._keyfield = 0 THEN v.r end),-1) sk0_r,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 THEN v.t end),-1) sk1_t,
        isnull(MAX(CASE WHEN aeddt._keyfield = 1 THEN v.r end),-1) sk1_r,
        isnull(MAX(CASE WHEN aeddt._keyfield = 2 THEN v.t end),-1) sk2_t,
        isnull(MAX(CASE WHEN aeddt._keyfield = 2 THEN v.r end),-1) sk2_r,
        isnull(MAX(CASE WHEN aeddt._keyfield = 3 THEN v.t end),-1) sk3_t,
        isnull(MAX(CASE WHEN aeddt._keyfield = 3 THEN v.r end),-1) sk3_r
    FROM _accrged639 ed WITH (NOLOCK)
    INNER JOIN _Acc9_ExtDim604 aeddt WITH (NOLOCK) 
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

OUTER APPLY (
    SELECT 
        isnull(MAX(CASE WHEN aedct._keyfield = 0 THEN v.t END), -1) sk0_t,
        isnull(MAX(CASE WHEN aedct._keyfield = 0 THEN v.r END), -1) sk0_r,
        isnull(MAX(CASE WHEN aedct._keyfield = 1 THEN v.t END), -1) sk1_t,
        isnull(MAX(CASE WHEN aedct._keyfield = 1 THEN v.r END), -1) sk1_r,
        isnull(MAX(CASE WHEN aedct._keyfield = 2 THEN v.t END), -1) sk2_t,
        isnull(MAX(CASE WHEN aedct._keyfield = 2 THEN v.r END), -1) sk2_r,
        isnull(MAX(CASE WHEN aedct._keyfield = 3 THEN v.t END), -1) sk3_t,
        isnull(MAX(CASE WHEN aedct._keyfield = 3 THEN v.r END), -1) sk3_r
    FROM _accrged639 ed WITH (NOLOCK)
    INNER JOIN _Acc9_ExtDim604 aedct WITH (NOLOCK) 
        ON aedct._Acc9_IDRRef = rg._AccountCtRRef 
        AND ed._KindRRef = aedct._DimKindRRef
    CROSS APPLY (
        SELECT 
             ed._Value_RTRef t, 
             ed._Value_RRRef r
    ) v
    WHERE ed.[_period] = rg.[_period]
      AND ed.[_RecorderTRef] = rg._RecorderTRef
      AND ed.[_RecorderRRef] = rg._RecorderRRef
      AND ed.[_LineNo] = rg._LineNo
) ct_sk

WHERE rg._period BETWEEN '4025-01-01 00:00:00' AND '4025-01-01 23:59:59'
  --AND ed._correspond IN (0, 1)
  AND deb._code IN (
      '20.1', '68.3.1', '73.2', '44.2', '44.3', 
      '90.10.1', '90.10.11', '90.7.1', '90.7.2', 
      '91.4.1', '91.4.11', '91.1.1'
  )
  ) t