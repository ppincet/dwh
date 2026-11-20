--- -- session part
insert ZSESSION (
    [ID],
    [PARENTID],
    [P_START],
    [P_END],
    [COMMAND],
    [STATUS]
)
values (?, ?, ?, ?, ?, ?)


;--- -- log part
;--- -- metric part