import os
import pathlib

DOCKER_DATA_PATH = "/code/data/"


def get_git_root():
    last_cwd = os.getcwd()
    while not os.path.isdir(".git"):
        os.chdir("..")
        cwd = os.getcwd()
        if cwd == last_cwd:
            raise OSError("no .git directory")
        last_cwd = cwd
    return last_cwd


LOCAL_DATA_PATH = str(pathlib.Path(get_git_root()) / "data")


def get_data_path():
    try:
        is_docker = os.environ["DOCKER_ENV_DATA_PROJECT"]
        if is_docker:
            path = DOCKER_DATA_PATH
        else:
            path = LOCAL_DATA_PATH
    except KeyError:
        path = LOCAL_DATA_PATH
    return path


def set_mlflow_uri():
    try:
        is_docker = os.environ["DOCKER_ENV_DATA_PROJECT"]
        if is_docker:
            # mlflow uri is set in docker
            pass
    except KeyError:
        os.environ["MLFLOW_TRACKING_URI"] = "http://127.0.0.1:5000/"


SET_MLFLOW_URI = set_mlflow_uri()
DATA_PATH = get_data_path()

WT_LIBRARY_MAP = {
    "AAYL49": "MIT_14_HL_scFV",
    "AAYL50": "MIT_14_HL_scFV",
    "AAYL51": "MIT_91_LH_scFV",
    "AAYL52": "MIT_95_HL_scFV",
}

LIBRARY_IS_HEAVY_MAP = {
    "AAYL49": True,
    "AAYL50": False,
    "AAYL51": True,
    "AAYL52": False,
}


def get_library(x: str) -> str:
    splits = x.split("_")
    if splits[0] == "MIT":
        return x
    else:
        return splits[0]


def aggregate_replicates(df, fillna="max"):
    """
    Collapse replicates into one row with mean `Pred_affinity` value. NAs are filled
    with the max `Pred_affinity` or dropped.

    df must have `Pred_affinity` and `POI` columns
    """
    if fillna == "max":
        df = df.fillna(df["Pred_affinity"].max())
    else:
        df = df.dropna()
    mean_pred_affinities = df.groupby("POI")["Pred_affinity"].mean()
    mean_replicate_df = df.drop_duplicates(subset=["POI"]).set_index("POI")
    mean_replicate_df["Pred_affinity"] = mean_pred_affinities
    return mean_replicate_df
