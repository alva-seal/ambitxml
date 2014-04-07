# import minidom xml parser
from xml.dom.minidom import parseString
import argparse
import os.path


parser = argparse.ArgumentParser()
#parser.add_argument('--manlap',nargs='?', type=int)
parser.add_argument('--manlap', default=0)
parser.add_argument('file', nargs='+', type=argparse.FileType('r'))
args = parser.parse_args()

manlap = int(args.manlap)
num_files = len(args.file)

for num_file in range(num_files):
	fo = args.file[num_file]
	print fo.name
	#remove first line and add a root tag
	preamble = fo.readline()
	rawdata = fo.read()
	fo.close()	
	xmldata = parseString(preamble + '<ambit>' + rawdata + '</ambit>')
	bahn = 1
	strokes = 0
	time = 0
	last_time = 0
	duration = 0
	swimstyle = 'undefined'
	xmllist = xmldata.getElementsByTagName('Sample')
	for s in xmllist :
		if  len(s.getElementsByTagName('Lap')) :
			xmlTag = s.getElementsByTagName('Lap')[0].toxml()
			xmlData=xmlTag.replace('<Lap>','').replace('</Lap>','')
			xmlTag = s.getElementsByTagName('Duration')[0].toxml()
			duration=xmlTag.replace('<Duration>','').replace('</Duration>','')
			if manlap == 1 :
				print "Bahn: " + str(bahn) +  " Schlaege: " + str(strokes) + " Time: " + str(duration) + " Stil: " + swimstyle
				bahn += 1
				strokes = 0
		if  len(s.getElementsByTagName('Swimming')) :
			xmlTag = s.getElementsByTagName('Type')[0].toxml()
			xmlData=xmlTag.replace('<Type>','').replace('</Type>','')
			xmlTag = s.getElementsByTagName('Time')[0].toxml()
			xmlData_time=xmlTag.replace('<Time>','').replace('</Time>','')
			if xmlData == 'StyleChange' :
				xmlTag = s.getElementsByTagName('PrevPoolLengthStyle')[0].toxml()
				swimstyle=xmlTag.replace('<PrevPoolLengthStyle>','').replace('</PrevPoolLengthStyle>','')
			
			if xmlData == 'Turn' :
				last_time = time
				time = float(xmlData_time)
				duration = time - last_time
				if manlap !=1 :
					print "Bahn: " + str(bahn) +  " Schlaege: " + str(strokes) + " Time: " + str(duration) + " Stil: " + swimstyle
					bahn += 1
					strokes = 0
			if xmlData == 'Stroke' :
				strokes += 1
