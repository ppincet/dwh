create table ZSESSION (
    ID UNIQUEIDENTIFIER not null,
    PARENTID UNIQUEIDENTIFIER,
    P_START datetime2 not null,
    P_END datetime2 not null,
    COMMAND varchar(50),
    STATUS varchar(20),
    constraint PK_ZSESSION primary key  nonclustered (ID)
);
create clusstered index  IX_ZSESSION_P_START on ZSESSION (P_START);
create  nonclustered index IX_ZSESSION_PARENTID on ZSESSION (PARENTID) where PARENTID is not null;
create nonclustered index IX_ZSESSION_STATUS on ZSESSION (STATUS, P_START) include (COMMAND, P_END);

create table ZLOG (
    SESSIONID UNIQUEIDENTIFIER not null,
    COMMAND varchar(50),
     varchar(max),
    LEVEL varchar(20)
)
create table ZMETRIC (
    SESSIONID UNIQUEIDENTIFIER not null,
    COMMAND varchar(50),
    ENTRY varchar(),
    DURATION bigint
)
