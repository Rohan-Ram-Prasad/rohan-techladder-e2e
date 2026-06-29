\# Techladder E2E Automation Framework



End-to-end automation framework for validating Techladder Voice AI call workflows.



\## Features



\- Authentication validation

\- Agent discovery

\- Batch creation

\- Batch polling

\- Call result verification

\- Fake call validation

\- Jenkins integration

\- GitHub integration



\## Project Structure



```

lib/

tests/

Jenkinsfile

requirements.txt

pytest.ini

```



\## Installation



```bash

pip install -r requirements.txt

```



\## Run Tests



```bash

pytest tests -v -s

```



\## Jenkins



Configured to run automatically through Jenkins pipelines.



\## Validation



Current validation checks:



\- Batch Status = completed

\- Call Status = failed

\- Completed At present

\- Duration = 0



\## Repository



https://github.com/Rohan-Ram-Prasad/rohan-techladder-e2e

