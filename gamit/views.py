from django.shortcuts import render, redirect,get_object_or_404, HttpResponseRedirect
import sys, os,re, asyncio,subprocess,random,string,operator
from django.views import generic
from subprocess import *
from multiprocessing import Process, Pipe
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required 

from django.http import JsonResponse, HttpResponse, FileResponse, Http404  
from django.core.paginator import Paginator
import psycopg2,pyproj
from pyproj import Proj, transform, CRS,Transformer
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
sys.path.insert(1, '/home/administrator/soft')
from postgresql import *
from datetime import datetime,date,timedelta
from django.core import serializers
import json
from django.contrib import messages 
from .models import *
from .forms import *
from .tokens import *
from django.contrib.auth.models import User 
from time import strftime, gmtime,time
from django.utils import timezone
from django.views.decorators.http import require_POST
from email.mime.text import MIMEText
import smtplib, pathlib

from functools import reduce
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string



odoo=time()-100
Tatah_date=date.today()
jil = Tatah_date.strftime('%Y') 
Julian = int(Tatah_date.strftime('%j'))


def thanks(request):
    return render(request, "thanks.html")
def sendemail(email, phone, system, text):
    gmail_sender = 'cors@gazar.gov.mn'
    gmail_passwd = '123gazar!@#'
    subject=text
    mail_IT="sumiya@gazar.gov.mn"
    html = """\
            <html>
            <head></head>
            <body>
                <p>Сайн байна уу?<br></p>Таны хариуцсан """+system.upper()+""" системийн талаар
                хэрэглэгчээс дараах хүсэлт ирлээ.<br>
                """+text+"""<br>
                холбоо утас:"""+phone+""" <br>
                имэйл:"""+email+""" <br>
                <br>Хүндэтгэсэн,
                <br>MONGOLIAN POSITIONING SYSTEM
                <br>
                <br>
                <br>Газар зохион байгуулалт, геодези, зураг зүйн газар.
                <br> 51-264596 | E: cors@gazar.gov.mn | www.gazar.gov.mn
                </p>
            </body>
            </html>
            """ 
    part2 = MIMEText(html, 'html', 'utf-8')
    server = smtplib.SMTP_SSL('smtp.gov.mn:465')
    server.login(gmail_sender, gmail_passwd)
    server.sendmail(gmail_sender, mail_IT, part2.as_string())
    server.quit()

