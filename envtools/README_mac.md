# Create
```shell
# pushd /Users/yingding/Code/VCS/ai/llm-train;
VERSION=3.12;
ENV_NAME="applyllm${VERSION}";
source ./envtools/create_env.sh -p ~/Code/VENV -e ${ENV_NAME} -v $VERSION;
# pip install --upgrade pip
# popd;
```

# Activate
```shell
VERSION=3.12;
ENV_NAME="applyllm${VERSION}";
PROJ_PATH="$HOME/Code/VCS/ai/applyllm/llm-examples/setup";
source ~/Code/VENV/${ENV_NAME}/bin/activate;
python3 -m pip install -r ${PROJ_PATH}/requirements_arm64_mac_312.txt --no-cache;
```