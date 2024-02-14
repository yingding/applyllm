# applyllm: python package
This repository contains code of [applyllm](https://pypi.org/project/applyllm/) python PyPI package, for loading and training open source llm models e.g. LlaMA2, Mixtral 8x7B, etc.

## Install the package
```shell
pip install applyllm
```

## Setup a local venv on Macosx Apple Silicon
```shell
python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r ./llm-examples/setup/requirements310mac.txt
```

## Build locally
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
make clean && make build && make reload
```

## Publish the test pypi package
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
make clean && make build && make testpypi
```
* `$HOME/.pypirc` shall be availabe, visit [Build python package docs](./BuildPackage.md) for details to create `$HOME/.pypirc` file to publish PyPI package
* visit https://test.pypi.org to see the test package published 

## Publish the pypi package
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
make clean && make build && make applyllm
```
* `$HOME/.pypirc` shall be availabe, visit [Build python package docs](./BuildPackage.md) for details to create `$HOME/.pypirc` file to publish PyPI package
* visit https://pypi.org/ to see the package published

## Add a jupyter notebook kernel to VENV
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
python3 -m pip install --upgrade pip
python3 -m pip install ipykernel
deactivate
```

We need to reactivate the venv so that the ipython kernel is available after installation.
```shell
VENV_NAME="llm3.10"
VENV_DIR="$HOME/VENV"
source ${VENV_DIR}/${VENV_NAME}/bin/activate;
python3 -m ipykernel install --user --name=${VENV_NAME} --display-name ${VENV_NAME}
```
Note: 
* restart the vs code, to select the venv as jupyter notebook kernel

Reference:
* https://ipython.readthedocs.io/en/stable/install/kernel_install.html
* https://anbasile.github.io/posts/2017-06-25-jupyter-venv/

## Remove ipykernel
```shell
VENV_NAME="llm3.10"
jupyter kernelspec uninstall -y ${VENV_NAME}
```

## Remove all package from venv
```
python3 -m pip freeze | xargs pip uninstall -y
python3 -m pip list
```

## Sync AIMLflow
```shell
aim_repo_path=./aimruns
mlflow_uri=./mlruns
mkdir ${aim_repo_path}
cd ${aim_repo_path}
aim init
cd ..
# start a watch process
aimlflow sync --mlflow-tracking-uri=${mlflow_uri} --aim-repo=${aim_repo_path}
# start a second terminal
aim up --repo=${aim_repo_path}
```

## Restart MLflow UI
If the default port 5000 is used
```shell
ps -A | grep gunicorn
pkill -f gunicorn
ps -A | grep gunicorn
# use relative path to set the backend-store-uri, full path with file:///root/sub/mlruns
mlflow ui --backend-store-uri llm-examples/mlruns
# mlflow server --host 127.0.0.1 --port 8080
```

Reference:
* https://stackoverflow.com/questions/60531166/how-to-safely-shutdown-mlflow-ui/63141642#63141642
* mlflow backend store uri https://stackoverflow.com/questions/63525498/how-do-i-set-a-different-local-directory-for-mlflow


# Relevant Tech Info

* [LLM tech docs](./LLM.md)
* [Build python package docs](./BuildPackage.md)
* mlflow https://mlflow.org/docs/latest/llms/langchain/guide/index.html
* mlflow langchain flavour https://mlflow.org/docs/latest/llms/langchain/index.html
* AIM https://github.com/aimhubio/aim
* AIM, Weights And Biases https://medium.com/aimstack/aim-tutorial-for-weights-and-biases-users-bfbdde76f21e


## Makefile **space 4 issue
Makefile need tab as indent, not space 4
* https://stackoverflow.com/questions/16931770/makefile4-missing-separator-stop/72198029#72198029


## Reference:
* build python resource package .whl https://docs.gitlab.com/ee/user/packages/workflows/build_packages.html#pypi
* upload .whl to the package registry https://docs.gitlab.com/ee/user/packages/pypi_repository/#install-from-the-group-level
* python package release name convention https://peps.python.org/pep-0440/
* build package with sub package https://stackoverflow.com/questions/44834/what-does-all-mean-in-python/35710527#35710527
* Merge dictionary https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python