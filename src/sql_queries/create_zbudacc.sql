create table ZBUDACC(
    Z_PERIOD char(8) not null,
    ZAMOUNT numeric(8,2) not null,
    Z_DT_TYPE binary(4) not null,
    Z_DT_REF binary(16) not null,
	Z_DT_SK1_TYPE binary(4) not null,
	Z_DT_SK1_REF binary(16) not null,
    Z_DT_SK2_TYPE binary(4) not null,
	Z_DT_SK2_REF binary(16) not null,
    Z_DT_SK3_TYPE binary(4) not null,
	Z_DT_SK3_REF binary(16) not null,
    Z_DT_SK4_TYPE binary(4) not null,
	Z_DT_SK4_REF binary(16) not null,
    Z_CT_TYPE binary(4) not null,
    Z_CT_REF binary(16) not null,
	Z_CT_SK1_TYPE binary(4) not null,
	Z_CT_SK1_REF binary(16) not null,
    Z_CT_SK2_TYPE binary(4) not null,
	Z_CT_SK2_REF binary(16) not null,
    Z_CT_SK3_TYPE binary(4) not null,
	Z_CT_SK3_REF binary(16) not null,
    Z_CT_SK4_TYPE binary(4) not null,
	Z_CT_SK4_REF binary(16) not null,
    
)

CREATE NONCLUSTERED INDEX UIX_ZBUDACC_DT_Type_Ref 
ON ZBUDACC (Z_DT_TYPE, Z_DT_REF)
CREATE NONCLUSTERED INDEX UIX_ZBUDACC_CT_Type_Ref 
ON ZBUDACC (Z_CT_TYPE, Z_CT_REF)
CREATE NONCLUSTERED INDEX UIX_ZBUDACC_DT_SK1_Type_Ref 
ON ZBUDACC (Z_DT_SK1_TYPE, Z_DT_SK1_REF)
CREATE NONCLUSTERED INDEX UIX_ZBUDACC_DT_SK2_Type_Ref 
ON ZBUDACC (Z_DT_SK2_TYPE, Z_DT_SK2_REF)
CREATE NONCLUSTERED INDEX UIX_ZBUDACC_DT_SK3_Type_Ref 
ON ZBUDACC (Z_DT_SK3_TYPE, Z_DT_SK3_REF)
CREATE NONCLUSTERED INDEX UIX_ZBUDACC_DT_SK4_Type_Ref 
ON ZBUDACC (Z_DT_SK4_TYPE, Z_DT_SK4_REF)