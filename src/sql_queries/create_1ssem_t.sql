drop table if exists ZBFTREG03;
create table  ZBFTREG03 (
    [0CALDAY] date,
    ZBPOSORG char(32),
    ZBFTDEP char(32),
    ZBFT073 decimal(10,3)
);

drop table if exists ZBEMPL;
create table ZBEMPL (
    ZBGUID char(32),
    ZBFT024 nvarchar(256),
    ZBEMPL nvarchar(10),
    ZBFT001 bit,
    ZBFT009 char(32),
    ZBFT010 date,
    ZBFT011 date,
    ZBFT012 date,
    ZBFT013 date,
    ZBFT014 char(32),
    ZBFT015 char(32),
    [0COMP_CODE] char(32),
    ZBFT016 char(32),
    ZBFT017 char(32),
    ZBFT018 char(32),
    ZBFT019 char(32),
    ZBFT020 char(32),
    ZBFT021 decimal(4,1)
);

drop table if exists ZBPOSORG;
create table ZBPOSORG (
    ZBGUID char(32),
    ZBPOSORG nvarchar(9),
    ZBPPOSORG nvarchar(150),
    ZBFT001 bit
);

drop table if exists ZBPOSDEP;
create table ZBPOSDEP (
    ZBGUID char(32),
    ZBFT024 nvarchar(256),
    ZBPOSDEP nvarchar(9),
    ZBPPOSDEP nvarchar(150),
    ZBFT001 bit,
    ZBPOSORG char(32)
);

drop table if exists 