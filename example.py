import time
import flask
import datetime
from mian import Client
from flask import request
from dateutil.relativedelta import relativedelta

# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
app = flask.Flask(__name__)
cookies = {}

stu = Client(cookies=cookies)


def CalTime(date1):
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = datetime.datetime.now().timetuple()

    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    differ = date2 - date1
    WeekTh = differ // datetime.timedelta(days=7) + 1

    return WeekTh


@app.route('/Login', methods=['GET', 'POST'])  # 用户登录模块
def login():
    if cookies == {}:
        lgn = stu.login(request.form.get('username'), request.form.get('password'))
        if lgn["code"] == 1002:
            return lgn
        elif lgn["code"] != 1000:
            return lgn
        elif lgn["code"] == 1000:
            return lgn


@app.route('/Info', methods=['GET', 'POST'])  # 获取个人信息
def info():
    result = stu.get_info(request.form.get('password'), request.form.get('username'))  # 获取个人信息
    return result


@app.route('/ScoreDetails', methods=['GET', 'POST'])  # 获取成绩信息
def ScoreDetails():
    result = stu.get_grade(int(request.form.get('year')), int(request.form.get('term')),
                           request.form.get('username'))  # 获取成绩信息，若接口错误请添加 use_personal_info=True，只填年份获取全年
    return result


@app.route('/Table', methods=['GET', 'POST'])  # 获取课程表信息
def Table():
    result = stu.get_schedule(int(request.form.get('year')), int(request.form.get('term')))  # 获取课程表信息
    return result


@app.route('/academia', methods=['GET', 'POST'])  # 获取学业生涯数据
def academia():
    result = stu.get_academia()  # 获取学业生涯数据
    return result


@app.route('/courses', methods=['GET', 'POST'])  # 用户登录模块
def courses():
    result = stu.get_selected_courses(int(request.form.get('year')), int(request.form.get('term')))  # 获取已选课程信息
    return result


@app.route('/GetInfo', methods=['GET', 'POST'])  # 开学信息模块
def GetInfo():
    getinfo = {}
    NowMonth = datetime.date.today().strftime("%-m")
    if NowMonth == '8' or NowMonth == '9' or NowMonth == '10' or NowMonth == '11' or NowMonth == '12' or NowMonth == '1' or NowMonth == '2':
        semester = "1"
        NowYear = datetime.date.today().strftime("%Y")
        NextYear = datetime.date.today() + relativedelta(years=1)
        SchoolYear = NowYear + "-" + NextYear.strftime('%Y')
        getinfo['SchoolYear'] = SchoolYear
        getinfo['semester'] = semester
        getinfo['teachWeek'] = CalTime("2022-8-21")
        getinfo['code'] = 1000
        return getinfo
    else:
        semester = "2"
        LastYear = datetime.date.today() - relativedelta(years=1)
        NowYear = datetime.date.today().strftime("%Y")
        SchoolYear = LastYear.strftime('%Y') + "-" + NowYear
        getinfo['SchoolYear'] = SchoolYear
        getinfo['semester'] = semester
        getinfo['teachWeek'] = CalTime("2022-8-21")
        getinfo['code'] = 1000
        return getinfo


if __name__ == '__main__':
    app.run(port=5001, debug=True, host='127.0.0.1')
