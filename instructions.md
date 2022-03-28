# Introduction

This is an example project on how to load and using the Kinect data from
within a python project.

It is recommended to use an IDE for development of this project. The
recommended IDE is `pycharm`, whether the community edition or the
version you can get from being a student.

# Getting up and running

## Pre-requisites

You will need to have `python 3` on your system - preferably a version
greater than `3.7`. This package may work with other versions however it
has not been tested.

## Virtual Environment

As specified in [Preparations for Submission](#submission), you will
need to provide a file with all your project requirements. The simplest
way is to use `poetry` to create and manage your virtual environment,
however `pipenv` and a plain `requirements.txt` is also allowed.

### Poetry

1.  Setup

    Make sure poetry is installed - it can be installed via
    `pip install poetry`.

    While not necessary, it is recommended to set your virtual
    environment to be placed in the repository directory to make it
    easier for IDEs to recognise it (this is required for pycharm). The
    following command sets it up.

    ``` {.bash org-language="sh"}
    poetry config virtrualenvs.in-project true --local
    ```

2.  First Time

    To finish setup of the virtual environment, you need to run the
    following:

    ``` {.bash org-language="sh"}
    poetry install
    ```

    You can activate the environment using the `poetry shell` command.

3.  Adding Libraries

    If you wish to add additional libraries to those currently
    installed, you can use the following:

    ``` {.bash org-language="sh"}
    poetry add library_name
    ```

### Pipenv

1.  Setup

    Pipenv can be installed via `pip install pipenv`. You will have to
    rename [file:Pipfile.example](Pipfile.example) to Pipfile to make
    this work.

2.  First Time

    In order to setup everything from the command line, the simplest way
    is to run:

    ``` {.bash org-language="sh"}
    pipenv update
    ```

    You can then activate the environment using `pipenv shell`

3.  Adding Libraries

    You can install a library using the following command:

    ``` {.bash org-language="sh"}
    pipenv install library_name
    ```

# Preparations for Submission []{#submission}

Please make sure that all packages used via pip are saved in
`requirements.txt`, `PipFile`, or `pyproject.toml`. **Specify which in
your instructions**.
