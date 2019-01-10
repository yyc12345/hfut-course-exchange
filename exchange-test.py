import requests
import time
import hashlib
import json
import config

virtualCost = '0'

fake_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
universal_header = {'User-Agent' : fake_ua}

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
    header = {'Content-Type': 'application/json', 'User-Agent' : fake_ua}
    
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
    header = {'Content-Type': 'application/json', 'User-Agent' : fake_ua}
    
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
    global universal_header

    # operate
    drop_data = {'studentAssoc': giver_id, 'lessonAssoc': config.lesson, 'courseSelectTurnAssoc': config.turn}
    add_data = {'studentAssoc': receiver_id, 'lessonAssoc': config.lesson,
        'courseSelectTurnAssoc': config.turn, 'scheduleGroupAssoc': '', 'virtualCost': virtualCost}
    readd_data = {'studentAssoc': giver_id, 'lessonAssoc': config.lesson,
            'courseSelectTurnAssoc': config.turn, 'scheduleGroupAssoc': '', 'virtualCost': virtualCost}

    drop_operator = giver_s.post(url_drop, data=drop_data, headers=universal_header)
    add_operator = receiver_s.post(url_add, data=add_data, headers=universal_header)
    readd_operator = giver_s.post(url_add, data=readd_data, headers=universal_header)

    # get result
    drop_temp = drop_operator.text
    add_temp = add_operator.text
    readd_temp = readd_operator.text

    # drop res
    check_data = {'studentId': giver_id, 'requestId': drop_temp}
    checker = giver_s.post(url_check, data=check_data, headers=universal_header)
    temp = json.loads(checker.text)
    print('Drop course status:')
    print(temp['success'])

    check_data = {'studentId': receiver_id, 'requestId': add_temp}
    checker = giver_s.post(url_check, data=check_data, headers=universal_header)
    temp = json.loads(checker.text)
    print('Add course status:')
    print(temp['success'])

    check_data = {'studentId': giver_id, 'requestId': readd_temp}
    checker = giver_s.post(url_check, data=check_data, headers=universal_header)
    temp = json.loads(checker.text)
    print('Re-add course status:')
    print(temp['success'])
    
def logout_giver():
    global giver_s
    global universal_header
    giver_s.get(logout_url, headers=universal_header)

def logout_receiver():
    global receiver_s
    global universal_header
    receiver_s.get(logout_url, headers=universal_header)

print('This app could not promise that you can exchange course successfully! You should edit config.py first. Press Enter to run this app. Are you sure?')
input()
login_giver()
login_receiver()
exchange_course()
logout_giver()
logout_receiver()
print('App exit!')
input()


