import Scrapper as WebScrape
import motor.motor_asyncio
import fetch as mydb
import datetime as dt
import asyncio 
import motor
import aiohttp 
import json
from random import randint,choice
db=mydb.mydb('SumitBot')
class Bot:  
       def  __init__ (self,token,db=mydb.mydb('SumitBot')):                
         self.api=r'https://api.telegram.org/bot'+token 
         self.offset=0
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
          
           async def updates(allowes_updates):
            async with aiohttp.ClientSession() as client:  
             asyncio.create_task(self.queue_handler())         
             while True:   
               res=(await (await client.post(url,data={"offset":self.offset,"allowed_updates":allowes_updates})).json())["result"]
               for l in res:
                 print(l)     
                 if l:
                  self.offset=l['update_id']+1      
                  self.que.append(asyncio.create_task(self.message_handler(l,client)))
           asyncio.run(updates(["messages","chat_member"]))

       async def queue_handler(self):
          while True:
             await asyncio.sleep(100)  
             if len(self.que)>10:
              for l in  self.que:
                print(l.exception())      
                if l.isdone():
                  self.que.remove(l) 

       async def message_handler(self,l,session):
                m=None
                 
                if "message" in l:     
                  if 'reply_to_message' in l:
                   m=l["reply_to_message"]
                  else:
                    m=l["message"]  
                elif "edited_message" in m:
                   m=l["edited_message"]
                if m: 
                 task=asyncio.create_task(self.GetUser(m,session))# 
                 try:
                  self.que.extend([asyncio.create_task(self.db.userupdate(m["from"])),
                                   asyncio.create_task(self.db.chatupdate(m["chat"])), 
                                   ])                  
                  permits=await task
                  if m["entities"][0]['type']=='bot_command' and m["from"]['is_bot']==False:
                   t=m['text']
                   c=m["entities"][0]['length']
                   a=t.replace('@ultra_99kbot','')
                   l=(m,(t[c:]).strip())
                   if permits=='private':   
                         self.que.append(asyncio.create_task(self.member[a](*l,session=session)))
                   else:
                      if a in self.member:
                        self.que.append(asyncio.create_task(self.member[a](*l,session=session)))
                      if a in self.admin:
                            if permits["status"]=="administrator":
                                  if permits[(self.admin[a])[0]]:
                                          self.que.append(asyncio.create_task(self.admin[a][1](*l,session=session)))
                 except:pass
          

       async def GetUser(self,m,session):
          chat=m["chat"]
          user=m["from"]
          permits='private'
          if chat["type"]!='private':
           params={'chat_id':chat["id"],'user_id':user["id"]}
           r=await session.post(self.api+'getChatMember',params=params) 
           permits=(await r.json())["result"]
          try:await self.db.userpermits(str(chat["id"]),permits)
          except:pass
          return permits   
      
       async def SendText(self,text,mess,session,reply=False,pin=False):
           chat_id=mess['chat']['id']
           message_id=mess['message_id']
           if reply==True:
              message_id=mess['message_id']
              params={"chat_id":chat_id
                      ,"text":text
                      ,"allow_sending_without_reply":True,
                      "reply_to_message_id":message_id
                      }
              msg=(await (await session.post(self.api+"sendMessage",data=params)).json())["result"]
           else:    
              params={"chat_id":chat_id
                      ,"text":text
                      ,"allow_sending_without_reply":True
                      }
              msg=(await (await session.post(self.api+"sendMessage",data=params)).json())["result"]
     
       async def PinMessage(self,msg,session):
               params={"chat_id":msg["chat"]["id"],
                       "message_id":msg['message_id']}
               await session.post(self.api+"pinChatMessage",data=params)

       async def SendButton(self,mess,text,session):
             chat_id=mess["chat"]["id"]
             message_id=mess["message_id"]
             data_tuple=await WebScrape.Pdfdrive(text,session)
             params={"chat_id":chat_id
                 ,"text":f"Matched links for the book- {text}:"
                 ,"allow_sending_without_reply":True,
                  "reply_to_message_id":message_id,
                  "parse_mode":"markdown",
                  "reply_Sendmarkup":{"inline_keyboard":[
                      [{ "text":(data_tuple[0])[0],"url":(data_tuple[0])[1]}],
                      [{ "text":data_tuple[1][0],"url":data_tuple[1][1]}],
                      [{ "text":data_tuple[2][0],"url":data_tuple[2][1]}],
                      [{ "text":data_tuple[3][0],"url":data_tuple[3][1]}],
                      [{ "text":data_tuple[4][0],"url":data_tuple[4][1]}],
                      [{ "text":data_tuple[5][0],"url":data_tuple[5][1]}],]}}
   
       async def SendImg(self,mess,path,session,pin=False):
        params={"chat_id":mess['chat']['id'],'photo':path}
        r=(await session.post(self.api+'sendPhoto',params=params).json())["result"]
       
       async def SendAudio(self,mess,path,session):pass
       async def Stream_on_VC():pass

       async def BanUser(self,m):pass
       async def MuteUser(self,m):pass   

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

                
if __name__=='__main__': 
 ins=Bot(r"5440775518:AAFeFhG4PH4TayXhkOBNoy-eRyqLQPAsk9Q/")
 ins.member={'/quote':quote}
       
 

ins.Pool()  