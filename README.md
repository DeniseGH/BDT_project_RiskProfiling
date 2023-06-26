# BDT_project_RiskProfiling

---

***Abstract***

The project is a big data system to manage

---

##### Framework functionalities
##### Framework functionalities



- [x] Creation of clients and retail stores using scraping 

- [x] Creation of Inventories for each retail shop starting from a raw list of products

- [x] Simulation of customers e.g clients that previously requested a loan

- [x] Simulation of loans records(with different statuses)

- [x] Simulation of clients affluence *turnout* 

- [x] Batch processing: data analysis with Spark monthly based

- [ ] Forecasting 

- [ ] Data analysis within a time window

- [ ] Management of damaged goods, expired ones etc.

  

---

##### Technologies

+ Spark
+ SQL
+ Redis

---

#### How to run

You can run the framework directly installing dependencies on your machine:

```bash
1 pip install -r requirements.txt 
2 python3 ./main.py

# Once simulator started, type the number of rows you want in the synthetic data
# It may take a minute to see the resulting database

3 python3 ./simulation_loan_application.py

# The program will ask you some information and will tailor you an offer

4 python3 ./simulation_ongoing_loans.py
```
Framework has been tested with:

