from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView, DeleteView

from .models import Report,ReportRevision
from .forms import ReportForm
# Create your views here.

class IndexView(ListView):
    model = Report
    template_name = "meta/index.html"
    context_object_name = "report_list"

class ReportNew(CreateView):
    template_name = "meta/report_new.html"
    form_class = ReportForm
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        new_revision = ReportRevision(content=self.request.POST['content'], report=form.instance,
                author=self.request.user)
        new_revision.save()
        form.instance.current_revision=new_revision
        return super(ReportNew, self).form_valid(form)

class ReportEdit(UpdateView):
    form_class = ReportForm
    template_name = 'meta/report_new.html'
    def get_object(self):
        return Report.objects.get(pk=self.kwargs['pk'])

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs['initial'].update({'content':self.object.current_revision.content})
        return form_class(**kwargs)

    def form_valid(self, form):
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
        #context['comment_list'] = ReplyPost.objects.filter(mainpost=context['mainpost'])
        return context

