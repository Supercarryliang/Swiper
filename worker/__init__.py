import os

from worker import config
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Swiper.settings")   #通过这段代码将celery与django结合起来

celery_app=Celery('worker')  #创建一个名为worker的celery对象
celery_app.config_from_object(config) #celery加载配置
celery_app.autodiscover_tasks()      #celery自动搜索任务

