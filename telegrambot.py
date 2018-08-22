import random
import time
from pprint import pprint

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#KeyboarInterrupt

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

import joke
bot = telepot.Bot('token')

cardList=[["項鍊","戒指"],["手機","平板"],["玻璃杯","馬克杯"],["沙發","板凳"],["充電線","延長線"]
        ,["蛋餅","漢堡"],["瑪莎拉蒂","藍寶堅尼"],["便條紙","A4紙"],["耳環","髮夾"],["Iphon6","Iphone5"]
        ,["拖鞋","布鞋"],["雨傘","雨衣"],["外向","內向"],["躲避球","橄欖球"],["照相機","攝影機"]
        ,["辣椒","芥末"],["端午節","中秋節"],["高麗菜","花椰菜"],["雞絲飯","雞肉飯"],["海豹","海豚"]
        ,["蝴蝶","蜜蜂"],["牛奶","豆漿"],["鍵盤","滑鼠"],["學士","碩士"],["滑板車","腳踏車"]
        ,["塑膠袋","垃圾袋"],["拉麵","泡麵"],["手指頭","腳指頭"],["樹葉","樹枝"],["海王星","冥王星"]
        ,["地球","火星"],["牙齒","牙套"],["牛","羊"],["天使","惡魔"],["公車","汽車"]
        ,["超級市場" ,"傳統市場"],["醫生","護士"],["冷氣","暖氣"],["飲料","啤酒"],["口香糖","薄荷糖"]
        ,["瓜子","花生"],["高鐵","地鐵"],["鯊魚","鱷魚"],["貓咪","小狗"],["裙子","熱褲"]
        ,["國民黨","民進黨"],["氣球","泡泡"],["內地人","台灣人"],["陰廟","佛壇"],["真菌","細菌"]
        ,["檸檬汁","西瓜汁"],["畫展","照片"],["甜甜圈","洋蔥圈"],["飛鏢","飛盤"],["警察","軍人"]
        ,["女神","死神"],["鍋貼","餃子"],["肯德基","麥當勞"],["交叉點","轉捩點"],["持之以恆","鍥而不捨"]
        ,["莫札特","貝多芬"],["Microsoft_Word","Microsoft_Excel"],["蜈蚣","馬陸"],["蜘蛛人","蝙蝠俠"],["鐵鎚","鐵釘"]
        ,["白血球","血小板"],["左心室","地下室"],["河馬","斑馬"],["電梯","階梯"],["玩命關頭","生死關頭"]
        ,["北極圈","北極熊"],["升糖素","胰島素"],["變形蟲","三葉蟲"],["萬有引力","地心引力"],["牙刷","牙膏"]
        ,["衛生紙","衛生棉"],["北科","台科"],["地縛靈","土地公"],["鬼娃娃","洋娃娃"],["章魚","烏賊"]
        ,["果糖","蔗糖"],["鹽巴","味精"],["白飯","麵食"],["一心二用","三心二意"],["孫悟空","沙悟淨"]
        ]
class Player():
    def __init__(self,name,id):
        self.name=name
        self.id=id
        self.card=""
        self.undercover=False
        self.owner=False
        self.voteRight=True
        self.beenVoted=0
        self.hasreport=[]
        self.bereport = 0
    def setVoteRightTrue(self):
        self.voteRight = True
    def setVoteRightFlase(self):
        self.voteRight = False
    def setCard(self,card):
        self.card=card
    def setUndercover(self):
        self.undercover=True
    def setowner(self):
        self.owner=True
    def isUndercover(self):
        return self.undercover
    def isowner(self):
        return self.owner
    def getId(self):
        return self.id
    def getCard(self):
        return self.card
    def getName(self):
        return self.name
    def canVote(self):
        return self.voteRight
    def plusVoted(self):
        self.beenVoted+=1
    def getBeenVoted(self):
        return self.beenVoted
    def setBeenVoted(self,Num):
        self.beenVoted=Num
#是owner嗎?
def isowner(msg,username):
    if players[username].isowner():
        return True
    else:
        return False
