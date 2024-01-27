from load import load_csv
from preprocess import process_data, transform_data
from train_predict import train_and_predict
from config import CSV_DATA_PATH
from prefect import flow

@flow(name="Build model flow")
def pipeline_build_model():

    print("Step 1 - Load data")
    df = load_csv(CSV_DATA_PATH)

    print("Step 2 - Prepocessing data")
    df_clean = process_data(df)

    print("Step 3 - Split data")
    x_train, x_test, y_train, y_test = transform_data(df_clean)

    print("Step 4 - Train and evaluate model")
    model, score_f1 = train_and_predict(x_train,y_train, x_test, y_test)
    print(score_f1)

d = pipeline_build_model().run()

