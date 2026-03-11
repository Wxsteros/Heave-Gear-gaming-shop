import time
Name=[]
score=[]
Time_list=[]
Shooter=int(input('please enter quantity shooter :'))
for i in range(Shooter):
    player=input('player name : ')
    point=int(input('PTS : '))
    time_player=float(input('time score :'))
    Name.append(player)
    score.append(point)
    Time_list.append(time_player)  

#HIT FACTOR
Hit_FactorList = []
for i in range(Shooter):
    Hf = score[i] / Time_list[i]
    Hit_FactorList.append(Hf)

max_Hf = max(Hit_FactorList)

#stage point and stage percent
Stage_point = []
stage_percent = []
for Hf in Hit_FactorList:
    sp = Hf / max_Hf * 40
    Stage_point.append(sp)
    stage_percent.append(sp / 40 * 100)

#รวมข้อมูล shooter
Shooter_data_new = []
for i in range(Shooter):
    Shooter_data_old = [Name[i], score[i], Time_list[i], Hit_FactorList[i], Stage_point[i], stage_percent[i]]
    Shooter_data_new.append(Shooter_data_old)
#เรียงลำดับข้อมูล
def get_shooter_data(Shooter_tuple): #คือการสร้างฟังก์ชันเพื่อดึงข้อมูลจาก tuple มาใช้ในการเรียงลำดับ
    return Shooter_tuple[5] #เรียงลำดับจาก stage percent

Shooter_data_sorted = sorted(Shooter_data_new,key=get_shooter_data, reverse=True) #เรียงลำดับจาก stage percent มากไปน้อย

print('shotgun sunday training 2021')
print('condition 1')
print(time.strftime('%Y-%m-%d %H:%M:%S'))
print('{0:-<90}'.format(""))
print('{0:<4}{1:>10}{2:>12}{3:>18}{4:>14}{5:>14}{6:>16}'.format('NO.','PTS','TIME','COMPETITOR','Hit Factor','Stage Point','Stage Percent'))
print('{0:-<90}'.format(""))
N = 1
for s in Shooter_data_sorted:
    print('{0:<4}{1:>10}{2:>12.2f}{3:>14}{4:>14.2f}{5:>14.2f}{6:>16.2f}'.format(N, s[1], s[2], s[0], s[3], s[4], s[5]))
    N += 1
print('{0:-<90}'.format(""))