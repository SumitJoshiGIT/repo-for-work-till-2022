import aiofiles
import Scrapper 
import motor.motor_asyncio
import fetch as mydb
import datetime as dt
import asyncio 
import motor
import aiohttp 
import json
from random import randint,choice
db=mydb.mydb('SumitBot')
class Bot():  
       def  __init__ (self,token,db=mydb.mydb('SumitBot')):                
         self.api=r'https://api.telegram.org/bot'+token 
         self.offset=-1
         self.form="Not What you inputted"
         self.error=f"Expected input is of form:\n {self.form}"
         self.db=db
         self.member={ }                      
         self.admin={'/ban':(("can_restrict_members")),
                     '/promote':(("can_promote_members")),
                     '/mute':(("can_restrict_members")),
                     '/automate':[]}
          
         self.que=[]
       
       def Pool(self):
           url=self.api+"GetUpdates?"
           async def updates(allowed_updates):
            async with aiohttp.ClientSession() as client:  
             asyncio.create_task(self.queue_handler())         
             while True:
              try:[(await self.gen(l,client)) for l in (await (await client.post(url,data={"offset":self.offset,"allowed_updates":allowed_updates})).json())["result"]]
              except:continue 
           asyncio.run(updates(["messages","chat_member"]))

       async def gen(self,l,client):       
         self.offset=l['update_id']+1      
         if "message" in l:     
            if 'reply_to_message' in l:self.que.append(asyncio.create_task(l["reply_to_message"],client))
            else:self.que.append(asyncio.create_task(self.message_handler(l["message"],client)))
         elif "edited_message" in l:self.que.append(asyncio.create_task(self.message_handler(l["edited_message"],client)))
   
       async def queue_handler(self):
          while True:
            await asyncio.sleep(1000)  
            for l in self.que: 
             if l==True:
              if l.done():self.que.remove(l)
       
       async def message_handler(self,m,session): 
                  task=asyncio.create_task(self.GetUser(m,session))    
                  self.que.extend([asyncio.create_task(self.db.userupdate(m["from"])),
                                   asyncio.create_task(self.db.chatupdate(m["chat"])),])                  
                  permits=await task
                  print(m)
                  try:k=m["entities"][0]['type']
                  except:k=None
                  if k=='bot_command' and m["from"]['is_bot']==False:
                   t=m['text']
                   c=m["entities"][0]['length']
                   a=t.replace('@ultra_99kbot','')[:c]
                   l=(m,(t[c:]).strip())
                   if a in self.member:    
                        self.que.append(asyncio.create_task(self.member[a](*l,session=session)))
                   elif permits and a in self.admin and permits["status"]=="administrator" and permits[(self.admin[a])[0]]:
                           self.que.append(asyncio.create_task(self.admin[a][1](*l,session=session)))  
                     

       async def GetUser(self,m,session):
          chat=m["chat"]
          user=m["from"]
          if chat["type"]!='private':
           params={'chat_id':chat["id"],'user_id':user["id"]}
           permits=(await(await session.post(self.api+'getChatMember',params=params)).json())["result"] 
           await self.db.userpermits(chat["id"],permits)
           return permits   
          
       async def SendText(self,text,mess,session,reply=False,pin=False):
           chat_id=mess['chat']['id']
           
           if reply==True:
              params={"chat_id":chat_id
                      ,"text":text
                      ,"allow_sending_without_reply":True,
                      "reply_to_message_id":mess['message_id']}
              msg=(await (await session.post(self.api+"sendMessage",data=params)).json())["result"]
           else:    
              params={"chat_id":chat_id,"text":text}
              msg=(await (await session.post(self.api+"sendMessage",data=params)).json())["result"]
     
       async def PinMessage(self,msg,session):
               params={"chat_id":msg["chat"]["id"],
                       "message_id":msg['message_id']}
               await session.post(self.api+"pinChatMessage",data=params)

       async def SendButton(self,mess,text,session,data_tuple=''):
             chat_id=mess["chat"]["id"]
             message_id=mess["message_id"]
             a=json.dumps([[{ "text":(data_tuple[n])[0],"url":(data_tuple[n])[1]}] for n in range(len(data_tuple))])
             params={"chat_id":chat_id
                 ,"text":text   
                 ,"allow_sending_without_reply":True,
                  "reply_to_message_id":message_id,
                  "parse_mode":"markdown",
                  "reply_Sendmarkup":{"inline_keyboard":a }}
        
             r=await(await session.post(self.api+'SendMessage')).json()
          
       async def SendPhoto (self,mess,session,file=0,path=0,pin=False): 
         async with aiofiles.open(file,"rb") as img_file:
          
            if img_file: 
             photo=aiohttp.FormData()
             photo.add_field("chat_id",str(mess['chat']['id']))
             photo.add_field('photo',
                         img_file,
                         filename='temp.jpg',
                         content_type='image/gif') 
            elif path:
                   photo={"chat_id":mess['chat']['id'],'photo':path}
            r=await session.post(self.api+'sendPhoto',data=photo) 
            print(r)

       async def SendAudio(self,mess,file,session):pass
       async def Stream_on_VC():pass

       async def BlockUser(self,m):pass
       async def MuteUser(self,m):pass   
       async def approve():pass
       async def SendMarkup(self,data_tuple,mess,session,mode='markup',reply=False):
         try:  
            data_tuple=data_tuple.split(',')
            chat_id=mess["chat"]["id"]
            if  reply==False:
             params={"chat_id":chat_id
                 ,"text":f"[{data_tuple[0]}]({data_tuple[1]})" 
                  ,"parse_mode":"markdown"}
            else:
              message_id=mess["message_id"]  
              params={"chat_id":chat_id
                 ,"text":f"[{data_tuple[0]}]({data_tuple[1]})"
                 ,"allow_sending_without_reply":False,
                  "reply_to_message_id":message_id,
                  "parse_mode":"markdown"}
            await session.post(self.api+"sendMessage",json=params)
         except:
            self.form="[<text>]<link>"
            await self.SendText(self.error,chat_id=(mess["chat"]["id"]),reply=True,message_id=mess['message_id'])
               
       async def SendPoll(self,mess,Questions,Choices,Answers,Heading,session):
         m=0
         url=self.api+"SendPoll"
         print(mess)
         chat_id=mess["chat"]["id"]
         await self.SendText(Heading,mess,session,pin=True)     
         while m<len(Questions):    
          params={
             "chat_id":chat_id,
             "question": Questions[m],
             "options": json.dumps(Choices[m]) ,
             "type": "quiz",
             "correct_option_id": Choices[m].index(Answers[m])
             }
          print(chat_id)
          await session.post(url,params=params)
          m+=1



