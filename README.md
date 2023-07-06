# BDT_project_RiskProfiling

---

***Abstract***

This project presents a novel algorithmic approach to improve risk assessment in banks by leveraging client behavioral profiles and loan repayment history. The objective is to develop an algorithm that can advise banks on whether to accept or decline new loan requests, while also providing tailored offers in case of acceptance. By employing machine learning techniques such as clustering and decision trees, the proposed algorithm provides reliable loan request evaluations. The system architecture incorporates data creation, storage, loan processing, and ongoing loan management. The implementation utilizes SQL, Redis, and Apache Spark technologies. This approach offers banks an effective tool to enhance risk mitigation, streamline loan management, and deliver personalized loan offers. 

---

##### Framework functionalities


- [x] Simulation of customers e.g. clients that previously requested a loan

- [x] Simulation of loans records (with different statuses)

- [x] Simulation of loan requests

- [x] Systematic approach for decision process through ML algorithms
      
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

<img width="879" alt="Schermata 2023-06-26 alle 22 56 42" src="https://github.com/DeniseGH/BDT_project_RiskProfiling/assets/128131934/b95a6a20-2d85-45de-b44b-3462603ab42e">


---


##### Project files

> 1. `SQL_manager`:  manages CRUD methods to interact with the SQL database
> 2. `redis_manager`: enables management of Redis stack



> Spark related
>
> 1. `Ongoing_loans/spark` : PySpark, batch processing of transactions



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

- By running the `main.py` file a SQL database in the project folder with three tables: loan_records, fully_paid, and ongoing is created.

- By running the `simulation_loan_application.py` file the trial begins by prompting the user to provide all the necessary information for making an informed decision. Alternatively, the input modality can be turned off, and a randomly generated loan request can be used.

- After inputting the data, the simulation generates three results using different algorithms: Hierarchical Clustering, KNN (K-Nearest Neighbors), and Decision Tree. These results provide insights into whether the loan request would be accepted or declined. If accepted, the simulation also reveals the suggested offer that our partner (the bank) would make to the user.

```python
# Tunable params
# You can modify them in the source code of main.py

NUMBER_OF_RECORDS = 1000 # number of records in the loan_records table
NUMBER_OF_ONGOING_RECORDS = 100 # number of ongoing loans in the ongoing table 
```

The ongoing loans simulation is based on the assumption that we have the ability to track loans that have been previously accepted in our bank over time. This allows us to mine transaction data and develop an automated system that monitors the number of payment delays and the remaining months for each loan. As the loans are fully repaid  or charged off, we enhance the algorithm by adding them to the loan_records table, along with the collected information on the number of delays. In a read data case, this iterative process enables us to continuously refine the algorithm.

How it works?

- By running the `simulation_ongoing_loans.py` file the trial begins by asking the user the start date and the length (in months) of the simulation
  
- Then a folder is created, with one directory per each month. Each directory contains the JSON files of transactions.
  
- An automated system to analyze loan transactions. Our system assumes that loan repayments should be made before the 27th of each month. Any transaction occurring after the 27th is considered as a late payment. The information about the months left and the number of delays of each ongoing loans are kept on a Redis hash. 


---

### Visual encoding of the decision making process through Decision Tree
With an high level of complexity

<img width="1077" alt="DT" src="https://github.com/DeniseGH/BDT_project_RiskProfiling/assets/128131934/1569dece-fffc-4210-8e9b-74f147209f9c">



