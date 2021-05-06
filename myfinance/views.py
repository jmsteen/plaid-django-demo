from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Transaction, Account
from django.shortcuts import render, get_object_or_404, redirect
from .models import Budget, Category, BudgetCategoryAmount, PlaidItem
from .forms import BudgetForm, CategoryForm, BudgetCategoryAmountForm
from django.urls import reverse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import plaid
from plaid import Client
import os
import json
from .secret_keys import PLAID_CLIENT_ID, PLAID_ENV, PLAID_PUBLIC_KEY, PLAID_SECRET
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Sum, Q
import collections
from .utils import categorize_transactions

client = Client(client_id=PLAID_CLIENT_ID,
				secret=PLAID_SECRET,
				environment=PLAID_ENV,
				api_version='2019-05-29')
logged_in = False

def index(request):
	
	latest_budgets = username = latest_transactions = accounts = None
	user = request.user
	global logged_in

	if user.is_authenticated:
		latest_budgets = user.budget_set.order_by('-date'[:5])
		latest_transactions = user.transaction_set.order_by('-date')[:5]
		logged_in = user.is_authenticated
		accounts = user.account_set.order_by('name')
		username = user.username

	data = {
		'latest_budgets': latest_budgets,
		'latest_transactions': latest_transactions,
		'logged_in': logged_in,
		'accounts': accounts,
		'username': username
	}
	return render(request, 'myfinance/index.html', data)

def transactions(request):
	global logged_in

	username = all_transactions = None
	user = request.user

	if user.is_authenticated:
		all_transactions = user.transaction_set.order_by('-date')
		paginator = Paginator(all_transactions, 100)

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		logged_in = user.is_authenticated
		username = user.username

		builtin_categories = Category.objects.filter(custom=False).order_by('description')

	data = {
		'all_transactions': all_transactions,
		'logged_in': logged_in,
		'username': username,
		'page_obj': page_obj,
		'builtin_categories': builtin_categories
	}
	return render(request, 'myfinance/transactions.html', data)

def budget(request, budget_id):
	user = request.user

	if user.is_authenticated:
		budget = user.budget_set.get(id=budget_id)

		categories = Category.objects.order_by('description')
		bcas = None

		bca_set = budget.budgetcategoryamount_set
		if bca_set.exists():
			bcas = {bca.category.id: bca.amount for bca in bca_set.filter(budget=budget_id)}
		budgeted_amts = []

		for cat in categories:
			if bcas and cat.id in bcas:
				child_cat_ids = [ c.id for c in cat.category_set.all() ] 
				
				month = budget.date.month
				year = budget.date.year

				if len(child_cat_ids) > 1:
					# QuerySet of dictionaries
					trans_sum_by_cat = Transaction.objects.filter(date__month=month) \
						.filter(date__year=year) \
						.filter(Q(builtin_category_id=cat.id) | Q(builtin_category_id__in=child_cat_ids)) \
						.values('builtin_category') \
						.annotate(Sum('amount')) \
						.order_by('-amount__sum')
				else:
					trans_sum_by_cat = Transaction.objects.filter(date__month=month) \
						.filter(date__year=year) \
						.filter(builtin_category_id=cat.id) \
						.values('builtin_category') \
						.annotate(Sum('amount')) \
						.order_by('-amount__sum')
					
				cat_dict, cat_sum = {}, 0

				if trans_sum_by_cat.count() > 0:
					cat_sum = 0
					for cat_dict in trans_sum_by_cat:
						cat_sum += cat_dict['amount__sum']

				budgeted_amts.append({ 'category': cat.description, 'amt': bcas[cat.id], 'cat_sum': cat_sum, 'id': cat.id })

	context = {
		'budget': budget,
		'categories': categories,
		'budgeted_amts': budgeted_amts
	}

	return render(request, 'myfinance/budget.html', context)

def budget_new(request):
	# Default to last month's budgeted amounts for each category
	#
	user = request.user
	budgets = user.budget_set

	if user.is_authenticated:
		last_month_budget = budgets.latest('date') if budgets.exists() else None
		last_month_bcas = []

		if last_month_budget:
			bca_set = last_month_budget.budgetcategoryamount_set
			if bca_set.exists():
				last_month_bcas = bca_set.filter(budget_id = last_month_budget.id)

		if request.method == 'POST':
			request_copy = request.POST.copy()
			form = BudgetForm(request_copy)
			form.data['date'] = form.data['date'] + '-01'
			form.data['user'] = user

			if form.is_valid():
				new_budget = form.save()

				for bca in last_month_bcas:
					new_bca = BudgetCategoryAmount(
						category=bca.category,
						budget=new_budget,
						amount=bca.amount
					)
					new_bca.save()

				return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

def budget_delete(request):
	id = request.POST["pk"]
	budget = get_object_or_404(Budget,pk=id)
	budget.delete()

	return HttpResponseRedirect('/')

