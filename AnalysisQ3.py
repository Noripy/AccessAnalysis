import re
import os
import time
from datetime import datetime

timeZoneTotal = {'00': 0, '01': 0,'02': 0, '03': 0, '04': 0,'05': 0, '06': 0, '07': 0,'08': 0, '09': 0, '10': 0,'11': 0, '12': 0,'13': 0, '14': 0,'15': 0, '16': 0,'17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,'23': 0} #時間帯ごと('00', '01', '02',...,'23'の順)でアクセス数の集計結果を取る.
remoteHostTotal = {}

RemoteHostPattern = re.compile("((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))")
TimePattern = re.compile("(\d{1,2})/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/(\d{1,4}):(\d{2}):(\d{2}):(\d{2})")
#月は英語の頭三文字(Jan/Feb/Mar/Apr/May/Jun/Jul/Aug/Sep/Oct/Nov/Dec)
fileIndex = 1

monthMap = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

period = ''

def TimeZoneReport(result):
    print(period+'における各時間帯毎のアクセス件数')
    for i in range(len(timeZoneTotal)):
        if i == 0:
            print(str(i)+'時: '+ str( result['00'] )+'件')
        elif i <= 9:
            print(str(i)+'時: '+ str( result['0'+str(i)] )+'件')
        else:
            print(str(i)+'時: '+ str( result[str(i)] )+'件')
    print()

def RemoteHostReport(result):
    print(period+'におけるリモートホスト別のアクセス件数')
    for k in result.keys():
        print(k+': '+str(result[k]) +'件')

#存在する月日を判定する
def checkDate(month, day):
    if day < 29:
        return True
    elif day == 29 or day == 30:
        if month == 2:
            return False
        else:
            return True
    else:#day == 31
        if month in {2, 3, 4, 6, 9, 11}:
            return False
        else:
            return True

print('期間の指定をします.(年, 月, 日の順に入力)\n')
print('期間開始の日付:')

yStart = input('期間開始の年は?(4桁までの整数を入力): ')
while True:
    if yStart.isdigit() and int(yStart) < 10000:
        print("OK!")
        break
    else:
        print("年が不適です.")
        yStart = input('期間開始の年は?(4桁までの整数を入力): ')

mStart = input('期間開始の月は?(1〜12の整数を入力): ')
while True:
    if mStart.isdigit() and 0 < int(mStart) < 13:
        print("OK!")
        break
    else:
        print("月が不適です.")
        mStart = input('期間開始の月は?(1〜12の整数を入力): ')

dStart = input('期間開始の日は?(1〜31の整数を入力): ')

while True:
    if dStart.isdigit() and 0 < int(dStart) < 32 :
        if checkDate(int(mStart), int(dStart)):
            print("OK!")
            break
        else:
            print(str(mStart)+"月"+str(dStart)+"日は存在しません.")
            dStart = input('期間開始の日は?(1〜31の整数を入力): ')
    else:
        print("日が不適です.")
        dStart = input('期間開始の日は?(1〜31の整数を入力): ')
print('\n期間終了の日付:')

yEnd = input('期間終了の年は?(4桁までの整数を入力): ')
while True:
    if yEnd.isdigit() and int(yEnd) < 10000 and int(yStart) <= int(yEnd) :
        print("OK!")
        break
    else:
        print("年が不適です.")
        yEnd = input('期間終了の年は?(4桁までの整数を入力): ')

mEnd = input('期間終了の月は?(1〜12の整数を入力): ')
while True:
    if mEnd.isdigit() and 0 < int(mEnd) < 13:
        if int(yStart) == int(yEnd):
            if int(mEnd) >= int(mStart):
                print("OK!")
                break
            else:
                print("月が不適です.")#年は同じで開始の月よりも前の月だとやり直しにする.
                mEnd = input('期間終了の月は?(1〜12の整数を入力): ')
        else:#int(yStart) <= int(yEnd)は既に考慮されてるので, int(yStart) > int(yEnd).
            print("OK!")
            break
    else:
        print("月が不適です.")
        mEnd = input('期間終了の月は?(1〜12の整数を入力): ')

dEnd = input('期間終了の日は?(1〜31の整数を入力): ')
while True:
    if dEnd.isdigit() and 0 < int(dEnd) < 32 :
        if checkDate(int(mEnd), int(dEnd)):
            print("OK!")
            break
        else:
            print(str(mEnd)+"月"+str(dEnd)+"日は存在しません.")
            dEnd = input('期間終了の日は?(1〜31の整数を入力): ')
    else:
        print("日が不適です.")
        dEnd = input('期間終了の日は?(1〜31の整数を入力): ')

period = yStart+'/'+mStart+'/'+dStart+'から'+yEnd+'/'+mEnd+'/'+dEnd
print('\n期間を'+ period +'で集計を開始します.\n')

#tz = pytz.timezone('Asia/Tokyo')

sDateTime = datetime.strptime(yStart+'/'+mStart+'/'+dStart, '%Y/%m/%d')
sDateTime.isoformat() 

eDateTime = datetime.strptime(yEnd+'/'+mEnd+'/'+dEnd, '%Y/%m/%d')
eDateTime.isoformat()

StartEpochTime = time.mktime(sDateTime.timetuple())
EndEpochTime = time.mktime(eDateTime.timetuple())

while os.path.exists('./access'+str(fileIndex)+'.log'):
    for line in open('access' + str(fileIndex)+ '.log', 'r'):
        date_result = TimePattern.search(line)#日付情報抽出
        if date_result is not None:
            day, month, year, hour, minute, second = date_result.groups()
            targetDateTime = datetime(int(year), monthMap[month], int(day), int(hour), int(minute), int(second))
            targetDateTime.isoformat()
            TargetEpochTime = time.mktime(targetDateTime.timetuple())
            if StartEpochTime < TargetEpochTime < EndEpochTime:
                timeZoneTotal[str(hour)] += 1 #時間帯ごとに集計
        
                rm_result = RemoteHostPattern.search(line)#リモートホスト情報抽出
                if rm_result is not None:
                    RemoteHostAddress = rm_result.group(1)
                    #以下のif-else文でリモートホスト別のアクセス件数の集計
                    if RemoteHostAddress in remoteHostTotal:
                        remoteHostTotal[RemoteHostAddress] += 1
                    else:
                        remoteHostTotal[RemoteHostAddress] = 1
    
    fileIndex += 1

TimeZoneReport(timeZoneTotal)
RemoteHostReport(remoteHostTotal)

