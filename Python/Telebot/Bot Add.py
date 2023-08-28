import Bot
import fetch as mydb
from bs4 import BeautifulSoup as bs
import textwrap
from random import choice,randint
from PIL import Image, ImageFont,ImageDraw

db=mydb.mydb('SumitBot')
Mybot=Bot(r"5440775518:AAFeFhG4PH4TayXhkOBNoy-eRyqLQPAsk9Q/",db)


async def quote(mess,text,session): 
    quote=await db.fetch_quote()
    text=textwrap.fill(text=quote[0],width=27)+f'\n\n    -{quote[1]}'
    color=choice(['black','white','red'])
    bck=randint(0,5)
    img=Image.open(f'backgrounds\{color}\{bck}.jpg')
    size=img.size[0]+img.size[1]
    quofont=ImageFont.truetype(r'fonts\0.ttf',size//50)
    ImageDraw.Draw(img).text((400,400),text,font=quofont,fill=color)
    path='temp\temp.jpg'
    img.save()
    Bot.SendImg(mess,path,session)
Mybot.member={'/quote':quote}
Mybot.Pool()
