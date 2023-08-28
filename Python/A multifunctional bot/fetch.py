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
          if userpermit:
             chat_permit_collec=self.db[str(chat_id)]
             m=await chat_permit_collec.find_one({"user":userpermit["user"]})
             if m:
               _id=m.pop("_id")
               if m!=userpermit:await chat_permit_collec.replace_one({"_id":_id},userpermit)
             else:await chat_permit_collec.insert_one(userpermit)
                 
     async def userupdate(self,user):         
             u=await self.Users.find_one({"id":user["id"]})
             if u:
               _id=u.pop("_id")
               if u!=user :await self.Users.replace_one({"_id":_id},user)
             else:await self.Users.insert_one(user)
                  
     async def chatupdate(self,chat):
             c=await self.Chats.find_one({"id":chat["id"]})  
             if c:  
              _id=c.pop("_id")    
              if c==chat:pass 
              elif c!=chat :await self.Chats.replace_one({"_id":_id},chat)  
             else:await self.Chats.insert_one(chat)
               
     async def get_chats(self,chat_id):
          self.Chats.find({"id":chat_id})
            
     async def fetch_quote(self):
            Qu=await self.SETTINGS.find_one({"setting_type":'Quote'})
            q=await self.Quotes.find_one({'Q':Qu["Q"]})
            await self.SETTINGS.update_one({"_id":Qu["_id"] },{'$set':{'Q':(q['Q']+1)}})
            return (q["Quote"],q["Author"])

     async def fetch_quote_random(self,n): 
            q=await self.Quotes.find_one({"Q":n})
            
            return (q["Quote"],q["Author"])
            
     async def register(self,chat_id,text):
             a=(await self.SETTINGS.find_one({"content_type":"Approvals"}))
             chat_id=str(chat_id)
             registered,passwords,blocked,waiting=a["registered"],a["passwords"],a["blocked"],a["waiting"]
             _id=a.pop("_id")
             if chat_id in registered:
                  print("This Chat is already registered!")
                  return "This Chat is already registered!"
             elif text ==passwords:     
                  registered+=","+chat_id
                  registered=json.dumps(registered)
                  self.SETTINGS.update_one({"_id":_id},{'$set':{"registered":registered}})
                  return "This Chat is already registered!"
             elif chat_id in blocked:     
                  return "This Chat is banned!"
             else:
               if not chat_id in waiting:
                      waiting+=','+chat_id
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
        asyncio.run(db.fetch_quote_random(400))
        from random import randint 
        print(randint(1,2))