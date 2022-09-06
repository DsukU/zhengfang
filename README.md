🏫 新正方教务管理系统 API

😁 几乎规避所有学校不同导致的兼容性问题，可放心食用！！


## 功能实现

- [√] 登录（自动识别是否需要验证码）
- [√] 个人信息
- [√] 成绩查询（两种接口）
- [√] 课表查询
- [√] 课程表 PDF
- [√] 学业生涯数据
- [√] 学业生涯（学业成绩总表） PDF （**存在兼容问题**）
- [√] 停补换课消息
- [√] 查询已选课程
- [√] 获取选课板块课列表
- [√] 选课
- [√] 退课
- [ ] 空教室查询

## 状态码

为了一些特殊的业务逻辑，如验证码错误后自动刷新页面获取等，使用了自定义状态码，详情如下：

| 状态码 | 内容                 |
| ------ | -------------------- |
| 998    | 网页弹窗未处理内容   |
| 999    | 接口逻辑或未知错误   |
| 1000   | 请求获取成功         |
| 1001   | （登录）需要验证码   |
| 1002   | 用户名或密码不正确   |
| 1003   | 请求超时             |
| 1004   | 验证码错误           |
| 1005   | 内容为空             |
| 1006   | cookies 失效或过期   |
| 1007   | 接口失效请更新       |
| 2333   | 系统维护或服务被 ban |

## Tips⚠️
- 本例程使用了Flask框架进行调用，如需其他环境请自行更改调用。
- 有些功能具备了传参功能，例如username，password 若根据自己的开发环境做出更改或增添。
- 请先在 `config.json` 中修改教务系统 `base_url` 和上下课时间 `raspisanie` 。
  - 只需填写`https://xxx.com`到 base_url 中，拼接后与类中 `self.xxurl` 不同的路径部分在 API 代码内增删改。
- 学业生涯数据为教务系统 **“学生学业情况查询”** 页面内容，获取数据时请留意 `config.json` 中 `ignore_type` 和 `detail_category_type`。
  - `ignore_type` 表示需要忽略的最顶部根类型，如 “主修”，“20XX 级 XX 专业” 等无用类型，**可留空数组，对结果无影响**。
  - `detail_category_type` 表示需要详细获取课程分类的类型，如 “其他课程” 需获取该网课属于什么类等，**可留空数组**。
- 教务系统的 cookies 在不同学校统一认证系统不同，**若系统开启了验证码且 cookies 格式内容与默认有出入**，请修改 `mian.py` 中 `login_with_kaptcha()` 中兼容差异注释部分。
- 兼容导致 学业生涯数据 PDF 表的导出会出现问题，待排查。
- 一个简单的测试示例

  ```python
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
          lgn = stu.login(request.args.get('username'), request.args.get('password'))
          if lgn["code"] == 1002:
              return lgn
          elif lgn["code"] != 1000:
              return lgn
          elif lgn["code"] == 1000:
              return lgn
  
  
  @app.route('/Info', methods=['GET', 'POST'])  # 获取个人信息
  def info():
      result = stu.get_info(request.args.get('password'), request.args.get('username'))  # 获取个人信息
      return result
  
  
  @app.route('/ScoreDetails', methods=['GET', 'POST'])  # 获取成绩信息
  def ScoreDetails():
      result = stu.get_grade(int(request.args.get('year')), int(request.args.get('term')),
                             request.args.get('username'))  # 获取成绩信息，若接口错误请添加 use_personal_info=True，只填年份获取全年
      return result
  
  
  @app.route('/Table', methods=['GET', 'POST'])  # 获取课程表信息
  def Table():
      result = stu.get_schedule(int(request.args.get('year')), int(request.args.get('term')))  # 获取课程表信息
      return result
  
  
  @app.route('/academia', methods=['GET', 'POST'])  # 获取学业生涯数据
  def academia():
      result = stu.get_academia()  # 获取学业生涯数据
      return result
  
  
  @app.route('/courses', methods=['GET', 'POST'])  # 用户登录模块
  def courses():
      result = stu.get_selected_courses(int(request.args.get('year')), int(request.args.get('term')))  # 获取已选课程信息
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

  ```
