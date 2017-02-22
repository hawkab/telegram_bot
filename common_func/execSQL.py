# -*- coding: utf-8 -*-
#!/usr/bin/python
import MySQLdb

def sql_exec ( request ):
    con = MySQLdb.connect("localhost","king","masterkey1","telegram_bot" )
    cur = con.cursor()
    cur.execute ( request )
    con.commit()
    result = cur.fetchall()
    con.close()
    return result