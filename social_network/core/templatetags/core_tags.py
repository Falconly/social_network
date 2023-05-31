from django import template

register = template.Library()


@register.simple_tag
def get_friend_menu():
    menu = [{'title': 'Друзья', 'url_name': 'core:friends'},
            {'title': 'Заявки', 'dropdowns': [{'title': 'Заявки в друзья', 'url_name': 'core:subs'},
                                              {'title': 'Отправленные заявки', 'url_name': 'core:from_request'},
                                              {'title': 'Отклоненные заявки', 'url_name': 'core:rejected_requests'},
                                              {'title': 'Вами отклоненные заявки', 'url_name': 'core:your_rejected_requests'}
                                              ]}]
    return menu
