import pandas

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

from classes import Loan


def loan_to_list(new_loan: Loan) -> list:
    '''
    :param new_loan: the loan request
    :return: a list of the numerical variables of the loan (where the categorical variable have been binarized)
    '''
    edu_cat = 0 if new_loan.client.education == "Graduated" else 1
    suff_cat = 0 if new_loan.client.suffering == "No" else 1
    coapp_cat = 0 if new_loan.client.coappl == "No" else 1
    purpose_cat = 0 if new_loan.purpose == "Dept consolidation" else 1
    loan_list = [new_loan.client.age, edu_cat, new_loan.client.income, new_loan.client.delay, suff_cat, coapp_cat,
                 new_loan.client.dep, new_loan.client.saves, new_loan.client.coappinc, new_loan.amount, purpose_cat, 0]
    return loan_list


def fit_decision_tree(rows, column_names):
    '''
    :param rows: rows from the SQL table
    :param column_names: name of the columns of the table in SQL
    :return:
    '''
    data = [row[3:] for row in rows]

    # Convert the data list to a DataFrame
    df = pandas.DataFrame(data)
    df.columns = column_names[3:]

    # Separate the features (X) and the target variable (y)
    X = df.iloc[:, :-1]  # All columns except the last one
    y = df.iloc[:, -1]  # Last column (status)

    # Encode the target variable to categorical labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    X['Education'] = X['Education'].map(lambda x: 0 if x == 'Graduated' else 1)
    X['CR_suffering'] = X['CR_suffering'].map(lambda x: 0 if x == 'No' else 1)
    X['Term'] = X['Term'].map(lambda x: 0 if x == 'Short Term' else 0)
    X['Purpose'] = X['Purpose'].map(lambda x: 1 if x == 'Debt Consolidation' else 0)
    X['CoApplicant'] = X['CoApplicant'].map(lambda x: 1 if x == 'Yes' else 0)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create an instance of the DecisionTreeClassifier
    tree = DecisionTreeClassifier(ccp_alpha=0.005)

    # Fit the decision tree on the training data
    tree.fit(X_train, y_train)

    # Make predictions on the testing data (in case of real data)
    # y_pred = tree.predict(X_test)
    # Evaluate the accuracy of the model
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy:", accuracy)

    # Get the unique class labels from the encoded target variable
    # class_labels = label_encoder.classes_
    # to plot the tree
    # plt.figure(figsize=(10, 10))
    # plot_tree(tree, feature_names=df.columns.tolist(), filled=True, class_names=class_labels)
    # plt.show()

    return tree


def predict_status_by_tree(new_loan: Loan, tree):
    '''
    :param new_loan: the new loan request
    :param tree: fitted tree on the loan records dataset
    :return:
    '''
    print("---- > We are now processing your request with a Decision Tree")
    example = loan_to_list(new_loan)

    # Make predictions on the new observation
    predicted_output = tree.predict([example])

    # If you have a classification tree, you can access the predicted class label directly
    predicted_class = predicted_output[0]
    if predicted_class == 2:
        print("By using the decision tree your loan request:", new_loan.loan_id, "it is accepted")
        return "Accepted"
    else:
        print("By using the decision tree your loan request:", new_loan.loan_id, "it is declined")
        return "Declined"
