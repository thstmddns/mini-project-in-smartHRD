from django.shortcuts import render, redirect
from django.http import JsonResponse
from member.models import Member 

from member.forms import MemberForm
from django.utils import timezone
# Create your views here.
# path("write", views.write), #회원가입폼으로 이동
# path("save", views.save),  #회원가입
# path("idcheck", views.idcheck), #아이디중복체크
# path("logon", views.logon), #페이지이동용
# path("logout", views.logout),#페이지이동용
# path("logon_proc", views.logon_proc),#로그온처리
# path("logout_proc", views.logout_proc),#로그아웃처리
def write(request):
    return render(request, "member\member_write.html")

def logon(request):
    return render(request, "member\logon.html")

def logout(request):
    return render(request, "member\logout.html")

def logon_proc(request):
    try:
        memberForm = MemberForm(request.POST)
        member = memberForm.save(commit=False) 
        member.wdate = timezone.now()
        member.save()
        result = {"result":"success"}
    except Exception as ex:
        print(ex)
        result = {"result":"fail"}

    return JsonResponse(result)

def save(request):
    print(123456789)
    try:
        mem_id = request.POST.get("mem_id")
        mem_password = request.POST.get("mem_password")
        mem_password= request.POST.get("mem_id")
        mem_google_id= request.POST.get("mem_google_id")
        mem_naver_id= request.POST.get("mem_naver_id")
        mem_type= request.POST.get("mem_type")
        mem_age= request.POST.get("mem_age")
        mem_name= request.POST.get("mem_name")
        mem_wdate= request.POST.get("mem_wdate")
        mem_update= request.POST.get("mem_update")
        
        sql = f"""
        INSERT INTO member(
            mem_seq,
            mem_id,
            mem_password,
            mem_google_id,
            mem_naver_id,
            mem_type,
            mem_age,
            mem_name,
            mem_wdate,
            mem_update)
         VALUES(
            mem_seq.next,
            '{mem_id}',
            '{mem_password}',
            '{mem_google_id}',
            '{mem_naver_id}',
            '{mem_type}',
            '{mem_age}',
            '{mem_name}',
            '{mem_wdate}',
            '{mem_update}'
               ) """
        print(sql)
        
        
        #세션에 저장해야 한다 
        result = {"result":"success"}
    except Exception as e:
        print(e)
        result = {"result":"fail"} #아이디 안쓰고 있음 사용가능 
    return JsonResponse(result)

def logout_proc(request):
    request.session["mem_id"] = None
    request.session["mem_name"] = None
    # request.session["email"] = None
    result = {"result":"success"}
    return redirect("edu:main")
 

def idcheck(request):
    mem_id = request.POST.get("mem_id")
    print(mem_id)
    #디비에가서 확인 
    try:
        Member.objects.get(mem_id=mem_id) #이미 사용중인 아이디임 사용못함
        result = {"result":"fail"}
    except:
        result = {"result":"success"} #아이디 안쓰고 있음 사용가능 
    return JsonResponse(result)
"""
insert into member_member(id, userid, password, username, email, phone, wdate)
values(1, 'test', '1234', '홍길동', 'hong@hanmail.net', '010-0000-0000', sysdate);
commit;
"""
