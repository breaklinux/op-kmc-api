#!/bin/bash
#需要提前启动redis服务
# shellcheck disable=SC2126
queryCeleryPkg=$(sudo pip3 list |grep "celery" |wc -l )
queryFlowerPkg=$(sudo pip3 list |grep "flower" |wc -l )

if [ queryCeleryPkg == "1" ] &&  [ $queryFlowerPkg == "1" ]
then
   celery -A deploy_kernel_upgrade_celery.main  worker -B -l info --concurrency=15  --beat
   celery -A deploy_kernel_upgrade_celery.main  flower --port=8888
else
    pip3 install celery
    pip3 install flower
    celery -A celery_kernel_upgrade.main  worker -B -l info --concurrency=500  --beat
    celery -A celery_kernel_upgrade.main  flower --port=8888
fi
