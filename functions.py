import random
import string
from faker import Faker


def random_ids():
    # dividing ID in 5 parts
    p1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    p2 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    p3 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    p4 = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    p5 = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # uniting ID parts for creating complete ID
    IDs = f"{p1}-{p2}-{p3}-{p4}-{p5}"
    return IDs


def name_surname():
    faker = Faker('it_IT')  # choosing italian names
    first_name = faker.first_name()
    last_name = faker.last_name()
    complete_name = f"{first_name} {last_name}"
    return complete_name


def age():
    aging = random.randint(25, 60)
    return aging


def education():
    weights = [0.21, 0.79]
    choices = ["Graduated", "Not graduated"]
    ed_level = random.choices(choices, weights=weights)[0]
    return ed_level


def income():
    random_percent = random.random()
    if random_percent < 0.7:
        income = random.randint(10, 30) * 100
    elif random_percent < 0.9:
        income = random.randint(31, 50) * 100
    else:
        income = random.randint(51, 60) * 100
    return income


def delay():
    weights = [0.7, 0.25, 0.05]
    choices = [0, 1, 2]
    delay = random.choices(choices, weights=weights)[0]
    return delay


def suffering():
    choices = ["No", "Yes"]
    weights = [0.85, 0.15]
    suffering = random.choices(choices, weights=weights)[0]
    return suffering


def co_applicant():
    choices = ["No", "Yes"]
    co_app = random.choice(choices)
    return co_app


def co_app_inc(co_app):
    if co_app == "Yes":
        co_app_inc = income()
    else:
        co_app_inc = 0
    return co_app_inc


def savings():
    return random.randint(200, 10000)


def dependents(income, co_app_inc):
    tot = income + co_app_inc
    number = [0, 1, 2, 3]
    if tot >= 2000:
        return random.choice(number)
    elif tot in range(1200, 1999):
        return random.choice(number[:-1])
    elif tot in range(800, 1199):
        return random.choice(number[:-2])
    else:
        return number[0]


def complex_income(income, co_app_inc, dependents):
    complex_income = income + co_app_inc - (dependents * 400)
    return complex_income


def monthly_dept(complex_income):
    mon_dept = complex_income * 0.30
    return round(mon_dept, 2)


def amount(monthly_dept):
    max_amount = monthly_dept * 120 if monthly_dept * 180 < 80000 else 80000
    LA = random.randint(2000, max_amount)
    return LA


def purpose(amount):
    purposes = ["Debt Consolidation", "Home improvement", "Vacation or travel", "Wedding expenses",
                "Education or tuition fees"]
    if amount <= 30000:
        loanPurpose = random.choice(purposes[2:])
    elif amount in range(30000, 50000):
        loanPurpose = random.choice(purposes[:-1])
    else:
        loanPurpose = random.choice(purposes[0:2])
    return loanPurpose


def interest_rate(purpose):
    if purpose == "Debt Consolidation":
        interest_rate = random.uniform(8, 8.8)
    else:
        interest_rate = random.uniform(7, 8)
    return round(interest_rate, 2)


def duration(amount, interest_rate, monthly_dept):
    number_of_months = (amount + (interest_rate / 100 * amount)) / monthly_dept
    return round(number_of_months)


def term(duration):
    if duration > 18:
        term = "Long Term"
    else:
        term = "Short Term"
    return term


def last_fee(duration, monthly_dept, interest_rate, amount):
    tot_debt = amount + (amount * interest_rate / 100)
    excess = tot_debt - (monthly_dept * duration)
    if excess < 0:
        last_rate = tot_debt - (monthly_dept * (duration - 1))

    else:
        last_rate = excess
    return round(last_rate, 2)


def status():
    status = ['Declined', 'Charged off', 'Fully Paid']
    weights = [0.05, 0.10, 0.85]
    loanStatus = random.choices(status, weights=weights)[0]
    return loanStatus
