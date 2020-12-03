# 上下班打卡提醒
## 使用方法
1. 需要Python 3.X环境
2. 需要安装`pyweathercn`包
```
pip3 install pyweathercn
```
3. key值获取
    * 若使用QQ提醒则前往[https://qmsg.zendee.cn/](https://qmsg.zendee.cn/)登录添加提醒QQ和获取`key`值
    * 若使用server酱提醒则前往[http://sc.ftqq.com/](http://sc.ftqq.com/)登录获取`key`值
4. 替换`key`值后将此代码放入VPS后执行即可
## 定时策略
以Centos为例：
```
# 进入编写定时脚本
crontab -e
# 需要定时两次脚本（上下班）
20 8 * * * cd /project/dingReminder &&  python dingReminder.py  >> dingReminder.log 2>&1
32 17 * * * cd /project/dingReminder &&  python dingReminder.py  >> dingReminder.log 2>&1
```
> linux 定时任务编写脚本可参考[Linux Crontab 定时任务](https://www.runoob.com/w3cnote/linux-crontab-tasks.html)