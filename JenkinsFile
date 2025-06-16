pipeline {
    agent any

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ --html=report.html --self-contained-html
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Pytest Report',
                    keepAll: true
                ])
            }
        }
    }
}