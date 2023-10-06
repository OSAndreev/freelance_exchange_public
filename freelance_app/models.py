from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    django_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    mail = models.EmailField()
    # password = models.CharField(max_length=20)
    bank_account = models.CharField(max_length=50)
    role = models.IntegerField(choices=[(0, 'Фрилансер'), (1, 'Заказчик')])
    about = models.CharField(max_length=150, null=True)


    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.mail}, {self.bank_account}, {self.role},' \
               f'{self.about}, {self.django_user_id}'


class Freelancer(models.Model):
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    degree = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user_id}, {self.degree}'


class Customer(models.Model):
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    degree = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user_id}, {self.degree}'


class Category(models.Model): # у нас две категории.0 индекс-дизайн, 1 индекс-разработка
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    explanation = models.CharField(max_length=200)
    cost = models.IntegerField()
    in_work = models.BooleanField(default=False)
    performer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=True, blank=True)
    degree_to_company = models.IntegerField(
        choices=[(0, 'Оценки нет'), (1, 'Очень плохо'), (2, "Плохо"), (3, "Средне"), (4, "Хорошо"), (5, "Отлично")], null=True, blank=True)
    degree_to_performer = models.IntegerField(
        choices=[(0, 'Оценки нет'), (1, 'Очень плохо'), (2, "Плохо"), (3, "Средне"), (4, "Хорошо"), (5, "Отлично")], null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    deadline = models.DateField()
    done = models.BooleanField(default=False)
    work_ready = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.customer}, {self.explanation}, {self.cost}, {self.in_work}, {self.performer}, {self.degree_to_company},' \
               f'{self.degree_to_performer}, {self.category}, {self.deadline}, {self.done}'


class Offers(models.Model):
    details = models.ForeignKey(Order, on_delete=models.CASCADE)
    freelance_variety = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    take = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.details}, {self.freelance_variety}, {self.take}'


class DealHistory(models.Model):
    from_who = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='deals_sent')
    to_who = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='deals_received')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_who}, {self.to_who}, {self.order}'


class BalanceOperations(models.Model):
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    type_operation = models.IntegerField(choices=[(0, 'Вывод средств'), (1, 'Пополнение')])
    summa = models.IntegerField()

    def __str__(self):
        return f'{self.user_id}, {self.type_operation}, {self.summa}'
