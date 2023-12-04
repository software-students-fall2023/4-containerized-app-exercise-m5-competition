# Audio Transcription Service

[![Web-App CI/CD](https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition/actions/workflows/web_app_test.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition/actions/workflows/web_app_test.yml)
[![Machine-Learning-Client CI](https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition/actions/workflows/ml_client_test.yml/badge.svg)](https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition/actions/workflows/ml_client_test.yml) 

## Introduction
Our Audio Transcription Service allows you to either record your own audio or upload an existing audio file. We will then provide you with an English transcription and sentiment polarity analysis of the content.

## Team Members
- [Jiasheng Wang](https://github.com/isomorphismss)
- [Vincent Bai](https://github.com/VincentBai-dotcom)
- [Fuzhen Li](https://github.com/fzfzlfz)
- [Yuantian Tan](https://github.com/AsukaTan)
- [Xuefeng Song](https://github.com/wowwowooo)

## Usage

### Accessing the Deployed Application

The application is deployed and publicly accessible. You can interact with it directly without installing anything locally.

- **URL**: [http://64.225.26.135:6001](http://64.225.26.135:6001)
- Just click the link or copy-paste it into your browser's address bar.

#### Special Instructions for Chrome Users
If you are using Google Chrome and need to use features like microphone access, follow these steps to bypass security restrictions due to the site being hosted on a bare IP address:

1. **Open Chrome Flags**:
   - Type `chrome://flags/#unsafely-treat-insecure-origin-as-secure` in your Chrome address bar and press `Enter`.

2. **Enable Insecure Origins**:
   - In the "Insecure origins treated as secure" section, add `http://64.225.26.135:6001`.
   - Change the dropdown from 'Disabled' to 'Enabled'.

3. **Relaunch Chrome**:
   - Click the 'Relaunch' button to apply the changes.

Please note that this workaround should be used cautiously as it can introduce security risks. It's recommended only for testing or non-sensitive use. We apologize for any inconvenience and are working to provide a more seamless experience in future updates.


### Prerequisites for Local Setup
- Ensure you have [Python](https://www.python.org/downloads/) 3.9 or higher installed on your system.
- Make sure you have [Docker](https://docs.docker.com/get-docker/) installed and running on your computer. 
- Our project includes a feature to record audio from the front-end. For this, ensure your computer has a microphone and that it is accessible via your browser.

### Running the Application Locally
- Clone the repository:

    ```shell
    git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition
    ```
- Navigate to the project root directory:

    ```shell
    cd 4-containerized-app-exercise-m5-competition
    ```
- Start the `Docker` application.
- Use `docker-compose` to build the images:

    ```shell
    docker-compose build
    ```
- Start the application using `docker-compose`:

    ```shell
    docker-compose up
    ```
- Verify that the project is up and running by checking for the following messages in your terminal:

    ```shell
    my_web_app    |  * Running on all addresses (0.0.0.0)
    my_web_app    |  * Running on http://127.0.0.1:5000
    ```

    ```shell
    my_ml_client  |  * Running on all addresses (0.0.0.0)
    my_ml_client  |  * Running on http://127.0.0.1:5000
    ```
- Access the application in your browser at:

    ```shell
    http://localhost:6001
    ```

### How to Use the Application
After starting the application (either locally or via the deployed URL) and navigating to the home page, you have the option to either register for an account or use the app as a guest. You can upload an existing audio file or record a new one using the app's record button. Once the audio is processed, you'll be able to view the transcript and sentiment analysis. 

If you choose to register and log in, you gain additional features like viewing your transcription history and listening to the original audio. 

### Kind Reminders
- Please avoid uploading excessively large files or recording very long audio, as this could lead to slow processing times. The system's timeout is set to 60 seconds.
- Currently, the supported audio file formats are `.wav` and `.webm`.

### Stopping the Application
To stop the application and remove the containers, execute the following command in your terminal:

```shell
docker-compose down
```

## Tests
Our project uses `pylint` for linting, `black` for formatting, `pytest` (for the machine-learning-client) and `pytest-flask` (for the web-app), with test coverage reported by `coverage`. To run these tests locally, follow these steps:

### Prerequisites
- Ensure you have [Python](https://www.python.org/downloads/) 3.9 or higher installed on your system.
- The application also depends on [ffmpeg](https://ffmpeg.org/download.html). While it is already included in the Dockerfile, and thus not required for Docker-based runs, you will need to install it locally for local testing. To do so, follow the installation instructions on the `ffmpeg` website and ensure that `ffmpeg` is added to your system's `PATH` environment variable.

### Cloning the Project

```shell
git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-m5-competition
```

### Navigating to the Project Root Directory

```shell
cd 4-containerized-app-exercise-m5-competition
```

### Installing pipenv
If `pipenv` is not installed on your machine, install it using:

```shell
pip install pipenv
```

### Installing Dependencies
Install all the necessary dependencies by executing:

```shell
pipenv install
```

### Activating the Virtual Environment
Activate the virtual environment using:

```shell
pipenv shell
```

### Running Tests
Navigate to either the `web-app` or `machine-learning-client` subdirectory depending on which component you want to test.

For the web-app:

```shell
cd web-app
```

For the machine-learning-client:

```shell
cd machine-learning-client
```

Run `pytest` and view the coverage report:

```shell
pipenv run coverage run -m pytest
```

```shell
pipenv run coverage report
```

To view a detailed HTML report showing lines covered and missed:

```shell
pipenv run coverage html
```

### Test Coverage Report (as of 12/02/2023, reported by Github Action)
- Machine-Learning-Client Coverage:

    ```shell
    Name                   Stmts   Miss  Cover
    ------------------------------------------
    app.py                    54      8    85%
    ml_client.py              18      0   100%
    tests\__init__.py          0      0   100%
    tests\test_ml_app.py      50      0   100%
    ------------------------------------------
    TOTAL                    122      8    93%
    ```

- Web-App Coverage:

    ```shell
    Name                    Stmts   Miss  Cover
    -------------------------------------------
    app.py                     89     10    89%
    tests\__init__.py           0      0   100%
    tests\test_web_app.py      86      0   100%
    -------------------------------------------
    TOTAL                     175     10    94%
    ```

## Conclusion
Thanks for trying out our application. If you have any questions or feedback, feel free to reach out to us via [GitHub Discussions](https://docs.github.com/en/discussions) for our repository. We appreciate your interest and support!
