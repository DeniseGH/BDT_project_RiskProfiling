from Clustering import hierarchical_clustering, predict_unknown_status, tailored_offer, knn_clustering
from classes import Loan, Client
from functions import random_ids
from input_data import user_loan_request
from tree import predict_status_by_tree, fit_decision_tree
from SQL_manager import DatabaseConnector

# ------- TRY TO MINE THE GENERATED DATA WITH THE LOAN REQUEST HERE
# trial_customer = Client(random_ids(), 'Mario Rossi', 35, 'Graduated', 3700, 0, "Yes", "No", 0, 6000, 0)
# new_loan = Loan(random_ids(), trial_customer, 27000, "Home improvement", "Long Term", "Unknown")

# ------- TRY WITH A RANDOM LOAN REQUEST
# new_loan = Loan.create_random_loan(Loan)
# print(new_loan2)

# ------- USER GIVES THE LOAN REQUEST IN INPUT
new_loan = user_loan_request()

db = DatabaseConnector("CREDIT_RECORDS.db")
db.execute_query("SELECT * FROM loan_records")
rows = db.fetchall()

# HC
cluster_matrix_result_HC = hierarchical_clustering(rows, new_loan)
loan_ids_list_HC = predict_unknown_status(cluster_matrix_result_HC)
tailored_offer(loan_ids_list_HC, new_loan)

# KNN
cluster_matrix_result_knn = knn_clustering(rows, new_loan)
loan_ids_list_KNN = predict_unknown_status(cluster_matrix_result_knn)
tailored_offer(loan_ids_list_KNN, new_loan)

# TREE
column_names = db.get_column_names("loan_records")
fitted_tree = fit_decision_tree(rows, column_names)
predict_status_by_tree(new_loan, fitted_tree)

