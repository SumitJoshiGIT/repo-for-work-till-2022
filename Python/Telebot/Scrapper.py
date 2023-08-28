from bs4 import BeautifulSoup as bs
import datetime as dt
import asyncio 
import aiohttp
import re as reg
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
         ,"Accept-Language":"en-US","Referer":"https://www.google.com/","Accept":"text/html"
         }
async def request(url,session):
  try: 
   response=await (await session.get(url,allow_redirects=True,headers=headers)).text()
  except:
     print("err")
  return bs(response,"html.parser")

async def Pdfdrive(Book,session):

   url="https://www.pdfdrive.com"
   ur=url+r'/search?q='+Book+"&searchin=en"
   data=await request(ur,session)
   data=data.find_all(attrs={'class':"file-left"},limit=6)
   print(data)
   links=[((l.a.img['alt'].split(':')[0]).replace("[]",' '),(url+(await request(url+l.a['href'],session)).find('a',{"id":"download-button-link"})['href'])) for l in data]
   return links
   
async def gktoday(session,date_=(dt.date.today()).strftime('%B-%#d-%Y')):
   url=r"https://www.gktoday.in/daily-current-affairs-quiz-"+f"{date_.lower()}/ "
   quiz_name="#Current_Affairs_Quiz:"+date_
   soup=await request(url,session)
   Q=[l.text for l in soup.find_all(attrs={'class':'wp_quiz_question testclass'})]
   A=[l.text for l in soup.find_all(attrs={'class':'ques_answer'})]
   
   A=[(reg.sub("Correct|Answer:|] ",'',l).split('['or']')[1])[:-1] for l in A]
   
   li=list(filter(lambda x: bool(reg.compile("\[[A-F]\].").match(str(x).strip()))==True,[l.text for l in soup.find_all('p')]))
   O=[list(map(lambda x: x.strip() if( x!='') else None ,reg.split('\[[A-F]\]',l.strip()))) for l in li]

   [l.remove(None) for l in O]
   return (Q,O,A,quiz_name)

async def news(self,session,mess,q='',country='',sources=''):
        headlines=" https://newsapi.org/v2/top-headlines"
        apiKey="779a2df2062343edace38b0cbff7a7bb"
        param={"q":q,"language":"en","country":country,"sources":sources,"pageSize":7,"apiKey":apiKey}
        r=await session.post(headlines,params=param) 
        a=(await r.json())["articles"]
        print('self')
        try:        
         b=(l['url'] for l in a)
         await self.sendText(f"Top International News Updates\n {dt.datetime.now().strftime('%H:%M:%S,%d %B %Y')}",mess) 
         [await self.Markup(mess,'Click to visit Source,'+l.strip()) for l in b]  
        except:
          await self.sendText("Not Found or APi error",mess)
if __name__=='__main__': 
 def gogoanime(keyword):
    url=r"https://gogoanime.run/"
    s=re.Session()
    link=request("https://gogoanime.run/category/one-piece",s)#.find("div",attrs={"class":"last_episodes"}).find_all('a')
   #link=[url+l["href"] for l in link]
    return link
#gogoanime("dafda")

#t=re.Session()
#a=request("https://oceansofgamess.com/?s=warcraft",t)
#a=a.find_all('a',attrs={"rel":"bookmark"})
#[print(l['href']) for l in a]
# a=gogoanime("one Piece").find_all('a')
#a=bs(re.post("https://gogoanime.run/search.html?keyword=robots&key_pres=&link_alias=&keyword_search_replace=").text,'html.parser').find_all('a')
# [print(l.text) for l in a]

   
#pd=Pdfdrive('newtonian mechanics')
#Answers=[l.extract().text.split("\n")[1] for l in soup.find_all(attrs={"class":"answer"})]
#Choices=[reg.split('\n\[[A-Z]\]',l[1].strip()) for l in li]
#Questions=[l[0].replace('\n','') for l in li]

 async def main():
   async with aiohttp.ClientSession() as session:
      res=await Pdfdrive("HC verma",session)
      
 asyncio.run(main())
