from classes import Loan, Client
from functions import interest_rate, duration, complex_income, monthly_dept, term, random_ids

# Prompt the user for information
def user_loan_request() -> Loan:
    print("Thanks for choosing us, we will now ask you some information: ")

    name_surname = input("Write your Name and Surname: ")

    while True:
        age = input("Write your age: ")
        if age.isdigit():
            age = int(age)
            break
        else:
            print("Invalid input. Please enter a valid integer for age.")

    education = input("Tell us about your education (Graduated/Not graduated): ")

    income = input("Income per month: ")

    while True:
        crif_delay = input("Tell us your CRIF High Mark Credit Information Services number of delays (0/1/2/3..): ")
        if crif_delay.isdigit():
            crif_delay = int(crif_delay)
            break
        else:
            print("Invalid input. Please enter a valid integer for the number of delays.")

    cr_suffering = input("Suffering declared at the Centrale dei Rischi (Yes/No): ")

    coapplicant = input("Co-Applicant (Yes/No): ")

    while True:
        dependents_no = input("Number of Dependents (0/1/2/3..): ")
        if dependents_no.isdigit():
            dependents_no = int(crif_delay)
            break
        else:
            print("Invalid input. Please enter a valid integer for the number of dependents you have.")

    savings = input("Estimate the savings you have in your bank accounts: ")

    coapp_income = input("Co-Applicant Income per month (0 if no Co-Applicant): ")

    amount = input("The amount you want for the loan: ")

    purpose = input("Purpose (choose between Dept Consolidation/Home improvement/Vacation or travel/Wedding expenses/Education or tuition fees)")

    tot_inc = complex_income(int(income), int(coapp_income), int(dependents_no))
    mon_dep = monthly_dept(tot_inc)
    int_rate = interest_rate(purpose)
    dur = duration(int(amount), int_rate, mon_dep)

    short_long_term = term(dur)

    # Print the collected information
    print("--- Summary of the Collected Information ---")
    print("Name and Surname:", name_surname)
    print("Age:", age)
    print("Education:", education)
    print("Income:", income)
    print("CRIF Delay:", crif_delay)
    print("CR Suffering:", cr_suffering)
    print("Co-Applicant:", coapplicant)
    print("Number of Dependents:", dependents_no)
    print("Savings:", savings)
    print("Co-Applicant Income:", coapp_income)
    print("Loan Amount:", amount)
    print("Purpose:", purpose)
    print("Term:", short_long_term)

    client = Client(random_ids(), name_surname, age, education, income, crif_delay, cr_suffering, coapplicant,
                    dependents_no, savings, coapp_income)

    return Loan(random_ids(), client, amount, purpose, short_long_term, "Unknown")
