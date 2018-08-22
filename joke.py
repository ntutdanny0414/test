import requests
from bs4 import BeautifulSoup
BASE_URL = 'https://www.ptt.cc'
DataList= []
def GetThumsUp(article):
    span = article.find('div',{'class':'nrec'})
    nrec = span.find('span',{'class':'hl'})
    if nrec != None:
        if nrec.get_text().isdigit() or nrec.get_text() == '爆':  #nrec.get_text()變數.isdigit()函式  可以判斷是不是數字 
            return nrec.get_text()
        else: return 0
    else: return 0

def PrintData(article,DataList):
    title = article.find('div',{'class':'title'})
    TitleName = title.find('a').get_text().strip()
    meta = article.find('div',{'class':'meta'})
    author = meta.find('div',{'class':'author'}).get_text().strip()
    Href = title.find('a')
    adress = BASE_URL+str(Href.get('href'))
    DataList.append(str('{0:<5}{2:<15}{1}\n{3}'.format(GetThumsUp(article),TitleName,author,adress)))
    return DataList

def main(msg):   
    url = 'https://www.ptt.cc/bbs/joke/index5961.html'   
    while True:
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.findAll('div',{'class':'r-ent'})
        for article in articles:    
            if GetThumsUp(article) == '爆': Data = PrintData(article,DataList)
            elif int(GetThumsUp(article)) >= 30: Data = PrintData(article,DataList)
    #print(soup.find('a',{'class':'btn wide'}))
        NextLink = soup.findAll('a',{'class':'btn wide'})
        url= BASE_URL+str(NextLink[1].get('href'))
        if len(Data) >= 20:
            return Data
#            bot.sendMessage(chatID,random.choice(Data))  #for i in Data:
            break
