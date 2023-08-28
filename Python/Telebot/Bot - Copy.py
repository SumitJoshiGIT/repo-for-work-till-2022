import time
import json
import Scrapper as WebScrape
import requests as re
from bs4 import BeautifulSoup as bs
import datetime as dt
import re as reg
import asyncio 
import csv

class TeleBot:
  
      def  __init__ (self,token):
         self.qno=1                    
         self.api=r'https://api.telegram.org/bot'+token 
         self.offset=-1
         self.form="Not What you inputted"
         self.error=f"Expected input is of form:\n {self.form}"
         self.comm={'/markup':self.Markup,
                    '/register':self.register,
                    '/book':self.book,
                    '/math':self.math,
                    '/joke':self.joke,
                    '/gkquiz':self.gkquiz,
                    '/newsint':self.newsint,
                    '/newsind':self.newsind}
         
                    
      def setting(self,w):
       if w=='r':
         with open("data\settings.txt","r") as file:
          out=eval(file.read())
         return out
       elif w=='w': 
         with open("data\settings.txt",'w') as  file:
           print(self.settings)  
           file.write(f'{self.settings}')
       return None
      
                     
        
      def ExecUpdates(self):
       self.settings=self.setting('r')
       self.registered=self.settings['registered']
       url=self.api+"GetUpdates?"
      
       def run():
           self.qno=self.settings.update({'qno':self.qno})
           res=re.post(url,data={"offset":self.offset})
           for l in res.json()['result']:
             try:
              self.update=l
              print(l)
              if self.update:
               
               self.max_uid=self.update['update_id']
               self.offset=self.max_uid+1
               m=self.update["message"]
               self.user=m['from']
               with open('users.txt','a') as file:
                    file.write(f'{self.user}\n')
               with open('chats.txt','a') as file:
                    file.write(f'{m["chat"]}\n')
               if self.user['is_bot']==False and m["entities"][0]['type']=='bot_command':
                     self.commandMode()
             except:
              continue
           
       while True:
          run()
          
      def commandMode(self):
         m=self.update['message']   
         t=m['text']
         c=int(m["entities"][0]['length'])
         a=t[:c].replace('@ultra_99kbot','')
         if a in self.comm:
          chat=m["chat"]   
          l=(self.update["message"],(t[c:]))
          u=(chat['id'],f'@{chat["username"]}')
          permits=self.userdata(chat['id'],self.user["id"])
          if not u in self.registered:
           if a=='/register':
             self.register(*l)
           else:  
            self.sendText('This chat is unregistered.',m,reply=True)  
          else:
            self.comm[a](*l) 
          print('done')
      def register(self,mess,t=''):
        name=f'@{mess["chat"]["username"]}'
        t=(mess["chat"]["id"],name)
        if t in self.registered:
          sendText('This chat is already registered!',mess,reply=True)
          return None
        self.settings.update({'registered':self.registered.append(t)})                    
        self.sendText(f'Registered:{name}',mess=mess,reply=True)   
     


      def userdata(self,chat_id,user_id):
          params={'chat_id':chat_id,'user_id':user_id}
          r=re.post(self.api+'getChatMember',params=params)
          return r.json()
          
       
      def book(self,mess,m=""):
             
             chat_id=mess["chat"]["id"]
             message_id=mess["message_id"]
             data_tuple=WebScrape.Pdfdrive(m)
             print(data_tuple)

             if data_tuple:
              params={"chat_id":chat_id
                 ,"text":f"Matched links for the book- {m}:"
                 ,"allow_sending_without_reply":True,
                  "reply_to_message_id":message_id,
                  "parse_mode":"markdown",
                  "reply_markup":{"inline_keyboard":[
                      [{ "text":(data_tuple[0])[0],"url":(data_tuple[0])[1]}],
                      [{ "text":data_tuple[1][0],"url":data_tuple[1][1]}],
                      [{ "text":data_tuple[2][0],"url":data_tuple[2][1]}],
                      [{ "text":data_tuple[3][0],"url":data_tuple[3][1]}],
                      [{ "text":data_tuple[4][0],"url":data_tuple[4][1]}],
                      [{ "text":data_tuple[5][0],"url":data_tuple[5][1]}],
                      
                      ]}}
              res=re.post(self.api+"sendMessage",json=params)
               
             else:
               self.sendText('No Results found.',mess,reply=True)
             print(data_tuple)
             
      def generateIMG(self,quote,author=''):
          
        text=textwrap.fill(text=quote,width=27)+f'\n\n    -{author}'
        color=choice(['black','white','red'])
        if self.bck==6:
            self.bck=0
            
        img=Image.open(f'backgrounds\{color}\{bck}.jpg')
        size=img.size[0]+img.size[1]
        i=ImageDraw.Draw(img)
        
        quofont=ImageFont.truetype(r'fonts\0.ttf',size//50)
        chfont=ImageFont.truetype(r'fonts\0.ttf',size//60)
        i.text((400,400),text,font=quofont,fill=color)
        i.text((100,img.size[1]-400),'Telegram:-@QFA_TG',font=chfont,fill='blue')
        img.save(f'temp\temp.jpg')
        return
    
      def quotefile(csv_f,mode="r",m=1):
          with open(csv_f,"r") as csv_file:   
           while 1: 
            if m!=0:
             obj=csv.reader(csv_file)
             if m>1 :
               (next(obj) for l in range(self.qno)) 
               generateImg(*(next(obj)[:3]))   
               yield sendImg(self.update["message"],path='temp\temp.jpg')
               self.sendImg
               self.qno+=1
          
      def sendImg(self,mess,path):
        
        params={"chat_id":mess['chat_id'],'photo':path}
        re.post(self.api+'sendPhoto',params=params)
        return re.json()
        
      def Markup(self,mess,data_tuple,mode='markup',reply=False):
       if type(data_tuple)== type('string'):    
         try:
            data_tuple=data_tuple.split(',')
            chat_id=mess["chat"]["id"]
            if  reply==False:
           
             params={"chat_id":chat_id
                 ,"text":f"[{data_tuple[0]}]({data_tuple[1]})" 
                  ,"parse_mode":"markdown"
                    }
            else:
              message_id=mess["message_id"]  
              params={"chat_id":chat_id
                 ,"text":f"[{data_tuple[0]}]({data_tuple[1]})"
                 ,"allow_sending_without_reply":False,
                  "reply_to_message_id":message_id,
                  "parse_mode":"markdown"
                    }
            res=re.post(self.api+"sendMessage",json=params)
            print(res)
          
         except:
            self.form="[<text>]<link>"
            self.sendText(self.error,chat_id=(mess["chat"]["id"],),reply=True,message_id=mess['message_id'])
              
      def sendText(self,text,mess,reply=False,pin=False):
           l=mess['chat']['id']
           def ms(params):
                 res=re.post(self.api+"sendMessage",data=params)
                 return res.json()      
           chat_id=mess["chat"]["id"]    
           if reply==True:
              message_id=mess['message_id']
              params={"chat_id":l
                      ,"text":text
                      ,"allow_sending_without_reply":True,
                      "reply_to_message_id":message_id
                      }
              ms(params)
           else:    
              params={"chat_id":l
                      ,"text":text
                      ,"allow_sending_without_reply":True
                      }
              ms(params)
              
           if pin:
               msg=ms(params)["result"]
               params={"chat_id":msg["chat"]["id"],
                       "message_id":msg['message_id']
                   }
               res=re.post(self.api+"pinChatMessage",data=params)
                       
      def Poll_Sender(self,mess,Questions,Choices,Answers,Heading):
         m=0
         chat_id=mess["chat"]["id"]
         self.sendText(Heading,mess,pin=True)
         while m<len(Questions):
          url=self.api+"SendPoll"
          params={
             "chat_id":chat_id,
             "question": Questions[m],
             "options": json.dumps(Choices[m]) ,
             "type": "quiz",
             "correct_option_id": Choices[m].index(Answers[m])
             }
          res=re.get(url,data=params)
          m+=1
          
      def joke(self,mess,txt):
        if txt:
         r=re.post(f"https://icanhazdadjoke.com/search?term={txt}",headers={"Accept":"application/json"})
         print(r)
         self.sendText(r.json()["joke"],mess,reply=True,message_id=mess['message_id'])
         
        else:
         r=re.get(f"https://icanhazdadjoke.com/",headers={"Accept":"text/plain"})
         self.sendText(r,mess,reply=True,)
    #Features  
      def math(self,mess,text):
        text=text.strip()
        for l,k in [("^","**"),("×","*"),("÷","/"),("\n",""),("/math",""),("@Quote_12bot","")]:
         try:
          text=text.replace(l,k)
         except:
          continue
        try:
          r=eval(text)
          self.sendText(r,chat_id=(mess["chat"]["id"],),reply=True,message_id=mess['message_id'])
        except:
            self.form="<arithmatical expression>"
            self.sendText(self.error,mess,reply=True)
            
      def newsint(self,mess,q='',country='',sources=''):
        headlines=" https://newsapi.org/v2/top-headlines"
        apiKey="779a2df2062343edace38b0cbff7a7bb" 
        param={"q":q,"language":"en","country":country,"sources":sources,"pageSize":7,"apiKey":apiKey}
        r=re.get(headlines,params=param) 
        r=re.get(headlines,params=param)
        a=r.json()["articles"]
        try:        
         b=(l['url'] for l in a)
         self.sendText(f"Top International News Updates\n {dt.datetime.now().strftime('%H:%M:%S,%d %B %Y')}",mess) 
         [self.Markup(mess,'Click to visit Source,'+l.strip()) for l in b]  
        except:
           self.sendText("Not Found or APi error",mess)      
             
      def newsind(self,mess,q='',country='in',sources=''):
        headlines=" https://newsapi.org/v2/top-headlines"
        apiKey="779a2df2062343edace38b0cbff7a7bb" 
        param={"q":q,"language":"en","country":country,"source":sources,"pageSize":7,"apiKey":apiKey}
        r=re.get(headlines,params=param)
        a=r.json()["articles"]
        print(a)
        try:      
         b=(l['url'] for l in a)
         self.sendText(f"Top Indian News Updates\n {dt.datetime.now().strftime('%H:%M:%S,%d %B %Y')}",mess) 
         [self.Markup(mess,'Click to visit Source,'+l.strip()) for l in b]  
        except:
           print(b)
           self.sendText("Not Found or APi error",mess)
           
      def gkquiz(self,m,a):
         self.Poll_Sender(m,*WebScrape.gktoday())
 
if __name__=='__main__': 
 ins=TeleBot(r"5440775518:AAFeFhG4PH4TayXhkOBNoy-eRyqLQPAsk9Q/")
 ins.ExecUpdates()         
 
