merge into ZETLLOG  t
using (select ? as ZTASKNAME) as s on t.ZTASKNAME = s.ZTASKNAME
when matched then 
            update set 
                ZSTARTWND = ?,
	            ZENDWND = ?,
	            ZLSTPERIOD = ?,
	            ZLSTTREF = ?,
	            ZLSTRREF = ?,
	            ZLSTLN = ? ,
	            ZTOTROWS = 0,
	            ZSTATUS = 'IN_PROGRESS',
	            ZUPDATED = getdate()           
when not matched then
            insert (
                ZTASKNAME,
	            ZSTARTWND,
	            ZENDWND,
	            ZLSTPERIOD,
                ZLSTTREF,
                ZLSTRREF,
                ZLSTLN,
                ZTOTROWS,
                ZSTATUS            
                )
            values (?, ?, ?, ?, ?, ?, ?, 0, 'IN_PROGRESS');

