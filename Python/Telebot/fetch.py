import motor.motor_asyncio
import asyncio
import json
from platform import system
if system()=='windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from bson.objectid import ObjectId
class mydb():
     def __init__(self,db,conn='mongodb://localhost:27017/'):  
          client=motor.motor_asyncio.AsyncIOMotorClient(conn)
          self.db=client[db]
          self.SETTINGS=self.db["SETTINGS"]
          self.Users=self.db["Users"]
          self.Chats=self.db["Chats"]
          self.Quotes=self.db["Quotes"]

     async def userpermits(self,chat_id,userpermit):
          if userpermit!='private':
             chatdb=self.db[chat_id]
             m=await chatdb.find_one({"id":userpermit["user"]["id"]})
             try: _id=m.pop("_id")
             except: None
             if m!=None:
                  userpermit=json.dumps(userpermit)
                  if m!=userpermit:await self.Users.replace_one({"_id":_id},userpermit)
                  elif m==userpermit:pass
             else:await self.Users.insert_one(userpermit)
                 
     async def userupdate(self,user):         
             u=await self.Users.find_one({"id":user["id"]})
             try:_id=u.pop("_id")
             except:None
             if bool(u)==True:
                   if u!=user:await self.Users.replace_one({"_id":_id},json.dumps(user))
                   elif u==user:pass
             else:await self.Users.insert_one(user)
             
     async def checkpermit(self,user,chat,level):
          a=self.ab[f"chat"].find({"user":user})
          
     async def chatupdate(self,chat):
             id=chat["id"]
             c=await self.Chats.find_one({"id":id})  
             try:_id=c.pop("_id")
             except:pass
              
             if bool(c)==True:
              if c==chat:
                   pass     
              elif c!=chat:
                   await self.Chats.replace_one({"_id":_id},json.dumps(chat))  
             else:
                 await self.Chats.insert_one(chat)                 
     async def get_chats(self):
          self.Chats.find()
          
       
                 
     async def fetch_quote(self):
            Qu=await self.SETTINGS.find_one({"setting_type":'Quote'})
            _id=Qu["_id"] 
            qno=Qu["Q"]
            q=await self.Quotes.find_one({'Q':qno})
            qno+=1
            await self.SETTINGS.update_one({"_id":_id},{'$set':{'Q':qno}})
            print(q["Quote"],q["Author"])
            return (q["Quote"],q["Author"])

     async def register(self,chat,text):
             a=((await self.SETTINGS.find_one({"content_type":"Approvals"})))
             chat=str(chat)
             registered,passwords,blocked,waiting=a["registered"],a["passwords"],a["blocked"],a["waiting"]
             
             _id=a.pop("_id")
             if chat in registered:
                  print("This Chat is already registered!")
                  return "This Chat is already registered!"
             elif text ==passwords:     
                  registered+=","+chat
                  registered=json.dumps(registered)
                  self.SETTINGS.update_one({"_id":_id},{'$set':{"registered":registered}})
                  return "This Chat is already registered!"
             elif chat in blocked:     
                  return "This Chat is banned!"
             else:
               if not chat in waiting:
                      waiting+=','+chat
                      waiting=json.dumps(waiting)
                      await self.SETTINGS.update_one({"_id":_id},{'$set':{"waiting":waiting}})
                      print("app")
                      return "Added Chat for Approval "
               else:
                      return "Chat Approval is due."


   
 
if __name__=="__main__": 
        db=mydb('SumitBot')
      
        c={'id': -1001529385994, 'title': 'Happy birthday Khushbu', 'username': 'speakfluenteng', 'type': 'supergroup'}
        u={'id': 2098351412, 'is_bot': False, 'first_name': 'Sumit', 'username': 'sumit_senpai', 'language_code': 'en'}    
        asyncio.run(db.userpermits())
     