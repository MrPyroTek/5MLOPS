import pandas as pd
from prefect import task


@task(name='load_csv', tags=['preprocessing'])
def load_csv(
        path: str,
) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0).reset_index(drop=True)
    return df
