# Containerized App Exercise

# Project Name

![Server Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Client Build Status](https://img.shields.io/badge/tests-100%25-success)

## Description
A plain-language, easy-to-understand description of your project goes here. This should include the main purpose of the project, its key features, and any unique elements it has. Try to keep it concise yet informative.

## Team Members
- [Vincent Bai](https://github.com/VincentBai-dotcom )

- [Jiasheng Wang](https://github.com/isomorphismss)
- [Fuzhen Li](https://github.com/fzfzlfz)
- [Xuefeng Song](https://github.com/wowwowooo)
- [Yuantian Tan](https://github.com/AsukaTan)

## Configuration and Setup
Using Git Bash, clone the directory using:

```
git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition
```

Open Docker

Open cmd

```
cd "path/to/root"
```

Then, manipulate docker 

```
docker-compose build
docker-compose up
```

Go to http://localhost:5000/

## Notes and Links

- Link to the Task Board:

  - [Project Board](https://github.com/orgs/software-students-fall2023/projects/82)

- formatted in accordance with [PEP 8](https://www.python.org/dev/peps/pep-0008/) using the [black](https://black.readthedocs.io/en/stable/) formatter.

- linted using [pylint](https://www.pylint.org/).

- The Machine Learning Client and Web App are tested using local environment.

- Coverage shows down below. 

  ```
  PS C:\Users\qq353\PycharmProjects\4-containerized-app-exercise-m5-competition\machine-learning-client> pipenv run coverage run -m pytest .\tests\test_ml_app.py
  =============================================================================== test session starts ===============================================================================
  platform win32 -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0
  rootdir: C:\Users\qq353\PycharmProjects\4-containerized-app-exercise-m5-competition
  configfile: pytest.ini
  plugins: requests-mock-1.11.0
  collected 3 items                                                                                                                                                                  
  
  tests\test_ml_app.py ...                                                                                                                                                     [100%]
  
  ================================================================================ warnings summary ================================================================================= 
  ..\..\..\.virtualenvs\4-containerized-app-exercise-m5-competitio-YPmqLdbi\Lib\site-packages\pkg_resources\__init__.py:2868
  ..\..\..\.virtualenvs\4-containerized-app-exercise-m5-competitio-YPmqLdbi\Lib\site-packages\pkg_resources\__init__.py:2868
    C:\Users\qq353\.virtualenvs\4-containerized-app-exercise-m5-competitio-YPmqLdbi\Lib\site-packages\pkg_resources\__init__.py:2868: DeprecationWarning: Deprecated call to `pkg_resources.declare_namespace('zope')`.
    Implementing implicit namespace packages (as specified in PEP 420) is preferred to `pkg_resources.declare_namespace`. See https://setuptools.pypa.io/en/latest/references/keywords.html#keyword-namespace-packages
      declare_namespace(pkg)
  
  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  ========================================================================== 3 passed, 2 warnings in 3.23s ========================================================================== 
  PS C:\Users\qq353\PycharmProjects\4-containerized-app-exercise-m5-competition\machine-learning-client> pipenv run coverage report                              
  Name                   Stmts   Miss  Cover
  ------------------------------------------
  app.py                    55     17    69%
  ml_client.py              11      0   100%
  tests\__init__.py          0      0   100%
  tests\test_ml_app.py      40      0   100%
  ------------------------------------------
  TOTAL                    106     17    84%
  PS C:\Users\qq353\PycharmProjects\4-containerized-app-exercise-m5-competition\machine-learning-client> 
  ```

