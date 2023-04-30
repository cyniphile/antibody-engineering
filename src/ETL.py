import torch
import esm  # type: ignore
from utils import DATA_PATH, LIBRARY_IS_HEAVY_MAP, WT_LIBRARY_MAP, get_library
from prefect import task, flow
from prefect.tasks import task_input_hash
import pandas as pd


CHAINS_TO_ADVANCE = ["AAYL49", "AAYL50"]
INCLUDED_FEATURES = ["Replicate", "Pred_affinity", "POI", "Sequence"]


@task
def extract_seeds_of_interest():
    """
    Filters data to seed chain of interest and expands CDRs sequence strings
    into columns.
    """
    df = pd.read_csv(f"{DATA_PATH}/MITLL_AAlphaBio_Ab_Binding_dataset.csv")
    # split out library prefix
    df["Library"] = df["POI"].apply(get_library)
    # Filter out negative samples
    target_df = df[df["Target"] == "MIT_Target"].copy()
    for library in CHAINS_TO_ADVANCE:
        cdr_dfs = []
        # Include wild type in library data
        lib_data = target_df[
            (target_df["Library"] == library)
            | (target_df["Library"] == WT_LIBRARY_MAP[library])
        ].copy()
        # expand each cdr string into one-col-per-residue format
        for cdr_index in range(1, 4):
            weight = "H" if LIBRARY_IS_HEAVY_MAP[library] else "L"
            cdr = f"CDR{weight}{cdr_index}"
            split_df = lib_data[cdr].str.split(pat="\s*", expand=True).iloc[:, 1:-1]  # type: ignore
            cdr_dfs.append(split_df.add_prefix(f"{cdr_index}_"))
        # concat the cdr dataframes into one
        all_cdrs_df = pd.concat(cdr_dfs, axis=1)
        other_features = target_df.loc[all_cdrs_df.index][INCLUDED_FEATURES]
        all_cdrs_df = pd.concat([other_features, all_cdrs_df], axis=1)
        all_cdrs_df.to_parquet(f"{DATA_PATH}/{library}_expanded.parquet")


@task
def extract_fasta(library: str):
    """
    export full sequences in fasta format digestible by the `esm` library's
    embedding extraction script:
    ```
    # run in colab with GPU for better speed
    !python extract.py esm2_t33_650M_UR50D ./data/{library}_full_seqs.fasta data/{library}_emb_esm2/  --include mean
    ```
    """
    df = pd.read_parquet(f"{DATA_PATH}/{library}_expanded.parquet")
    with open(f"{DATA_PATH}/{library}_full_seqs.fasta", "w") as f:
        (
            df.reset_index().apply(
                lambda seq: f.write(
                    f">{seq['index']}|{seq['POI']}-{seq['Replicate']}|{seq['Pred_affinity']}\n{seq['Sequence']}\n"
                ),
                axis=1,
            )
        )


@task
def export_ESM_embeddings(library: str):
    """
    given a set of embeddings extracted from ESM via ESM's `extract.py` script
    format those into a dataframe and save to parquet file
    """
    fasta_path = f"./data/{library}_full_seqs.fasta"
    emb_path = f"./data/{library}_emb_esm2"  # Path to directory of embeddings
    EMB_LAYER = 33  # default
    ys = []
    Xs = []
    ixs = []
    pois = []
    for header, _seq in esm.data.read_fasta(fasta_path):
        info = header.split("|")  # type: ignore
        scaled_effect = info[-1]
        # original index from Engelhart dataframe
        index = info[0]
        ys.append(float(scaled_effect))
        pois.append(info[1].split("-")[0])
        fn = f"{emb_path}/{header}.pt"
        embeddings = torch.load(fn)
        Xs.append(embeddings["mean_representations"][EMB_LAYER])
        ixs.append(index)
    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_df = pd.DataFrame(Xs)
    Xs_df["Pred_affinity"] = ys
    Xs_df["POI"] = pois
    # use original index from Engelhart df
    Xs_df = Xs_df.set_index(pd.Series(ixs))
    # suffix trick to cast col names to str for parquet
    Xs_df.add_suffix("").to_parquet(f"{DATA_PATH}/{library}_emb_esm2.parquet")


@flow
def extract_seeds_of_interest_flow():
    extract_seeds_of_interest()


@flow
def export_ESM_embeddings_flow(library: str):
    export_ESM_embeddings(library)


if __name__ == "__main__":
    extract_seeds_of_interest_flow()
