from pygame.locals import *
import pygame
import sys
pygame.init()    # Pygameを初期化
screen = pygame.display.set_mode((400, 330))    # 画面を作成，必要
pygame.display.set_caption("MOETAIJIN")    # タイトルを作成
FPS=60####First Parson SHooooting
clock = pygame.time.Clock()

class Chara:
    def __init__(self,NAME,SPEC,SEX,CHP,MHP,CST,MST,CMP,MMP,AC,AGI,REGI,ATK,DEX,KICK,
    STAN,STOP,POTD,TATE,TECH,STAT,ATTK): # 属性に値を一括で設定するメソッドを定義
        self.NAME = NAME #1名前
        self.SPEC = SPEC #2種族
        self.SEX  = SEX  #3性別
        self.CHP  = CHP  #4現在のHP
        self.MHP  = MHP  #5最大HP
        self.CST  = CST  #6carentST
        self.MST  = MST  #7最大スタミナ
        self.CMT  = CMP  #8現在のMP
        self.MMP  = MMP   #9最大マナ
        self.AC   = AC   #10アーマークラス
        self.AGI  = AGI  #11回避力
        self.REGI = REGI #12呪文抵抗力
        self.ATK  = ATK  #13攻撃力
        self.DEX  = DEX  #14命中力
        self.KICK = KICK #15キック力

        self.STAN = STAN #残りスタン時間
        self.STOP = STOP #残り硬直
        self.POTD = POTD #POTdelay
        self.TATE = TATE #残り防御時間
        self.TECH = TECH #出している技
        self.STAT = STAT #状態 FREE,TATE,ATTK,STAN,STOP,DEAD
        self.ATTK = ATTK #attk当てるまで


#####                 1       2      3    4    5    6    7    8    9   10   11   12   13   14   15
#####              NAME    SPEC    SEX  CHP  MHP  CST  MST  CMP  MMP   AC  AGI REGI  ATK  DEX KICK
Pla1 = Chara("haemitsu", "PAND","FEME", 360, 360, 280, 280,  20,  20, 150,   0,  90, 100, 100, 100,
                0,0,0,0,"","FREE",-1) # はえみつ
Pla2 = Chara("sudetoke", "COGU","MALE", 315, 315, 250, 250,  30,  30, 150,   0,  90, 100, 100, 100,
                0,0,0,0,"","FREE",-1) # 素手刀剣


class Tech:
    def __init__(self, ID,Ndelay,Nstart,Name,Stmn, Dmg, Delay,Startup,Stop,Type): # 属性に値を一括で設定するメソッドを定義
        self.ID =ID
        self.Ndelay = Ndelay
        self.Nstart = Nstart
        self.Name   = Name
        self.Stmn   = Stmn
        self.Dmg = Dmg
        self.Delay = Delay
        self.Startup = Startup
        self.Stop = Stop
        self.Type = Type

P1TECHS=[
        #Player1
        #####        Nd Ns              Name stmn Dmg Delay Start Stop   Type
            Tech(0,0,-1,"      殴叩       ",  0,1.0, 200, 60,   120,"ATTK"), # 新しいインスタンスを作成
            Tech(1,0,-1,"  シールド ガード  ", 10,0.0, 240, 20,    40,"TATE"), # 新しいインスタンスを作成
            Tech(2,0,-1,"チャージド ブラント",  15,1.2, 600,100,   200,"BRAK"), # 新しいインスタンスを作成
]
P2TECHS=[
            #Player2
            #####        Nd Ns              Name stmn Dmg Delay Start Stop   Type
            Tech(0,0,-1,"      突刺      ",  0,1.0, 300,  60,   100,"ATTK"), # 新しいインスタンスを作成
            Tech(1,0,-1,"  シールドガード  ",  10,0.0, 240,  20,   40,"TATE"), # 新しいインスタンスを作成
            Tech(2,0,-1,"チャージド スラッシュ",15,1.2, 300,  60,  100,"BRAK"), # 新しいインスタンスを作成
]

#関数
def timespend():
    Pla1.STOP-=1
    Pla2.STOP-=1
    Pla1.TATE-=1
    Pla2.TATE-=1
    Pla1.ATTK-=1
    Pla2.ATTK-=1
    Pla1.STAN-=1
    Pla2.STAN-=1
    for i in P2TECHS:
        i.Ndelay-=1
        i.Nstart-=1
    for i in P1TECHS:
        i.Ndelay-=1
        i.Nstart-=1

