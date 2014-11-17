import os
import random
import xml.etree.ElementTree as et
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


class LessonView(TemplateView):

    prefix = None
    lesson_name = None
    action_template_name = None

    def get_template_names(self):
        lesson_id = self.kwargs.get('lesson')
        if lesson_id is None:
            return ('{prefix}/{action}'.format(
                prefix=self.prefix, action=self.action_template_name
            ),)
        return ('{prefix}/{name}{id}.html'.format(
            prefix=self.prefix, name=self.lesson_name, id=lesson_id
        ),)

    def get(self, request, *args, **kwargs):
        if kwargs.get('lesson') is None:
            return redirect('home')
        self.request = request
        return super(LessonView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if kwargs.get('lesson') is not None:
            return self.get(request, *args, **kwargs)
        self.request = request
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class BannerocityView(LessonView):

    prefix = 'bannerocity'
    lesson_name = 'bannerocity'
    action_template_name = 'bannerocity.php'

    def get_context_data(self, **kwargs):
        context = super(BannerocityView, self).get_context_data(**kwargs)
        context.update({
            'num': random.randint(1000, 10000),
            'message': self.request.POST.get('message'),
            'zipcode': self.request.POST.get('zipcode'),
            'date': self.request.POST.get('date'),
            'name': self.request.POST.get('name'),
            'phone': self.request.POST.get('phone'),
            'email': self.request.POST.get('email'),
        })
        return context


class BSIView(LessonView):

    prefix = 'bsi'
    lesson_name = 'case2_'
    action_template_name = 'radiocall.php'

    def get_context_data(self, **kwargs):
        context = super(BSIView, self).get_context_data(**kwargs)
        context.update({
            'caller': self.request.POST.get('caller'),
        })
        return context


class DonutView(LessonView):

    prefix = 'donuts'
    lesson_name = 'donuts'
    action_template_name = 'donuts.php'

    def get_context_data(self, **kwargs):
        context = super(DonutView, self).get_context_data(**kwargs)
        context.update({
            'num': random.randint(1000, 10000),
            'name': self.request.POST.get('name'),
            'minutes': self.request.POST.get('minutes'),
            'total': self.request.POST.get('total'),
        })
        return context


class YouCubeView(TemplateView):
    template_name = 'youcube/youcube13.html'


class YouCubeAddView(TemplateView):

    template_name = 'youcube/youcubeadd.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(YouCubeAddView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        fn = finders.find('youcube/blog.xml')
        if fn:
            tree = et.parse(fn)
        else:
            tree = et.fromstring(
                '<?xml version=\"1.0\" encoding=\"utf-8\" ?>'
                '<blog><title>YouCube - The Blog for Cube Puzzlers</title>'
                '<author>Puzzler Ruby</author><entries></entries></blog>'
            )
        root = tree.getroot()
        e = et.Element('entry')
        sub = et.Element('date')
        sub.text = self.request.POST.get('date', '')
        e.append(sub)
        sub = et.Element('body')
        sub.text = self.request.POST.get('body', '')
        e.append(sub)
        image = self.request.POST.get('image')
        if image is not None:
            sub = et.Element('image')
            sub.text = image
            e.append(sub)
        root.find('entries').append(e)
        tree.write(os.path.join(
            settings.BASE_DIR, 'base', 'static', 'youcube', 'blog.xml',
        ))

        return HttpResponse()


class HomeView(TemplateView):
    template_name = 'home.html'


bannerocity = BannerocityView.as_view()
bsi = BSIView.as_view()
donuts = DonutView.as_view()
youcube = YouCubeView.as_view()
youcube_add = YouCubeAddView.as_view()
home = HomeView.as_view()
