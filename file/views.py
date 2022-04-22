from django.shortcuts import HttpResponse,render,redirect
from django.http import StreamingHttpResponse
import os

def upload(request):
    if request.method == "GET":
        return render(request,'index.html')
    elif request.method == "POST":
        # 从请求的files中获取上传文件的文件名，file为html页面typ e =file类型的input的name
        filename = request.FILES['upload_file'].name
        if os.path.exists("file/file_space") == False:
            os.mkdir("file/file_space")
        with open("file/file_space"+"/"+filename,'wb') as  f:
            # 从上传的文件中一点一点的读
            for chunk in request.FILES['upload_file'].chunks():
                f.write(chunk)
        return redirect('/file/listfile')

def listfile(request):
    if request.method == "GET":
        file_path="file/file_space/"
        list_file = os.listdir(file_path)
        return render(request,"listfile.html",{'list_file':list_file})


def download(request,a1):
    if request.method == "GET":
        filename='file/ile_space/'+a1
        file_path = os.path.join(filename)  # 下载文件的绝对路径
        if not os.path.isfile(file_path):  # 判断下载文件是否存在
            return HttpResponse("Sorry but Not Found the File")
        def file_iterator(file_path, chunk_size=512):
            with open(file_path, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        try:
            # 设置响应头
            # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
            response = StreamingHttpResponse(file_iterator(file_path))
            # 以流的形式下载文件,这样可以实现任意格式的文件下载
            response['Content-Type'] = 'application/octet-stream'
            # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        except:
            return HttpResponse("Sorry but Not Found the File")
        return response


