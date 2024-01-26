"""
このモジュールは、私的汎用モジュールとして準備しました。
使用するには 環境変数PYTHONPATHにこの親フォルダを追加するか、
import sys からフォルダを追加してください
"""
#このファイルをインポートして使用する場合は，環境変数PYTHONPATHにこの親フォルダを登録してください
#別件ですが，環境変数PYTHONDONTWRITEBYTECODE=1と設定するとコンパイルキャッシュがなくなります．
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape, portrait
from PIL import Image
from reportlab.lib.units import cm
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import os
import random
import unicodedata
import argparse
import math
import datetime
import requests
import io
from zipfile import ZipFile
import tempfile



class Rct:
    """
    独自矩形クラス
    """
    left=10
    bottom=10
    width=100
    height=100
    def __init__(self, left=0, bottom=0, width=600, height=842) :
        self.left=left
        self.bottom=bottom
        self.width=width
        self.height=height
    def shrink(self, left_margin=10, top_margin=10, right_margin=10, bottom_margin=10):
        return Rct(self.left+left_margin,self.bottom+bottom_margin,self.width-(left_margin+right_margin),self.height-(top_margin+bottom_margin))
    def devide(self, nth, cols, rows):
        w = self.width / cols
        h = self.height / rows
        b = self.bottom+(rows-1-(nth // cols)) *(self.height/rows)
        l = self.left+(self.width / cols) * (nth % cols)
        return Rct(l,b,w,h)
    def combine(self, rct):
        b = self.bottom if self.bottom < rct.bottom else rct.bottom
        l = self.left if self.left < rct.left else rct.left
        r = self.left+self.width if self.left+self.width > rct.left+rct.width else rct.left+rct.width
        t = self.bottom+self.height if self.bottom+self.height > rct.bottom+rct.height else rct.bottom+rct.height
        return Rct(l,b,r-l,t-b)
    def drawImage(self, page, image, iswhole=False):
        if image.split('.')[-1]=='svg':
            self.drawImage0(page, image, iswhole)
        else:
            self.drawImage1(page, image, iswhole)
    def drawImage0(self, page, image, isMid=False):
        '''svg対応 左下寄せ/中央寄せ'''
        drawing = svg2rlg(image)
        rx, ry = (self.width/drawing.width,self.height/drawing.height)
        r = ry if rx > ry else rx
        w = drawing.width * r
        h = drawing.height * r
        drawing.width = w
        drawing.height = h
        drawing.scale(r, r)
        l = (self.width - w)/2 if isMid else 0
        b = (self.height - h)/2 if isMid else 0
        renderPDF.draw(drawing, page, self.left+l, self.bottom+b)
    def drawImage1(self, page, image, iswhole=False):
        im = Image.open(image)
        w, h = im.size
        r = self.width / w
        mw, mh = 0, 0
        if r < self.height / h:
            r = r if iswhole else self.height / h
            mh = (self.height-r*h)/2 if iswhole else 0
            pw = (w - self.width/r) / 2
            im = im if iswhole else im.crop((pw, 0, w-pw, h))
        else:
            r = self.height / h if iswhole else r
            mw = (self.width-r*w)/2  if iswhole else 0
            ph = (h - self.height/r) / 2
            im = im if iswhole else im.crop((0, ph , w, h-ph))
        page.drawInlineImage(im, self.left+mw, self.bottom+mh, im.size[0]*r, im.size[1]*r)
    def drawStr(self, page, str, font="GF", position=1, color=(0,0,0)):
        page.setFont(font, self.height*.95, self.height)
        page.setFillColorRGB(color[0],color[1],color[2])
        w = page.stringWidth(str)
        if position == 0:
            page.drawString(self.left, self.bottom+self.height*.1, str)
        elif position == 1:
            page.drawString(self.left+(self.width-w)/2, self.bottom+self.height*.1, str)
        else:
            page.drawString(self.left+(self.width-w), self.bottom+self.height*.1, str)
        page.setFillColorRGB(0.0, 0.0, 0.0)
        
    def fillMe(self, page, color=(1,1,1), backtrans=True):
        if backtrans:
            page.setFillAlpha(0.5)
            page.setFillColorRGB(color[0],color[1],color[2])
            page.setStrokeAlpha(0.0)
            page.rect(self.left, self.bottom, self.width, self.height, fill=True)
            page.setFillAlpha(1.0)
            page.setFillColorRGB(0.0, 0.0, 0.0)
            page.setStrokeAlpha(1.0)
        
    def _textdevider(self, str, font="GF", size=10.5):
        strs = []
        j = 0
        for i in range(len(str)):
            if pdfmetrics.stringWidth(str[j:i], font, size) > self.width:
                strs.append(str[j:i-1])
                j = i - 1
        strs.append(str[j:])
        return strs
    def _sepby(self, s, m):
        res = []
        while len(ss:=self._sep2by(s, m))>1:
            res.append(f"{ss[0]}")
            s=ss[1]
        return res
    def _sep2by(self, s, m):
        jmark = re.compile(r'[．。、，「」『』（）【】〔〕［］｛｝〈〉《》〘〙〚〛"]')
        if len(s) < m and '\n' not in s:
            return [s]
        ss=s.split('\n')
        if len(ss[0]) < m:
            return [f"{ss[0]}\n", s[len(ss[0])+1:]]
        ss=[s[:m],s[m:]]
        if re.match(jmark, ss[0][-1]):
            while re.match(jmark, ss[0][-1]):
                ss[1]=ss[0][-1]+ss[1]
                ss[0]=ss[0][:-1]
            ss[1]=ss[0][-1]+ss[1]
            ss[0]=ss[0][:-1]
        if len(ss[1])>0 and re.match(jmark, ss[1][0]):
            while re.match(jmark, ss[1][0]):
                ss[1]=ss[0][-1]+ss[1]
                ss[0]=ss[0][:-1]
        return ss
    def drawLines(self, page, str, count=-1):
        n=int(math.sqrt(len(str)*self.width/self.height)+2)
        s=self._sepby(str, n) if count < 0 else count
        for i in range(len(s)):
            r=self.devide(i,1,len(s))
            r.drawLine(page, s[i], propo=True)
    def drawLine(self, page, str, font="GF", propo=True):
        page.setFont(font, self.height*.95, self.height)
        w = page.stringWidth(str)
        m = (self.width-w)/(len(str)-1) if propo else 0
        r=self
        for c in str:
            r.width = page.stringWidth(c)
            self.drawStr(page, c)
            r.left += (r.width+m)

    def drawTxt(self, page, strs, font="GF", lineHeight=12):
        t = page.beginText( )
        t.setTextOrigin(self.left, self.bottom+self.height-lineHeight)
        t.setFont(font, lineHeight*.95)
        for str in strs:
            for s in self._textdevider(str, font, lineHeight*.95):
                t.textLine(text=s)
        page.drawText(t)
    def slash(self, page, isBack=False):
        if isBack:
            page.line(self.left, self.bottom+self.height, self.left+self.width, self.bottom)
        else:
            page.line(self.left, self.bottom, self.left+self.width, self.bottom+self.height)
    def drawAround(self, page, flgs=[True,True,True,True]):
        if flgs[0]:
            page.line(self.left, self.bottom, self.left, self.bottom+self.height)
        if flgs[1]:
            page.line(self.left, self.bottom+self.height, self.left+self.width, self.bottom+self.height)
        if flgs[2]:
            page.line(self.left+self.width, self.bottom, self.left+self.width, self.bottom+self.height)
        if flgs[3]:
            page.line(self.left, self.bottom, self.left+self.width, self.bottom)
    def _rotateRct(self, page, deg=45, upside=True):
        page.translate(self.left + self.width/2, self.bottom + self.height/2)
        page.rotate(deg * (1 if upside else -1))
        page.translate(-self.left-self.width/2,-self.bottom-self.height/2)
    def _calcRatate(self, page, str, n, lineheight=40, upside=True):
        if n == 0 or n == len(str):
            return 0
        else:
            a = math.asin((page.stringWidth(str[n-1:n+1])/2)/lineheight)
            return a * 180 / math.pi*(-1)
    def _sumCalcRatate(self, page, str, lineheight=40, upside=True):
        sum = 0.0
        for i in range(len(str)):
            sum += self._calcRatate(page, str, i, lineheight, upside)
        return sum
    def drawRStr(self, page, str, upside=True, n=6):
        x = self.left + self.width / 2
        y = self.bottom + self.height / 2
        r = self.height / 2
        f = r / n
        r1=self.devide(0 if upside else (n-1),1,n)
        r1.drawStr(page, "")
        self._rotateRct(page, self._sumCalcRatate(page, str, (self.height-r1.height)/2)/(-2), upside)
        for i in range(len(str)):
            r1=self.devide(0 if upside else (n-1),1,n)
            self._rotateRct(page, self._calcRatate(page, str, i, (self.height-r1.height)/2), upside)
            r1.drawStr(page, str[i])
            lr = (self.width-page.stringWidth(str[i]))/2
#            r1.shrink(lr,0,lr,0).drawAround(page)
        self._rotateRct(page, self._sumCalcRatate(page, str, (self.height-r1.height)/2)/(-2), upside)


# 600x842
class PubBuilder():
    """
    独自Pdf工場クラス
    """
    pg = None
    JFONT = r"C:\Windows\Fonts\yumin.ttf"
    if not os.path.exists(JFONT):
        response = requests.get("https://moji.or.jp/wp-content/ipafont/IPAfont/ipamp00303.zip")
        zip_data = io.BytesIO(response.content)
        with ZipFile(zip_data, 'r') as zip_ref:
            zip_ref.extract('ipamp00303/ipamp.ttf', tempfile.gettempdir())
        JFONT = os.path.join(tempfile.gettempdir(),'ipamp00303/ipamp.ttf')

    def __init__(self, file="p.pdf", title="test", author="auth", subject="subj", isLandscape=False) :
        if isLandscape:
            self.pg = canvas.Canvas(file, pagesize=landscape(A4))
        else:
            self.pg = canvas.Canvas(file)
        self.pg.setAuthor(title)
        self.pg.setTitle(author)
        self.pg.setSubject(subject)
        pdfmetrics.registerFont(TTFont('GF', self.JFONT))
    def save(self):
        self.pg.save()
    def make(self):
        for i in range(6*6):
            r = Rct().shrink(20,40,20,20).devide(i,6,6)
            r.drawAround(self.pg)
        self.pg.showPage()

