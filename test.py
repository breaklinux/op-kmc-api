
import datetime
endTime = datetime.datetime.now() + datetime.timedelta(minutes=5)
result = {"Status":"aaaa"}
while True:
    if result['Status'] == "SUCCESS":
        print('add is ready  ! Status = %s' % result['Status'], result)
        break
    else:
        print('add NOT ready ! Status = %s' % result['Status'])
        if datetime.datetime.now() >= endTime:
           break
