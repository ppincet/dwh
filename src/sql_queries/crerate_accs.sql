create table Z_ACCOUNT(
	ID binary(16) not null,
    Z_TYPE binary(4) not null,
	Z_CODE nvarchar(11) not null,
	Z_DESCR nvarchar(120) not null
)
ALTER TABLE Z_ACCOUNT 
ADD CONSTRAINT PK_Z_SUBKONTO PRIMARY KEY CLUSTERED (ID, Z_TYPE);

