--- -- [0] clustered
drop index if exists IX_ZLSF_FACT1_ZID on ZLSF_FACT1;
create unique clustered index IX_ZLSF_FACT1_ZID
on ZLSF_FACT1 (ZID asc)
with (
    pad_index = off,
    statistics_norecompute = off,
    sort_in_tempdb = on,
    ignore_dup_key = off,
    drop_existing = off,
    online = off,
    allow_row_locks = on,
    allow_page_locks = on,
    optimize_for_sequential_key = off
) on [PRIMARY];

;--- -- [1] unclustered 
drop index if exists IX_ZLSF_FACT1_ZPERIOD on ZLSF_FACT1;
create nonclustered index IX_ZLSF_FACT1_ZPERIOD
on ZLSF_FACT1 (ZPERIOD)
with (
    pad_index = off,
    statistics_norecompute = off,
    sort_in_tempdb = on,
    drop_existing = off,
    online = off,
    allow_row_locks = on,
    allow_page_locks = on
) on [PRIMARY];
;--- -- [2] drop clust
drop index if exists IX_ZLSF_FACT1_ZPERIOD on ZLSF_FACT1;
;--- -- [3] drop unclust
drop index if exists IX_ZLSF_FACT1_ZID on ZLSF_FACT1;
;--- -- [4]
drop index if exists IX_ZLSF_FACT_STG_DT_V_KEYS on ZLSF_FACT_STG;
create clustered index IX_ZLSF_FACT_STG_DT_V_KEYS on ZLSF_FACT_STG (DT_V, DS, SID, OP, ISRET, BARC);
