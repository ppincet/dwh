update ZETLLOG       
set
    ZLSTPERIOD = ?,
    ZLSTTREF = ?,
    ZLSTRREF = ?,
    ZLSTLN = ?,
    ZTOTROWS = ?,
    ZSTATUS = ?,
    ZUPDATED = getdate(),
    ZLASTDAY = ?

where ZTASKNAME = ?