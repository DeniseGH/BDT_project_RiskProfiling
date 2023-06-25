from functions import random_ids, name_surname, age, income, delay, suffering, education, co_applicant, savings, \
    purpose, dependents, co_app_inc, complex_income, amount, status, term, monthly_dept, interest_rate, duration, \
    last_fee
from SQL_manager import DatabaseConnector


class Client:
    """
    The Client class creates clients profiles
    """
    def __init__(self, customer_id: str, name: str, age: int, education: str, income: int,
                 delay: int, suffering: str, coappl: str, dep: int, saves: int, coappinc: int):
        """
        :param customer_id: creates random customer ID composed of 32 alphanumeric characters
        :param name: italian name and surname of the client
        :param age: age randomly chosen between 25 and 60
        :param education: education grade (dichotomous variable)
        :param income: applicant net monthly income per month (approximately calculated)
        :param delay: "Centrale dei Rischi" delay in previous payment
        :param suffering: "Centrale Rischi Finanziari" bank suffering
        :param coappl: other applicant of the loan (dichotomous variable)
        :param dep: number of people dependent on the applicant (and eventually co-applicant)
        :param saves: available savings
        :param coappinc: co-applicant net monthly income per month (approximately calculated)
        """
        self.customer_id = customer_id
        self.name = name
        self.age = age
        self.education = education
        self.income = income
        self.delay = delay
        self.suffering = suffering
        self.coappl = coappl
        self.dep = dep
        self.saves = saves
        self.coappinc = coappinc

    def create_random_client(self):
        """
        this function creates clients parameters
        :return: client profile
        """
        cl_income = income()
        co_app = co_applicant()
        coapp_inc = co_app_inc(co_app)
        client = self(random_ids(), name_surname(), age(), education(), cl_income,
                      delay(), suffering(), co_app, dependents(cl_income, coapp_inc), savings(), coapp_inc)
        return client


class Loan:
    """
    This class creates Loan profiles based on client requests
    """

    def __init__(self, loan_id: str, client: Client, amount: int, purpose: str, term: str, status: str):
        """
        :param loan_id: creates random loan ID composed of 32 alphanumeric characters
        :param client: links the parameters of the loan to those of the customer
        :param amount: loan amount requests by the customer
        :param purpose: purpose of the loan
        :param term: term of the loan (dichotomous variable)
        :param status: refers to the status of the loan
        """
        self.loan_id = loan_id
        self.client = client
        self.amount = amount
        self.purpose = purpose
        self.term = term
        self.status = status

    def create_random_loan(self):
        """
        This function creates random loan requests based on client profiles
        :return: loan request
        """
        client = Client.create_random_client(Client)
        tot_inc = complex_income(client.income, client.coappinc, client.dep)
        mon_dep = monthly_dept(tot_inc)
        loan_amount = amount(mon_dep)
        pur = purpose(loan_amount)
        int_rate = interest_rate(pur)
        dur = duration(loan_amount, int_rate, mon_dep)

        loan = self(random_ids(), client , loan_amount, pur, term(dur), status())
        return loan

    def __str__(self):
        print("Info about the loan you are processing: ")
        print("-------")
        print("Loan ID: ", self.loan_id)
        print("Client income: ", self.client.income)
        print("Is there a co-applicant? ", self.client.coappl)
        print("Number of dependents: ", self.client.dep)
        print("Delay data from the CRIF: ", self.client.delay)
        print("Suffering in another loan: ", self.client.suffering)
        print("Loan amount requested: ", self.amount)
        print("Purpose of the loan: ", self.purpose)
        print("-------")
        return ""


class Fully_Paid(Loan):
    """
    This class refers to all the loan that has already been fully repaid to the bank and adds other information
    about the loan itself
    """

    def __init__(self, loan_id, client, amount, purpose, term, status, monthly_dept,
                 interest_rate, duration, last_fee, delay):
        """
        :param monthly_dept: monthly fee owed by the customer
        :param interest_rate: interest rate applied on the loan
        :param duration: duration of the loan in months
        :param last_fee: last fee of the loan may be different from the other because of roundings applied to the different amounts
        :param delay: late payment of loan instalments
        """
        super().__init__(loan_id, client, amount, purpose, term, status)
        self.monthly_dept = monthly_dept
        self.interest_rate = interest_rate
        self.duration = duration
        self.last_fee = last_fee
        self.delay = delay

    @staticmethod
    def extract_fully_paid_loans():
        """
        this function extracts from the principle table all the loans which status is "Fully Paid"
        :return: loan profiles with complete information
        """
        db = DatabaseConnector('CREDIT_RECORDS.db')

        db.execute_query("SELECT * FROM loan_records WHERE Status = 'Fully Paid'")
        rows = db.fetchall()

        column_names = db.get_column_names('loan_records')
        db.close()
        fully_paid_loans = []
        for row in rows:
            row_data = dict(zip(column_names, row))
            client = Client(
                row_data['Customer_ID'], row_data['Name_Surname'], row_data['Age'], row_data['Education'],
                row_data['Income'],
                row_data['CRIF_delay'], row_data['CR_suffering'], row_data['CoApplicant'], row_data['Dependents_No'],
                row_data['Savings'],
                row_data['CoApp_Income']
            )
            loan = Loan(
                row_data['Loan_ID'], client, row_data['Amount'], row_data['Purpose'], row_data['Term'],
                row_data['Status']
            )

            tot_inc = complex_income(client.income, client.coappinc, client.dep)
            mon_dep = monthly_dept(tot_inc)
            pur = loan.purpose
            amount_loan = loan.amount
            int_rate = interest_rate(pur)
            dur = duration(amount_loan, int_rate, mon_dep)
            l_fee = last_fee(dur, mon_dep, int_rate, amount_loan)

            paid_information = [(loan.loan_id, amount_loan,
                                 mon_dep, int_rate, dur, delay(), l_fee)]

            fully_paid_loans.extend(paid_information)

        return fully_paid_loans


