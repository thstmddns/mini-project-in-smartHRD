from django import forms 

#모델클래스를 import 해야 한다 
#from 폴더명.파일명 import 클래스명 
from member.models import Member
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member 
        fields = ['mem_id', 'mem_name', 'mem_password', 'mem_type', 'mem_age', 'mem_name']
        labels = {'mem_id':'아이디', 
                  'mem_password':'패스워드',
                  'mem_type':'회원유형',
                  'mem_age':'나이',
                  'mem_name':'이름'}