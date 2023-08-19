from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm


class NewConversation(View):
    def get(self, request, item_pk):
        item = get_object_or_404(Item, pk=item_pk)

        if item.created_by == request.user:
            return redirect('dashboard:index')
        
        conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

        if conversations:
            return redirect('conversation:inbox')
        
        form = ConversationMessageForm()

        return render(request, 'conversation/new.html', {
            'form': form
        })
    
    def post(self, request, item_pk):
        item = get_object_or_404(Item, pk=item_pk)

        if request.method == 'POST':
            form = ConversationMessageForm(request.POST)

            if form.is_valid():
                conversation = Conversation.objects.create(item=item)
                conversation.members.add(request.user)
                conversation.members.add(item.created_by)

                conversation_message = form.save(commit=False)
                conversation_message.conversation = conversation
                conversation_message.created_by = request.user
                conversation_message.save()

                return redirect('item:detail', pk=item_pk)
        else:
            form = ConversationMessageForm()

        return render(request, 'conversation/new.html', {
            'form': form
        })


class Inbox(View):
    def get(self, request):
        conversations = Conversation.objects.filter(members__in=[request.user.id])

        return render(request, 'conversation/inbox.html', {
            'conversations': conversations
        })
    


class Detail(View):
    def get(self, request, pk):
        conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
        form = ConversationMessageForm()
        return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
        })
    
    def post(self, request, pk):
        conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

        if request.method == 'POST':
            form = ConversationMessageForm(request.POST)

            if form.is_valid():
                conversation_message = form.save(commit=False)
                conversation_message.conversation = conversation
                conversation_message.created_by = request.user
                conversation_message.save()
                conversation.save()

                return redirect('conversation:detail', pk=pk)
        else:
            form = ConversationMessageForm()


        return render(request, 'conversation/detail.html', {
            'conversation': conversation,
            'form': form,
        }) 