"""
 1.公共返回数据格式
"""

def kmc_Response(msg=None, token=None, taskId=None):
    if not token:
        data = {"code": 0, "message": msg, "data": {"token": "", "state": "false"}, "task_id": str(taskId)}
    else:
        data = {"code": 0, "message": msg, "data": {"token": token, "state": "true"}, "task_id": str(taskId)}
    return data
