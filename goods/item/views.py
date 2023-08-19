from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, Category
from .forms import EditItemForm, NewItemForm
from django.views import View

from comment.models import Comment


class Detail(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        comments = Comment.objects.filter(belonging_item=item)[0:1]
        related_item = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
        return render(request, 'item/detail.html', {
            'item': item,
            'related_item': related_item,
            'comments': comments,
        })


class New(View):
    def get(self, request):
        form = NewItemForm()
        return render(request, 'item/form.html', {
        'form': form,
        'title': "New Item",
    })

    def post(self, request):
        if request.method == 'POST':
            form= NewItemForm(request.POST, request.FILES)

            if form.is_valid():
                item = form.save(commit=False)  # situation is get the instance from form but only '
                                                # in memory', not in database. Before save it you want to make some changes:
                item.created_by = request.user
                item.save()

                return redirect('item:detail', pk=item.id)
        
        else:
            form = NewItemForm()

        return render(request, 'item/form.html', {
            'form': form,
            'title': "New Item",
        })


class Edit(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk, created_by=request.user)
        form = EditItemForm(instance=item)
        return render(request, 'item/form.html', {
            'form': form,
            'title': 'Edit Item'
        })
    
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk, created_by=request.user)
        if request.method == 'POST':
            form = EditItemForm(request.POST, request.FILES, instance=item)

            if form.is_valid():
                form.save()

                return redirect('item:detail', pk=item.id)
            
        else :
            form = EditItemForm(instance=item)

        return render(request, 'item/form.html', {
            'form': form,
            'title': 'Edit Item'
        })


class Delete(View):
    
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk, created_by=request.user)
        item.delete()
        return redirect('dashboard:index')


class Items(View):
    def get(self, request):
        query = request.GET.get('query', '')
        category_id = request.GET.get('category', 0)
        categories = Category.objects.all()
        items = Item.objects.filter(is_sold=False)

        if category_id:
            items = items.filter(category_id=category_id)

        if query:
            items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

        return render(request, 'item/items.html', {
            'items': items,
            'query': query,
            'categories': categories,
            'category_id': int(category_id),
        })
