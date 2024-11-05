from django.urls import path
from . import views
from .feeds import LatestReportsFeed

app_name = 'recipe'

urlpatterns = [
    path('', views.report_list, name="report_list"),  
    path('tag/<slug:tag_slug>/', views.report_list, name='report_list_by_tag'),
    path("<int:year>/<int:month>/<int:day>/<slug:report>/", views.report_detail, name="report_detail"),
    path('<int:report_id>/share/', views.report_share, name='report_share'),
    path('<int:report_id>/comment/', views.report_comment, name='report_comment'),
    path('feed/', LatestReportsFeed(), name='report_feed'),
    path('search/', views.report_search, name='report_search'),
    path('report/<int:report_id>/rate/', views.rate_report, name='rate_report'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('recipe_book/<int:book_id>/', views.recipe_book_detail, name='recipe_book_detail'),
    path('purchase_recipe_book/<int:book_id>/', views.purchase_recipe_book, name='purchase_recipe_book'),
]