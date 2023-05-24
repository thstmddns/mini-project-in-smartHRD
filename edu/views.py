from django.shortcuts import render
#from board.models import Board
from django.db import connection
#from common.commonUtil import dictfetchall, commonPage

# Create your views here.

# def list(request, pg):
#     cursor = connection.cursor()
#     sql = "select count(*) from board_board"
#     cursor.execute(sql)
#     totalCnt = int(cursor.fetchone()[0])
#     cp = commonPage(totalCnt, pg, 10)

#     sql = f"""
#         select A.edu_seq, A.edu_name, A.mem_name, A.edu_score, to_char(A.edu_wdate, 'yyyy-mm-dd') wdate, A.edu_hit, num
#         from 
#         (
#             select edu_seq, edu_name, mem_name, edu_score, wdate, edu_hit, row_number() over(order by wdate desc) num, ceil(row_number() over(order by id desc)/10)-1 pg
#             from board_board
#             -- 검색 조건 필요할 경우에 여기에
#         ) A
#         where A.pg={pg}
#     """
    
#     cursor.execute(sql)
    
#     eduList = dictfetchall(cursor)
#     print(cp)
#     return render(request, "edu/edu_list.html", {'eduList':eduList, "commonPage":cp})


# def detail(request, edu_seq):

#     board = Board.objects.get(edu_seq=edu_seq)
    
#     board.hit = board.hit+1
#     board.save()

#     return render(request, "edu/edu_detail.html", {'eduItem':board})

# from board.forms import BoardForm
# def write(request):
#     return render(request, "board/board_write.html")

# from django.utils import timezone
# from django.shortcuts import redirect    
# def save(request):
    
#     form = BoardForm(request.POST)
    
#     board = form.save(commit=False)   
    
#     board.wdate = timezone.now()
#     board.hit = 0 
#     board.save()
    
#     return redirect("board:list", pg=0)
  
def main(request):
    return render(request, "edu/main.html")
