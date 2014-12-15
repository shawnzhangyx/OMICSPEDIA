from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pagination(list, page, page_limit):
    paginator = Paginator(list, page_limit) 

    try:
        list_out = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_out = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_out = paginator.page(paginator.num_pages)
        
    return list_out 