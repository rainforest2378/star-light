# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:28:44 2019

@author: fyl
"""

import MySQLdb
import nmap


nm = nmap.PortScanner()
input_data = raw_input("请输入您要扫描的网段，端口：")
scan_row= input_data.split(" ")
temp=scan_row[0]    #接收用户输入的主机
tport=scan_row[1]    #接收用户输入的端口
a=nm.scan(hosts=temp,arguments='-sV',ports=tport)

conn = MySQLdb.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',passwd='fyl@chjtxmysql',db='fyl',charset='utf8')
cursor = conn.cursor()


for host in nm.all_hosts():    #遍历扫描主机
    sql="insert into service_detection(hostname,hostip,hoststate,port,portstate,protocal,service,version,scantime) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))    #输出主机及主机名
    print('State : %s' % nm[host].state())    #输出主机状态，如up、down
    hostname=nm[host].hostnames()[0]['name']
    hostip=host
    hoststate=nm[host].state()
    scantime=a['nmap']['scanstats']['timestr']
        
    for proto in nm[host].all_protocols():    #遍历扫描协议，如tcp、udp
        print('----------')
        print('Protocol : %s' % proto)    #输入协议名
        protocal=proto
        lport = nm[host][proto].keys()    #获取协议的所有扫描端口
        sorted(lport)    #端口列表排序
        
        for sport in lport:    #遍历端口及输出端口与状态，服务和版本信息
            portstate=nm[host][proto][sport]['state']
            service=nm[host][proto][sport]['name']
            version=nm[host][proto][sport]['version']
            port=sport
            print('port : %s\t state : %s\t service: %s\t version: %s ' % (port, portstate,service,version))
            
            try:
                cursor.execute(sql,(hostname,hostip,hoststate,port,portstate,protocal,service,version,scantime))
                conn.commit()   #把修改的数据提交到数据库
            except Exception as e:
                print('failed')
                conn.rollback() #捕捉到错误就回滚


# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()
