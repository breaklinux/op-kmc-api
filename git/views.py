from django.http import JsonResponse
from config import read_config as rc
import gitlab,os,json

#��¼
def login(url,token):
    session = gitlab.Gitlab(url, token)
    return session

#��ȡ���û��µ�������Ŀ
def get_project_id(session,project_name):
    project_id = session.projects.list(search=project_name)
    for i in project_id:
        return i.id

#��ȡ������Ŀ����Ϣ
def get_project_info(session,project_id):
    project_info = session.projects.get(project_id)
    return project_info

#��ȡ��Ŀ�ڷ�֧��Ϣ
def get_project_branch(project_info):
    branch = project_info.branches.list()
    branch_list = []
    for i in branch:
        branch_list.append(i.name)
    return branch_list

#��ȡ��Ŀ��tags��Ϣ
def get_project_tags(project_info):
    tags = project_info.tags.list()
    tags_list = []
    for i in tags:
        tags_list.append(i.name)
    return tags_list

#pull����
def clone_cmd(http_url_to_repo,project_name,project_branch,project_tags,token):  #����git_url���ص�ַ����Ŀ���ơ���Ŀ��֧������Ŀtags
    path=os.getcwd().replace("\\","/")
    git_workspace=path+"/git/git_space/"
    project_workspace=path+"/git/git_space/"+project_name
    os.system('rm -rf '+project_workspace)  #ɾ��Ŀ¼�������½�,��������޷�ɾ�������ļ��������޸�
    if os.path.exists(project_workspace) == True:
        os.removedirs(project_workspace)
    if os.path.exists(git_workspace) == False:
        os.makedirs(git_workspace)
    # os.chdir(git_space)   #�л���Ŀ¼
    http_url_to_repo=http_url_to_repo.split('//')
    if project_branch is None:
        git_cmd = "git clone --branch " + str(project_tags) + " " + str(http_url_to_repo[0]) + "//" + str(token) + "@" + str(http_url_to_repo[1]) + " " + str(project_workspace)
    elif project_tags is None:
        git_cmd = "git clone -b " + str(project_branch) + " " + str(http_url_to_repo[0]) + "//" + str(token) + "@" + str(http_url_to_repo[1]) + " " + str(project_workspace)
    print("git clone address: {0}".format(git_cmd))
    os.system(git_cmd)
    # os.chdir(path)

#��ڣ���ȡbranch��tags����ǰ��
def project(request):
    if request.method == "POST":  #��ȡgit_url��token��project_name,git_urlΪurl/����project��Ŀ����(��������)
        text = json.loads(request.body)
        # url = text.get('url')  #���������������д�������ļ���
        # token = text.get('token') #���������������д�������ļ���
        url = rc.read_config('git','git_url')
        token = rc.read_config('git','git_token')
        project_name = text.get('project_name') #�ֿ��ڲ�����������������Ȼ�������
        session = login(url,token)
        project_id = get_project_id(session,project_name)
        project_info = get_project_info(session,project_id)
        http_url_to_repo = project_info.http_url_to_repo  #git clone���ص�ַ
        project_branch = get_project_branch(project_info)
        project_tegs = get_project_tags(project_info)
        #��������
        data={"project_name":project_name,"http_url_to_repo":http_url_to_repo,"project_branch":project_branch,"project_tegs":project_tegs}
        return JsonResponse(data)

#��ڣ�ִ��clone����
def clone(request):
    text = json.loads(request.body)  #ǰ�˷���project�����Żص�ֵ
    http_url_to_repo = text.get('http_url_to_repo')
    project_name = text.get('project_name')
    project_branch = text.get('project_branch')
    project_tags = text.get('project_tags')
    token = rc.read_config('git','git_token')
    # token = text.get('token')
    clone_cmd(http_url_to_repo,project_name,project_branch,project_tags,token)
    data={"status":"ok"}
    return JsonResponse(data)
    #���������ӽ��սű��Ȳ���