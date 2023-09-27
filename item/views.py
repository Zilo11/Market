from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

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
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.is_approved = False

            item.save()
            messages.success(request,'Thank you! Your Product is under review by the administrators, You shall see it in the platform soon')
            
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

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
            return redirect('item_detail', pk=pk)

    # Get items with similar user interactions
    similar_items = Item.objects.filter(reviews__user=request.user).exclude(pk=pk).distinct()

    return render(request, 'item_detail.html', {
        'item': item,
        'reviews': reviews,
        'form': form,
        'similar_items': similar_items
    })
    