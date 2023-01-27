# COMS 4701 HW 1 Programming

Assignment overview:
Grid world path planning using search algorithms. 

## Install / Run Instructions

Create and activate a virtual environment for the project (at the project root directory):

```
python -m venv .venv
```

To enter the enviroment, please run the following if you are using a Mac

```
source .venv/bin/activate
```

If you are using Windows, please run

```
.venv\scripts\activate.bat
```

Install poetry in your virtual environment.

```
pip install poetry
```

Install all project dependencies

```
poetry install
```

This will set up the packages needed for the homework.

You can now modify files in `hw1/` and run the program at the root directory of the project via

```
poetry run main [directory of the grid world .npy files]
```
