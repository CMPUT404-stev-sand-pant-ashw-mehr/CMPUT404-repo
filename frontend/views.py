from django.shortcuts import render
from django.views import View

class Index(View):
<<<<<<< HEAD
<<<<<<< HEAD
    def get(self, request, *args, **kwargs):
=======
    def get(self, request):
>>>>>>> 03b29879a368a6a8752038b7ccbe3af6930724d3
=======
    def get(self, request):
>>>>>>> 03b29879a368a6a8752038b7ccbe3af6930724d3
        return render(request, 'frontend/index.html')
    