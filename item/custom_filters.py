from django import template

register = template.Library()

@register.filter
def average_rate(reviews):
    total_rating = sum(review.rate for review in reviews)
    count = len(reviews)
    
    if count != 0:
        return total_rating / count
    else:
        return 0