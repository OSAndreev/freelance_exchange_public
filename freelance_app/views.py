import django_filters
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from datetime import date

from .models import *
from .serializers import *
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import *

def start_page(request):
    return render(request, 'start.html')
### Никитины
def freelancer_main_page(request):
    user_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    freelancer = Freelancer.objects.get(user_id=user_id)
    offers = Offers.objects.filter(freelance_variety=freelancer)
    queryset = Order.objects.filter(in_work=0)

    q_list = list(Order.objects.filter(in_work=0).values_list('id', flat=True))
    of_list = list(Offers.objects.filter(freelance_variety=freelancer).values_list('details', flat=True))
    took = []

    for i in q_list:
        if (i in of_list):
            took.append(True)
        else:
            took.append(False)


    balance = check_my_balance(user_id)

    return render(request, 'order_list.html', {'object_list': zip(queryset, took), 'offers_list': offers, 'balance': balance})

def update_deal_history(pk):
    order = Order.objects.get(id=pk)
    deal = DealHistory.objects.create(from_who=order.customer.user_id, to_who=order.performer.user_id, order=order)
    deal.save()

def refuse_offer(request, pk):
    order = Order.objects.get(pk=pk)
    Offers.objects.filter(details=order).delete()
    return redirect('freelancer_main_page')

def update_offers(request,pk):
    order = Order.objects.get(pk=pk)
    user_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    freelancer = Freelancer.objects.get(user_id=user_id)
    new_offer = Offers.objects.create(details=order, freelance_variety=freelancer, take=False)
    new_offer.save()

    return redirect('freelancer_main_page')

def freelancer_my_works(request, pk=''):
    user_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    freelancer = Freelancer.objects.get(user_id=user_id)
    queryset = Order.objects.filter(in_work=1, performer=freelancer)
    form = WorkReadyForm()
    if request.method == 'POST':
        form = WorkReadyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            work_form = cd.get('work_form')
            degree = cd.get('degree')
            try:
                order = Order.objects.get(pk=pk)
                if order.degree_to_company is None and order.done:
                    order.degree_to_company = degree
                else:
                    order.work_ready = work_form
                order.save()
                update_customer_degree(order.customer)
                return redirect('my_works')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('Не валид')


    work_ready_list = list(Order.objects.filter(performer=freelancer).values_list('work_ready', flat=True))
    rejected = []

    for i in work_ready_list:
        if i != None and " is not accepted." in i:
            rejected.append(True)
        else:
            rejected.append(False)
    print(rejected)
    object_list = zip(queryset, rejected)
    return render(request,'my_works.html', {"object_list": object_list, "form" : form, "balance":
                                            check_my_balance(user_id)})

def update_customer_degree(customer):
    all_degrees = list(Order.objects.filter(customer=customer).values_list('degree_to_company', flat=True))
    print(all_degrees)
    all_d = []
    for i in all_degrees:
        if i != None:
            all_d.append(i)

    if all_d != []:
        degree = round(sum(all_d) / len(all_d))
        customer.degree = degree
        customer.save()
#### Никитины

def customer_main_page(request, pk=''):
    userdata_id = get_object_or_404(UserData, django_user_id=request.user.id)
    customer_id = get_object_or_404(Customer, user_id=userdata_id)
    queryset = Order.objects.filter(customer_id=customer_id)
    form = WorkReadyForm()
    if request.method == 'POST':
        form = WorkReadyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            degree = cd.get('degree')
            try:
                order = Order.objects.get(pk=pk)
                if order.degree_to_performer is None and order.done is True:
                    order.degree_to_performer = degree
                    order.save()
                performer = Order.objects.get(pk=pk)
                update_performer_degree(performer.performer)
                return redirect('customer_main_page')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('Не валид')



    work_ready_list = list(Order.objects.filter(customer=customer_id).values_list('work_ready', flat=True))
    rejected = []
    print(work_ready_list)

    balance = check_my_balance(customer_id.user_id)
    for i in work_ready_list:
        if i != None and " is not accepted." in i:
            rejected.append(True)
        else:
            rejected.append(False)

    orders_id_list = list(Order.objects.filter(customer=customer_id).values_list('id', flat=True))
    offered = []
    for j in orders_id_list:
        try:
            Offers.objects.get(details=Order.objects.get(id=j))
            offered.append(False)
        except:
            offered.append(True)
    object_list = zip(queryset, rejected, offered)
    return render(request, 'customer_main_page.html', {'object_list': object_list, 'form': form, 'balance': balance})

