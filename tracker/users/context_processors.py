
def get_menu(request):
    return {
        'top_nav': [
            {'title': 'Главная', 'url_name': 'home'},
            {'title': 'Профиль', 'url_name': 'profile'},
            {'title': 'Авторизация', 'url_name': 'users:login'},
            {'title': 'Регистрация', 'url_name': 'users:register'},  # Исправил дублирование названий

        ],
        'side_nav': [
            {'title': 'Привычки', 'url_name': 'habits'},
            {'title': 'Цели', 'url_name': 'goals'},
            {'title': 'Прогресс', 'url_name': 'progress'},
        ]
    }