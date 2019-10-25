# -*- coding: utf-8 -*-
"""

@author: fyl
"""

import MySQLdb
import nmap


nm = nmap.PortScanner()
network_prefix = raw_input("请输入您要扫描的网段：")
scan_raw_result = nm.scan(hosts=network_prefix, arguments='-O --fuzzy')
conn = MySQLdb.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',passwd='fyl@chjtxmysql',db='fyl',charset='utf8')
cursor = conn.cursor()

# 分析扫描结果
for host, result in scan_raw_result['scan'].items():
    if result['status']['state'] == 'up':
        print('#' * 17 + 'Host:' + host + '#' * 17)
        print('-' * 20 + 'os_guess' + '-' * 20)
        for os in result['osmatch']:
            osname=os['name']#os名称
            accuracy=os['accuracy']#os可能性
            print('操作系统为：' + osname + ' ' * 3 + '准确度为：' + accuracy)
            scantime=scan_raw_result['nmap']['scanstats']['timestr']
            hostname=nm[host].hostnames()[0]['name']
            hostip=host
            hoststate=nm[host].state()
            
            
            sql="insert into os_detection (hostname,hostip,hoststate,os,os_accuracy,scantime) VALUE (%s,%s,%s,%s,%s,%s);"
            try:
                cursor.execute(sql,(hostname,hostip,hoststate,osname,accuracy,scantime))
                conn.commit()   #把修改的数据提交到数据库
            except Exception as e:
                print('failed')
                conn.rollback() #捕捉到错误就回滚

    
    
# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()
