# Pyfarmsay
![Badger](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-4/actions/workflows/github-workflow.yml/badge.svg)

Expanding on the existing package, [pycowsay](https://pypi.org/project/pycowsay/), pyfarmsay does not only feature a talking cow, but an entire talking farm! Our beautiful farm features a talking cow, pig, chicken, dog, penguin, and sheep. 

## Install 
To install our package on your local machine, run the following command:

```
pip install pyfarmsay 
```

To install into a virtual environment, make sure you install pipenv by running the following:
```
pip install pipenv
```
and then use the following command to install our package into an isolated virtual environment. 
```
pipenv install pyfarmsay 
```

This will create a virtual environment, which you can access by running ```pipenv shell```

## Run 
Once pyfarmsay is installed on your machine (or virtual environment), you can use it from the command line or from within a python file. 
### From the Command Line
To run the package from the command line, all you have to do is invoke the package name, followed by the animal of your choice and your desired message:
```
pyfarmsay [ANIMAL] [MESSAGE]
```
For example, 

```
pyfarmsay cow i say moo
```
will output

```
 -----------
< i say moo >
 -----------
    \
     \
      ^__^
      (oo)\_______
      (__)\       )\/\
          ||----w |
          ||     ||

```

### Import into a python module
Use the following import statement at the very top of your `.py` file to use the functions from within your module. 
```
from pyfarmsay import pyfarmsay
```
or 

```
from pyfarmsay.pyfarmsay import [function name]
```
to import a specific function from the package.
## Package functions
Pyfarmsay comes with the following 7 main functions, each accepting a message argument:

1. `cowsay` (use `cow` for the animal argument if you are invoking the function from the command line)
2. `pigsay` (use `pig` for the animal argument if you are invoking the function from the command line)
3. `chickensay` (use `chicken` for the animal argument if you are invoking the function from the command line)
4. `sheepsay` (use `sheep` for the animal argument if you are invoking the function from the command line)
5. `penguinsay` (use `penguin` for the animal argument if you are invoking the function from the command line)
6. `dogsay` (use `dog` for the animal argument if you are invoking the function from the command line)
7. `farmsay` (use `farm` for the animal argument if you are invoking the function from the command line)

Our animals can only repeat what you tell them to say, so if no message is given, each animal will call out their native animal sound. 


