from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
# specific imports
from .models import Report,ReportRevision
from .forms import ReportForm, ReportRevisionForm
# Create your views here.

class IndexView(ListView):
    #model = Report
    template_name = "meta/index.html"
    context_object_name = "report_list"
    paginate_by = 25
    
    def get_queryset(self):
        tab = self.request.GET.get('tab') or 'Active'
        if tab == 'Active':
            return Report.objects.filter(status=0)
        elif tab == 'Closed':
            return Report.objects.filter(status=2)
            
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab') or 'Active'
        context['total'] = Report.objects.all().count()
        context['open'] = Report.objects.filter(status=0).count()
        context['closed'] = Report.objects.filter(status=2).count()
        
        return context

class ReportNew(CreateView):
    template_name = "meta/report_new.html"
    form_class = ReportForm
    
    @method_decorator(permission_required("meta.add_report",login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(ReportNew, self).dispatch(*args, **kwargs)
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        new_revision = ReportRevision(content=self.request.POST['content'], report=form.instance,
                author=self.request.user)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(ReportNew, self).form_valid(form)

class ReportEdit(UpdateView):
    form_class = ReportRevisionForm
    template_name = 'meta/report_new.html'
    
    @method_decorator(permission_required("meta.change_report",login_url="/accounts/email-verification/"))
    def dispatch(self, *args, **kwargs):
        return super(ReportEdit, self).dispatch(*args, **kwargs)
        
    def get_object(self):
        return Report.objects.get(pk=self.kwargs['pk'])

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'content':self.object.current_revision.content})
        return form_class(**kwargs)

    def form_valid(self, form):
        if form.cleaned_data['content'] != self.object.current_revision.content:
            new_revision = ReportRevision(content=self.request.POST['content'],
                       revision_summary=self.request.POST['summary'], report=self.object,
                       author=self.request.user)
            new_revision.save()
            self.object.current_revision=new_revision
            self.object.save()
        return super(ReportEdit, self).form_valid(form)


class ReportDetails(DetailView): 
    template_name = "meta/report_detail.html"
    model = Report
    context_object_name = "report"

    def get_object(self):
        obj = super(ReportDetails, self).get_object()
        Report.update_report_views(obj, request=self.request)
        return obj
    def get_context_data(self, **kwargs):
        context = super(ReportDetails, self).get_context_data(**kwargs)
        tab = self.request.GET.get('tab')
        if not tab:
            tab = 'votes'
        
        sort_dict = {'votes':'-vote_count','oldest':'created'}
        sort_value = sort_dict[tab]
        context['comments'] = context['report'].get_comments().order_by(sort_value)
        context['tab'] = tab

        return context

