from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wiki.models import Page

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
    
    
def replace_wikilinks(matchobj):
    title = matchobj.group(4)
    try: obj = Page.objects.get(title=title.replace('_', ' '))
    except Page.DoesNotExist: 
        #return '<b>no match</b>'
        return matchobj.group(1)+ ' wikilink-not-exist' + matchobj.group(2) + 'data-toggle="tooltip" title="page does not exist" data-placement="bottom"'  + matchobj.group(3)
    else:
        return matchobj.group(0)