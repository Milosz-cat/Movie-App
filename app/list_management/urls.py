from django.urls import path
from . import views


urlpatterns = [
    path("list/<str:name>/", views.list_movies, name="list"),
    path(
        "rate_movie/<str:title>/<str:year>/<int:rating>/",
        views.rate_movie,
        name="rate_movie",
    ),
    path("ranking/<str:name>/", views.ranking, name="ranking"),
    path("best_picture", views.best_picture, name="best_picture"),
    path("add_list/<str:type>/", views.add_list, name="add_list"),
    path("choose_list", views.choose_list, name="choose_list"),
    path("person_choose_list", views.person_choose_list, name="person_choose_list"),
    path(
        "add_to_list/<str:movie_title>/<int:movie_year>/<str:name>/",
        views.add_to_list,
        name="add_to_list",
    ),
    path("person_list/<str:name>", views.person_list, name="person_list"),
    path(
        "add_person_to_list/<str:name>/<int:id>",
        views.add_person_to_list,
        name="add_person_to_list",
    ),
    path("remove_list/<str:name>/<str:type>", views.remove_list, name="remove_list"),
    path(
        "remove_from_list/<str:name>/<str:type>/<int:id>",
        views.remove_from_list,
        name="remove_from_list",
    ),
]
