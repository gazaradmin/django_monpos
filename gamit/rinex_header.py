# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(1, '/home/administrator/soft')
from postgresql import sqlutga, sqlinsert,sqldelete
def addspace(str,str_must):
	str_new=str.ljust(str_must)
	return str_new
def station_info(file,text):
	log = open(file,'a+')
	log.write(text)
	log.close()	

def header(site_infos):
	header_file='/home/administrator/soft/log/monpos_header.txt'	
	os.chdir('/home/administrator/soft/log')
	os.system('rm -rf '+header_file)

	crux_type='update_insert:\n'
	station_info(header_file,crux_type)
	rec=''
	ant=''
	deltaAnt=''
	for row in site_infos:
		deltaAnt='"ANTENNA: DELTA H/E/N" + '+startyeardoy+':'+startepoch+' '+stopyeardoy+':'+stopepoch+' : { 0:"'+ant_ht.strip()+'", 1:"'+ant_e.strip()+'", 2:"'+ant_n.strip()+'" }\n'
		ant='"ANT # / TYPE" : {1:"'+ ant_type.strip()+'", 2:"'+dome.strip()+'"}\n'
		rec='"REC # / TYPE / VERS" : { 1:"'+rec_type.strip()+'"}\n'
	row=rec+ant+deltaAnt
	station_info(header_file,row)
