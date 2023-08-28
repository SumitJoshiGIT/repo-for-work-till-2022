       def generateIMG(self,quote,author=''):
 
        text=textwrap.fill(text=quote,width=27)+f'\n\n    -{author}'
        color=choice(['black','white','red'])
        bck=1
        img=Image.open(f'backgrounds\{color}\{bck}.jpg')
        size=img.size[0]+img.size[1]
        self.quofont=ImageFont.truetype(r'fonts\0.ttf',size//50)
        self.chfont=ImageFont.truetype(r'fonts\0.ttf',size//60)   
        i=ImageDraw.Draw(img)        
        i.text((400,400),text,font=self.quofont,fill=color)
        i.text((100,img.size[1]-400),'Telegram:-@QFA_TG',font=self.chfont,fill='blue')
        img.save(f'temp\temp.jpg')