def category_new(request, budget_id):
	user = request.user

	if user.is_authenticated:
		form = CategoryForm(request.POST)

		budget = user.budget_set.get(id=budget_id)

		new_category = Category(description=request.POST['description'], user=user)
		new_category.save()
		new_budg_cat_amt = BudgetCategoryAmount(
			category=new_category,
			budget=budget,
			amount=0
			)
		new_budg_cat_amt.save()

		return HttpResponseRedirect(reverse('myfinance:budget', args=[budget.id]))
	else:
		return HttpResponseRedirect('/')

def bca_new(request, budget_id):
	user = request.user

	if user.is_authenticated:
		category_id = int(request.POST['category_id'])
		all_budgets = user.budget_set.all()
		if all_budgets.count() > 1:
			last_budget_id=all_budgets[all_budgets.count() - 2].id
			try:
				last_month_bca = get_object_or_404(BudgetCategoryAmount,budget=last_budget_id, category=category_id)
			except:
				last_month_bca = None

		budget = user.budget_set.get(id=budget_id)
		category = Category.objects.get(id=category_id)
		amount = last_month_bca.amount if last_month_bca else 0

		bca = BudgetCategoryAmount(budget=budget, category=category, amount=amount)
		bca.save()

		return HttpResponseRedirect(reverse('myfinance:budget', args=[budget_id]))
	else:
		return HttpResponseRedirect('/')

def bca_delete(request, budget_id, category_id):
	user = request.user
	if user.is_authenticated:
		budget = user.budget_set.get(id=budget_id)
		category = user.category_set.get(id=category_id)
		bca = get_object_or_404(BudgetCategoryAmount,budget=budget, category=category)
		bca.delete()

		return HttpResponseRedirect(reverse('myfinance:budget', args=[budget.id]))
	else:
		return HttpResponseRedirect('/')

def category_edit(request, budget_id, category_id):
	user = request.user
	context = {}

	if user.is_authenticated:
		budget = user.budget_set.get(id=budget_id)
		category = Category.objects.get(id=category_id)
		amount = BudgetCategoryAmount.objects.filter(budget=budget_id, category=category_id).first().amount

		context = {
			'budget': budget,
			'category': category,
			'amount': amount
		}
	return render(request, 'myfinance/category-edit.html', context)

def category_update(request, budget_id, category_id):
	user = request.user
	
	if user.is_authenticated:
		form = BudgetCategoryAmountForm(request.POST)
		amount = request.POST["amount"]
		description = request.POST["description"]
		category = Category.objects.get(id=category_id)
		category.description = description

		bca = BudgetCategoryAmount.objects.filter(budget=budget_id, category=category_id).first()
		bca.amount = amount
	
		if form.is_valid():
			bca.save(update_fields=['amount'])
			category.save(update_fields=['description'])

		return HttpResponseRedirect(reverse('myfinance:budget', args=[budget_id]))
	else:
		return HttpResponseRedirect('/')

@csrf_protect
def link_account(request):
	context = {}
	return render(request, 'myfinance/link-account.html', context)

@ensure_csrf_cookie
def create_link_token(request):
	user = request.user

	if user.is_authenticated:
		data = {
			'user': {
				'client_user_id': str(user.id)
			},
			'products': ["transactions"],
			'client_name': "John's Finance App",
			'country_codes': ['US'],
			'language': 'en'
		}

		response = { 'link_token': client.post('link/token/create', data) }

		link_token = response['link_token']
		return JsonResponse(link_token)
	else:
		return HttpResponseRedirect('/')

def get_access_token(request):
	user = request.user

	if user.is_authenticated:
		body_data = json.loads(request.body.decode())
		public_token = body_data["public_token"]
		accounts = body_data["accounts"]

		exchange_response = \
			client.Item.public_token.exchange(public_token)
		access_token = exchange_response['access_token']
		item_id = exchange_response['item_id']

		user = request.user
		plaid_item = None

		try:
			plaid_item = user.plaiditem_set.get(item_id=item_id)
		except:
			new_plaid_item = PlaidItem(user=user, access_token=access_token, item_id=item_id)
			new_plaid_item.save()
			plaid_item = user.plaiditem_set.get(item_id=item_id)

		for account in accounts:
			try:
				existing_acct = user.account_set.get(plaid_account_id=account['account_id'])
				continue
			except:
				new_acct = Account()
				new_acct.plaid_account_id = account['id']
				new_acct.mask = account['mask']
				new_acct.name = account['name']
				new_acct.subtype = account['subtype']
				new_acct.account_type = account['type']
				new_acct.user = user
				new_acct.item = plaid_item
				new_acct.save()

		# Pretty printing in development
		json.dumps(exchange_response, sort_keys=True, indent=4)
		print(exchange_response)

	return redirect('/')

def get_auth(request):
	user = request.user

	try:
		auth_response = client.post('auth/get', access_token)
	except plaid.errors.PlaidError as e:
		return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
	json.dumps(auth_response, sort_keys=True, indent=4)
	print(auth_response)
	return JsonResponse({'error': None, 'auth': auth_response})

