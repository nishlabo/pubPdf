import sys
from pubPdf import PubPdf
import argparse
import datetime

def makeDay(page, r, yr，mt，dy):
		r.drawAround(page)
		r.devide(0, 2, 2).drawStr(page, f"{dy}")

def makepg(page, yr, mt):
	r0=PubPdf.Rct(width=842, height=600).shrink().shrink(20,20,20,20)
	d=datetime.datetime(yr,mt,1)
	li=list(range(0,35))
	i = d.isoweekday()%7
	while d.month==mt:
		r = r0.devide(i,7,5)
		makeDay(page, r, yr, mt, d.day)
		li.remove(i)
		d=d+datetime.timedelta(days=1)
		i = (i+1)%35
	r0.devide(li.pop(0),7,5).drawStr(page, f"{mt}")
	r0.devide(li.pop(0),7,5).devide(1,1,3).drawStr(page, f"{yr}")

if __name__ == "__main__":
	ps=argparse.ArgumentParser()
	ps.add_argument(dest="year", help="年")
	ps.add_argument(dest="month", help="月")
	ps.add_argument('-f', dest="pdffile", default="month.pdf", help="出力ファイル名の指定")
	ps.add_argument('--landscape', dest="isLandscape", action="store_true", help="横向き指定")
	args=ps.parse_args()
	pp=PubPdf.PubBuilder(args.pdffile, isLandscape=True)
	makepg(pp.pg, int(args.year), int(args.month))
	pp.save()