def techstart(Pla,Tech):
    Pla.STOP=Tech.Stop
    Tech.Ndelay=Tech.Delay
    Tech.Nstart=Tech.Startup
    Pla.TECH=Tech.Name
    Pla.CST-=Tech.Stmn

def attack(Pla,Tech):
    if Pla.STAT=="FREE" and Tech.Ndelay < 0:
        techstart(Pla,Tech)
        Tech.Nstart=-1
        Pla.STAT="ATTK"
        Pla.ATTK=Tech.Startup
def siruga(Pla,Tech):
    if (Pla.STAT=="FREE" or Pla.STAT=="ATTK") and Tech.Ndelay < 0:
        techstart(Pla,Tech)
        Pla.STAT="TATE"
        Pla.ATTK=-1
        Tech.Nstart=-1
        Pla.TATE=Tech.Startup

def tecnich(Pla,Tech):
    if Pla.STAT=="FREE" and Tech.Ndelay<0:
        Pla.STAT="TECH"
        techstart(Pla,Tech)

def status(Pla):
    if Pla.CHP<0:
        Pla.STAT="DEAD"
    elif Pla.STOP <= 0 and Pla.STAN <= 0:
        Pla.STAT="FREE"
        Pla.TECH=""
    elif Pla.STAN>0:
        Pla.STAT="STAN"
    elif Pla.STAT=="ATTK":
        pass
    elif Pla.TATE>0:
        Pla.STAT="TATE"
    else:
        Pla.STAT="TECH"

def bougyo(Pla,Opp,TECHS):
    for t in TECHS:
        if t.Nstart == 0:
            if Opp.TATE>0:
                if t.Type=="BRAK":
                    Opp.CHP-=Pla.ATK*t.Dmg
                    Opp.STAN=150
                else:
                    Opp.Stmn+=10
            else:
                Opp.CHP-=Pla.ATK*t.Dmg
#処理ループ
def main():
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # ESCキーならスクリプトを終了
                    pygame.quit()
                    sys.exit()
                    print("esc")
                if event.key == K_1:
                    attack(Pla1,P1TECHS[0])
                if event.key == K_2:
                    siruga(Pla1,P1TECHS[1])
                if event.key == K_3:
                    tecnich(Pla1,P1TECHS[2])
                if event.key == K_8:
                    attack(Pla2,P2TECHS[0])
                if event.key == K_9:
                    siruga(Pla2,P2TECHS[1])
                if event.key == K_0:
                    tecnich(Pla2,P2TECHS[2])
                break
        #####
        timespend()

        #####防御判定
        if Pla1.ATTK == 0:
            if Pla2.TATE>0:
                Pla2.CST+=10
            else:
                Pla2.CHP-=Pla1.ATK*P1TECHS[0].Dmg
        if Pla2.ATTK == 0:
            if Pla1.TATE>0:
                Pla1.CST+=10
            else:
                Pla1.CHP-=Pla2.ATK*P2TECHS[0].Dmg

        #####他の技防御判定

        bougyo(Pla1,Pla2,P1TECHS)
        bougyo(Pla2,Pla1,P2TECHS)

        ######ステータス更新
        status(Pla2)
        status(Pla1)

        ######表示

        print("\033[2J"+"\033[H"+Pla1.NAME+"\n"
        +"HP{}/{},ST{}/{}".format(Pla1.CHP,Pla1.MHP,Pla1.CST,Pla1.MST)+"\n"
        +str(Pla1.STAT)+"\n"
        +str(Pla1.TECH)+"\n"
        +"---------------------------"+"\n"
        +Pla2.NAME+"\n"
        +"HP{}/{},ST{}/{}".format(Pla2.CHP,Pla2.MHP,Pla2.CST,Pla2.MST)+"\n"
        +str(Pla2.STAT)+"\n"
        +str(Pla2.TECH),end="")

        ######勝敗表示
        if Pla1.STAT=="DEAD" or Pla2.STAT=="DEAD":
            print("\n"+"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeend")
            if Pla1.STAT=="DEAD":
                print(Pla2.NAME+"win!!!")
            elif Pla2.STAT=="DEAD":
                print(Pla1.NAME+"win!!!")
            else:
                print("DOLOOOOOO")
            pygame.quit()
            sys.exit()

        ####フレーム管理
        clock.tick(FPS)

if __name__ == '__main__':
    main()
