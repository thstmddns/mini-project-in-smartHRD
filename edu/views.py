from django.shortcuts import render
#from edu.models import Edu
# from edu_review import eduReview
# from edu_item import eduItem
from django.db import connection

from common.CommonUtils import dictfetchall, commonPage
# from django.core.paginator import Paginator
#from edu.forms import EduForm

# # Create your views here.



def index(request, pg):
    cursor = connection.cursor()
    sql = "select count(*) from edu"
    cursor.execute(sql)
    totalCnt = int(cursor.fetchone()[0])
    
    search_tag = request.GET.get('search', '')
    cp = commonPage(totalCnt, pg, 10)

    sql = f"""
        select A.mem_seq, A.edu_seq, A.edu_name, A.edu_score, A.edu_hit,
            to_char(A.edu_wdate, 'yyyy-mm-dd') edu_wdate, A.mem_id, num
        from 
        (
            select  A.mem_seq, A.edu_seq, A.edu_name, 
                    A.edu_score, A.edu_hit, 
                    A.edu_wdate, B.mem_id,
                    row_number() over(order by A.edu_wdate desc) num,
                    ceil(row_number() over(order by A.edu_wdate  desc)/10)-1 pg
            from edu A 
            left outer join member B on A.mem_seq=B.mem_seq
            where A.edu_name like '%{search_tag}%'
            -- 검색 조건 필요할 경우에 여기에
        ) A
        where A.pg={pg}
    """
    
    cursor.execute(sql)
    
    boardList = dictfetchall(cursor)

    return render(request, "edu/edu_index.html", {'eduList':boardList, "commonPage":cp})


def edu_detail(request, edu_seq):
    cursor = connection.cursor()

    sql = f"""
    select edu_name, edu_locate, edu_phone, edu_content,  edu_score, edu_hit, edu_wdate
    from edu
    where edu_seq = {edu_seq}
    """
    cursor.execute(sql)
    eduInfo = dictfetchall(cursor)[0]
    print(eduInfo)
    sql = f"""
    select edu_item_title, edu_item_content, edu_item_pic, edu_item_price
    from edu_item
    where edu_seq = {edu_seq}
    """
    cursor.execute(sql)
    eduList = dictfetchall(cursor)

    sql = f"""
    SELECT C.mem_id, A.edu_review_title, A.edu_review_content,
    A.edu_review_wdate, A.edu_review_rating
    FROM edu_review A
        JOIN edu B
        ON A.edu_seq = B.edu_seq
    INNER JOIN member C
        ON B.mem_seq = C.mem_seq
    where B.edu_seq = {edu_seq}
    """
    cursor.execute(sql)
    eduReList = dictfetchall(cursor)
    print(eduReList)
    return render(request, 'edu/edu_detail.html',  
                  {'eduInfo':eduInfo, "eduList":eduList, 'eduReList':eduReList})


def write(request):
    return render(request, "edu/edu_write.html")

# from django.utils import timezone
from django.shortcuts import redirect    

# def save(request):
    
#     form = EduForm(request.POST)
    
#     board = form.save(commit=False)   
    
#     board.wdate = timezone.now()
#     board.hit = 0 
#     board.save()
    
#     return redirect("board:list", pg=0)
  
def main(request):
    return render(request, "edu/main.html")

# def delete(request, edu_item_seq):
#     content = get_object(request, edu_item_seq)
#     content.delete()
#     return redirect("edu/index")

def login(request):
    return render(request, "edu/login.html")
