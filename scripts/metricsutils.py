import os
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
from neuralhydrology.evaluation import metrics



def gather_nse_metrics(run_dir: str, exp_name: str) -> pd.DataFrame:
    """Gathers NSE metrics for all runs that are related to a certain experiment.

    Parameters
    ----------
    run_dir: str
        Parent directory that contains several run directories
    exp_name: str
        Name of the experiment that will be used for filtering run directories

    Returns
    -------
    pd.DataFrame
        NSE values for each basin related to the runs for the specified experiment name as DataFrame.
    """
    id_arr = []
    nse_arr = []
    exp_arr = []
    timespan_arr = []
    folders = os.listdir(run_dir)
    exp_folders = list(filter(lambda x: x.startswith(exp_name), folders))
    for folder in exp_folders:
        exp_run_dir = Path(run_dir + folder)
        with open(exp_run_dir / "test" / "model_epoch030" / "test_results.p", "rb") as fp:
            results = pickle.load(fp)
        for key in results.keys():
            id_arr.append(key)
            nse_arr.append(results[key]['1D']['NSE'])
            exp_arr.append(exp_name)
            if key in ["100061", "100068", "100085", "159783", "100086"]:
                timespan_arr.append("short")
            else:
                timespan_arr.append("full")
    return pd.DataFrame(data={"basin_id": id_arr, "nse": nse_arr, "exp_name": exp_arr, "timespan": timespan_arr})


def calculate_yearly_nse(run_dir: str, exp_name: str, start_year: int, end_year: int) -> pd.DataFrame:
    """Calculates yearly NSE metrics for all runs that are related to a certain experiment within a specified time span.

    Parameters
    ----------
    run_dir: str
        Parent directory that contains several run directories
    exp_name: str
        Name of the experiment that will be used for filtering run directories
    start_year: int
        Start year of the time span
    end_year: int
        End year of the time span

    Returns
    -------
    pd.DataFrame
        Yearly NSE values for each basin related to the runs for the specified experiment name as DataFrame.
    """

    id_arr = []
    nse_arr = []
    exp_arr = []
    year_arr = []
    folders = os.listdir(run_dir)
    exp_folders = list(filter(lambda x: x.startswith(exp_name), folders))
    for folder in exp_folders:
        exp_run_dir = Path(run_dir + folder)
        with open(exp_run_dir / "test" / "model_epoch030" / "test_results.p", "rb") as fp:
            results = pickle.load(fp)
        for key in results.keys():
            for year in range(start_year, end_year + 1):
                id_arr.append(key)
                exp_arr.append(exp_name)
                year_arr.append(year)
                qobs = results[key]['1D']['xr']['discharge_spec_obs']
                qsim = results[key]['1D']['xr']['discharge_spec_sim']
                try:
                    nse = metrics.nse(qobs.loc[str(year)].isel(time_step=-1),
                                    qsim.loc[str(year)].isel(time_step=-1))
                    nse_arr.append(nse)
                except KeyError:
                    nse_arr.append(np.nan)
    result = pd.DataFrame(data={"basin_id": id_arr, "nse": nse_arr, "exp_name": exp_arr, "year": year_arr})
    return result

def gather_simulation_timeseries(run_dir, exp_names, basin):
    res_dict = {}
    for exp in exp_names:
        folders = os.listdir(run_dir)

        exp_folders = list(filter(lambda x: x.startswith(exp), folders))
        exp_run_dir = Path(run_dir + exp_folders[0])
        with open(exp_run_dir / "test" / "model_epoch030" / "test_results.p", "rb") as fp:
            results = pickle.load(fp)
            xd = results[basin]["1D"]["xr"]
            exp = exp.rstrip("-" + basin)
            res_dict[exp] = xd
    return res_dict
