import aiofiles
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
         self.member={}                      
         self.admin={'/ban':(("can_restrict_members")),
                     '/promote':(("can_promote_members")),
                     '/mute':(("can_restrict_members")),
                     '/automate':[]}
         self.que=[]
         self.questions={
             1:"What is your name",
             2:"What is your age"
             ,3:"What is your gender"
             ,4:"Send your photograph"
             ,4:"Where do you live"
             ,5:"Here are some girls"
             ,6:"Send a screenshot of the payment:"}
        
       def qsender():

        for l in self.questions:
           res=(await self.SendText()).json()            
           yeild (SendText(l))


      



         
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
                  
                  try:k=m["entities"][0]['type']
                  except:k=None
                  if k=='bot_command' and m["from"]['is_bot']==False:
                   t=m['text']
                   if ". 
                     

       
          
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

       async def BlockUser(self,m):pass
       async def approve():pass

                        





