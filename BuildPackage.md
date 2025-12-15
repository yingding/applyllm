# Create Gitlab Python Artifacts
## Build
```shell
projroot=$HOME/Code/VCS/ai
package="applyllm";
pushd $projroot/$package;
python3 -m build;
popd;
```

Output
```console
* Creating venv isolated environment...
* Installing packages in isolated environment... (setuptools>=61.0)
* Getting build dependencies for sdist...
running egg_info
creating applyllm.egg-info
writing applyllm.egg-info/PKG-INFO
writing dependency_links to applyllm.egg-info/dependency_links.txt
writing top-level names to applyllm.egg-info/top_level.txt
writing manifest file 'applyllm.egg-info/SOURCES.txt'
reading manifest file 'applyllm.egg-info/SOURCES.txt'
writing manifest file 'applyllm.egg-info/SOURCES.txt'
* Building sdist...
running sdist
running egg_info
writing applyllm.egg-info/PKG-INFO
writing dependency_links to applyllm.egg-info/dependency_links.txt
writing top-level names to applyllm.egg-info/top_level.txt
reading manifest file 'applyllm.egg-info/SOURCES.txt'
writing manifest file 'applyllm.egg-info/SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md

running check
creating applyllm-0.0.1
creating applyllm-0.0.1/applyllm
creating applyllm-0.0.1/applyllm.egg-info
copying files to applyllm-0.0.1...
copying pyproject.toml -> applyllm-0.0.1
copying applyllm/__init__.py -> applyllm-0.0.1/applyllm
copying applyllm/test.py -> applyllm-0.0.1/applyllm
copying applyllm.egg-info/PKG-INFO -> applyllm-0.0.1/applyllm.egg-info
copying applyllm.egg-info/SOURCES.txt -> applyllm-0.0.1/applyllm.egg-info
copying applyllm.egg-info/dependency_links.txt -> applyllm-0.0.1/applyllm.egg-info
copying applyllm.egg-info/top_level.txt -> applyllm-0.0.1/applyllm.egg-info
copying applyllm.egg-info/SOURCES.txt -> applyllm-0.0.1/applyllm.egg-info
Writing applyllm-0.0.1/setup.cfg
Creating tar archive
removing 'applyllm-0.0.1' (and everything under it)
* Building wheel from sdist
* Creating venv isolated environment...
* Installing packages in isolated environment... (setuptools>=61.0)
* Getting build dependencies for wheel...
running egg_info
writing applyllm.egg-info/PKG-INFO
writing dependency_links to applyllm.egg-info/dependency_links.txt
writing top-level names to applyllm.egg-info/top_level.txt
reading manifest file 'applyllm.egg-info/SOURCES.txt'
writing manifest file 'applyllm.egg-info/SOURCES.txt'
* Installing packages in isolated environment... (wheel)
* Building wheel...
running bdist_wheel
running build
running build_py
creating build
creating build/lib
creating build/lib/applyllm
copying applyllm/__init__.py -> build/lib/applyllm
copying applyllm/test.py -> build/lib/applyllm
running egg_info
writing applyllm.egg-info/PKG-INFO
writing dependency_links to applyllm.egg-info/dependency_links.txt
writing top-level names to applyllm.egg-info/top_level.txt
reading manifest file 'applyllm.egg-info/SOURCES.txt'
writing manifest file 'applyllm.egg-info/SOURCES.txt'
installing to build/bdist.macosx-13-arm64/wheel
running install
running install_lib
creating build/bdist.macosx-13-arm64
creating build/bdist.macosx-13-arm64/wheel
creating build/bdist.macosx-13-arm64/wheel/applyllm
copying build/lib/applyllm/__init__.py -> build/bdist.macosx-13-arm64/wheel/applyllm
copying build/lib/applyllm/test.py -> build/bdist.macosx-13-arm64/wheel/applyllm
running install_egg_info
Copying applyllm.egg-info to build/bdist.macosx-13-arm64/wheel/applyllm-0.0.1-py3.10.egg-info
running install_scripts
creating build/bdist.macosx-13-arm64/wheel/applyllm-0.0.1.dist-info/WHEEL
creating '/Users/yingding/VCS/github/ml/llm-examples/ApplyLlm/dist/.tmp-izj9j4uq/applyllm-0.0.1-py3-none-any.whl' and adding 'build/bdist.macosx-13-arm64/wheel' to it
adding 'applyllm/__init__.py'
adding 'applyllm/test.py'
adding 'applyllm-0.0.1.dist-info/METADATA'
adding 'applyllm-0.0.1.dist-info/WHEEL'
adding 'applyllm-0.0.1.dist-info/top_level.txt'
adding 'applyllm-0.0.1.dist-info/RECORD'
removing build/bdist.macosx-13-arm64/wheel
Successfully built applyllm-0.0.1.tar.gz and applyllm-0.0.1-py3-none-any.whl
```

You can found the `.whl` distribution package file
in `$package` -> `dist` folder

## Using deploy token
* Create gitlab group deployment token https://docs.gitlab.com/ee/user/project/deploy_tokens/

Group -> Settings -> Repository -> deploy tokens 

Add the access credential in user home dir.
`touch $HOME/.pypirc`

Push to the project, 
`https://gitlab.example.com/api/v4/projects/<project_id>/packages/pypi`
<project_id> in project -> Settings -> General -> Naming, topics, avatar
or "group%2Fproject" as URL-encoded path for "group/project"

```
[distutils]
index-servers =
    gitlab-lrz

[gitlab-lrz]
repository = https://gitlab.lrz.de/api/v4/projects/dzkj%2Fllm/packages/pypi
username = <deploy token username>
password = <deploy token>
```
* From gitlab group level https://docs.gitlab.com/ee/user/packages/pypi_repository/#install-from-the-group-level


## Allow every one to pull from project
gitlab project -> Settings -> General -> Visibilty, project features, permissions -> expand
Package registry -> Allow anyone to pull from Package Registry (activate) -> Save

(Pull from the group)
Click the published version in the package registry to see how to pull:
```shell
python3 -m pip install applyllm --no-deps --no-cache-dir --index-url https://gitlab.lrz.de/api/v4/projects/150553/packages/pypi/simple --trusted-host https://gitlab.lrz.de
```
* pull from the group https://docs.gitlab.com/ee/user/packages/pypi_repository/#install-from-the-group-level
* install your private gitlab pypi package https://stackoverflow.com/questions/2477117/pip-requirements-txt-with-alternative-index/2477610#2477610


## Publish a PyPI package by using twine
Local without CI/CD
```shell
package="./applyllm";
cd $package;
python3 -m twine upload --repository gitlab-lrz dist/*
```

You shall see the "package/tag" in the package registry

## Python package dependency
Reference:
* https://peps.python.org/pep-0631/