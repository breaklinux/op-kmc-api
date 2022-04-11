import datetime

def runTime():
    print("时间",datetime.datetime.now())
    return datetime.datetime.now()


def runTimeCalculate(msg, startDeployTime, endDeployTime):
    """
    1.耗时时间计算(结束时间减去-开始时间)
    """
    calculate = (endDeployTime - startDeployTime).seconds / 1000
    print(str(msg) + str(calculate) + "秒")
    return calculate


