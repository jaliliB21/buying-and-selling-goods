from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Comment
from item.models import Item
from .forms import AddCommentForm


class ShowAllCommentsItem(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        comments = Comment.objects.filter(belonging_item=item)
        form = AddCommentForm()
        return render(request, 'comment/comments.html', {
            'comments': comments,
            'form': form,
            'item': item,
        })
    
    def post(self, request, pk):
        
        item = get_object_or_404(Item, pk=pk)

        if request.method == 'POST':
            form = AddCommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.posted_py = request.user
                comment.belonging_item = item
                comment.save()
                return redirect('comment:comments', pk=item.pk)
        else:
            form = AddCommentForm()

        return render(request, 'comment/comments.html', {
            'form': form,
            'item': item,
        })
        
