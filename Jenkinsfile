pipeline {
    agent any // Or a specific agent like 'agent { label 'your-linux-agent' }'

    environment {
        // Define environment variables if needed, e.g., for browser choice
        BROWSER = 'chrome' // Or 'firefox', etc.
        // For headless Chrome/Firefox, set relevant display variables
        // DISPLAY = ':99' // For Xvfb or similar if running on Linux with no GUI
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your Git repository
                git url: 'https://github.com/goodtogo01/End2End_Python.git',
                    branch: 'main' // Or 'master', or use 'credentialsId: 'your-credential-id'' for private repos
            }
        }

       // ... (previous Jenkinsfile code) ...

        stage('Setup Python Environment & Install Dependencies') {
            steps {
                script {
                    echo 'Setting up Python virtual environment and installing dependencies...'

                    // --- Recommended order for venv and pip/webdriver-manager ---
                    // 1. Create venv
                    sh 'python3 -m venv venv'
                    // 2. Activate venv
                    sh '. venv/bin/activate && \\' // Use '\' for line continuation in Groovy sh block
                       'pip install --upgrade pip && \\' // Upgrade pip inside venv
                       'pip install --upgrade webdriver-manager' // Upgrade webdriver-manager inside venv
                    // 3. Clear the webdriver_manager cache on the agent
                    //    The cache is usually in the user's home directory, not necessarily in the venv
                    //    So, `rm -rf ~/.wdm` should be outside the activated venv context if that's where the cache is.
                    //    However, `webdriver_manager` typically stores cache relative to the user running the script.
                    //    If Jenkins is running as a specific user, that user's home dir needs cleaning.
                    sh 'rm -rf ~/.wdm'
                    echo 'webdriver_manager cleaned and upgraded.'
                    // --- End recommended order ---

                    // Install project-specific dependencies
                    sh '. venv/bin/activate && pip install --no-cache-dir -r requirements.txt'
                    echo 'Python environment setup complete.'

                    // (Optional: Xvfb setup if needed for headless Browse on Linux)
                    // sh 'Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99'
                }
            }
        }



        stage('Run Tests') {
            steps {
                script {
                    // Activate virtual environment and run pytest
                    // --html and --self-contained-html are for generating a single HTML report
                    // --junitxml is for JUnit style reports, useful for Jenkins test result trend graphs
                    // '|| true' is used to ensure the pipeline doesn't fail immediately on test failures,
                    // allowing the HTML report to be published. Jenkins will still mark the build as unstable/failed.
                    sh '. venv/bin/activate && pytest tests/ --html=report.html --self-contained-html --junitxml=results.xml || true'
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                // Publish HTML report
                publishHTML (
                    target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: '.', // The directory where report.html is located
                        reportFiles: 'report.html',
                        reportName: 'Pytest HTML Report'
                    ]
                )
                // Publish JUnit XML results for Jenkins' built-in test result trends
                junit 'results.xml'
            }
        }

        stage('Cleanup') {
            steps {
                // Clean up virtual environment if needed (optional)
                sh 'rm -rf venv'
                // If you started Xvfb, kill it here
                // sh 'killall Xvfb'
            }
        }
    }

    // Post-build actions (e.g., notifications)
    post {
        always {
            cleanWs() // Clean up the workspace after the build
        }
        success {
            echo 'Build Successful!'
            // You can add notifications here, e.g., Slack
        }
        failure {
            echo 'Build Failed!'
        }
        unstable {
            echo 'Build Unstable (tests failed)!'
        }
    }
}