from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from item.models import Item
from django.views import View


class Index(View):
    def get(self, request):
        items = Item.objects.filter(created_by=request.user)

        return render(request, 'dashboard/index.html', {
            'items': items,
        })