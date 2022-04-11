"""kmc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from deploy_kernel_upgrade_celery import views as k8s_os_system_upgrade
from deploy_k8s_base_celery import views as k8s_base_init
from deploy_docker_service_celery import views as k8s_deploy_docker
from deploy_k8s_master_celery import views as k8s_master
from deploy_k8s_network_celery import views as k8s_cni
from deploy_k8s_node_celecy import views as k8s_node
from django.urls import path, re_path, include

urlpatterns = [
   # url(r'^admin/', admin.site.urls),
   path('os_upgrade', k8s_os_system_upgrade.kernelUpgrade),
   path('k8s_init', k8s_base_init.k8sInit),
   path('deploy_docker', k8s_deploy_docker.dockerService),
   path('k8s_master', k8s_master.k8sMaster),
   path('k8s_cni', k8s_cni.k8sNetwork),
   path('k8s_node', k8s_node.k8sNode)
]