#you out!
def deleteplayer(chatID,username):
    global howManyPlayer
    global howmanyundercover
    usernamedata.remove(username)
    howManyPlayer = howManyPlayer - 1
    if players[username].isUndercover() and  players[username].isowner():
        howmanyundercover = howmanyundercover - 1
        bot.sendMessage(chatId, '抓到臥底了喔!')
        Index = random.choice(usernamedata)
        players[Index].setowner()
        bot.sendMessage(chatId, "owner88了喔,"+str(Index)+'變owner')
    elif players[username].isUndercover():
        howmanyundercover = howmanyundercover - 1
        bot.sendMessage(chatId, '抓到臥底了喔!')
    elif players[username].isowner():
        Index = random.choice(usernamedata)
        players[Index].setowner()
        bot.sendMessage(chatId, "owner88了喔,"+str(Index)+'變owner')
    else :
        bot.sendMessage(chatId, username+'   say goodbyeeee~')
    del players[username]
    HintRound = True
#printoutcome and reset
def dealWithHints(msg,index):
    global Hints
    global errorHints
    global usernamedata
    global HinterList
    global thisRoundHints
    if msg['text'] in Hints:
        bot.sendMessage(msg['chat']['id'],str(HinterList[index]+'給的提示已被說過囉~失去提示機會啦~'))
        if HinterList[index] in errorHints.keys():errorHints[HinterList[index]]+=1
        else:errorHints[HinterList[index]] = 1
    else: Hints.append(msg['text'])
    thisRoundHints[HinterList[index]]=msg['text']
    printCurrentHint(msg,chatId)
def resetVotedRightTrue():
    for username in usernamedata:
        votePlayer = players[username]
        votePlayer.setVoteRightTrue()
def resetVotedRightFalse():
    for username in usernamedata:
        votePlayer = players[username]
        votePlayer.setVoteRightFlase()
def printCurrentHint(msg,chatId):
    String = ''
    errorString = ''
    global thisRoundHints
    global errorHints
    for hint in thisRoundHints.keys():
        String = String +'  '+ hint +'的提示:'+ thisRoundHints[hint] +'\n'
    for error in errorHints.keys():    
        errorString = errorString+'  '+error + str(errorHints[error])+'\n'
    bot.sendMessage(chatId,'大家給的提示:\n'+String+'\n\n錯誤提示累積結果:\n'+errorString)
    
def Hint(msg):
    chatId = msg['chat']['id']
    global usernamedata
    global can_hint
    global HinterList
    global index
#    global UnHintedPlayers
    if can_hint:
        if '@' + msg['from']['username'] not in HinterList:
            pass
        elif '@' + msg['from']['username'] not in usernamedata:
            index = (index+1) % len(HinterList)
            bot.sendMessage(chatId,'現在輪到'+str(HinterList[index])+'提供提示\n提示的格式:「/hint [提示內容]」')
        else:
            if '@' + msg['from']['username'] == str(HinterList[index]): 
                dealWithHints(msg,index)
                index = (index+1) % len(HinterList)
            else:
                bot.sendMessage(chatId,'現在不是你提示的時間喔!')
            if (index) % len(HinterList) == 0:
                can_hint = False
                showVoteButton(msg)
                thisRoundHints = {}
            else:bot.sendMessage(chatId,'現在輪到'+str(HinterList[index])+'提供提示\n提示的格式:「/hint [提示內容]」')
    else: bot.sendMessage(chatId,"嘖嘖，現在還不是給提示環節啦")


def printOutcome(chatId):
    global howManyPlayer
    global howmanyundercover
    global isEnd
    isEnd=True
    if howmanyundercover == 0:
        survive = ''
        bot.sendMessage(chatId, '臥底都被抓到啦!!')
        for i in range(len(usernamedata)):
            if players[usernamedata[i]].isUndercover():
                pass
            else:
                survive = survive + ' ' + str(usernamedata[i])
        bot.sendMessage(chatId, '正義勝利啦!!')
        bot.sendMessage(chatId, '存活:'+survive)

    elif howmanyundercover < (howManyPlayer - howmanyundercover):
        survive = ''
        for i in range(len(usernamedata)):
            if players[usernamedata[i]].isUndercover():
                pass
            else:
                survive = survive + ' ' + str(usernamedata[i])
        bot.sendMessage(chatId, '正義勝利啦!!')
        bot.sendMessage(chatId, '存活:'+survive)
    elif howmanyundercover >= (howManyPlayer - howmanyundercover):
        bot.sendMessage(chatId, '平民這樣也可以輸?!')
    printunder = ''
    for i in range(len(undercover)):
        printunder = printunder + ' ' + str(undercover[i])
    bot.sendMessage(chatId, '臥底有:'+printunder)
    bot.sendMessage(chatId, "owner 輸入/newgame 開始新遊戲")
    exit()