def update_performer_degree(performer):
    all_degrees = list(Order.objects.filter(performer=performer).values_list('degree_to_performer', flat=True))
    print(all_degrees)
    all_d = []
    for i in all_degrees:
        if i != None:
            all_d.append(i)

    if all_d != []:
        degree = round(sum(all_d) / len(all_d))
        performer.degree = degree
        performer.save()


def check_my_balance(user_id):
    adding_operation_list = list(
        BalanceOperations.objects.filter(user_id=user_id, type_operation=1).values_list('summa', flat=True))
    print(adding_operation_list)
    withdraw_operation_list = list(
        BalanceOperations.objects.filter(user_id=user_id, type_operation=0).values_list('summa', flat=True))
    if user_id.role == 1:
        deal_history = list(DealHistory.objects.filter(from_who=user_id).values_list('order'))
    else:
        deal_history = list(DealHistory.objects.filter(to_who=user_id).values_list('order'))
    balance = sum(adding_operation_list)

    if withdraw_operation_list != []:
        balance = sum(adding_operation_list) - sum(withdraw_operation_list)
    if deal_history != []:
        for i in deal_history:
            order = Order.objects.get(id=i[0])
            print(order)
            if user_id.role == 1:
                balance -= order.cost
            else:
                balance += order.cost
    print(balance)
    return balance


def accept_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.done = True
    order.in_work = 1
    order.save()
    update_deal_history(pk)
    return redirect('customer_main_page')


def refuse_order(request, pk):
    order = Order.objects.get(pk=pk)
    if " is not accepted."  not in order.work_ready:
        order.work_ready = order.work_ready + ' is not accepted.'
        order.save()
    return redirect('customer_main_page')


def create_order(request): # Отлично работает
    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            created_order = form.save(commit=False)
            user_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
            all_cost =  list(Order.objects.filter(customer=get_object_or_404(Customer, user_id=user_id), done = False).values_list('cost', flat=True))
            print(all_cost)
            if created_order.cost <= (check_my_balance(user_id) - sum(all_cost)) and (created_order.deadline > date.today()):
                created_order.customer = get_object_or_404(Customer, user_id=user_id)
                created_order.save()
                return redirect('customer_main_page')
            else:
                return redirect('create_order')
        else:
            error = 'Форма была неверной'

    form = OrderForm()
    u_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    balance = check_my_balance(u_id)
    data = {
        'form' : form,
        'error' : error,
        'balance': balance
    }
    return render(request, 'new_order.html', data)


def create_user(request):
    error = ''
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            created_user = form.save(commit=False)
            created_user.django_user_id = get_object_or_404(User, id=request.user.id)
            created_user.save()
            user_id = UserData.objects.get(django_user_id=get_object_or_404(User, id=request.user.id))
            if created_user.role == 1:
                new_customer = Customer.objects.create(user_id=user_id)
                new_balance_operation = BalanceOperations.objects.create(user_id=user_id, type_operation=1, summa=0)
                new_balance_operation.save()
                new_customer.save()
                return redirect('create_order')
            elif created_user.role == 0:
                new_freelancer = Freelancer.objects.create(user_id=user_id)
                new_balance_operation = BalanceOperations.objects.create(user_id=user_id, type_operation=1, summa=0)
                new_balance_operation.save()
                new_freelancer.save()
                return redirect('freelancer_main_page')
        else:
            error = 'Форма была неверной'
    form = UserDataForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'create_user.html', data)


