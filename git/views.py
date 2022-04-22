from django.http import JsonResponse
from config import read_config as rc
import gitlab,os,json

#登录
def login(url,token):
    session = gitlab.Gitlab(url, token)
    return session

#获取该用户下的所有项目
def get_project_id(session,project_name):
    project_id = session.projects.list(search=project_name)
    for i in project_id:
        return i.id

#获取单个项目内信息
def get_project_info(session,project_id):
    project_info = session.projects.get(project_id)
    return project_info

#获取项目内分支信息
def get_project_branch(project_info):
    branch = project_info.branches.list()
    branch_list = []
    for i in branch:
        branch_list.append(i.name)
    return branch_list

#获取项目内tags信息
def get_project_tags(project_info):
    tags = project_info.tags.list()
    tags_list = []
    for i in tags:
        tags_list.append(i.name)
    return tags_list

#pull代码
def clone_cmd(http_url_to_repo,project_name,project_branch,project_tags,token):  #传入git_url下载地址、项目名称、项目分支或者项目tags
    path=os.getcwd().replace("\\","/")
    git_workspace=path+"/git/git_space/"
    project_workspace=path+"/git/git_space/"+project_name
    os.system('rm -rf '+project_workspace)  #删除目录，用于新建,这个方法无法删除隐藏文件，还需修改
    if os.path.exists(project_workspace) == True:
        os.removedirs(project_workspace)
    if os.path.exists(git_workspace) == False:
        os.makedirs(git_workspace)
    # os.chdir(git_space)   #切换至目录
    http_url_to_repo=http_url_to_repo.split('//')
    if project_branch is None:
        git_cmd = "git clone --branch " + str(project_tags) + " " + str(http_url_to_repo[0]) + "//" + str(token) + "@" + str(http_url_to_repo[1]) + " " + str(project_workspace)
    elif project_tags is None:
        git_cmd = "git clone -b " + str(project_branch) + " " + str(http_url_to_repo[0]) + "//" + str(token) + "@" + str(http_url_to_repo[1]) + " " + str(project_workspace)
    print("git clone address: {0}".format(git_cmd))
    os.system(git_cmd)
    # os.chdir(path)

#入口，获取branch及tags返回前端
def project(request):
    if request.method == "POST":  #获取git_url、token、project_name,git_url为url/不带project项目名称(三级域名)
        text = json.loads(request.body)
        # url = text.get('url')  #这个参数后续可以写到配置文件内
        # token = text.get('token') #这个参数后续可以写到配置文件内
        url = rc.read_config('git','git_url')
        token = rc.read_config('git','git_token')
        project_name = text.get('project_name') #仓库内参数不可以重名，不然会出问题
        session = login(url,token)
        project_id = get_project_id(session,project_name)
        project_info = get_project_info(session,project_id)
        http_url_to_repo = project_info.http_url_to_repo  #git clone下载地址
        project_branch = get_project_branch(project_info)
        project_tegs = get_project_tags(project_info)
        #返回数据
        data={"project_name":project_name,"http_url_to_repo":http_url_to_repo,"project_branch":project_branch,"project_tegs":project_tegs}
        return JsonResponse(data)

#入口，执行clone操作
def clone(request):
    text = json.loads(request.body)  #前端返回project方法放回的值
    http_url_to_repo = text.get('http_url_to_repo')
    project_name = text.get('project_name')
    project_branch = text.get('project_branch')
    project_tags = text.get('project_tags')
    token = rc.read_config('git','git_token')
    # token = text.get('token')
    clone_cmd(http_url_to_repo,project_name,project_branch,project_tags,token)
    data={"status":"ok"}
    return JsonResponse(data)
    #后续可添加接收脚本等操作