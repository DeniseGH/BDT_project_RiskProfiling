# BDT_project_RiskProfiling

---

***Abstract***

The project is a big data system to manage

---

##### Framework functionalities


- [x] Simulation of customers e.g. clients that previously requested a loan

- [x] Simulation of loans records (with different statuses)

- [x] Simulation of loan requests

- [x] Decision tree provides a systematic approach for financial institutions to evaluate and respond to loan applications
      
- [x] Tailored offers based on clustering of past loans 

- [x] Batch processing: data analysis of transactions with Spark monthly based

- [ ] Forecasting of the interest rate based on the inflation rate

- [ ] Evaluation of the loans request over different periods of time

- [ ] Tailored offers based on social media activity, psychometrics, and geolocation markers 

  

---

##### Technologies

+ Spark
+ SQL
+ Redis

---

##### Architecture

![Esselunga_project drawio](https://user-images.githubusercontent.com/61838905/176533733-2c342f80-1883-4be3-8182-f263f1c4420c.png)



---



##### Project files

> 1. `SQL_manager`:  manages CRUD methods to interact with the SQL database
> 2. `redis_manager`: enables management of Redis stack



> Spark related
>
> 1. `Ongoing_loans/spark.py` : PySpark, batch processing of transactions



> Folder
>
> 1. `Ongoing_loans:` contains all the scripts about the processing of ongoing loans


---

#### How to run

You can run the framework directly installing dependencies on your machine:

```bash
1 pip install -r requirements.txt 
2 python3 ./main.py

# it might take a couple of minutes to create the database

3 python3 ./simulation_loan_application.py

# The program will ask you some information and will tailor you an offer

4 python3 ./simulation_ongoing_loans.py

# The program will ask you some information in input, then it will simulate n months of transaction and count payments and delays 
# of the ongoing loan repayments
```

Framework has been tested with:

- Python 3.9.13
- MacOS Version 11.6

---

#### Introduction: 

In our research, we assume to collaborate with a financial institution, such as a bank, and obtained access to its loan records that include both declined and accepted loan applications. Additionally, we assume to know the behaviours of these loans in particular  if they are ongoing, fully paid, and charged off. Utilizing this data, we have conducted a carefully designed simulation to develop a decision-making framework for the financial institution.

#### Objective: 

Our project aims to identify loans from the existing records that are most similar to a new loan request. By analyzing the behavior and outcomes of these similar loans (i.e., whether they were charged off, declined, or fully paid), we can make informed decisions to either decline the loan request or propose a loan offer that closely matches the patterns observed in the similar records. This approach enables the financial institution to effectively assess the potential risk associated with the new loan and make informed lending decisions.

#### Simulators

The loan application simulation replicates the user's loan request process on a website. Using historical loan records, it generates a tailored offer, including the potential denial of the loan request, based on past loan outcomes.


How it works?

- Running the main.py file creates a SQL database in the project folder with three tables: loan_records, fully_paid, and ongoing.

- The loan application simulation trial begins by prompting the user to provide all the necessary information for making an informed decision. Alternatively, the input modality can be turned off, and a randomly generated loan request can be used.

- After inputting the data, the simulation generates three results using different algorithms: Hierarchical Clustering, KNN (K-Nearest Neighbors), and Decision Tree. These results provide insights into whether the loan request would be accepted or declined. If accepted, the simulation also reveals the suggested offer that our partner (the bank) would make to the user.

```python
# Tunable params
# You can modify them in the source code of main.py

NUMBER_OF_RECORDS = 1000 # number of records in the loan_records table
NUMBER_OF_ONGOING_RECORDS = 100 # number of ongoing loans in the ongoing table 
```

The ongoing loans simulation is based on the assumption that we have the ability to track loans that have been previously accepted in our bank over time. This allows us to mine transaction data and develop an automated system that monitors the number of payment delays and the remaining months for each loan. As the loans are fully repaid  or charged off, we enhance the algorithm by adding them to the loan_records table, along with the collected information on the number of delays. In a read data case, this iterative process enables us to continuously refine the algorithm.

How it works?

- 

---


