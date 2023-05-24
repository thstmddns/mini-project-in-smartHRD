from django.shortcuts import render
from django.db import connection
from res.resUtil import dictfetchall


# Create your views here.
def res_index(request):
    cursor = connection.cursor()

    sql = """
    select res.res_seq, res.mem_seq, res.res_name, res.res_hit, res.res_wdate, mem.mem_name
    from restaurant res join member mem
    on res.mem_seq = mem.mem_seq
    """

    cursor.execute(sql)
    resList = dictfetchall(cursor)
    return render(request, 'res/res_index.html', {'res_List':resList})

def res_detail(request, res_seq, mem_seq):
    cursor = connection.cursor()

    sql = f"""
    select res_name, res_locate, res_phone, res_content,  res_score, res_hit
    from restaurant
    where res_seq = {res_seq} and mem_seq = {mem_seq}
    """
    cursor.execute(sql)
    resInfo = cursor.fetchone()
    print(resInfo)
    
    sql = f"""
    select item.res_item_title, item.res_item_content, item.res_item_pic, item.res_item_price, item.res_item_price
    from res_item item
    where item.res_seq = {res_seq} and item.mem_seq = {mem_seq}
    """

    cursor.execute(sql)
    menuList = dictfetchall(cursor)
    return render(request, 'res/res_index.html',  
                  {'resInfo':resInfo, "menuList":menuList})

