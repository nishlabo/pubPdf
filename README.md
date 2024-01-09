"# pubPdf" 

必要なライブラリ
reportlab
svglib

こんな感じで
>>> import PubPdf
>>> p=PubPdf.PubBuilder("1.pdf")
>>> r=PubPdf.Rct()
>>> r.devide(12,1,32).drawStr(p.pg, "ABC")
>>> p.save()
>>> exit()

これはさすがにダメかも
218行目 JFONT = r"C:\Windows\Fonts\yumin.ttf"
