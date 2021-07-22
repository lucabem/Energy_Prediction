from urllib.parse import urlparse

import mlflow
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

from preprocess.utils import get_current_time, scale_data
from utils.functions import train_test, eval_metrics, train_cv

from utils.constants import X


def run_knn(experiment_id, dataset, params=None):
    print(get_current_time(), "- Starting KNN Model...")

    train_x, test_x, train_y, test_y = train_test(dataset)

    train_x = scale_data(train_x, columns=X)
    test_x = scale_data(test_x, columns=X)

    if params is None:
        n_neighbors = [i for i in np.arange(3, 40, 1)]
        weights = ['uniform', 'distance']
    else:
        n_neighbors = params['n_neighbors']
        weights = params['weights']

    for n_neighbor in n_neighbors:
        for weight in weights:
            name = '_'.join(['knn', str(n_neighbor), 'weight', str(weight)])
            with mlflow.start_run(experiment_id=experiment_id,
                                  run_name=name,
                                  tags={'type_model': 'KNN',
                                        'train': 'holdout'}):
                model = KNeighborsRegressor(n_neighbors=n_neighbor,
                                            weights=weight,
                                            n_jobs=10)
                model.fit(train_x, train_y)

                predicted_qualities = model.predict(test_x)

                (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

                mlflow.log_param("n_neighbor", n_neighbor)
                mlflow.log_param("weight", weight)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                mlflow.sklearn.log_model(model, "model")

    print(get_current_time(), "- Ended KNN Model...")


def run_knn_cv(experiment_id, dataset, params=None):
    print(get_current_time(), "- Starting KNN CV Model...")

    if params is None:
        n_neighbors = [i for i in np.arange(3, 40, 1)]
        weights = ['uniform', 'distance']
    else:
        n_neighbors = params['n_neighbors']
        weights = params['weights']

    for n_neighbor in n_neighbors:
        for weight in weights:
            name = '_'.join(['knn', str(n_neighbor), 'weight', str(weight)])
            with mlflow.start_run(experiment_id=experiment_id,
                                  run_name=name,
                                  tags={'type_model': 'KNN',
                                        'train': 'cv'}):
                model = KNeighborsRegressor(n_neighbors=n_neighbor,
                                            weights=weight,
                                            n_jobs=8)

                rmse, mae, r2 = train_cv(model, dataset)

                mlflow.log_param("n_neighbor", n_neighbor)
                mlflow.log_param("weight", weight)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

    print(get_current_time(), "- Ended KNN CV Model...")
