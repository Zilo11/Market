from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item, FavoriteItem
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse



def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_approved=True, is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

@login_required
def add_to_favorite(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = request.user

    favorite_list, created = FavoriteItem.objects.get_or_create(user=user)
    if item in favorite_list.items.all():
        return JsonResponse({'message': 'Item already in favorites'})

    if favorite_list.counter >= 5:
        return JsonResponse({"message": "Maximum number of items reached"})
    
    favorite_list.items.add(item)
    favorite_list.counter += 1
    favorite_list.save()

    return redirect('item:detail', pk)

@login_required
def remove_from_favorite(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = request.user

    try:
        favorite_list = FavoriteItem.objects.get(user=user)
    except FavoriteItem.DoesNotExist:
        return JsonResponse({'message': 'FavoriteItem does not exist'})

    if item not in favorite_list.items.all():
        return JsonResponse({'message': 'Item not found in favorites'})
    
    if favorite_list.counter <= 0:
        return JsonResponse({"message": "Minimum number of elements reached"})

    favorite_list.items.remove(item)
    favorite_list.counter -= 1
    favorite_list.save()
    return redirect('core:favorite')

    
@login_required
def admin_approval(request):
    if not request.user.is_superuser:
        return redirect('/')  # Redirect to home or any other appropriate page

    if request.method == 'POST':
        items_to_approve = Item.objects.filter(is_approved=False)
        for item in items_to_approve:
            item_id = str(item.id)
            action = request.POST.get('action_' + item_id)
            
            if action == 'approve':
                item.is_approved = True
                item.save()
            elif action == 'delete':
                item.delete()

    items_to_approve = Item.objects.filter(is_approved=False)

    return render(request, 'item/admin_approval.html', {
        'items_to_approve': items_to_approve
    })

            

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:2]
    
    if request.user.is_authenticated:
        favorite = FavoriteItem.objects.get(user=request.user)
        favorite_counter = favorite.counter

        if favorite_counter > 5:
            messages.info(request, 'Your Cart is full.Remove some items to inorder to')

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        # 'favorite_counter': favorite_counter 
    })

# from plyer import notification
# from django.contrib.auth.models import User

# from plyer import notification
# from django.contrib.auth.models import User

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.is_approved = False

            item.save()
            messages.success(request, 'Thank you! Your Product is under review by the administrators. You shall see it on the platform soon.')

            # # Get the users to notify
            # users_to_notify = User.objects.exclude(id=request.user.id)

            # # Send notifications to each user
            # for user in users_to_notify:
            #     send_notification(user.username, item.name, "Has been added on PostMarket, Be the First to see")

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        # 'title': 'New item',
    })

# def send_notification(username, title, message):
#     notification.notify(
#         title=title,
#         message=message,
#         timeout=10,  # Notification duration in seconds
#         app_name=username,  # Use the username as the app_name to ensure unique notifications per user
#         # app_icon=image_path  # Set the image path as the app_icon to display the image in the notification
#     )
    


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.user == item.created_by or request.user.is_superuser:
        item.delete()

    return redirect('core:index')



def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    reviews = item.reviews.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('item:detail', pk=pk)
    else:
        form = ReviewForm()

    # Get items with similar user interactions
    similar_items = Item.objects.filter(reviews__user=request.user).exclude(pk=pk).distinct()

    return render(request, 'item_detail.html', {
        'item': item,
        'reviews': reviews,
        'form': form,
        'similar_items': similar_items
    })
    