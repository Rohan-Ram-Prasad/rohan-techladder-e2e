pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run E2E Automation') {
            steps {
                bat 'pytest tests -v -s'
            }
        }

    }
}