from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from res.resUtil import dictfetchall
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.
# def res_index(request):
    # cursor = connection.cursor()

    # sql = """
    # select res.res_seq, res.mem_seq, res.res_name, res.res_hit, res.res_wdate, mem.mem_name
    # from restaurant res join member mem
    # on res.mem_seq = mem.mem_seq
    # order by res.res_seq desc
    # """

    # cursor.execute(sql)
    # resList = dictfetchall(cursor)
#     return render(request, 'res/res_index.html', {'res_list':resList})

def res_index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    cursor = connection.cursor()

    sql = """
    select res.res_seq, res.mem_seq, res.res_name, res.res_hit, res.res_wdate, mem.mem_name
    from restaurant res join member mem
    on res.mem_seq = mem.mem_seq
    order by res.res_seq desc
    """

    cursor.execute(sql)
    resList = dictfetchall(cursor)
    # 조회

    # 페이징처리
    paginator = Paginator(resList, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    print(page_obj)
    context = {'question_list': page_obj, 'res_list':resList}
    return render(request, 'res/res_index.html', context) #, context



def res_detail(request, res_seq):
    cursor = connection.cursor()

    sql = f"""
    select res_name, res_locate, res_phone, res_content,  res_score, res_hit, res_wdate
    from restaurant
    where res_seq = {res_seq}
    """
    cursor.execute(sql)
    resInfo = dictfetchall(cursor)[0]

    
    sql = f"""
    select res_item_title, res_item_content, res_item_pic, res_item_price
    from res_item
    where res_seq = {res_seq}
    """
    cursor.execute(sql)
    menuList = dictfetchall(cursor)


    sql = f"""
    SELECT mem.mem_id, rev.res_review_title, rev.res_review_content,
    rev.res_review_wdate, rev.res_review_rating
    FROM res_review rev
        JOIN restaurant res
        ON rev.res_seq = res.res_seq
    INNER JOIN member mem
        ON res.mem_seq = mem.mem_seq
    where res.res_seq = {res_seq}
    """
    cursor.execute(sql)
    reviewList = dictfetchall(cursor)
    return render(request, 'res/res_detail.html',  
                  {'resInfo':resInfo, "menuList":menuList, 'reviewList':reviewList})

def res_join_form(request):
    return render(request, 'res/res_join_form.html')





def res_join_save(request):

    mem_id = request.POST.get('mem_id')
    password = request.POST.get('pwd')
    age = request.POST.get('age')
    name = request.POST.get('name')
    cursor = connection.cursor()
    membertype = request.POST.get('membertype')

    print(membertype)
    sql = f"""
    insert into member (
    mem_seq, mem_id, mem_password, mem_google_id, mem_naver_id, mem_type, mem_age, mem_name, mem_wdate, mem_update)
    values(mem_seq.NEXTVAL, '{mem_id}', '{password}', 'N', 'N', 1, '{age}', '{name}', sysdate, sysdate)
    """  
    # cursor.execute(sql)
    # connection.commit()  
    return redirect('res:main')






def main(request):
    return render(request, 'res/res_main.html')

def write(request):
    return render(request, 'res/res_write.html')

def write_save(request):
    title = request.POST.get('title')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    content = request.POST.get('content')
# mem_seq 가져와야함 (작성자 회원정보에서)
    cursor = connection.cursor()
    sql = f"""
    insert into restaurant (res_seq, mem_seq, res_name, res_locate, res_phone, res_content, res_hit, res_wdate)
    values (res_seq.NEXTVAL, mem_seq.NEXTVAL, '{title}', '{address}', '{phone}', '{content}', 0, sysdate)
    
    """
    print(sql)
    cursor.execute(sql)
    connection.commit()
    return redirect('res:index')


    #