#產生新遊戲
def newgame(msg):####
    global canjoin
    global canNewgame
    global isEnd
    global thisRoundHints
    thisRoundHints.clear()
    chatId =msg['chat']['id'] 
    bot.sendMessage(chatId,'New game starts!')
    canjoin = True
    canNewgame = False
    isEnd = False


'''def newgame(msg):
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    global howManyPlayer
    global howmanyundercover
    if len(players) != 0 :
        if username not in usernamedata:
            bot.sendMessage(chatId, "已建立新局,輸/join就好了喔")
        elif isowner(msg,username):
            del usernamedata[:]
            del undercover[:]
            players.clear()
            howManyPlayer = 0
            howmanyundercover = 0
            canjoin = True
            bot.sendMessage(chatId, "已經開始新的遊戲！ 用 /join 加入並用 /start 開始遊戲")
        else:
            bot.sendMessage(chatId,"想幹嘛?")
    else:
        bot.sendMessage(chatId, "已經開始新的遊戲！ 用 /join 加入並用 /start 開始遊戲")'''
#加入遊戲 建構玩家加入玩家列表
'''def join(msg):
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    if username in players:
        bot.sendMessage(chatId, '你加過了,87')
    else:
        global howManyPlayer 
        howManyPlayer += 1
        player = Player(str(msg['from']['first_name'])+str(msg['from']['last_name']),msg['from']['id'])
        if len(players) == 0:
            player.setowner()
        players[username] = player
        usernamedata.append(username)
        String = str(msg['from']['first_name'])+" 已加入遊戲"
        bot.sendMessage(chatId, String)
        String = "現在有"+str(howManyPlayer)+"位玩家"+',owner開始請/start'
        bot.sendMessage(chatId,String)
#開始遊戲 決定誰是臥底 發卡'''
'''def start(msg):
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    if username not in usernamedata:
        bot.sendMessage(chatId, "要先輸/join喔")
    elif not isowner(msg,username):
        bot.sendMessage(chatId,"你誰啊")
    elif len(players) < 2:
        bot.sendMessage(chatId,"在等等吧~~這樣不好玩")
    elif canjoin == False:
        bot.sendMessage(chatId,"開始了喔")
    else:
        randomUndercover()
        assignCard(players)
        sendCardMesaage(players)
        bot.sendMessage(chatId,"遊戲開始!")
        canjoin = False
        HintRound = True
        bot.sendMessage(chatId,'現在請大家說出自己的提示')
        #go(chatId)'''
def WhosMole(msg):###呼叫遊戲
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    global howManyPlayer
    global howmanyundercover
    global usernamedata
    global undercover
    global players
    global canStart
    global thisRoundHints
    if len(players) != 0 :
        if canStart and username == usernamedata[0]:###判斷是否能開始遊戲
            bot.sendMessage(chatId, 'Hi!', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/start"), KeyboardButton(text="/gameRule")]]
                                ))
        else: 
            if canjoin and username not in usernamedata:###判斷是否能加入遊戲
                bot.sendMessage(chatId, 'Welcome to Who\'s mole game', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/join"), KeyboardButton(text="/gameRule")]]))
            elif isowner(msg,username)and canNewgame:###判斷使否為owner且是否能開始遊戲(在建立newgame到start之間不能再newgame)
                del usernamedata[:]
                del undercover[:]
                thisRoundHints.clear()
                players.clear()
                howManyPlayer = 0
                howmanyundercover = 0
                bot.sendMessage(chatId, 'Welcome to Who\'s mole game', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/newgame"), KeyboardButton(text="/gameRule")]]
                                ))
                setOwner(msg)###因為owner不用再輸入一次/join，所以在這建立所需資訊
            else:###遊戲已啟動後，呼叫WhosMole只會有gameRule的選項
                bot.sendMessage(chatId, 'Hi!',reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/gameRule")]]))
    elif len(players) == 0:
        bot.sendMessage(chatId, 'Welcome to Who\'s mole game', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/newgame"), KeyboardButton(text="/gameRule")]]
                        ))
        setOwner(msg)###因為owner不用再輸入一次/join，所以在這建立所需資訊