def get_transactions(request):
	user = request.user

	if user.is_authenticated:
		transactions = []
		plaid_items = user.plaiditem_set.all()

		timespan_weeks = 4 * 24 # Plaid only goes back 24 months
		start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(weeks=(-timespan_weeks)))
		end_date = '{:%Y-%m-%d}'.format(datetime.now())

		for item in plaid_items:
			try:
				access_token = item.access_token

				data = {
					'client_id': PLAID_CLIENT_ID,
					'access_token': access_token,
					'secret': PLAID_SECRET,
					'start_date': start_date,
					'end_date': end_date
				}

				response = client.Transactions.get(access_token,
									start_date=start_date,
									end_date=end_date)

				transactions = response['transactions']
					
				accounts = response['accounts']
				error = None

				for account in accounts:
					try:
						existing_acct = user.account_set.get(plaid_account_id=account['account_id'])
						continue
					except:
						new_acct = Account()
						new_acct.plaid_account_id = account['account_id']
						new_acct.balances = account['balances']
						new_acct.mask = account['mask']
						new_acct.name = account['name']
						new_acct.official_name = account['official_name']
						new_acct.subtype = account['subtype']
						new_acct.account_type = account['type']
						new_acct.user = user
						new_acct.save()

				while len(transactions) < response['total_transactions']:
					response = client.Transactions.get(access_token,
											start_date=start_date,
											end_date=end_date,
											offset=len(transactions)
											)
					transactions.extend(response['transactions'])
				
				categorize_transactions(transactions)

				for transaction in transactions:
					try:
						existing_trans = user.transaction_set.get(transaction_id=transaction['transaction_id'])
						builtin_cat = Category.objects.get(pk=transaction['builtin_cat_id'])
						existing_trans.builtin_category = builtin_cat
						existing_trans.save()
						continue
					except Transaction.DoesNotExist:
						new_trans = Transaction()
						new_trans.account = user.account_set.get(plaid_account_id=transaction['account_id'])
						new_trans.account_owner = transaction['account_owner']
						new_trans.amount = transaction['amount']
						new_trans.authorized_date = transaction['authorized_date']

						builtin_cat = Category.objects.get(pk=transaction['builtin_cat_id'])
						new_trans.builtin_category = builtin_cat

						new_trans.category = transaction['category']
						new_trans.category_id = transaction['category_id']
						new_trans.date = datetime.strptime(transaction['date'], '%Y-%m-%d')
						new_trans.iso_currency_code = transaction['iso_currency_code']
						new_trans.location = transaction['location']
						new_trans.merchant_name = transaction['merchant_name']
						new_trans.name = transaction['name']
						new_trans.payment_meta = transaction['payment_meta']
						new_trans.payment_channel = transaction['payment_channel']
						new_trans.pending = transaction['pending']
						new_trans.pending_transaction_id = transaction['pending_transaction_id']
						new_trans.transaction_code = transaction['transaction_code']
						new_trans.transaction_id = transaction['transaction_id']
						new_trans.transaction_type = transaction['transaction_type']
						new_trans.unofficial_currency_code = transaction['unofficial_currency_code']
						new_trans.user = user
						new_trans.save()
			except Exception as e:
				print(e)
				# error = {'display_message': 'You need to link your account.' }
		json.dumps(transactions, sort_keys=True, indent=4)
		return HttpResponseRedirect('/',{'error': error, 'transactions': transactions})
	else:
		redirect('/')

def signup(request):
	
	return render(request, 'myfinance/signup.html',)

def create_user(request):
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username, email, password)

	
	user.save()
	print('User created successfully')
	return HttpResponseRedirect('/log_in_form')

def log_in_form(request):
	return render(request, 'myfinance/log-in.html',)

def log_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
	else:
		print('invalid credentials')
	return HttpResponseRedirect('/', {'username': username})

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def refresh_accounts(request):
	user = request.user
	items = user.plaiditem_set.all()

	for item in items:
		access_token = item.access_token
		response = client.Accounts.get(access_token)

		accounts = response['accounts']
		for account in accounts:
			acc = Account.objects.get(plaid_account_id=account['account_id'])
			acc.balances = account['balances']
			acc.mask = account['mask']
			acc.name = account['name']
			acc.official_name = account['official_name']
			acc.subtype = account['subtype']
			acc.account_type = account['type']
			acc.save()


	return HttpResponseRedirect('/')

def trans_category_update(request):
	user = request.user
	
	if user.is_authenticated:
		body_data = json.loads(request.body.decode())
		trans_id = body_data["trans_id"]
		category_id = body_data["cat_id"]

		category = Category.objects.get(id=category_id)
		trans = Transaction.objects.filter(pk=trans_id).first()
		trans.builtin_category = category
	
		trans.save(update_fields=['builtin_category'])

		return HttpResponseRedirect(reverse('myfinance:transactions'))
	else:
		return HttpResponseRedirect('/')

# Private helper methods

def get_top10_popular_categories():
	past_duration = datetime.now() - timedelta(weeks=12)
	top_cats = Transaction.objects.filter(date__gt=past_duration).values('category').annotate(Sum('amount')).order_by('-amount__sum')
	return top_cats
