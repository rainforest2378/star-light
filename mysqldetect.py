# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:28:44 2019

@author: fyl
"""

import MySQLdb
import nmap

nm = nmap.PortScanner()
temp = raw_input("请输入您要扫描的网段：")
a=nm.scan(hosts=temp,arguments='--script mysql-info',ports='3306')#扫描网段中的数据库

conn = MySQLdb.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',passwd='fyl@chjtxmysql',db='fyl',charset='utf8')
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()

for host in nm.all_hosts():    #遍历扫描主机
    sql="insert into mysql_detection(hostname,hostip,hoststate,port,portstate,mysql_info,service,scantime) VALUE (%s,%s,%s,%s,%s,%s,%s,%s);"
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))    #输出主机及主机名
    print('State : %s' % nm[host].state())    #输出主机状态，如up、down
    hostname=nm[host].hostnames()[0]['name']
    hostip=host
    hoststate=nm[host].state()
    port=3306
    scantime=a['nmap']['scanstats']['timestr']
    service= a['scan'][host]['tcp'][3306]['name']
    portstate=nm[host]['tcp'][port]['state']
    print('port : %s\tstate : %s' % (port,portstate))
    
    
    if(portstate=='open'):#如果3306端口开放，获取数据库信息，否则扫描下一个主机
        mysql_info=a['scan'][host]['tcp'][port]['script']['mysql-info']
        print('service:%s\t mysql_info:%s\t'% (service,mysql_info))#输出数据库信息
        try:
            cursor.execute(sql,(hostname,hostip,hoststate,port,portstate,mysql_info,service,scantime))
            conn.commit()   #把修改的数据提交到数据库
        except Exception as e:
            print('failed')
            conn.rollback() #捕捉到错误就回滚
    else:
        break

cursor.close()# 关闭光标对象
conn.close()# 关闭数据库连接
