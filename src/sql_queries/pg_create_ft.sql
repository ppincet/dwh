create table ZLSF_FACT (
	ZDSID bigint,
	ZSKUID bigint,
	ZBARCODE varchar(15),
	ZAMNT numeric(16,5),
	ZCOST numeric(17, 3),
	ZVAT numeric(10, 5),
	ZVOL numeric(10, 4),
	ZNETW numeric(12, 6),
	ZGROSSW numeric(12,6),
	ZPERIOD datetime2
)	