import os
import pytesseract
from pytesseract import Output
from PIL import Image
import pandas as pd
from  pdf2image import convert_from_path
from fpdf import FPDF
import tempfile
import textwrap
from PIL import Image,ImageEnhance
import numpy as np
import cv2

os.environ["Path"]+=os.pathsep+r"C:\Program Files (x86)\Tesseract-OCR"
os.environ["Path"]+=os.pathsep+r"C:\Program Files (x86)\poppler-22.01.0\Library\bin"
 
poppler_path = r"C:\path\to\poppler-xx\bin"
custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng'



def filter_data(image):
     d = pytesseract.image_to_data(image, config=custom_config ,output_type=Output.DICT)
     di = pytesseract.image_to_string(image, config=custom_config)
     #print(di)
     #print(d)
     df = pd.DataFrame(d)
     # clean up blanks
     df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
     # sort blocks vertically
     sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
     
     for block in sorted_blocks:
         
        curr = df1[df1['block_num']==block]
        sel = curr[curr.text.str.len()>3]
        char_w = (sel.width/sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = 0, 0, 0
        text=''
        for ix, ln in curr.iterrows():
            # add new line when necessary
            
            if prev_par != ln['par_num']:
                text += '\n'
                prev_par = ln['par_num']
                prev_line = ln['line_num']
                prev_left = 0
            elif prev_line != ln['line_num']:
                text += '\n'
                prev_line = ln['line_num']
                prev_left = 0

            added = 0  # num of spaces that should be added
            if ln['left']/char_w > prev_left + 1:
                added = int((ln['left'])/char_w) - prev_left
                text += ' ' * added 
            text += ln['text'] + ' '
            prev_left += len(ln['text']) + added + 1      
        text += '\n'
        print(text)
     return text

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def image_processor(file):
    # TODO : Implement using opencv
    temp_filename = set_image_dpi(file.convert("L"))
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new

def set_image_dpi(im):
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.Resampling.LANCZOS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename
def basic_adjustments(image):
      from time import sleep
      image=ImageEnhance.Sharpness(image).enhance(100)
      image.show()
      image=ImageEnhance.Contrast(image).enhance(100)
      image=ImageEnhance(a1).Brightness(image).enhance(70)
      image.show()
      sleep(60)
      return image
def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
   
    or_image = cv2.bitwise_or(img, closing)
    return or_image

def create_pdf(pdf_path):
     path=r"\files"
     a4_width_mm = 210
     pt_to_mm = 0.35
     fontsize_pt = 10
     fontsize_mm = fontsize_pt * pt_to_mm
     margin_bottom_mm = 10
     character_width_mm = 7 * pt_to_mm
     width_text = a4_width_mm / character_width_mm
     
     images= convert_from_path(pdf_path)
     
     pdf = FPDF(orientation='P', unit='mm', format='A4')
     pdf.set_auto_page_break(True, margin=margin_bottom_mm)

     def add_pages(text):
        pdf.add_page()
        pdf.set_font(family='Courier', size=fontsize_pt)
        splitted = text.split('\n')
        for line in splitted:
            
            try:lines = textwrap.wrap(line, width_text)
            except:print(line)
            if len(lines) == 0:pdf.ln()
            for wrap in lines:pdf.cell(0, fontsize_mm, wrap, ln=1)
               
     #[img.save("img.jpg") for img in images]       
     [add_pages(filter_data(image_processor(basic_adjustments(l)))) for l in images]
     pdf.output("newpdf.pdf", 'F')


create_pdf("test_pdf.pdf")
