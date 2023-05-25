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
    print( totalCnt, pg ) 

    cp = commonPage(totalCnt, pg, 10)

    sql = """select edu.edu_name, edu.edu_score, edu.edu_hit, 
    edu.edu_wdate, mem.mem_id, num
    from member mem join edu
    on mem.mem_seq = edu.mem_seq """

    sql = f"""
        select A.mem_seq, A.edu_name, A.edu_score, A.edu_hit,
            to_char(A.edu_wdate, 'yyyy-mm-dd') edu_wdate, A.mem_id, num
        from 
        (
            select  A.mem_seq, A.edu_name, 
                    A.edu_score, A.edu_hit, 
                    A.edu_wdate, B.mem_id,
                    row_number() over(order by A.edu_wdate desc) num,
                    ceil(row_number() over(order by A.edu_wdate  desc)/10)-1 pg
            from edu A 
            left outer join member B on A.mem_seq=B.mem_seq
            -- 검색 조건 필요할 경우에 여기에
        ) A
        where A.pg={pg}
    """
    # 캐싱(데이터 검색 효율성을 높이는)을 위해 별칭 사용(A)
    cursor.execute(sql)
    #print(dictfetchall(cursor))


    # Board 모델 클래스 안에 objects 요소가 부모클래스에 존재
    # boardList = Board.objects.all()
    boardList = dictfetchall(cursor)
    print(boardList)
    return render(request, "edu/edu_index.html", {'eduList':boardList, "commonPage":cp})





    cursor = connection.cursor()
    sql = """select edu.edu_name, edu.edu_score, edu.edu_hit, 
    edu.edu_wdate, mem.mem_id
    from member mem join edu
    on mem.mem_seq = edu.mem_seq """
    cursor.execute(sql)
    eduList = dictfetchall(cursor)
    print(eduList)
    

    return render(request, "edu/edu_index.html", {'eduList':eduList})


# def detail(request, edu_seq):

#     board = Edu.objects.get(edu_seq=edu_seq)
    
    # board.hit = board.hit+1
    # board.save()
    
    # cursor = connection.cursor()
    # sql = "select count(*) from "
    # cursor.execute(sql)

    # sql = f"""
    #     select A.edu_review_seq, A.edu_review_title, mem_id, A.edu_review_content, to_char(A.edu_review_wdate, 'yyyy-mm-dd') wdate, A.edu_review_rating, num
    #         from 
    #         (
    #             select edu_review_seq, edu_review_title, mem_id, edu_review_content, wdate, edu_review_rating, row_number() over(order by wdate desc) num, ceil(row_number() over(order by wdate desc)/10)-1 pg
    #             from edu_review
    #             -- 검색 조건 필요할 경우에 여기에
    #         ) A
    #         where A.pg={edu_review_seq}
    #     """
        
    #     cursor.execute(sql)
        
    #     eduReviewList = dictfetchall(cursor)

    #     cursor = connection.cursor()
    #     sql = "select count(*) from "
    #     cursor.execute(sql)

    #     sql = f"""
    #         select A.edu_item_seq, A.edu_item_title, mem_id, A.edu_item_content, to_char(A.etc_item_wdate, 'yyyy-mm-dd') wdate, A.edu_item_price, num
    #         from 
    #         (
    #             select edu_item_seq, edu_item_title, mem_id, edu_item_content, wdate, edu_item_price, row_number() over(order by wdate desc) num, ceil(row_number() over(order by wdate desc)/10)-1 pg
    #             from edu_item
    #             -- 검색 조건 필요할 경우에 여기에
    #         ) A
    #         where A.pg={edu_item_seq}
    #     """
        
    #     cursor.execute(sql)
        
    #     eduItemList = dictfetchall(cursor)

#     return render(request, "edu/edu_detail.html", 'eduReviewList':eduReviewList, 'eduReviewItem':board, 'eduItemList':eduItemList, )


# def write(request):
#     return render(request, "edu/edu_write.html")

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

def delete(request, edu_item_seq):
    content = get_object(request, edu_item_seq)
    content.delete()
    return redirect("edu/index")