class MyprojectLoginView(LoginView):
    template_name = "login_page.html"
    form_class = AuthUserForm
    success_url = reverse_lazy('create_order')
    def get_success_url(self):
        logined_user = get_object_or_404(User, id=self.request.user.id)
        logined_user = get_object_or_404(UserData, django_user_id=logined_user)
        if logined_user.role == 0:
            return reverse_lazy('freelancer_main_page')
        elif logined_user.role == 1:
            return reverse_lazy('customer_main_page')
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('create_user')
    success_msg = "Пользователь успешно создан"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)  # Авторизация пользователя
        return response


def order_responses(request, order_id):
    userdata_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    user_offers = Offers.objects.filter(details=get_object_or_404(Order, pk=order_id))
    data = {'user_offers': user_offers}
    return render(request, 'order_responses.html', context=data)

def assign_to_order(request, pk):
    offer = Offers.objects.get(pk=pk)
    order = offer.details

    # Убираем других назначенных на этот заказ
    offers = Offers.objects.filter(details=order)
    for now_offer in offers:
        now_offer.take = False
        now_offer.save()

    offer.take = True
    offer.save()
    order.in_work = 1
    order.performer = offer.freelance_variety
    order.save()
    return redirect('order_responses', order.pk)

def remove_from_order(request, pk):
    offer = Offers.objects.get(pk=pk)
    order = offer.details
    offer.take = False
    offer.save()
    #Совсем необязательная штука, проверяем, а вдруг мы назначили нескольких
    offers = Offers.objects.filter(details=order)
    if not any(now_offer.take for now_offer in offers):
        order.in_work = 0
        order.performer = None
        order.save()
    return redirect('order_responses', order.pk)

def add_order(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('start_page')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddOrderForm()
    return render(request, 'customer_main_page.html', {'form': form})


class OrderFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['customer', 'performer', 'cost', 'degree_to_company', 'degree_to_performer', 'id']

class OrderViewAll(ListView):
    model = Order
    template_name = 'order_list.html'


    def get_queryset(self):
        filter_set = OrderFilter(self.request.GET, queryset=Order.objects.all())
        return filter_set.qs

class OrderUpdateView(UpdateView):
    model = Order
    form_class = UpdateOrderForm
    template_name = 'update_order.html'
    success_url = reverse_lazy('start_page')


# new
def my_balance(request):
    user_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)

            operation.user_id = user_id
            operation.summa = abs(operation.summa)

            if user_id.role == 1:
                all_cost = list(Order.objects.filter(customer=get_object_or_404(Customer, user_id=user_id),
                                                    done=False).values_list('cost', flat=True))

                if operation.type_operation == 1 or operation.summa <= (check_my_balance(user_id) - sum(all_cost)):
                    operation.save()
                return redirect('my_balance_customer')
            else:
                if operation.type_operation == 1 or operation.summa <= check_my_balance(user_id):
                    operation.save()
                return redirect('my_balance_freelancer')
    balance = check_my_balance(user_id)
    form = BalanceForm()
    data = {
        'balance': balance,
        'form': form,
        'user_id': user_id
    }
    return render(request, 'balance_update.html', context=data)

def show_deal_history(request):
    user_id = get_object_or_404(UserData, django_user_id=get_object_or_404(User, id=request.user.id))
    if user_id.role == 1:
        d_history = DealHistory.objects.filter(from_who=user_id)
    else:
        d_history = DealHistory.objects.filter(to_who=user_id)

    balance_operations = BalanceOperations.objects.filter(user_id=user_id)
    return render(request, 'deal_history.html', context={'deal_history': d_history,
                                                         'balance_operations': balance_operations})

def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    Offers.objects.filter(details=order).delete()
    order.delete()
    return redirect('customer_main_page')






