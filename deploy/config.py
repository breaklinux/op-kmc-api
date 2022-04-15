from kombu import Queue

# 参考地址: https://blog.csdn.net/qq_33961117/article/details/100770533
# 配置代理人，指定代理人将任务存到哪里,这里是redis的14号库
broker_url = 'redis://192.168.1.200:6379/14'
# celery worker的并发数，默认是服务器的内核数目,也是命令行-c参数指定的数目
# CELERYD_CONCURRENCY = 8
worker_concurrency = 4
result_backend = 'redis://192.168.1.200:6379/15'
# celery worker 每次去BROKER中预取任务的数量-
worker_prefetch_multiplier = 4
include = ['deploy_kernel_upgrade_celery.tasks', 'deploy_k8s_base_celery.tasks',
           'deploy_docker_service_celery.tasks', 'deploy_k8s_master_celery.tasks',
           'deploy_k8s_network_celery.tasks', 'deploy_k8s_node_celery.tasks',
           ]
# 每个worker执行了多少任务就会死掉，默认是无限的,释放内存
worker_max_tasks_per_child = 50

# 任务结果保存时间
worker_task_result_expires = 60 * 60 * 2

# 非常重要,有些情况下可以防止死锁
worker_force_execv = True

# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
worker_disable_rate_limits = True

# 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
worker_result_serializer = "json"

# CELERY_TASK_DEFAULT_QUEUE = "default" # 默认队列
worker_task_default_queue = "default"

task_queues = (
    Queue("default", routing_key="default"),
    Queue("base", routing_key="base.#"),
)

task_routes = {
    # res = tasks.test.apply_async(queue='default', routing_key='default')
    # 以上如果指定队列执行，则下列指定方式失效
    "test": {'queue': 'base', 'routing_key': 'base.info'},
    # "test1": {'queue': 'base', 'routing_key': 'base.test'},
}
# 定义默认队列和默认的交换机routing_key
task_default_queue = 'default'
task_default_exchange = 'default'
task_default_routing_key = 'default'

# 设置时区，默认UTC
timezone = 'Asia/Shanghai'
