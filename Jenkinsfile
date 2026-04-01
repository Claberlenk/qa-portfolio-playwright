pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.50.0-jammy'
            args '--ipc=host'
        }
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('API Tests') {
            steps {
                sh 'pytest tests/api -m api -v --tb=short --junitxml=reports/api-results.xml'
            }
            post {
                always {
                    junit 'reports/api-results.xml'
                }
            }
        }

        stage('UI Tests') {
            steps {
                sh '''
                    pytest tests/ui -m ui -v --tb=short \
                        --junitxml=reports/ui-results.xml \
                        --browser chromium
                '''
            }
            post {
                always {
                    junit 'reports/ui-results.xml'
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'playwright-report',
                        reportFiles: 'index.html',
                        reportName: 'Playwright Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            cleanWs()
        }
        failure {
            echo 'Pipeline failed — check test reports above.'
        }
    }
}
