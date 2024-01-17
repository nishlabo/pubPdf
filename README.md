"# pubPdf" 

必要なライブラリ
- reportlab
- svglib

こんな感じで
```test
from pubPdf import *
p=pubPdf.PubBuilder("1.pdf")
r=PubPdf.Rct().shrink(20,20,20,20)
r.drawAround(p.pg)
r.devide(12,1,32).drawStr(p.pg, "ABC")
p.save()
exit()
```

これはさすがにダメかも
218行目 JFONT = r"C:\Windows\Fonts\yumin.ttf"
