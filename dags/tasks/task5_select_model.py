from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
from tasks.task4_train_models import prepare_data


def train_and_save_model(model, X, y, path_to_model='/app/clean_data/best_model.pckl'):
    model.fit(X, y)
    dump(model, path_to_model)
    print(f"[Task 5] {str(model)} saved at {path_to_model}")


def select_and_save_best_model(ti):
    """
    Task (5) — Pull XCom scores from tasks 4', 4'', 4''',
    identify the best model (highest neg_mean_squared_error → closest to 0),
    retrain it on all data and save to /app/clean_data/best_model.pckl.
    """

    # --- Pull scores from XCom ---------------------------------------------
    lr_score = ti.xcom_pull(key='score', task_ids='train_linear_regression')
    dt_score = ti.xcom_pull(key='score', task_ids='train_decision_tree')
    rf_score = ti.xcom_pull(key='score', task_ids='train_random_forest')
    
    print(f"[Task 5] Scores received via XCom:")
    print(f"         LinearRegression      → {lr_score:.4f}")
    print(f"         DecisionTreeRegressor → {dt_score:.4f}")
    print(f"         RandomForestRegressor → {rf_score:.4f}")

    # --- Select best (neg_mse: higher = better, i.e. closest to 0) ---------
    scores = {
        'LinearRegression':      (lr_score, LinearRegression()),
        'DecisionTreeRegressor': (dt_score, DecisionTreeRegressor()),
        'RandomForestRegressor': (rf_score, RandomForestRegressor()),
    }

    best_name = max(scores, key=lambda k: scores[k][0])
    best_model = scores[best_name][1]
    print(f"[Task 5] Best model: {best_name} (score={scores[best_name][0]:.4f})")

    # --- Retrain on ALL data and save --------------------------------------
    X, y = prepare_data()
    train_and_save_model(best_model, X, y)