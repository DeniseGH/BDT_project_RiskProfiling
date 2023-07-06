import numpy as np
import pandas
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.neighbors import NearestNeighbors
from gower import gower_matrix

from classes import Loan, Client
from functions import monthly_dept, complex_income, duration, random_ids, last_fee
from input_data import user_loan_request
from tree import predict_status_by_tree, fit_decision_tree
from SQL_manager import DatabaseConnector


def compute_gower_matrix(rows,new_loan: Loan):
    '''
    :param rows: rows: a list of rows containing the records of the past loans given from a bank
    :param new_loan: the new loan request
    :return: the distance matrix computed with the Gower Distance
    '''
    data = [row[2:-1] for row in rows]

    new_row = [
        new_loan.client.name,
        new_loan.client.age,
        new_loan.client.education,
        new_loan.client.income,
        new_loan.client.delay,
        new_loan.client.suffering,
        new_loan.client.coappl,
        new_loan.client.dep,
        new_loan.client.saves,
        new_loan.client.coappinc,
        new_loan.amount,
        new_loan.purpose,
        new_loan.term
    ]

    data.append(new_row)

    # Convert the data list to a pandas DataFrame
    df = pandas.DataFrame(data)

    # Calculate the Gower distance matrix
    distance_matrix = gower_matrix(df)
    return distance_matrix


def hierarchical_clustering(rows, new_loan):
    '''
    :param rows: a list of rows containing the records of the past loans given from a bank
    :param new_loan: the new loan request
    :return: the loan ids and the status of the loans in the same cluster of the new_loan
    '''
    print("---- > We are now processing your request with Hierarchical Clustering")

    loan_ids = [row[0] for row in rows]
    loan_ids.append(new_loan.loan_id)
    status = [row[-1] for row in rows]
    status.append("Unknown")

    distance_matrix = compute_gower_matrix(rows, new_loan)

    # Perform hierarchical clustering on the distance matrix
    linkage_matrix = linkage(distance_matrix, method='ward')

    cluster_loan_ids = []
    num_cluster = 60

    while len(cluster_loan_ids) < 6:
        clusters = fcluster(linkage_matrix, t=num_cluster, criterion='maxclust')

        # Find the cluster of the new loan
        new_loan_cluster = clusters[-1]

        # Filter the statuses based on the cluster of the new loan
        cluster_loan_ids = [loan_ids[i] for i, cluster in enumerate(clusters) if cluster == new_loan_cluster]
        num_cluster -= 1

    cluster_statuses = [status[i] for i, cluster in enumerate(clusters) if cluster == new_loan_cluster]

    # Create a matrix with the loan IDs and statuses of loans in the same cluster as the new loan
    cluster_matrix = np.column_stack((cluster_loan_ids, cluster_statuses))

    print("In our records we found ", len(cluster_loan_ids) - 1, " loans similar to you request")
    return cluster_matrix


def knn_clustering(rows, new_loan):
    '''
        :param rows: a list of rows containing the records of the past loans given from a bank
        :param new_loan: the new loan request
        :return: the loan ids and the status of the loans in the same cluster of the new_loan
    '''

    n_neighbors= 5
    print(" ---- > We are now processing your request with KNN with n = ", n_neighbors)

    loan_ids = [row[0] for row in rows]
    loan_ids.append(new_loan.loan_id)
    status = [row[-1] for row in rows]
    status.append("Unknown")

    distance_matrix = compute_gower_matrix(rows, new_loan)

    # Find the k-nearest neighbors
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='precomputed')

    knn.fit(distance_matrix)

    # Get the indices of the k-nearest neighbors for the last data point
    last_data_point = distance_matrix[-1:]  # Assuming distance_matrix is a numpy array or a list of lists
    knn_indices = knn.kneighbors(last_data_point, return_distance=False)

    knn_indices = np.concatenate((knn_indices[:, 1:], knn_indices[:, 0:1]), axis=1)

    loan_ids_knn = [loan_ids[idx] for idx in knn_indices[0]]

    statuses_knn = [status[idx] for idx in knn_indices[0]]

    # Create a matrix with the loan IDs and statuses of loans in the same cluster as the new loan
    cluster_matrix = np.column_stack((loan_ids_knn, statuses_knn))
    return cluster_matrix


