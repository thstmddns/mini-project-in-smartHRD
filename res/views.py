from django.shortcuts import render, redirect
from django.db import connection
from res.resUtil import dictfetchall
from django.utils import timezone

# Create your views here.
def res_index(request):
    cursor = connection.cursor()

    sql = """
    select res.res_seq, res.mem_seq, res.res_name, res.res_hit, res.res_wdate, mem.mem_name
    from restaurant res join member mem
    on res.mem_seq = mem.mem_seq
    order by res.res_seq desc
    """

    cursor.execute(sql)
    resList = dictfetchall(cursor)
    return render(request, 'res/res_index.html', {'res_list':resList})

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
    select mem.mem_id, rev.res_review_title, rev.res_review_content,
    rev.res_review_wdate, rev.res_review_rating
    from res_review rev join member mem
    on rev.res_seq = mem.res_seq
    where res_seq = {res_seq}

    """

    # sql = f"""
    # select B.mem_id, rev.res_review_title, rev.res_review_content,
    # rev.res_review_wdate, rev.res_review_rating
    # from res_review rev join
    #     (select res.res_seq, mem.mem_id
    #     from restaurant res join member mem
    #     on res.res_seq = mem.res_seq
    #     where res_seq = {res_seq}) B
    # on rev.res_seq = B.res_seq
    # """
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
    membertype = request.POST.get('membertype')
    age = request.POST.get('age')
    name = request.POST.get('name')
    cursor = connection.cursor()
    sql = f"""
    insert into member values(mem_req.NEXTVAL, '{mem_id}', '{password}', 'N', 'N', 1, {age}, '윤', sysdate, sysdate)
    """
    cursor.execute(sql)
    connection.commit()

    return redirect('res:main')

def main(request):
    return render(request, 'res/res_main.html')

def write(request):
    return render(request, 'res/res_write.html')