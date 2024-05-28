import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score, f1_score, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def find_best_parameters(model, parameters, X, y, cv=10, verbose=1, n_jobs=-1):
    grid_object = GridSearchCV(model, parameters, scoring=make_scorer(accuracy_score), cv=cv, verbose=verbose,
                               n_jobs=n_jobs)
    grid_object = grid_object.fit(X, y)
    return grid_object.best_estimator_


def main():
    # Read the data from the CSV file
    data = pd.read_csv('games.csv', header=0, sep=',')

    X = data[['White player Elo', 'Black player Elo']]
    y = data['Result']

    accuracy_results = {}

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=42)

    # First model is SVM
    # Data is linearly not separable, so we use RBF kernel

    # Finding the best parameters for SVM without opening

    # svc = SVC(kernel='rbf')
    # parameters = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    #               'gamma': [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10]}
    # svc = find_best_parameters(svc, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(svc.get_params())

    # Best parameters are C=1000 and gamma=0.000001

    svc = SVC(kernel='rbf', C=1000, gamma=0.000001)
    svc.fit(X_train, y_train)
    y_pred = svc.predict(X_test)
    accuracy_results['SVM'] = [accuracy_score(y_test, y_pred)]
    # print(f'SVM accuracy without opening {accuracy_score(y_test, y_pred)}')
    # print(f'SVM f1 score without opening {f1_score(y_test, y_pred, average='weighted')}')

    # Second model is Random Forest

    # Finding the best parameters for Random Forest without opening

    # random_forest = RandomForestClassifier() parameters = { 'n_estimators': [100, 150, 200, 250, 300, 350, 400,
    # 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000], 'max_features': ['log2', 'sqrt',
    # 'auto'] } random_forest = find_best_parameters(random_forest, parameters, X_train, y_train, cv=5, verbose=1,
    # n_jobs=-1) print(random_forest.get_params())

    # Best parameters are n_estimators=200 and max_features='sqrt'

    random_forest = RandomForestClassifier(n_estimators=200, max_features='sqrt')
    random_forest.fit(X_train, y_train)
    y_pred = random_forest.predict(X_test)
    accuracy_results['Random Forest'] = [accuracy_score(y_test, y_pred)]
    # print(f'Random forest accuracy without opening: {accuracy_score(y_test, y_pred)}')
    # print(f'Random forest f1 score without opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Third model is Decision Tree

    # Finding the best parameters for Decision Tree without opening

    # dt_clf = DecisionTreeClassifier()
    # parameters = {'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    # dt_clf = find_best_parameters(dt_clf, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(dt_clf.get_params())

    # Best parameter is max_depth=10

    dt_clf = DecisionTreeClassifier(max_depth=10)
    dt_clf.fit(X_train, y_train)
    y_pred = dt_clf.predict(X_test)
    accuracy_results['Decision Tree'] = [accuracy_score(y_test, y_pred)]
    # print(f'Decision tree accuracy without opening: {accuracy_score(y_test, y_pred)}')
    # print(f'Decision tree f1 score without opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Next model is Gradient Boosting Machine

    # Finding the best parameters for Gradient Boosting without opening

    # gb_clf = GradientBoostingClassifier()
    # parameters = {'n_estimators': [50, 100, 150, 200, 250, 300, 350, 400],
    #               'max_depth': [3, 4, 5]}
    # gb_clf = find_best_parameters(gb_clf, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(gb_clf.get_params())

    # Best parameters are n_estimators=50 and max_depth=4

    gb_clf = GradientBoostingClassifier(n_estimators=50, max_depth=4)
    gb_clf.fit(X_train, y_train)
    y_pred = gb_clf.predict(X_test)
    accuracy_results['Gradient Boosting'] = [accuracy_score(y_test, y_pred)]
    # print(f'Gradient boosting accuracy without opening: {accuracy_score(y_test, y_pred)}')
    # print(f'Gradient boosting f1 score without opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Last model is AdaBoost

    # Finding the best parameters for AdaBoost without opening

    # ab_clf = AdaBoostClassifier()
    # parameters = {'n_estimators': [50, 100, 150, 200, 250, 300, 350, 400]}
    # ab_clf = find_best_parameters(ab_clf, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(ab_clf.get_params())

    # Best parameter is n_estimators=100

    ab_clf = AdaBoostClassifier(n_estimators=100)
    ab_clf.fit(X_train, y_train)
    y_pred = ab_clf.predict(X_test)
    accuracy_results['AdaBoost'] = [accuracy_score(y_test, y_pred)]
    # print(f'AdaBoost accuracy without opening: {accuracy_score(y_test, y_pred)}')
    # print(f'AdaBoost f1 score without opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Now we will add opening to the data

    label_encoder_object = LabelEncoder()
    data['Opening'] = label_encoder_object.fit_transform(data['Opening'])
    X = data[['White player Elo', 'Black player Elo', 'Opening']]
    y = data['Result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, random_state=42)

    # Finding the best parameters for SVM with opening

    # svc = SVC(kernel='rbf')
    # parameters = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
    #               'gamma': [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10]}
    # svc = find_best_parameters(svc, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(svc.get_params())

    # Best parameters are C=1000 and gamma=0.000001

    svc = SVC(kernel='rbf', C=1000, gamma=0.000001)
    svc.fit(X_train, y_train)
    y_pred = svc.predict(X_test)
    accuracy_results['SVM'].append(accuracy_score(y_test, y_pred))
    # print(f'SVM accuracy with opening {accuracy_score(y_test, y_pred)}')
    # print(f'SVM f1 score with opening {f1_score(y_test, y_pred, average='weighted')}')

    # Finding the best parameters for Random Forest with opening

    # random_forest = RandomForestClassifier()
    # parameters = {
    #     'n_estimators': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950,
    #                      1000],
    #     'max_features': ['log2', 'sqrt', 'auto']
    # }
    # random_forest = find_best_parameters(random_forest, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(random_forest.get_params())

    # Best parameters are n_estimators=850 and max_features='log2'

    random_forest = RandomForestClassifier(n_estimators=850, max_features='log2')
    random_forest.fit(X_train, y_train)
    y_pred = random_forest.predict(X_test)
    accuracy_results['Random Forest'].append(accuracy_score(y_test, y_pred))
    # print(f'Random forest accuracy with opening: {accuracy_score(y_test, y_pred)}')
    # print(f'Random forest f1 score with opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Finding the best parameters for Decision Tree with opening

    # dt_clf = DecisionTreeClassifier()
    # parameters = {'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    # dt_clf = find_best_parameters(dt_clf, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(dt_clf.get_params())

    # Best parameter is max_depth=10

    dt_clf = DecisionTreeClassifier(max_depth=10)
    dt_clf.fit(X_train, y_train)
    y_pred = dt_clf.predict(X_test)
    accuracy_results['Decision Tree'].append(accuracy_score(y_test, y_pred))
    # print(f'Decision tree accuracy with opening: {accuracy_score(y_test, y_pred)}')
    # print(f'Decision tree f1 score with opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Finding the best parameters for Gradient Boosting with opening

    # gb_clf = GradientBoostingClassifier()
    # parameters = {'n_estimators': [50, 100, 150, 200, 250, 300, 350, 400],
    #               'max_depth': [3, 4, 5]}
    # gb_clf = find_best_parameters(gb_clf, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(gb_clf.get_params())

    # Best parameters are n_estimators=50 and max_depth=3

    gb_clf = GradientBoostingClassifier(n_estimators=50, max_depth=3)
    gb_clf.fit(X_train, y_train)
    y_pred = gb_clf.predict(X_test)
    accuracy_results['Gradient Boosting'].append(accuracy_score(y_test, y_pred))
    # print(f'Gradient boosting accuracy with opening: {accuracy_score(y_test, y_pred)}')
    # print(f'Gradient boosting f1 score with opening: {f1_score(y_test, y_pred, average='weighted')}')

    # Finding the best parameters for AdaBoost with opening

    # ab_clf = AdaBoostClassifier()
    # parameters = {'n_estimators': [50, 100, 150, 200, 250, 300, 350, 400]}
    # ab_clf = find_best_parameters(ab_clf, parameters, X_train, y_train, cv=5, verbose=1, n_jobs=-1)
    # print(ab_clf.get_params())

    # Best parameter is n_estimators=250

    ab_clf = AdaBoostClassifier(n_estimators=250)
    ab_clf.fit(X_train, y_train)
    y_pred = ab_clf.predict(X_test)
    accuracy_results['AdaBoost'].append(accuracy_score(y_test, y_pred))
    # print(f'AdaBoost accuracy with opening: {accuracy_score(y_test, y_pred)}')
    # print(f'AdaBoost f1 score with opening: {f1_score(y_test, y_pred, average='weighted')}')

    without_opening = [v[0] for v in accuracy_results.values()]
    with_opening = [v[1] for v in accuracy_results.values()]

    labels = list(accuracy_results.keys())

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, without_opening, width, label='Without opening')
    rects2 = ax.bar(x + width / 2, with_opening, width, label='With opening')

    ax.set_ylabel('Accuracy')
    ax.set_title('Model Accuracy Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plot = sns.barplot()
    plot.set(ylim=(0.0, 1.0))

    plt.xticks(rotation=45)

    fig.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()