# This function takes a decision looking at the status of the closest loans
def predict_unknown_status(cluster_matrix):
    '''
    :param cluster_matrix: matrix where in the first column loan ids in the same cluster of the loan request and
    in the second column the statuses of these loans
    :return: statuses of the closest loans (if the loan is accepted), or a string "declined" id the loan is declined
    '''
    statuses = cluster_matrix[:-1, 1]
    unique_statuses, counts = np.unique(statuses, return_counts=True)

    fp_count = counts[unique_statuses == "Fully Paid"][0] if "Fully Paid" in unique_statuses else 0
    d_count = (counts[unique_statuses == "Declined"])[0] if "Declined" in unique_statuses else 0
    co_count = (counts[(unique_statuses == "Charged off")])[0] if "Charged off" in unique_statuses else 0

    if "Fully Paid" in unique_statuses:
        if fp_count > d_count + 5 * (co_count):
            print("Looking at the previous results your loan request: ", cluster_matrix[-1, 0], "it is accepted")
            return [row[0] for row in cluster_matrix if row[1] == "Fully Paid"]

    print("Looking at the previous results your loan request: it is declined")
    return "Declined"


# This function suggests a offer based on the similar loans
def tailored_offer(loan_ids_list, new_loan):
    '''
    :param loan_ids_list: list of loan ids in the same cluster of the loan request
    :param new_loan: the loan request
    :return: None
    '''
    if loan_ids_list == "Declined":
        print("No tailored offer for a declined loan")
    else:
        db = DatabaseConnector("CREDIT_RECORDS.db")

        # Prepare the SQL query
        query = "SELECT Amount, Monthly_Dept, Duration, Interest_Rate  FROM fully_paid WHERE loan_id IN ({}) AND delay = 0".format(
            ','.join(['?'] * len(loan_ids_list)))

        # Execute the query with the loan IDs as parameters
        db.execute_query(query, loan_ids_list)

        # Fetch all rows
        rows = db.fetchall()

        if rows == []:
            print("there are no fully paid loans with o delay")
            query = "SELECT * FROM fully_paid WHERE loan_id IN ({}) AND delay = 1".format(
                ','.join(['?'] * len(loan_ids_list)))

            # Execute the query with the loan IDs as parameters
            db.execute_query(query, loan_ids_list)

            # Fetch all rows
            rows = db.fetchall()

        if rows == []:
            print("there are no fully paid loans with 1 delay")
            query = "SELECT * FROM fully_paid WHERE loan_id IN ({}) AND delay = 2".format(
                ','.join(['?'] * len(loan_ids_list)))

            # Execute the query with the loan IDs as parameters
            db.execute_query(query, loan_ids_list)

            # Fetch all rows
            rows = db.fetchall()

        print("------------------------------")
        print("The closest options that have less delays and are fully paid: ")
        print("Loan_Amount, Monthly_Dept, Duration, Interest_Rate")

        interest_rate_sum = 0
        count = 0

        for row in rows:
            print(row)
            interest_rate_sum += row[3]
            count += 1

        average_interest_rate = interest_rate_sum / count

        # Close the cursor and connection
        db.close()

        monthly_repayment = monthly_dept(
            complex_income(new_loan.client.income, new_loan.client.coappinc, new_loan.client.dep))
        dur = duration(new_loan.amount, average_interest_rate, monthly_repayment)
        print("------------------------------")
        print("We advice the following offer: ")
        print("Amount: ", new_loan.amount)
        print("Interest rate: ", round(average_interest_rate, 2))
        print("Monthly dept: ", monthly_repayment)
        print("Duration: ", dur)
        print("Last Repayment: ", last_fee(dur, monthly_repayment, average_interest_rate, new_loan.amount))
        print("------------------------------")
        print("------------------------------")


