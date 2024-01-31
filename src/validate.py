import pandas as pd
from prefect import task, flow
import great_expectations as ge
import json


@task(name="validate_df_great_expectation", tags=['validation'])
def validate_df_great_expectation(
        df: pd.DataFrame,
) -> bool:
    expectation_suite = json.load(open("/app/gx/expectations/HeartDisease-expectation.json"))
    df_ge = ge.from_pandas(df, expectation_suite=expectation_suite)
    validation = df_ge.validate()
    validation_json = validation.to_json_dict()
    with open("validation_data.json", "w") as json_file:
        json.dump(validation_json, json_file)

    return validation["success"]



@flow(name="validate_df", retries=1, retry_delay_seconds=30)
def validate_df(
        df: pd.DataFrame,
):
    is_valid= validate_df_great_expectation(df)
    if (is_valid):
        print("Validation passed")
    else:
        print("Validation failed")
        raise ValueError("Validation failed")
