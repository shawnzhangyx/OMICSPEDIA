from django.shortcuts import render,render_to_response
from django.template import RequestContext
# Create your views here.

def page_view(request,**kwargs):
    context = RequestContext(request)
    help_html = 'help/'+kwargs['help_page']+'.html'
    return render_to_response(help_html,context)
