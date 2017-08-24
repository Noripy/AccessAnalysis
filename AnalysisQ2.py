import re
import os

timeZoneTotal = {'00': 0, '01': 0,'02': 0, '03': 0, '04': 0,'05': 0, '06': 0, '07': 0,'08': 0, '09': 0, '10': 0,'11': 0, '12': 0,'13': 0, '14': 0,'15': 0, '16': 0,'17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,'23': 0} #時間帯ごと('00', '01', '02',...,'23'の順)でアクセス数の集計結果を取る.
remoteHostTotal = {}

RemoteHostPattern = re.compile("((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))")
TimePattern = re.compile("(\d{1,2})/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/(\d{1,4}):(\d{2}):(\d{2}):(\d{2})")
#月は英語の頭三文字(Jan/Feb/Mar/Apr/May/Jun/Jul/Aug/Sep/Oct/Nov/Dec)

fileIndex = 1

def TimeZoneReport(result):
    print('各時間帯毎のアクセス件数')
    for i in range(len(timeZoneTotal)):
        if i == 0:
            print(str(i)+'時: '+ str( result['00'] )+'件')
        elif i <= 9:
            print(str(i)+'時: '+ str( result['0'+str(i)] )+'件')
        else:
            print(str(i)+'時: '+ str( result[str(i)] )+'件')
    print()

def RemoteHostReport(result):
    print('リモートホスト別のアクセス件数')
    for k in result.keys():
        print(k+': '+str(result[k]) +'件')

while os.path.exists('./access'+str(fileIndex)+'.log'):
    for line in open('access' + str(fileIndex)+ '.log', 'r'):
        #print(line)
        rm_result = RemoteHostPattern.search(line)#リモートホスト情報抽出
        if rm_result is not None:
            #print(m)
            RemoteHostAddress = rm_result.group(1)
            #以下のif-else文でリモートホスト別のアクセス件数の集計
            if RemoteHostAddress in remoteHostTotal:
                remoteHostTotal[RemoteHostAddress] += 1
            else:
                remoteHostTotal[RemoteHostAddress] = 1
    
        date_result = TimePattern.search(line)#日付情報抽出
        if date_result is not None:
            day, month, year, hour, minute, second = date_result.groups()
            #print('year:'+ str(year) + ' month:'+ str(month) + ' day:'+ str(day) + ' hour:'+ str(hour) + ' minute:'+ str(minute) + ' second:'+ str(second))
            timeZoneTotal[str(hour)] += 1 #時間帯ごとに集計
    fileIndex += 1

TimeZoneReport(timeZoneTotal)
RemoteHostReport(remoteHostTotal)

