from itertools import chain
from django.views import generic

from django.db.models import Q

from accounts.models import User
from pages.models import NewsAndEvent
from books.models import Book


class SearchView(generic.ListView):
    template_name = 'searchs/search_view.html'
    paginate_by = 20
    count = 0
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if query is not None:
            news_events_results  = NewsAndEvent.objects.search(query)
            user_results      = User.objects.search(query)
            book_results       = Book.objects.search(query)
            
            # combine querysets 
            queryset_chain = chain(
                    news_events_results,
                    user_results,
                    book_results
            )        
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return NewsAndEvent.objects.none() # just an empty queryset as default
