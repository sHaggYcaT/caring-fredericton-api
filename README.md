# Civic Tech - Caring Calendar API #

This project contains the back end APIs used by the Caring Calendar application.  The endpoints are
agnostic to the client interface being used (React, Angular, iOS, Android).

## Functionality: ##

* Organization Management (Registration, Verification, Updates)
* Scheduling Events

## Project Setup ##

NPM is used to install the serverless tools whereas pip is used to install runtime Python packages.

### NPM Dependencies ###

Ensure the prerequisites are installed
```
- OPTIONAL: Node Virtual Manager (nvm)
- Node 8.12.x (for working with serverless)
```

Install the NPM dependencies
```
npm install
```

### Python Dependencies ###

Ensure the prerequisites are installed
```
- Python3.7
- pip (tool for installing Python packages)
```

Create virtual env for python3.7 inside project directory:
```
python3.7 -m venv venv 
```

Activate newly created environment
```
. venv/bin/activate
```

Install the required python packages
```
pip install -r requirements.txt
```

Create a test user account
```
cd scripts
./user_sign_up.py <username> <password> -p <profile name> - s <stage_name>
```

OPTIONAL: Exit the virtual environment using the following command
```
deactivate
```

## Serverless Deployment ##

The application can be deployed by issuing the following commands:
```
export AWS_PROFILE=test
export AWS_REGION=ca-central-1
npm run deploy -- --stage <stage name>
```

** NOTES: **

* Replace **test** with your assume role profile name
* Please include your name to stage name if you want to create custom AWS stack for testing purposes.  For example:
> ```
> npm run deploy -- --stage hpowell
> ```

## Running project locally ##

The project can be run locally using the following command:
```
export AWS_PROFILE=test
export AWS_REGION=ca-central-1
npm run local -- --stage <stage name>
```

**NOTES**:

* This command must be run inside an activated virtual environment
* Any environment (stage name) can be used, optionally you may want to use `config/local.yaml` configuration file
* When running locally timeout, access, and file size restrictions do not behave the same as within an AWS service