def get_ip_address(request):
    """ use requestobject to fetch client machine's IP Address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')    ### Real IP address of client Machine
    return ip  

def station_info(file,text):
	log = open(file,'a+')
	log.write(text)
	log.close()

def header(file, ant_ht,ant_type,dome, rec_type,dir):
	header_file='/Project/django/monpos/logs/monpos_header'+dir+'.txt'	
	os.chdir('/Project/django/monpos/logs')
	crux_type='update_insert:\n'
	station_info(header_file,crux_type)
	cors='O-'+file[0:4].upper()+': \n'
	deltaAnt='"ANTENNA: DELTA H/E/N" : { 0:"'+ant_ht.strip()+'", 1:"0", 2:"0" }\n'
	ant='"ANT # / TYPE" : {1:"'+ ant_type.strip()+'", 2:"'+dome.strip()+'"}\n'
	rec='"REC # / TYPE / VERS" : { 1:"'+rec_type.strip()+'"}\n'
	row=cors+rec+ant+deltaAnt
	station_info(header_file,row)

def randomString(stringLength=4):
    letters = string.ascii_lowercase
    randval=''.join(random.choice(letters) for i in range(stringLength))
    os.system('mkdir /home/administrator/mong/'+randval)
    os.system('mkdir /home/administrator/mong/'+randval+'/rinex')
    os.system('mkdir /home/administrator/mong/'+randval+'/igs')
    os.system('mkdir /home/administrator/mong/'+randval+'/tables')
    os.system('mkdir /home/administrator/mong/' + randval + '/brdc')

    return str(randval)

def dms_to_dd(orolt):
    orolt_utga = orolt.split()
    if(len(orolt_utga) == 1):
        orolt_utga.append('0')
        orolt_utga.append('0')
    if(len(orolt_utga) == 2):
        orolt_utga.append('0')
    garalt = (float(orolt_utga[0]) + float(orolt_utga[1])/60 + float(orolt_utga[2])/3600)
    return str(garalt)

def dd_to_dms(orolt, oron):
    deg = int(float(orolt))
    min = int((float(orolt) - float(deg)) * 60)
    sec = float((float(orolt) - float(deg) - (float(min)/60)) * 3600)
    sec_rounded = str(round(sec, oron))
    return str(str(deg) + " " + str(min) + " " + str(sec_rounded))
####### BILINEAR ARGAAR BODOH FUNCTION#########
##https://rosettacode.org/wiki/Bilinear_interpolation
def bilinear_interpolation(x, y, points):
    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points
    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')
    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
            ) / ((x2 - x1) * (y2 - y1) + 0.0)
###########GARALT############

def base(request):
    syslist = model_system.objects.all()
    context={
        'syslist':syslist
    }
    return render(request, "base.html", context)

def answer(request):
    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('question')
    context ={'form':form}
    return render(request,'answer.html',context)

def monpos(request, *args, **kwargs):
    up_files,site,deactive,ant,rec, year, gnss_list=[],[],[],[],[],[],[]
    # select = "select antenna from antennas order by antenna asc"
    select = "select antenas from antenna order by antenas asc"

    antennas=sqlutga(select,'')
    for antenna in antennas:
        ant.append(antenna[0])
    select = "select receiver from receiver order by receiver asc"
    receivers=sqlutga(select,'')
    for receiver in receivers:
        rec.append(receiver[0])
    select = "select distinct (year) from ref_rinex"
    years=sqlutga(select,'')
    for yr in years:
        year.append(yr[0])
    year.sort()
    select = "select site from ref_coord_cartesian where status=%s"
    sites=sqlutga(select,['mgl'])
    for st in sites:
        site.append(st[0])
    site.sort()
    context= {
        'ant':ant,
        'rec':rec,
        'year':year,
        'site':site,
    }
    if request.method == 'POST':
        os.system('rm /Project/django/monpos/media/*')
        suljee = request.POST.getlist('suljee')
        height = request.POST.getlist('height[]')
        receiver = request.POST.getlist('receiver[]')
        antenna = request.POST.getlist('antenna[]')
        mail = request.POST.getlist('mail')
        antenna = request.POST.getlist('antenna[]')
        add_gnss=request.POST.getlist('gnss')
        gnss_list=['1']+add_gnss    
        unuudur=date.today()
        gnss_list=[''.join(gnss_list)] 
        directory=randomString()
        messages=(mail,gnss_list, antenna, receiver, height, suljee,directory)  
        for count,up_file in enumerate(request.FILES.getlist('myfile[]')):
            if str(up_file).endswith("o") != True and str(up_file).endswith("O") != True: 
                return render(request, 'index.html', {'messages': "Та зөвхөн статик хэмжилтийн файл хуулах ёстой."})      
            else:  
                fs = FileSystemStorage()
                filename = fs.save(up_file.name, up_file)
                ant=antenna[count][0:16].strip()
                dome=antenna[count][-4:].strip()
                header(filename,height[count],ant,dome,receiver[count],directory)
                up_files.append(filename)
        sql_cmd=sql =  "Insert into user_upload (mail, gnss_option, file_name, ant_type, rec_type, height, suljee, upload_date, directory) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        zam='python3 /home/administrator/soft/sd_usno_def.py '+ str(directory) + ' ' + str(gnss_list[0]) + ' ' + str(mail[0])+ ' '+str(suljee[0])
        sqlinsert(sql_cmd,[str(mail),str(gnss_list), str(up_files), str(antenna), str(receiver), str(height), str(suljee), str(unuudur), str(zam)])
        for aa in up_files:
            os.system('/home/administrator/soft/gfzrnx_lx -finp /Project/django/monpos/media/'+ aa + ' -fout /home/administrator/mong/'+directory+'/rinex/::RX2:: -crux /Project/django/monpos/logs/monpos_header'+directory+'.txt -chk -f -q -smp 30 -split 86400 -vo 2')
            #os.system('cp -rf /home/administrator/github/monpos/gamit/media/*.*o )
        os.chdir('/home/administrator/mong/'+directory)
        os.system('chmod 777 -Rf /home/administrator/mong/'+directory)
        gnss_list=' '.join(map(str, gnss_list))
        mail=' '.join(map(str, mail))
        suljee=' '.join(map(str, suljee))
        onlyfiles = [f for f in os.listdir('/home/administrator/mong/'+directory+'/rinex') if f.endswith('o')]
        listfiles=[]
        for file in onlyfiles:
            rinexday=file[4:7]
            rinexyear=2000+int(file[9:11])
            odruud=str(rinexday)
            for file2 in onlyfiles:
                rinexday2=file2[4:7]
                rinexyear2=2000+int(file2[9:11])
                odruud2=str(rinexday2)
                if not odruud in odruud2:
                    return render(request, 'monpos.html', {'messages':'Таны илгээсэн RINEX өгөгдлүүд дотор UTC-ийн тооллоор 1 өдөр хэмжигдээгүй өгөгдөл агуулагдсан тул боловсруулах боломжгүй байна.'})
                    exit()    
            # listfiles.append[odruud]
            rinexheader=file[0:4]
            rinex_date = datetime.strptime(str(rinexyear) +" "+str(rinexday),'%Y %j') 
            curD = datetime.now()
            diff=(curD-rinex_date).days
            if int(diff)<2:
                return render(request, 'monpos.html', {'messages':'Таны илгээсэн RINEX өгөгдлийг боловсруулахад шаардлагатай засварын мэдээллүүд үүсээгүй байна. Дэлгэрэнгүйг https://www.igs.org/products/ хуудаснаас танилцана уу.'})
                exit()
            elif rinexheader in site:
                return render(request, 'monpos.html', {'messages':'Та Монгол Улсын GNSS-ийн байнгын ажиллагаатай станцын сүлжээний өгөгдлийг боловсруулах шаардлагагүй.'})
                exit()
            elif int(diff)<13 and len(gnss_list)>1:
                return render(request, 'monpos.html', {'messages':'Өнөөдрийн байдлаар MONPOS систем таны '+str(file)+' өгөгдлийн GPS-ээс бусад дагуулын мэдээг боловсруулах боломжгүй байна. Дэлгэрэнгүйг https://www.igs.org/products/ хуудаснаас танилцана уу.'})
                exit()
            elif rinexheader in ['XXXX','xxxx']:
                return render(request, 'monpos.html', {'messages':'Таны илгээсэн RINEX өгөгдлийн толгойн мэдээлэл бүрэн бус байна. Дэлгэрэнгүйг https://www.igs.org/formats-and-standards/ хуудаснаас танилцана уу.'})
                exit()        
        for i in ['autcln.cmd', 'itrf08.apr','lfile.apr','process.defaults', 'pole.usno', 'sestbl.', 'sites.defaults','sittbl.','station.info','ut1.usno']:
            os.system('cp /home/administrator/gg/tables/'+str(i) +' tables')
        try:
            #os.system('python3 /home/administrator/soft/sd_usno_def.py '+ str(directory) + ' ' + str(gnss_list[0]) + ' ' + str(mail[0])+ ' '+str(suljee[0]))
            p = subprocess.Popen(['python3', '/home/administrator/soft/sd_usno_def.py', directory, gnss_list, mail, suljee], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as ex:
            return (ex.errno, "", ex.strerror)
        return render(request, 'monpos.html', {'messages':'Таны өгөгдлийг хүлээн авлаа. '+ str(mail) +' хаяг руу үр дүнг хүргүүлнэ.'})
        
        #del request.session
        #return render(request, 'index.html', {'messages':messages})
        
            
    return render(request, "monpos.html",context)

def loadmonitor(request,site, jil):
   #select = "select ((concat(year,'-01-01'))::date + (doy || ' days')::interval)::date ognoo, site, year, doy, x, y, z from monitor WHERE site=%s"
   if str(jil)=='0':
       select="SELECT site, year, doy, (select x from ref_coord_cartesian where site=%s)-x, (select y from ref_coord_cartesian where site=%s)-y, (select z from ref_coord_cartesian where site=%s)-z FROM public.monitor where site=%s order by year asc, doy asc"
       #select = "select year, doy, x, y, z, site FROM monitor WHERE site=%s order by year asc, doy asc"
       antennas=sqlutga(select,[site,site,site,site])
   else:
       select="SELECT site, year, doy, (select x from ref_coord_cartesian where site=%s)-x, (select y from ref_coord_cartesian where site=%s)-y, (select z from ref_coord_cartesian where site=%s)-z FROM public.monitor where site=%s and year=%s order by year asc, doy asc"

       #select = "select year, doy, x, y, z, site FROM monitor WHERE site=%s and year=%s order by doy asc"
       antennas=sqlutga(select,[site,site,site,site,str(jil)])
   list_all=[]
   for anten in antennas:
       year= anten[1]
       doy= anten[2]
       ognoo=datetime(int(year), 1, 1) + timedelta(int(doy) - 1)
       list_all.append({'ognoo':str(ognoo), 'site':anten[0], 'dx':round(anten[3],3), 'dy':round(anten[4],3), 'dz':round(anten[5],3)})
   return HttpResponse(json.dumps(list_all), content_type="application/json")

def xyz2bl(x,y,z):
    inproj = pyproj.Proj("+proj=geocent +datum=WGS84 +units=m +no_defs")
    outproj = pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs")
    val= pyproj.transform(inproj, outproj, x,y,z)
    return([val[0],val[1]])

def xyz2lb(x,y,z):
    inproj = pyproj.Proj("+proj=geocent +datum=WGS84 +units=m +no_defs")
    outproj = pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs")
    val= pyproj.transform(inproj, outproj, x,y,z)
    return([val[1],val[0]])

def monrtk(request):
    active_sites,ccc,zas_sites, deactive_sites,deactive_contact,zaswar_contact, aaa,bbb= [],[],[],[],[],[],[],[]
    cur_cmd = "select site_id from cors_sites where ognoo=%s"
    cur_cors=sqlutga(cur_cmd,['00:00'])
    for cors in cur_cors:
        sqlcmd = "select site,x,y,z from ref_coord_cartesian where id=%s"
        ref_sites=sqlutga(sqlcmd,[cors[0]])
        for ref_site in ref_sites:
            xyz=xyz2lb(ref_site[1],ref_site[2],ref_site[3])
            aaa.append(xyz)
            active_sites.append(ref_site[0])
    zas_cmd = "select site_id from cors_sites where ognoo=%s"
    zas=sqlutga(zas_cmd,['засвартай'])
    for cors in zas:
        sql_contact = "select s.site, c.email_geodesy, c.utas, c.huniii_ner, c.baiguuullaga, t.ognoo, t.timestamp from ftp_email c, ref_coord_cartesian s, cors_sites t where s.id=%s and c.id=s.id and t.site_id=s.id order by t.ognoo desc"
        sqlcmd = "select site,x,y,z from ref_coord_cartesian where id=%s"
        contact1=sqlutga(sql_contact,[cors[0]])
        ref_sites=sqlutga(sqlcmd,[cors[0]])
        zaswar_contact.append({'site':str(contact1[0][0]), 'email':str(contact1[0][1]), 'utas':str(contact1[0][2]),'hunii_ner':str(contact1[0][3]),'baiguullaga':str(contact1[0][4]),'ognoo':str(contact1[0][5]),'time':str(contact1[0][6])})
        for ref_site in ref_sites:
            xyz=xyz2lb(ref_site[1],ref_site[2],ref_site[3])          
            bbb.append(xyz)
            #active=active+(ref_site[0], xyz[0],xyz[1],xyz[2])
    tas_cmd = "select site_id from cors_sites where ognoo<>'00:00' and ognoo<>'засвартай'"
    tasarsan_cors=sqlutga(tas_cmd,[''])
    for cors in tasarsan_cors:
        sql_contact = "select s.site, c.email_geodesy, c.utas, c.huniii_ner, c.baiguuullaga, t.ognoo, t.timestamp from ftp_email c, ref_coord_cartesian s, cors_sites t where s.id=%s and c.id=s.id and t.site_id=s.id order by t.ognoo desc"
        sqlcmd = "select site,x,y,z from ref_coord_cartesian where id=%s"
        contact1=sqlutga(sql_contact,[cors[0]])
        deactive_contact.append({'site':str(contact1[0][0]), 'email':str(contact1[0][1]), 'utas':str(contact1[0][2]),'hunii_ner':str(contact1[0][3]),'baiguullaga':str(contact1[0][4]),'ognoo':str(contact1[0][5]),'time':str(contact1[0][6])})
        ref_sites=sqlutga(sqlcmd,[cors[0]])
        for ref_site in ref_sites:
            xyz=xyz2lb(ref_site[1],ref_site[2],ref_site[3])
            ccc.append(xyz)
    stat, cors = [], []
    sqlcmd = "SELECT site, COUNT(rnx_v2) FROM ref_rinex where year=%s GROUP BY site order by COUNT (rnx_v2) desc"
    print('--------------------------jil---------------------------------', jil)
    count_file=sqlutga(sqlcmd,[jil])
    select_cors = "SELECT site FROM ref_coord_cartesian where status=%s"
    hariuts_cors = "SELECT baiguuullaga FROM ftp_email where id=(select id from ref_coord_cartesian where site=%s)"
    all_cors=sqlutga(select_cors,['mgl'])
    for ref in count_file:
        hariuts=sqlutga(hariuts_cors,[ref[0]])
        stat.append([ref[0],ref[1],int(int(ref[1])*100/int(Julian)),hariuts[0][0]])
        cors.append(ref[0])
    for site in all_cors:
        if not site[0] in cors:
            hariuts=sqlutga(hariuts_cors,[site[0]])
            stat.append([site[0],0,int(0*100/int(Julian)),hariuts[0][0]])
    tas=len(deactive_contact)
    cur=len(active_sites)
    zas=len(zaswar_contact)
    cors_all=cur+tas+zas
    context = {
		'all_sites': cors_all,
		'active_coord':aaa,
		'active_sites':active_sites,
		'zaswar_coord':bbb,
		'zaswar_contact':zaswar_contact,
		'deactive_coord':ccc,
		'deactive_contact':deactive_contact,
		'tas':tas,
		'cur':cur,
		'zas':zas,
		'rinex': stat,
		'doy':Julian,
    }
    return render(request, "monrtk.html", context)

def mongeocalc_hand(request,*args, **kwargs):
    if request.method =='POST':
        inform=inForm(request.POST)
        outform=outForm(request.POST)
        if inform.is_valid() and outform.is_valid():
            sys_in = inform.cleaned_data['sys_in']
            x_in = inform.cleaned_data['x_in']
            y_in = inform.cleaned_data['y_in']
            z_in = inform.cleaned_data['z_in']
            dms_in = inform.cleaned_data['wgs_in']
            sys_out = outform.cleaned_data['sys_out']
            dms_out = outform.cleaned_data['wgs_out']
            dec_format=outform.cleaned_data['dec_out']
            transformer=Transformer.from_crs(CRS.from_epsg(sys_in),CRS.from_epsg(sys_out))
            tr_wgs84=Transformer.from_crs(CRS.from_epsg(sys_in),CRS.from_epsg(4326))
            out = transformer.transform(x_in,y_in,z_in) 
            out_wgs = tr_wgs84.transform(x_in,y_in,z_in)
            x_map,y_map = out_wgs[0], out_wgs[1]
            post = request.POST.copy()
            # x_out = str(round(float(out[0]),int(dec_format)))
            # y_out= str(round(float(out[1]),int(dec_format)))
            # z_out= str(round(float(out[2]),int(dec_format)))
            post['x_out'] = str(round(float(out[0]),int(dec_format)))
            post['y_out'] = str(round(float(out[1]),int(dec_format)))
            post['z_out'] = str(round(float(out[2]),int(dec_format)))
            request.POST = post
            outform = outForm(request.POST)
            return render(request, 'mongeocalc_hand.html',{'inform':inform,'outform':outform,'x_map': x_map, 'y_map': y_map})  
    context={
        'inform':inForm(),
        'outform':outForm()
    }
    return render(request, 'mongeocalc_hand.html',context)
    
def mongeocalc(request,*args, **kwargs):
    if request.method =='POST':
        sys_in = request.POST.get('sys_in')
        sys_out = request.POST.get('id_sys_out')
        x_in = request.POST.get('x_in')
        y_in = request.POST.get('y_in')
        z_in = request.POST.get('z_in')
        dms_in = request.POST.get('id_in_dms')
        dms_out = request.POST.get('id_out_dms')
        dec_format=request.POST.get('decimal_format')  
        transformer=Transformer.from_crs(CRS.from_epsg(sys_in),CRS.from_epsg(sys_out))
        tr_wgs84=Transformer.from_crs(CRS.from_epsg(sys_in),CRS.from_epsg(4326))
        out = transformer.transform(x_in,y_in,z_in) 
        out_wgs = tr_wgs84.transform(x_in,y_in,z_in)
        x_map,y_map = out_wgs[0], out_wgs[1]                             
        post = request.POST.copy()
        post['x_out'] = str(round(float(out[0]),int(dec_format)))
        post['y_out'] = str(round(float(out[1]),int(dec_format)))
        post['z_out'] = str(round(float(out[2]),int(dec_format)))
        request.POST = post
        form = ConvertForm(request.POST)
        return render(request, 'mongeocalc.html', {'form': form,'x_map': x_map, 'y_map': y_map})
    else:
        form = ConvertForm()
        return render(request, 'mongeocalc.html', {'form': form})

def add_question(request):
    ip_address = get_ip_address(request)
    allquestions = Question.objects.all().order_by('-created')
    if request.method == 'POST':
        form_ans=AnswerForm(request.POST)
        asuult_id = request.POST.get("asuult_id")
        form=QuestionForm(request.POST)
        
        if form.is_valid():
            system= form.cleaned_data.get("system")            
            myobj=form.save()
            myobj.userip = str(ip_address)
            myobj.save()
            context={
                'ip':ip_address,
                'system':system,
            }
            # sendemail(str(myobj.email), str(myobj.phone), str(system), str(myobj.asuult))
            return render(request,'thanks.html',context)
        if form_ans.is_valid():
            question= Question.objects.filter(id=asuult_id)
            answer = form_ans.save(commit=False)
            answer.question_id_id = asuult_id
            answer.userip = str(ip_address)
            answer.save()
            form=QuestionForm()
            context={
         'allquestions': allquestions,
         'form':form,
         'form_ans':form_ans
         }
            return render(request, "question.html",context)
      
    form=QuestionForm()
    answer_form = AnswerForm()
    context={
         'allquestions': allquestions,
         'form':form,
         'form_ans':answer_form
         }
    return render(request, "question.html",context)

def CorsDetailView(request):
    if request.user.is_authenticated:
        lfile = model_lfile.objects.filter(status='mgl').order_by('site')
        paginator=Paginator(lfile,4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        index = 0  # edited to something easier without index
        max_index = len(paginator.page_range)
        page_range = list(paginator.page_range)[index:max_index]
        return render(request, 'monstatic.html', {'page_obj': page_obj,'page_range':page_range})
    else:
        return render(request, 'login.html')

def download(request,name):
    if request.method == 'POST':
        date=request.POST.get('datepicker')            
        if date:
            cors_name=str(name)
            date_dt2 = datetime.strptime(date, "%Y-%m-%d")
            shortjil = int(date_dt2.strftime('%y'))
            longjil = int(date_dt2.strftime('%Y'))
            Julian = date_dt2.strftime('%j')
            filename=cors_name+Julian+'0.'+str(shortjil)+'d.Z'
            file_path = os.path.join(settings.DOWNLOAD_ROOT, str(longjil), str(Julian), filename)     
            check_file=pathlib.Path(file_path)
            if check_file.exists():
                data=Statistic(user=request.user,file=filename)
                data.save()
                response = FileResponse(open(file_path, 'rb'))
                return response
            else:
                return redirect('monstatic')

def statistic(request):
    stat = Statistic.objects.all()
    return render(request, "statistic.html",{'stat':stat})

def delete_question(request, id):
    if request.method == 'POST':
        Question.objects.filter(id=id).delete()
        return redirect('question')
    form=QuestionForm()
    answer_form = AnswerForm()
    context={
         'allquestions': allquestions,
         'form':form,
         'form_ans':answer_form
         }
    return render(request, "question.html",context)


@login_required
def logout(request):
    dj_logout(request)
    return redirect('monpos')

def login(request):
    if request.method == 'POST':
        ner = request.POST.get('ner')
        paasuurt = request.POST.get('paasuurt')
        bihenbe = authenticate(username=ner, password=paasuurt)
        if bihenbe:
            dj_login(request, bihenbe)
            return redirect('monpos')
        else:
            messages.error(request, 'Нэр эсвэл нууц үг буруу байна.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        messages.success(request, 'Таны бүртгэл амжилттай идэвхжлээ.')
        return redirect('login')
    else:
        return redirect('index')


def sendmail(email_user, text_user):
    gmail_sender = 'no-reply@gazar.gov.mn'
    gmail_passwd = '123gazar!@#'
    server = smtplib.SMTP_SSL('smtp.gov.mn:465')
    part2 = MIMEText(text_user, 'html', 'utf-8')
    server.login(gmail_sender, gmail_passwd)
    server.sendmail(gmail_sender, email_user, part2.as_string())
    server.quit()

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            if str(user.profile.email).endswith('mn'):
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                sendmail(user.email, message)
                # user.email_user(subject, message)
                messages.success(request, 'Таны цахим хуудас руу бүртгэлийг идэвхжүүлэх холбоосийг илгээлээ.')
                return redirect('login')
            else:
                uprof = Profile.objects.filter(signup_confirmation=False)
                uprof.delete()
                u = User.objects.get(username = user.username)
                u.delete()
                messages.error(request, 'Уучлаарай. Та албан ёсны цахим шуудан (.mn, .gov.mn, .edu.mn) ашиглана уу.')
                form = SignUpForm()
                return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})