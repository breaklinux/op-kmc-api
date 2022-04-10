#!/bin/bash
#需要提前启动redis服务
queryPkg=$(sudo pip3 list |grep celery |wc -l )
if [ $queryPkg == "1" ]
then
   celery -A celery_tasks.main  worker -B -l info --concurrency=1000  --beat
else
    pip3 install celery
    celery -A celery_tasks.main  worker -B -l info --concurrency=1000  --beat
fi
