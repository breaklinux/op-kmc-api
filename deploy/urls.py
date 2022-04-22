from deploy.deploy_kernel_upgrade_celery import views as k8s_os_system_upgrade
from deploy.deploy_k8s_base_celery import views as k8s_base_init
from deploy.deploy_docker_service_celery import views as k8s_deploy_docker
from deploy.deploy_k8s_master_celery import views as k8s_master
from deploy.deploy_k8s_network_celery import views as k8s_cni
from deploy.deploy_k8s_node_celery import views as k8s_node
from deploy import views as k8s_deploy
from django.urls import path

urlpatterns = [
    path('os_upgrade', k8s_os_system_upgrade.kernelUpgrade),
    path('k8s_init', k8s_base_init.k8sInit),
    path('deploy_docker', k8s_deploy_docker.dockerService),
    path('k8s_master', k8s_master.k8sMaster),
    path('k8s_cni', k8s_cni.k8sNetwork),
    path('k8s_node', k8s_node.k8sNode),
    path('k8s_deploy' ,k8s_deploy.k8sDeploy)
]