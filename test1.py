from flask import Flask
from flask import request
import json
import nmap
import time, datetime
import pymysql
# 创建flask对象
app = Flask(__name__)

@app.route("/config/update", methods=["POST"],endpoint="2")
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    configID = get_Data.get('configID')
    #IPRange = get_Data.get('IPRange')
    serviceName = get_Data.get('serviceName')
    startTime = get_Data.get('startTime')
    intervalTime=get_Data.get('intervalTime')
    endTime = get_Data.get('endTime')
    repeatTimes = get_Data.get('repeatTimes')
    enable=get_Data.get('enable')
    configTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("""
           UPDATE schedule
           SET configTime=%s,serviceName=%s,startTime=%s,intervalTime=%s,endTime=%s,repeatTimes=%s,enable=%s
           WHERE id=%s
        """, (configTime, serviceName, startTime, intervalTime, endTime, repeatTimes, enable, configID))
    conn.commit()  # 把修改的数据提交到数据库

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    print('Program now starts on %s' % startTime)
    print('Executing...')

    return_dict['result'] = tt2(configID)


    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt2(configID):
    # result_str = "%s今年%s岁" % (name, age)
    status="ok"

    return status,configID


@app.route("/config/add", methods=["POST"],endpoint="1")
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    IPRange = get_Data.get('IPRange')
    serviceName = get_Data.get('serviceName')
    startTime = get_Data.get('startTime')
    intervalTime=get_Data.get('intervalTime')
    endTime = get_Data.get('endTime')
    repeatTimes = get_Data.get('repeatTimes')
    enable=get_Data.get('enable')
    configTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into schedule(configTime,IPRange,serviceName,startTime,intervalTime,endTime,repeatTimes,enable) VALUE (%s,%s,%s,%s,%s,%s,%s,%s);"

    cursor.execute(sql, (configTime,IPRange,serviceName,startTime,intervalTime,endTime,repeatTimes,enable))
    conn.commit()  # 把修改的数据提交到数据库

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    print('Program now starts on %s' % startTime)
    print('Executing...')

    return_dict['statu'] = tt1()


    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt1():
    # result_str = "%s今年%s岁" % (name, age)
    status="ok"
    return status

@app.route("/read/", methods=["POST"],endpoint="1")
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    IPRange = get_Data.get('IPRange')
    serviceName = get_Data.get('serviceName')
    startTime = get_Data.get('startTime')
    intervalTime=get_Data.get('intervalTime')
    endTime = get_Data.get('endTime')
    repeatTimes = get_Data.get('repeatTimes')
    enable=get_Data.get('enable')
    configTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into schedule(configTime,IPRange,serviceName,startTime,intervalTime,endTime,repeatTimes,enable) VALUE (%s,%s,%s,%s,%s,%s,%s,%s);"

    cursor.execute(sql, (configTime,IPRange,serviceName,startTime,intervalTime,endTime,repeatTimes,enable))
    conn.commit()  # 把修改的数据提交到数据库

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    print('Program now starts on %s' % startTime)
    print('Executing...')

    return_dict['statu'] = tt1()


    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt1():
    # result_str = "%s今年%s岁" % (name, age)
    status="ok"
    return status



if __name__ == "__main__":
    app.run()