def setOwner(msg):###owner建立資訊的地方
    username = '@' + msg['from']['username']
    global howManyPlayer
    global players
    global usernamedata
    howManyPlayer += 1
    player = Player(str(msg['from']['first_name']),msg['from']['id'])    
    player.setowner()
    players[username] = player
    usernamedata.append(username)
    print('usernamedata:',usernamedata)
    print('players:',players)

def join(msg):###一般玩家加入遊戲的function，玩家數超過4位時，便可以啟動/start
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    if username in players:
        bot.sendMessage(chatId, '你加過了,87')
    else:
        global howManyPlayer
        howManyPlayer += 1
        player = Player(str(msg['from']['first_name']),msg['from']['id'])        
        players[username] = player
        usernamedata.append(username)
        String = str(msg['from']['first_name'])+" 已加入遊戲"
        bot.sendMessage(chatId, String)
        String = "現在有"+str(howManyPlayer)+"位玩家"
        bot.sendMessage(chatId,String)
        if len(usernamedata) >= 4:###玩家數超過4位時，便可以啟動/start
            global canStart
            String = "已達遊戲最低人數,owner可以輸入「WhosMole」來開始遊戲!"
            bot.sendMessage(chatId,String)
            canStart = True
        print(usernamedata)
        
def start(msg):####修正
    global canStart
    global HintRound
    global canNewgame
    global usernamedata
    global HinterList
    global index
    global can_hint
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    if username not in usernamedata:
        bot.sendMessage(chatId, "要先輸'WhosMole'或'/join'喔")
    elif not isowner(msg,username):
        bot.sendMessage(chatId,"你誰啊")
    elif len(players) < 4:
        bot.sendMessage(chatId,"在等等吧~~這樣不好玩")
    elif canjoin == False:
        bot.sendMessage(chatId,"開始了喔")
    else:
        randomUndercover()
        assignCard(players)
        sendCardMesaage(players)
        bot.sendMessage(chatId,"遊戲開始!")
        canjoin = False
        can_hint = True
        canNewgame = True
        canStart = False
        
        HinterList = usernamedata
        bot.sendMessage(chatId,'現在進入到提示環節~')
        bot.sendMessage(chatId,'首先輪到'+str(HinterList[index])+'提供提示\n提示的格式:「/hint [提示內容]」')
#        go(chatId)
        
 
def gameRule(msg):###遊戲規則講解
    
    bot.sendMessage(chatId,'【誰是臥底-遊戲規則】\n'
                    +'此遊戲會將參加者分為兩隊，並且BOT會各自私訊題目\n'
        +'在不公布答案的條件下，參加者輪流提示自己的題目\n'
        +'並判斷究竟自己是臥底方還是平民方，在投票時將敵方投票出局。\n'
        +'若自己是臥底，努力生存到臥底方人數和平民方人數一樣時便能獲勝;\n'
        +'如果是平民方，將全數臥底方投票出局便能獲勝。')  
     
#指令控制中心
def handle(msg):
    global chatId
    global canNewgame
    chatId = msg['chat']['id']
    pprint(msg)
    username = '@' + msg['from']['username']
    massage = msg['text'].split(' ')
    if( massage[0]=='WhosMoleGame'):####修正
        WhosMole(msg)
        print("hi")
    if not canjoin and (username not in players):
        pass
    else:
        if( massage[0]=="/join"):
            join(msg)
        elif( massage[0]=='/newgame'and canNewgame):
            newgame(msg)
        elif( massage[0]=='/start'):
            start(msg)
        elif( massage[0]=='/help'):
            help(msg)
        elif( massage[0]=='/help@WhoIsUndercoverBot'):
            help(msg)
        elif ( massage[0]=='/hint'):
            Hint(msg)
        #elif(len(massage)==2 and massage[0]=='/vote' ):
        # ↑↑ 上面的elif是原本的程式碼,因為要嘗試讓def haha運行,所以改成下面的程式
        elif( massage[0]=='/haha' ):
            targetName=massage[0]
            showVoteButton(msg)
            #vote(msg['chat']['id'],username,targetName)
            # ↑↑ 原本def vote的資料
        elif(len(massage)==2 and massage[0]=='/report' ):
            targetName=massage[1]
            report(msg,msg['chat']['id'],targetName,username)
        elif ('/笑話' in msg['text']):
            Data = joke.main(msg)
            bot.sendMessage(msg['chat']['id'],random.choice(Data))
        elif( massage[0]=='/voteStatus'):
            printVote(msg['chat']['id'])
        elif( massage[0]=='haha'):
            bot.sendMessage(msg['chat']['id'],"笑屁")
        elif( massage[0]=='你可以滾了'):
            bot.sendMessage(msg['chat']['id'],"http://i.imgur.com/rAVzont.jpg")
        elif( massage[0]=='傻眼'):
            bot.sendMessage(msg['chat']['id'],"https://i.imgur.com/iU6V8Ja.png")
        elif(massage[0]=='@WhoIsUndercoverBot'):
            bot.sendMessage(msg['chat']['id'],"幹嘛（‘·д·）")
        elif(massage[0]=='問號'):
            bot.sendMessage(msg['chat']['id'],"http://i.imgur.com/friaaLF.jpg")
        elif(massage[0]=="test"):
            printOutcome(msg['chat']['id'])
        elif(massage[0]=="/gameRule"):
            gameRule(msg)
