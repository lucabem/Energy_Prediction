import warnings

import numpy as np
from mlflow.tracking import MlflowClient

from models.ann_mlflow import run_mlp
from models.dt_mlflow import run_dt
from models.elasticnet_mlflow import run_elasticnet
from models.knn_mflow import run_knn
from models.lightgbm_mlflow import run_lgbm
from models.xgb_mlflow import run_xgb
from preprocess.utils import *
from utils.functions import test_best_model, print_test_errors, eval_metrics, save_best_params, plot_frecuencies

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    np.random.seed(2021)

    trainmodels = True

    data = load_cleaned_data()
    train, test = split_data(data)
    client = MlflowClient()

    if trainmodels:
        # try:
        #     experiment_elasticnet = client.create_experiment("ElasticNet")
        # except:
        #     experiment_elasticnet = client.get_experiment_by_name("ElasticNet").experiment_id
        #
        # params = {
        #     'alphas': [i for i in np.arange(0, 1.1, 0.1)],
        #     'l1_ratios': [i for i in np.arange(0, 1.1, 0.1)]
        # }
        #
        # run_elasticnet(experiment_id=experiment_elasticnet,
        #                dataset=train,
        #                params=params)
        #
        # params_stats_elasticnet = save_best_params(experiment_id=experiment_elasticnet)
        #
        # real, predictions = test_best_model(experiment_elasticnet, test)
        #
        # data = pd.DataFrame(data={
        #     'Date': test['Date'],
        #     'Real': real,
        #     'Pred': predictions
        # })
        #
        # print_test_errors(data,
        #                   method='ElasticNet')
        # (rmse, mae, r2) = eval_metrics(real, predictions)
        #
        # print(get_current_time(), "- Score RMSE Test -", rmse)
        # data.to_csv('predictions/15mins/elasticNet_2017.csv')
        # print(get_current_time(), "- Saved results of ElasticNet to CSV")
        #
        # try:
        #     experiment_knn = client.create_experiment("KNN")
        # except:
        #     experiment_knn = client.get_experiment_by_name("KNN").experiment_id
        # run_knn(experiment_id=experiment_knn,
        #         dataset=train)
        #
        # params_stats_knn = save_best_params(experiment_id=experiment_knn)
        #
        # real, predictions = test_best_model(experiment_knn, test)
        #
        # predictions = predictions.reshape(-1)
        #
        # data = pd.DataFrame(data={
        #     'Date': test['Date'],
        #     'Real': real,
        #     'Pred': predictions
        # })
        #
        # print_test_errors(data,
        #                   method='KNN')
        # (rmse, mae, r2) = eval_metrics(real, predictions)
        #
        # print(get_current_time(), "- Score RMSE KNN Test -", rmse)
        # data.to_csv('predictions/15mins/KNN_2017.csv')
        # print(get_current_time(), "- Saved results of KNN to CSV")
        #
        # try:
        #     experiment_lgbm = client.create_experiment("LGBM")
        # except:
        #     experiment_lgbm = client.get_experiment_by_name("LGBM").experiment_id
        # run_lgbm(experiment_id=experiment_lgbm,
        #          dataset=train,
        #          verbose=True)
        #
        # params_stats_lgbm = save_best_params(experiment_id=experiment_lgbm)
        #
        # real, predictions = test_best_model(experiment_lgbm, test)
        #
        # data = pd.DataFrame(data={
        #     'Date': test['Date'],
        #     'Real': real,
        #     'Pred': predictions
        # })
        #
        # print_test_errors(data,
        #                   method='LGBM')
        # (rmse, mae, r2) = eval_metrics(real, predictions)
        #
        # print(get_current_time(), "- Score RMSE LGBM Test -", rmse)
        # data.to_csv('predictions/15mins/LGBM_2017.csv')
        # print(get_current_time(), "- Saved results of LGBM to CSV")
        #
        # try:
        #     experiment_dt = client.create_experiment("DT")
        # except:
        #     experiment_dt = client.get_experiment_by_name("DT").experiment_id
        # run_dt(experiment_id=experiment_dt,
        #        dataset=train)
        #
        # params_stats_dt = save_best_params(experiment_id=experiment_dt)
        #
        # real, predictions = test_best_model(experiment_dt, test)
        #
        # data = pd.DataFrame(data={
        #     'Date': test['Date'],
        #     'Real': real,
        #     'Pred': predictions
        # })
        #
        # print_test_errors(data,
        #                   method='DT')
        # (rmse, mae, r2) = eval_metrics(real, predictions)
        #
        # print(get_current_time(), "- Score RMSE DT Test -", rmse)
        # print(get_current_time(), "- Saved results of DT to CSV")
        # data.to_csv('predictions/15mins/dt_2017.csv')

        try:
            experiment_xgb = client.create_experiment("XGB")
        except:
            experiment_xgb = client.get_experiment_by_name("XGB").experiment_id
        run_xgb(experiment_id=experiment_xgb,
                dataset=train,
                verbose=True)

        params_stats_xgb = save_best_params(experiment_id=experiment_xgb)

        real, predictions = test_best_model(experiment_xgb, test)

        data = pd.DataFrame(data={
            'Date': test['Date'],
            'Real': real,
            'Pred': predictions
        })

        print_test_errors(data,
                          method='XGB')
        (rmse, mae, r2) = eval_metrics(real, predictions)

        print(get_current_time(), "- Score RMSE XGB Test -", rmse)
        print(get_current_time(), "- Saved results of XGB to CSV")
        data.to_csv('predictions/15mins/xgb_2017.csv')

        try:
            experiment_mlp = client.create_experiment("MLP")
        except:
            experiment_mlp = client.get_experiment_by_name("MLP").experiment_id
        run_mlp(experiment_id=experiment_mlp,
                dataset=train,
                verbose=True)

        params_stats_mlp = save_best_params(experiment_id=experiment_mlp)

        real, predictions = test_best_model(experiment_mlp, test)

        data = pd.DataFrame(data={
            'Date': test['Date'],
            'Real': real,
            'Pred': predictions
        })

        print_test_errors(data,
                          method='MLP')
        (rmse, mae, r2) = eval_metrics(real, predictions)

        print(get_current_time(), "- Score RMSE MLP Test -", rmse)
        print(get_current_time(), "- Saved results of MLP to CSV")
        data.to_csv('predictions/15mins/mlp_2017.csv')

    models = os.listdir('predictions/15mins')
    name_models = [name.split('_')[0] for name in models]

    print(get_current_time(), '- Plotting predictions..')
    for model in models:
        path = 'predictions/15mins/' + model
        data = pd.read_csv(path)
        data = data.drop(columns=['Date.1'])
        plot_frecuencies(data=data,
                         method=name_models[models.index(model)])
