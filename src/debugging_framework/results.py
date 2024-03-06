from typing import List, Tuple
import pandas as pd


def initialize_dataframe(
    subject_names: List[Tuple[str, int]], tool_names: List[str], number_of_runs
):
    # Initialize the DataFrame
    columns = pd.MultiIndex.from_tuples(subject_names, names=["Subject", "ID"])
    index = pd.MultiIndex.from_product(
        [range(1, number_of_runs + 1), tool_names], names=["Run", "Approach"]
    )
    results_df = pd.DataFrame(index=index, columns=columns).fillna({})
    return results_df