def checkName(String):
    if(String in usernamedata):
        return True
    else:
        return False
#發卡
def assignCard(players):
    cardList1 = random.choice(cardList)
    for player in players:
        if players[player].isUndercover():
            players[player].setCard(cardList1[0])
        else :
            players[player].setCard(cardList1[1])
#隨機抽臥底
def randomUndercover():
    global howManyPlayer
    global howmanyundercover
    howmanyundercover = howManyPlayer // 4
    Index = random.sample(usernamedata,howmanyundercover)
    for i in range(len(Index)):
        players[Index[i]].setUndercover()
        undercover.append(Index[i])
#傳送
def sendCardMesaage(players):
    for player in players:
        bot.sendMessage(players[player].getId(),players[player].getCard())
def status(msg):
    global howManyPlayer
    chatId=msg['chat']['id']
    String = "現在有"+str(howManyPlayer)+"位玩家"
    bot.sendMessage(chatId,String)
    allplayer = ''
    for player in players:
        allplayer = allplayer +' '+ player
    bot.sendMessage(chatId,'玩家有:'+ allplayer)
#    String = "臥底是"+str(undercover.getName())
#    bot.sendMessage(chatId,String)
def help(msg):
    chatId=msg['chat']['id']

    bot.sendMessage(chatId,"/newgame 重新遊戲 \n /join 加入遊戲 \n /start 開始遊戲 \n /report @UserID 檢舉功能")

def on_callback_query(msg):
    global usernamedata
    global chatId
    global isButtonTime
    global button
    global HinterList
    global can_hint
    global isEnd
    global message_with_inline_keyboard
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    msg_idf = telepot.message_identifier(message_with_inline_keyboard)
    print("idf",msg_idf)
    print('Callback Query:', query_id, from_id, query_data)
    if(query_data in usernamedata):
        vote(("@"+str(msg['from']['username'])),query_data)
        bot.answerCallbackQuery(query_id, text='投票囉')
    elif(query_data == "結束投票"):
        
        bot.answerCallbackQuery(query_id, text='結束投票囉')
        if message_with_inline_keyboard:
            bot.editMessageText(msg_idf, printVote())
            dealVote()
            if not isEnd:
                HinterList=usernamedata
                index = 0
                can_hint = True
                bot.sendMessage(chatId,'現在進入到提示環節~')
                bot.sendMessage(chatId,'首先輪到'+str(HinterList[index])+'提供提示\n提示的格式:「/hint [提示內容]」')
        
        else:
            bot.answerCallbackQuery(query_id, text='No previous message to edit')
    
