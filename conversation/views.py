from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation

from django.contrib import messages
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:inbox')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Send notification to the sender
            sender = request.user
            sender_notification_text = f"Your message regarding item {item} has been sent."
            send_notification(sender, sender_notification_text)

            # Send notification to the recipient
            recipient = item.created_by
            recipient_notification_text = f"You have a new message regarding item {item}."
            send_notification(recipient, recipient_notification_text)

            messages.success(request, "Message sent successfully.")
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form
    })
from plyer import notification

def send_notification(user, message):
    notification.notify(
        title='New Message',
        message=message,
        app_icon=None,  # You can provide an icon file path here if desired
        timeout=10,  # The notification will automatically disappear after 10 seconds
    )

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
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
        'form': form
    })
    
    
    
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_message_to_conversation(conversation_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'conversation_{conversation_id}',
        {
            'type': 'conversation.message',
            'message': message
        }
    )
    
from django.http import HttpResponse

def websocket_consumer(request, conversation_id):
    # Implement the desired behavior for handling WebSocket connections
    # You can access the conversation_id parameter and perform actions accordingly
    
    # Example: Return a simple message with the conversation_id
    message = f"WebSocket connection established for conversation ID: {conversation_id}"
    return HttpResponse(message)
    