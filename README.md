# The Impact of Land Cover Data on Rainfall-Runoff Prediction Using an Entity-Aware-LSTM
The code in this repository relates to the abstract [The Impact of Land Cover Data on Rainfall-Runoff Prediction
Using an Entity-Aware-LSTM](https://meetingorganizer.copernicus.org/EGU21/EGU21-1136.html) presented as a vPICO
presentation at the EGU General Assembly 2021 in the session _HS3.4 - 'Deep learning in hydrological science'_.
All results and graphics can be reproduced following the README instructions and running the Jupyer Notebook in this repository.

`Drost, S., Netzel, F., Wytzisk-Ahrens, A., and Mudersbach, C.: The Impact of Land Cover Data on Rainfall-Runoff
Prediction Using an Entity-Aware-LSTM, EGU General Assembly 2021, online, 19–30 Apr 2021, EGU21-1136,
https://doi.org/10.5194/egusphere-egu21-1136, 2021.`

## Get started
To get prepared for running the code and reproducing the results you first have to set up your local environment by
installing all required Python dependencies and downloading those datasets that are not included in this repository.
Especially, we make extensive use of the great [neuralHydrology](https://github.com/neuralhydrology/neuralhydrology)
Python package, which implements several Deep Learning models for use cases from the hydrology.
1. Make sure, you have locally installed a conda distribution (e.g., [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
   or [Anaconda](https://docs.anaconda.com/))
    
2. Recreate the conda environment by running `conda env create -f environment.yml` from the conda command line and activate
it with `conda activate egu21-rrp-landcover-lstm`

3. Install the neuralHydrology package by running `pip install git+https://github.com/neuralhydrology/neuralhydrology.git`. 
   If you'd rather wish to install a specific version, you can clone the repository to your local machine by running
   `git clone https://github.com/neuralhydrology/neuralhydrology.git`, checkout a certain branch and install it with
   `pip install -e .`. For our studies, we used the 1.0.0-alpha release.
   
4. Download the CAMELS-GB dataset which contains hydro-meteorological timeseries for 671 catchments across Great Britain. 
   This dataset is required for training the LSTM and EA-LSTM models for certain experiments. You can access the dataset via
   https://catalogue.ceh.ac.uk/documents/8344e4f3-d2ea-44f5-8afa-86d2987543a9 by creating an account for the Environmental
   Information Data Centre.
   
5. Extract the CAMELS-GB archive and copy the whole _timeseries_ folder to _./data/camels-gb_.  
   
## Project structure
* `./config`: The _./config_ folder contains config files for training and evaluating the models via _neuralHydrology_ used
  in 4 different experiments.
  
* `./data`: The _./data_ folder holds all datasets, required for model training and evaluation. In particular, these are:
   * `./wv`: Timeseries data and land cover frequencies as static attributes for 12 subbasins from the Wupper region as
   well as some geospatial datasets related to these.
     
   * `./camels-gb`: After downloading the CAMELS-GB dataset and copying the timeseries folder, _./camels-gb_ contains 
   timeseries data for the 671 CAMELS-GB catchments as well as land cover frequencies as static attributes.
     
* `./runs`: After [model training and evaluation](#model-training-and-evaluation), this folder contains the results
  created by the neuralHydrology package. These results will be used in the Jupyter Notebook for producing the figures.
  
* `./scripts`: For convenience, this folder contains some scripts which will be utilized by the Jupyter Notebook.

## Model training and evaluation
We trained and evaluated LSTM and EA-LSTM models to predict in 4 different experimental setups to predict rainfall runoff
of 12 subbasins located in the Wupper region. You can train the models from scratch by using the configurations files
provided within the _./config_ folder. For a detailed documentation of the neuralHydrology package have a look in its
[documentation](https://neuralhydrology.readthedocs.io/en/latest/index.html).   
### Model training
To start training one of the models, run `nh-run --config-file /path/to/config.yml`. For instance, to train the model for the
_ealstm-camelsgb-wv_ experiment, run `nh-run --config-file ./ealstm-camelsgb-wv.yml` from the root of this repository. To
train multiple models the neuralHydrology package supports certain execution parameters you can read about in the
package documentation.
### Model evaluation
After training, you can evaluate your models by running `nh-run evaluate --run-dir /path/to/run_dir/`. Just specify one
of the generated run directories, which contains the model states.  
**Note:** For _ealstm-camels-wv_ and _lstm-camels-wv_
you have to replace the config file within the created run directories by the _ealstm-camels-wv-test.yml_ and _lstm-camels-wv-test.yml_
configuration files, since we use CAMEL-GB for training and the Wupper region dataset for testing.

## Run the code
For reproducing the figures you can run the _./analysis.ipynb_ via Jupyter Notebook. Start the server by running
`jupyter notebook` from conda prompt and have fun.

## License
Apache License, Version 2.0