def dealVote():
    global howManyPlayer
    global usernamedata
    global players
    global chatId
    global howManyPlayer 
    global howmanyundercover 
    global undercover
    beVotedPlayer = ""
    for username in usernamedata:
        print(str(username) + str(players[username].getBeenVoted()))
        if(players[username].getBeenVoted()>howManyPlayer//2):
            print("final"+username)
            beVotedPlayer = username
    if(beVotedPlayer==""):
        bot.sendMessage(chatId,"沒事沒事")
    elif((howManyPlayer-howmanyundercover)==howmanyundercover or beVotedPlayer in undercover or howmanyundercover==0):
        deleteplayer(chatId,beVotedPlayer)
        printOutcome(chatId)
    elif(players[beVotedPlayer].isUndercover()):
        deleteplayer(chatId,beVotedPlayer)
        bot.sendMessage(chatId,"抓到臥底啦")
    else:
        deleteplayer(chatId,beVotedPlayer)
        bot.sendMessage(chatId,"有暴民阿")
    
def resetVotedNumber():
    for username in usernamedata:
        votePlayer = players[username]
        votePlayer.setBeenVoted(0)

def vote(username,VotedUsername):
    # ↑↑ def vote沒動
    print('vote這裡')
    global chatId
    global canvote
    global usernamedata
    print(chatId)
    if(username in usernamedata):
        if canvote :
            if(players[username].canVote()):
    
                players[VotedUsername].plusVoted()
            else:
                bot.sendMessage(chatId,username+"投票過了87")
            
            players[username].setVoteRightFlase()
        elif HintRound == True:
            Str = ''
            global UnHintedPlayers
            for player in UnHintedPlayers:
                Str = Str+ '' +player
            bot.sendMessage(chatId,"提示環節還未結束啊啊\n"+Str+'快點提示!')

        else:
            bot.sendMessage(chatId,"嘖嘖，現在不能投阿")
    else :
        bot.sendMessage(chatId,"嘖嘖",username,"你來亂的阿!?")

def showVoteButton(msg):
    pprint(msg)
    global usernamedata
    global keyboards
    global players
    global message_with_inline_keyboard
    resetVotedRightTrue()
    resetVotedNumber()
    print('我是haha')
    if(len(keyboards)>0):
        del keyboards[:]
    for username in usernamedata:
        keyboards.append([InlineKeyboardButton(text=(players[username].getName()), callback_data=username)])
    keyboards.append([InlineKeyboardButton(text="結束投票", callback_data="結束投票")])
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard = keyboards)
    message_with_inline_keyboard = bot.sendMessage(chat_id, "現在開始投票", reply_markup = keyboard)
    print('我是XDXDXDXD')
def printVote():
    String=""
    global canvote
    if canvote :
        for username in usernamedata:
            votePlayer = players[username]
            String=String + votePlayer.getName() + "被投了" + str(votePlayer.getBeenVoted()) + "票" + "\r\n"
        return String
    else:
         bot.sendMessage(chatId,'還沒投呢!')
         
         
         
'''def printUsername(chatId):
    String=""
    for username in usernamedata:
        votePlayer = players[username]
        String=String + votePlayer.getName() + ":" + username + "\r\n"
    bot.sendMessage(chatId,String)'''

def checkWhoisMaxVoted():
    maxVotePlayer = players[usernamedata[0]]
    for username in usernamedata:
        votePlayer = players[username]
        if(votePlayer.getBeenVoted() > maxVotePlayer.getBeenVoted()):
            maxVotePlayer=username
    return maxVotePlayer
'''def timer(chatId,n,sec):  
    
    每n秒執行一次
    
    while True:
        if sec == 0 :
            break
        bot.sendMessage(chatId,str(sec))
        sec -= 1
        time.sleep(n)'''

def deletereport(msg,chatId,targetName):
    global howManyPlayer
    global howmanyundercover
    deleteplayer(chatId,targetName)
    bot.sendMessage(chatId,targetName + "你太壞了掰掰囉")
    if howmanyundercover == 0:
        bot.sendMessage(chatId,"沒臥底了")
        newgame(msg)
def deleterecord(username):
    for I in players[username].hasreport:
	    players[I].bereport -= 1
def report(msg,chatId,targetName,username):
    if username not in usernamedata:
        bot.sendMessage(chatId,"乾～你又沒玩檢舉屁喔")
    elif targetName not in usernamedata:
        bot.sendMessage(chatId,"此人不在遊戲內！！87")
    
    elif targetName in players[username].hasreport:
        bot.sendMessage(chatId,"你要讓他死嗎？")
    
    else:
        players[username].hasreport.append(targetName)
        players[targetName].bereport += 1
        bot.sendMessage(chatId,targetName + "被檢舉了")
        if players[targetName].bereport >= howManyPlayer//2:
            # deleteplayer(chatId,targetName)
            deleterecord(targetName)
            deletereport(msg,chatId,targetName)
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()#等候輸入
message_with_inline_keyboard=None
keyboards=[]
HinterList = []
errorHints = {}
chatId=0
players = {} #@username player
Hints = []
usernamedata = []
howManyPlayer = 0
howmanyundercover = 0
index = 0
undercover = []
canjoin = True
HintRound = False
canvote = True
can_hint = False
isButtonTime = True
canNewgame = True
canStart = True
isEnd = False
thisRoundHints = {}
while 1:
    time.sleep(1)
