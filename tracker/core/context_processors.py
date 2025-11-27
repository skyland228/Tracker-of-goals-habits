
def get_menu(request):
    return {
        'side_nav': [
            {'title': 'Привычки', 'url_name': 'habits'},
            {'title': 'Основные Цели', 'url_name': 'general_goals'},
            {'title': 'Подцели', 'url_name': 'temporal_goals'},
        ]
    }