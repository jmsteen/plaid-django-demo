from django.urls import path

from . import views

app_name = 'myfinance'
urlpatterns = [
    path('', views.index, name='index'),
    path('budget/<int:budget_id>/', views.budget, name='budget'),
    path('budget/<int:budget_id>/category/<int:category_id>/edit', views.category_edit, name='category-edit'),
    path('budget/<int:budget_id>/category/<int:category_id>/update', views.category_update, name='category-update'),
    path('budget/new', views.budget_new, name='budget-new'),
    path('budget/delete', views.budget_delete, name='budget-delete'),
    path('<int:budget_id>/category/new', views.category_new, name='category-new'),
    path('budget/<int:budget_id>/category/<int:category_id>/delete', views.bca_delete, name='bca-delete'),
    path('budget/<int:budget_id>/bca/new', views.bca_new, name='bca-new'),
    path('link_account', views.link_account, name='link-account'),
    path('transactions', views.transactions, name='transactions'),
    path('transactions/get', views.get_transactions, name='get-transactions'),
    path('trans_category_update', views.trans_category_update, name='trans-category-update'),
    path('create_link_token', views.create_link_token, name='create-link-token'),
    path('get_access_token', views.get_access_token, name='get-access-token'),
    path('auth', views.get_auth, name="get-auth"),
    path('signup', views.signup, name="signup"),
    path('create_user', views.create_user, name='create-user'),
    path('log_in', views.log_in, name='log-in'),
    path('log_in_form', views.log_in_form, name='log-in-form'),
    path('log_out', views.log_out, name='log-out'),
    path('refresh_accounts', views.refresh_accounts, name='refresh-accounts')
]