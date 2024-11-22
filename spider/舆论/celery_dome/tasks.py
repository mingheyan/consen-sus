# 注册任务
import time

from celery import shared_task

### 写个类，继承 Task，写方法
from celery import Task

from django.core.mail import send_mail
from django.conf import settings


class SendEmailTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # 任务执行成功，会执行这个
        info = f'爬虫任务成功-- 任务id是:{task_id} , 参数是:{args} , 执行成功 !'
        # 发送邮件--》django中发送邮件
        send_mail('celery监控成功告警', info, settings.EMAIL_HOST_USER, ['3215421266@qq.com'])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 任务执行失败，会执行这个
        info = f'爬虫任务失败-- 任务id是:{task_id} , 参数是:{args} , 执行失败，请去flower中查看原因 !'
        # 发送邮件--》django中发送邮件
        send_mail('celery监控爬虫失败告警', info, settings.EMAIL_HOST_USER, ['3215421266@qq.com'])

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # 任务执行重试，会执行这个
        print('重试了！！！')


# 以后使用shared_task 替换掉 app.task

# 任务函数
@shared_task
def add(a, b):
    return a + b


@shared_task
def send_email(to_user):
    time.sleep(2)
    return '发送邮件成功:%s' % to_user


# @shared_task(base=SendEmailTask, bind=True)  # 只要执行它成功或失败，都会给 616564099@qq.com发送邮件
# def crawl_cnblogs(self):
#     # req=[]
#     # print(req['s'])
#     print('爬去cnblogs网站技术博客了')
#     return True
import logging
@shared_task(base=SendEmailTask, bind=True)  # 只要执行它成功或失败，都会给 616564099@qq.com发送邮件
def crawl_cnblogs(self):
    res={}
    print(555)
        # logging.info('爬去cnblogs网站技术博客了')
    # except Exception as e:
    #     logging.error(e)
    return True

from celery import shared_task
# from celery.task import Task

class MyTask(Task):
    def __init__(self):
        self.counter = 0

    def l(self, pa):
        self.counter += 1
        print(pa)

    def r(self):
        print(self.counter)
        pa = self.counter
        pa += 1
        self.l(pa)

    def run(self,PA):
        print(PA)
        self.r()

# 创建 MyTask 的实例
@shared_task
def celery_send_sms_code():
    print('准备调用发送短信代码...')
    time.sleep(2)
    # CCP().send_template_sms(mobile, [code, 5], 1)
    print('短信业务代码调用成功...')

celery_send_sms_code.delay()

my_task_instance = MyTask()
# 使用 shared_task 装饰器装饰一个函数
@shared_task(base=SendEmailTask, bind=True)
def execute_my_task(self,PA):
    my_task_instance.run(PA)

# 调用任务时，通常会这样做：
# execute_my_task.delay()




