# from django import template

# register = template.Library()

# @register.filter
# def groupby(value, key):
#     grouped = {}
#     for item in value:
#         group_key = key(item)
#         if group_key in grouped:
#             grouped[group_key].append(item)
#         else:
#             grouped[group_key] = [item]
#     return grouped.items()