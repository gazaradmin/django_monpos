from django.forms import ModelForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class uploadFrm(forms.Form):
    title = forms.CharField(max_length=50)
    up_file = forms.FileField()


class ConvertForm(ModelForm):
    class Meta:
        model = Convert
        fields = ('x_in', 'y_in', 'z_in', 'sys_in', 'x_out', 'y_out', 'z_out', 'sys_out',)
        labels = {
            'sys_in': 'Систем:',
            'sys_out': 'Систем:',
            }
        widgets = {
            'sys_in':forms.Select(attrs = {'onchange' : "sysin()"}),
            'sys_out':forms.Select(attrs = {'onchange' : "sysout()"}),
            'x_in': forms.TextInput(attrs={'class':'form-control','placeholder': 'Утга оруулах'}),
            'y_in': forms.TextInput(attrs={'class':'form-control','placeholder': 'Утга оруулах'}),
            'z_in': forms.TextInput(attrs={'class':'form-control','placeholder': 'Утга оруулах'}),
            'x_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            'y_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            'z_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     x_in = cleaned_data.get("x_in")
    #     y_in = cleaned_data.get("y_in")
    #     z_in = cleaned_data.get("z_in")
    #     sys_in = cleaned_data.get("sys_in")
    #     sys_out = cleaned_data.get("sys_out")
    #     if not (x_in and y_in and z_in and sys_in and sys_out):
    #         msg = "Must put 'help' in subject when cc'ing yourself."
    #     return cleaned_data

class inForm(ModelForm):
    class Meta:
        model = Convert
        fields = ('sys_in','wgs_in', 'x_in', 'y_in', 'z_in', )
        labels = {
            'sys_in': 'Систем:',
            'x_in': 'B (dms):',
            'y_in': 'L (dms):',
            'z_in': 'H_ell (m):',
            'wgs_in':'Формат'
            }
        widgets = {
            'sys_in':forms.Select(attrs = {'onchange' : "sysin();"}),
            'x_in': forms.TextInput(attrs={'class':'form-control','placeholder': 'Утга оруулах'}),
            'y_in': forms.TextInput(attrs={'class':'form-control','placeholder': 'Утга оруулах'}),
            'z_in': forms.TextInput(attrs={'class':'form-control','placeholder': 'Утга оруулах'}),
            }
class outForm(ModelForm):
    class Meta:
        model = Convert
        fields = ('sys_out','wgs_out','x_out', 'y_out', 'z_out', 'dec_out')
        labels = {
            'sys_out': 'Систем:',
            'x_out': 'B (dms):',
            'y_out': 'L (dms):',
            'z_out': 'H_ell (m):',
            'wgs_out':'Формат',
            'dec_out':'Орон .?'
            }
        widgets = {
            'sys_out':forms.Select(attrs = {'onchange' : "sysout();"}),
            'x_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            'y_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            'z_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            }

class HardwareForm(ModelForm):
    class Meta:
        model = site_hardware
        fields = ('fid','Receiver','Receiver_SN','Antenna_Radome', 'Last_Data_Available', 'Constellation', 'Data_Center','left','right','north','south')
        labels = {
            'fid':'CORS',
            'Receiver': 'Хүлээн авагч:',
            'Receiver_SN': 'Хувийн дугаар',
            'Antenna': 'Антен',
            'Antenna_Radome': 'Антены бүрхүүл',
            'Last_Data_Available': 'Сүүлийн өгөгдөл',
            'Constellation':'Хиймэл дагуул',
            'Data_Center':'Өгөгдлийн төв',
            'left':'Зүүн талаас',
            'right':'Баруун талаас',
            'north':'Хойд талаас',
            'south':'Урд талаас',
            }
        widgets = {
            'sys_out':forms.Select(attrs = {'onchange' : "sysout();"}),
            'x_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            'y_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            'z_out': forms.TextInput(attrs={'class':'form-control','placeholder': 'Үр дүн'}),
            }

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('system', 'name', 'email', 'phone', 'asuult')
        labels = {
            'system': 'Холбогдох цахим систем:',
            'name': 'Хэрэглэгчийн нэр:',
            'email':'Цахим шуудан',
            'phone':'Холбогдох утас',
            'asuult':'Таны асуулт',
                        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Заавал'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder': ''}),
            'asuult': forms.Textarea (attrs={'class':'form-control','placeholder': '1000 тэмдэгтэд багтаана уу.'}),
            }
class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('answer',)
        labels = {
            'answer': 'Таны хариулт:',
            }
        widgets = {
            'answer': forms.TextInput(attrs={'class':'form-control','placeholder': '1000 тэмдэгтэд багтаана уу.'}),
            }
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Нэр'}))
    last_name = forms.CharField(max_length=12, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Овог'}))
    org = forms.CharField(max_length=12, min_length=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Байгууллага'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Цахим шуудан (.mn, .gov.mn, .edu.mn)'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Нууц үг'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Нууц үг давтах'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Утасны дугаар'}))
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'org','username', 'email', 'password1', 'password2',)