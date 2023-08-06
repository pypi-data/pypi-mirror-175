kubelink automatically sync files to kubernetes pods. It speed up your development. You just work with your local files and kubelink automatically syncing them to your kubernetes cluster.

Using kubelink is as simple as:
1. `kubelink create --name mypreset --source ./ --destination /code --namespace default --selector "app=backend"` to create a preset with your settings
2. `kubelink watch mypreset` to start syncing files


Installation
============






How to build and publish package
--------------------------------
1.  Build setup.py
```
python setup.py sdist bdist_wheel
```
2. 
```
twine upload dist/*
```