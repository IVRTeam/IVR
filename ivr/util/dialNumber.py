# 呼叫电话号码的包
from ESL import *
from threading import Thread
from mains.models import Phonelist, State
import datetime
from django.db import connection

# 定义多线程（异步）
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

# 呼叫电话号码的函数
def dial(con, cmd_out, number):
    # 保存通话时长
    duration = "0"
    # 保存用户按键
    keys = []
    # 订阅事件
    con.events('plain', 'CHANNEL_CREATE DTMF CHANNEL_HANGUP_COMPLETE')
    con.filter("Caller-Destination-Number",number)
    content = con.api(cmd_out).getBody()
    flag = content.startswith('+OK')
    # print(flag)
    # print("事件正文---------")
    # print(content)
    # print("结果---------")
    if flag :
        num = 0
        e = con.recvEvent()
        uuid1 = e.getHeader("Unique-ID")
        con.filter("Unique-ID",uuid1)
        print('uuid is ' + uuid1)
        cmd_music = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/begin.wav both'
        con.bgapi(cmd_music)
        print(cmd_music)
        # cmd_exist = 'uuid_exists ' + uuid1
        while 1:
            e = con.recvEvent()
            header = e.getHeader("Event-Name")
            if header == 'CHANNEL_HANGUP_COMPLETE':
                duration = e.getHeader("variable_billsec")
                print("通话时长为：" + duration)
                #print(e.serialize())
                break
            elif header == 'DTMF':
                dtmf = e.getHeader("DTMF-Digit")
                keys.append(dtmf)
                print(dtmf)
                if dtmf == '0':
                    cmd_in = 'originate user/1000 &park'
                    con.bgapi(cmd_in)
                    cmd_hint = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/normal/0.wav both'
                    con.bgapi(cmd_hint)
                    e1 = con.recvEvent()
                    uuid2 = e1.getHeader("Unique-ID")
                    print('Another uuid is ' + uuid2)
                    cmd_bridge = 'uuid_bridge ' + uuid1 + ' ' + uuid2
                    print(cmd_bridge)
                    con.bgapi(cmd_bridge)
                    break
                elif dtmf == '1':
                    cmd_stop = 'uuid_break ' + uuid1 + ' all'
                    con.bgapi(cmd_stop)
                    cmd_hint = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/normal/1.wav both'
                    con.bgapi(cmd_hint)
                    cmd_music1 = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/qr.wav both'
                    con.bgapi(cmd_music1)
                    cmd_music = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/begin.wav both'
                    con.bgapi(cmd_music)
                elif dtmf == '2':
                    cmd_stop = 'uuid_break ' + uuid1 + ' all'
                    con.bgapi(cmd_stop)
                    '''
                    cmd_hint = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/normal/2.wav both'
                    con.api(cmd_hint)
                    '''
                    path = ' /usr/local/freeswitch/Bennett_test/record/' + number + '_' + uuid1 + '_test' + str(num) + '.wav'
                    start_record = 'uuid_record ' + uuid1 + ' start' + path
                    print(start_record)
                    con.api(start_record)
                    num = num + 1
                elif dtmf == '3':
                    stop_record = 'uuid_record ' + uuid1 + ' stop all'
                    con.bgapi(stop_record)
                    cmd_hint = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/normal/3.wav both'
                    con.bgapi(cmd_hint)
                    cmd_music = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/begin.wav both'
                    con.bgapi(cmd_music)
                elif dtmf == '4':
                    cmd_stop = 'uuid_break ' + uuid1 + ' all'
                    con.bgapi(cmd_stop)
                    cmd_hint = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/normal/4.wav both'
                    con.bgapi(cmd_hint)
                    cmd_record = 'uuid_broadcast ' + uuid1 + path + ' both'
                    print(cmd_record)
                    con.bgapi(cmd_record)
                    cmd_music = 'uuid_broadcast ' + uuid1 + ' /usr/local/freeswitch/Bennett_test/sounds/begin.wav both'
                    con.bgapi(cmd_music)
                elif dtmf == '5':
                    hangup = 'uuid_kill ' + uuid1
                    print(hangup)
                    con.api(hangup)
                    break
    print('Over!')
    con.disconnect()
    return duration, keys

@async
def dial_number(number, uid):
    fs_ip = '127.0.0.1'
    fs_esl_port = '8021'
    fs_esl_auth = 'ClueCon'
    callTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("callTime is " + callTime)
    cmd_out = 'originate {ignore_early_media=true}sofia/gateway/gw2/'
    con = ESLconnection(fs_ip, fs_esl_port, fs_esl_auth)
    cmd = cmd_out + number + ' &park'
    if con.connected():
        duration, keys = dial(con, cmd, number)
        status = '呼叫成功'
        digits = keys
        if duration == "0":
            status = '呼叫失败'
            digits = ''
        # 这一行有问题，电话号码并不是唯一值，应该将用户id和电话号码一起传过来
        cursor = connection.cursor()
        cursor.callproc("addState", (uid, number, status, callTime, duration, str(digits)))
        # phone = Phonelist.objects.get(number=number)
        # sta = State.createState(status, callTime, callLength, digits, phone)
        # sta.save()
    #
    # else:
    #     duration = "0"
    #     keys = []