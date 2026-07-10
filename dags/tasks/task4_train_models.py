import pandas as pd
from sklearn.model_selection import cross_val_score
 
  
def prepare_data(path_to_data='/app/clean_data/fulldata.csv'):
    df = pd.read_csv(path_to_data)
    df = df.sort_values(['city', 'date'], ascending=True)
 
    dfs = []
    for c in df['city'].unique():
        df_temp = df[df['city'] == c].copy()
 
        # creating target
        df_temp['target'] = df_temp['temperature'].shift(1)
 
        # creating features (lag features)
        for i in range(1, 10):
            df_temp[f'temp_m-{i}'] = df_temp['temperature'].shift(-i)
 
        df_temp = df_temp.dropna()
        dfs.append(df_temp)
 
    df_final = pd.concat(dfs, axis=0, ignore_index=False)
    df_final = df_final.drop(['date'], axis=1)
    df_final = pd.get_dummies(df_final)
 
    features = df_final.drop(['target'], axis=1)
    target = df_final['target']
 
    return features, target
 
 
def compute_model_score(model, X, y):
    cross_validation = cross_val_score(
        model,
        X,
        y,
        cv=3,
        scoring='neg_mean_squared_error'
    )
    return cross_validation.mean()


def train_and_evaluate_model(model, ti):
    """
    Generic task for any regression model.
    Computes cross-val score and pushes it to XCom.
    """
    X, y = prepare_data()
    score = compute_model_score(model, X, y)
    model_name = type(model).__name__
    print(f"[Task 4] {model_name} score: {score}")
    ti.xcom_push(key='score', value=score)
