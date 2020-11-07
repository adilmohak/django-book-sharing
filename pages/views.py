from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

from .models import Contact, NewsAndEvent
from .forms import ContactForm, NewsAndEventForm

# class HomeView(generic.TemplateView):
#     template_name = 'pages/index.html'


# def home_view(request):
#     return render(request, 'pages/index.html', {})


class ContactCreateView(generic.CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super(ContactCreateView, self).get_context_data(**kwargs)
        if self.request == 'GET':
            context['form'] = ContactForm()
        else:
            context['form'] = ContactForm(self.request.POST)
        return context
    
    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        form = context['form']
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Thank you for the message! We will be in touch very soon.')
            return redirect('pages:contact')

        return super(ContactCreateView, self).form_invalid(form)


class NewsAndEventList(generic.ListView):
    model = NewsAndEvent
    context_object_name = 'items'
    template_name='pages/newsandevent_list.html'
