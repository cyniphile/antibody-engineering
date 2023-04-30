# COVID Antibody Engineering 

Engineering to improve the affinity of a COVID antibody using the dataset from [Engelhart et al. 2021](https://www.nature.com/articles/s41597-022-01779-4).

- See `Data Exploration.ipynb` for EDA.
- See `Fitness Modeling.ipynb` for antibody fitness modeling w.r.t binding affinity.
- See `Candidate Generation.ipynb` for generating candidate sequences for another round of wet-lab testing. 
  - Proposed sequences are in `data/` as explained in the notebook.


## Install

- [Install docker](https://docs.docker.com/get-docker/) and start the daemon.
- `docker-compose up` will start the container and print URLs to connect to the Jupyter web UI.
	- If you're using VSCode, install the [Remote Development Extensions Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) to easily run code and otherwise work within the docker container. 
	- Attach to the `{repo_name}-notebook-1` container.
	- Be sure to install the VSCode Python extension in the *remote* container as well. 

- The Prefect UI is available at `http://localhost:4200/` to view jobs.
- Jupyter notebooks are available at `http://localhost:8888/`. 
  - Ensure that notebooks are "trusted" in the top right corner to display interactive plots.
- Download data: `docker-compose exec -i notebook python download_data.py` 

## Usage

You can use poetry to run up an environment without Docker to save on overhead. 

- Install [poetry](https://python-poetry.org/docs/).
- Configure to create a virtual environment in the project: `poetry` config virtualenvs.in-project true`
- `poetry install` and point your notebooks to the venv.
- To add/remove packages:
  - `poetry {add|remove} {package}` 
  - `poetry export -f requirements.txt --output requirements.txt --without-hashes`. 
  - Run an environment shell: `poetry shell`
  - Run mflow locally: `mlflow ui`
  - Run `docker-compose up --build` to rebuild the image with new packages, or for faster turnaround, `docker-compose exec notebook pip install -r /usr/src/app/requirements.txt`
- To preprocess data for use in notebooks, run the Prefect flows from the `ETL.py` module:
  - `extract_seeds_of_interest` will preprocess some of the seed chains into dataframes of CDR mutations.
  - `export_ESM_embeddings` will preprocess the ESM embeddings for the sequences in the dataset `library`.

