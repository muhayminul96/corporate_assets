from django.urls import path
from assets_log.views import *

urlpatterns = [
    path('', home),
    path('get_all_company', get_all_company),
    path('store_company', store_company),
    path('get_all_employee/<company_id>', get_all_employee),
    path('store_employee', store_employee),
    path('get_all_asset/<company_id>', get_all_asset),
    path('store_asset', store_asset),
]
