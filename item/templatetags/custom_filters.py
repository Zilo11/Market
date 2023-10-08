from django import template

register = template.Library()

@register.filter(name='average_rate')
def average_rate(reviews):
    # Implement your logic to calculate the average rate using the `reviews` queryset
    # Return the average rate value
    
    # Example implementation:
    total = 0
    count = 0
    for review in reviews:
        total += review.rate
        count += 1
    
    if count > 0:
        average = total / count
        return round(average, 2)
    else:
        return 0