import textwrap
from random import choice,randint
from PIL import Image, ImageFont,ImageDraw 

if __name__=='__main__': 

  ins=Bot(r"5440775518:AAFeFhG4PH4TayXhkOBNoy-eRyqLQPAsk9Q/",db)
  
  async def quote(mess,tex,session,path=r'temp\temp.jpg'): 

    r=randint(1,450000)
    try:quote=await db.fetch_quote_random(r)
    except:print("Error")
    text=textwrap.fill(text=quote[0],width=27)+f'\n\n    -{(quote[1].split(",")[0])}'
    l=(len(text.split('\n')))
    if  l <15:siz=48
    elif l<23:siz=38
    else :siz=30
    color=choice(['black','white'])
    img=Image.open(f'backgrounds\{color}\{randint(0,5)}.jpg')
    ImageDraw.Draw(img).text((100,100),text,font=ImageFont.truetype(r'fonts\0.ttf',siz),fill=color)
    img.save(path) 
   
    await ins.SendPhoto(mess=mess,session=session,file=path) 
         
    
  async def book(mess,text,session):
        data_tuple=await Scrapper.Pdfdrive(text,session)
        await ins.SendButton(mess,text,session,data_tuple=data_tuple)

  async def example(mess,tex,session):
        text="fdlkfldfldjfl"
        await ins.SendButton(mess,text,session,data_tuple=(("hello","kale"),))

  async def news(mess,tex,session):
      try:         
        await ins.sendText(f"Top International News Updates\n {dt.datetime.now().strftime('%H:%M:%S,%d %B %Y')}",mess) 
        a=await Scrapper.news()
        [await ins.Markup(mess,'Click to visit Source,'+m.strip()) for m in (l['url'] for l in a)]  
      except:await ins.sendText("Not Found or APi error",mess)
         
  ins.member={'/quote':quote,'/book':book,"/b":example}
  ins.Pool()  
