import requests
import time
import hashlib
import json
import config

# 这也是一个固定值，看起来像照搬的别的系统，没有删干净
virtualCost = '0'

url_add = 'http://jxglstu.hfut.edu.cn/eams5-student/ws/for-std/course-select/add-request'
url_drop = 'http://jxglstu.hfut.edu.cn/eams5-student/ws/for-std/course-select/drop-request'
url_check = 'http://jxglstu.hfut.edu.cn/eams5-student/ws/for-std/course-select/add-drop-response'
salt_url = 'http://jxglstu.hfut.edu.cn/eams5-student/login-salt'
login_url = "http://jxglstu.hfut.edu.cn/eams5-student/login"
logout_url = "http://jxglstu.hfut.edu.cn/eams5-student/logout"
info_url = 'http://jxglstu.hfut.edu.cn/eams5-student/for-std/student-info'

giver_s = requests.Session()
giver_id = '11111'
receiver_s = requests.Session()
receiver_id = '11111'

def login_giver():
    global giver_s
    response = giver_s.get(salt_url)
    while response.status_code == 404:
        giver_s = requests.Session()
        response = receiver_s.get(salt_url)
    temp = response.text
    password = temp + "-" + config.giver_password
    hash = hashlib.sha1()
    hash.update(password.encode('utf-8'))
    password = hash.hexdigest()
    data = {'username': config.giver_username, 'password': password, 'captcha': ''}
    data = json.dumps(data, separators=(',', ':')).encode(encoding='utf-8')
    header = {'Content-Type': 'application/json'}
    
    giver_s.post(login_url,data=data,headers=header)
    giver_s.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-select')
    res = giver_s.get(info_url)
    global giver_id
    giver_id = res.url.split('/')[-1]

    print('Giver login OK')

def login_receiver():
    global receiver_s
    response = receiver_s.get(salt_url)
    while response.status_code == 404:
        receiver_s = requests.Session()
        response = receiver_s.get(salt_url)
    temp = response.text
    password = temp + "-" + config.receiver_password
    hash = hashlib.sha1()
    hash.update(password.encode('utf-8'))
    password = hash.hexdigest()
    data = {'username': config.receiver_username, 'password': password, 'captcha': ''}
    data = json.dumps(data, separators=(',', ':')).encode(encoding='utf-8')
    header = {'Content-Type': 'application/json'}
    
    receiver_s.post(login_url,data=data,headers=header)
    receiver_s.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-select')
    res = receiver_s.get(info_url)
    global receiver_id
    receiver_id = res.url.split('/')[-1]

    print('Receiver login OK')

def exchange_course():
    global receiver_id
    global receiver_s
    global giver_id
    global giver_s

    # drop course
    drop_data = {'studentAssoc': giver_id, 'lessonAssoc': config.lesson, 'courseSelectTurnAssoc': config.turn}
    drop_operator = giver_s.post(url_drop, data=drop_data)
    temp = drop_operator.text
    drop_data = {'studentId': giver_id, 'requestId': temp}
    drop_checker = giver_s.post(url_check, data=drop_data)
    temp = json.loads(drop_checker.text)
    if not temp['success']:
        print('Fail to drop course. Give up.')
        return
    print('Drop course OK')

    # add course
    add_data = {'studentAssoc': receiver_id, 'lessonAssoc': config.lesson,
        'courseSelectTurnAssoc': config.turn, 'scheduleGroupAssoc': '', 'virtualCost': virtualCost}
    add_operator = receiver_s.post(url_add, data=add_data)
    temp = add_operator.text
    add_data = {'studentId': receiver_id, 'requestId': temp}
    add_checker = receiver_s.post(url_check, data=add_data)
    temp = json.loads(add_checker.text)
    if not temp['success']:
        print('Fail to add course. Try to re-add course')

        # re-add
        readd_data = {'studentAssoc': giver_id, 'lessonAssoc': config.lesson,
            'courseSelectTurnAssoc': config.turn, 'scheduleGroupAssoc': '', 'virtualCost': virtualCost}
        readd_operator = giver_s.post(url_add, data=readd_data)
        temp = readd_operator.text
        readd_data = {'studentId': giver_id, 'requestId': temp}
        readd_checker = giver_s.post(url_check, data=readd_data)
        temp = json.loads(readd_checker.text)
        if not temp['success']:
            print('BAD NEWS. You lost your course! Your course might be captured by others.');
        print('Fail to exchange. But you do not lose anything. Everying stays the same.')
    print('Congratulation! Your course has been exchanged successfully!')

def logout_giver():
    global giver_s
    giver_s.get(logout_url)

def logout_receiver():
    global receiver_s
    receiver_s.get(logout_url)

print('This app could not promise that you can exchange course successfully! You should edit config.py first. Press Enter to run this app. Are you sure?')
input()
login_giver()
login_receiver()
exchange_course()
logout_giver()
logout_receiver()
print('App exit!')
input()


