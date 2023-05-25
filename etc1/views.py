from django.shortcuts import render
from etc.models import Etc
from etc_review import etcReview
from etc_item import etcItem
from django.db import connection
from common.commonUtil import dictfetchall, commonPage
from etc.forms import EtcForm

# Create your views here.

def list(request, pg):
    cursor = connection.cursor()
    sql = "select count(*) from board_board"
    cursor.execute(sql)
    totalCnt = int(cursor.fetchone()[0])
    cp = commonPage(totalCnt, pg, 10)

    sql = f"""
        select A.etc_seq, A.etc_name, mem_id, A.etc_score, to_char(A.etc_wdate, 'yyyy-mm-dd') wdate, A.etc_hit, num
        from 
        (
            select etc_seq, etc_name, mem_id, etc_score, wdate, etc_hit, row_number() over(order by wdate desc) num, ceil(row_number() over(order by wdate desc)/10)-1 pg
            from etc
            -- 검색 조건 필요할 경우에 여기에
        ) A
        where A.pg={pg}
    """
    
    cursor.execute(sql)
    
    etcList = dictfetchall(cursor)
    print(cp)
    return render(request, "etc/etc_index.html", {'etcList':etcList, "commonPage":cp})


def detail(request, etc_seq):

    board = Etc.objects.get(etc_seq=etc_seq)
    
    board.hit = board.hit+1
    board.save()
    
    cursor = connection.cursor()
    sql = "select count(*) from "
    cursor.execute(sql)

    sql = f"""
        select A.etc_review_seq, A.etc_review_title, mem_id, A.etc_review_content, to_char(A.etc_review_wdate, 'yyyy-mm-dd') wdate, A.etc_review_rating, num
        from 
        (
            select etc_review_seq, etc_review_title, mem_id, etc_review_content, wdate, etc_review_rating, row_number() over(order by wdate desc) num, ceil(row_number() over(order by wdate desc)/10)-1 pg
            from etc_review
            -- 검색 조건 필요할 경우에 여기에
        ) A
        where A.pg={etc_review_seq}
    """
    
    cursor.execute(sql)
    
    etcReviewList = dictfetchall(cursor)

    cursor = connection.cursor()
    sql = "select count(*) from "
    cursor.execute(sql)

    sql = f"""
        select A.etc_item_seq, A.etc_item_title, mem_id, A.etc_item_content, to_char(A.etc_item_wdate, 'yyyy-mm-dd') wdate, A.etc_item_price, num
        from 
        (
            select etc_item_seq, etcitemw_title, mem_id, etc_item_content, wdate, etc_item_price, row_number() over(order by wdate desc) num, ceil(row_number() over(order by wdate desc)/10)-1 pg
            from etc_item
            -- 검색 조건 필요할 경우에 여기에
        ) A
        where A.pg={etc_item_seq}
    """
    
    cursor.execute(sql)
    
    etcItemList = dictfetchall(cursor)


    return render(request, "etc/etc_detail.html", {'etcReviewList':etcReviewList, 'etcReviewItem':board, 'etcItemList':etcItemList, })


def write(request):
    return render(request, "etc/etc_write.html")

from django.utils import timezone
from django.shortcuts import redirect    

def save(request):
    
    form = EtcForm(request.POST)
    
    board = form.save(commit=False)   
    
    board.wdate = timezone.now()
    board.hit = 0 
    board.save()
    
    return redirect("board:list", pg=0)
  
def main(request):
    return render(request, "etc/main.html")

# @login_required
def delete(request, etc_item_seq):
    content = get_object(request, etc_item_seq)
    content.delete()
    return redirect("etc/index")

