
def get_menu(request):
    return {
        'side_nav': [
            {'title': 'Привычки', 'url_name': 'habits'},
            {'title': 'Цели', 'url_name': 'goals'},
            {'title': 'Прогресс', 'url_name': 'progress'},
        ]
    }