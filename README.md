"# pubPdf" 

必要なライブラリ
- reportlab
- svglib

こんな感じで
```test
from pubPdf.pubPdf import *
p=PubBuilder("1.pdf")
r=Rct().shrink(20,20,20,20)
r.drawAround(p.pg)
r.devide(12,1,32).drawStr(p.pg, "ABC")
p.save()
exit()
```

これはさすがにダメかも
218行目 JFONT = r"C:\Windows\Fonts\yumin.ttf"
バージョン等の関係でDockerのpythonで使っているときは
sed -i -e "s/C:\\\Windows\\\Fonts\\\yumin.ttf/\/usr\/share\/fonts\/opentype\/ipafont-mincho\/ipam.ttf/" /usr/local/lib/python3.12/site-packages/pubPdf/pubPdf.py
