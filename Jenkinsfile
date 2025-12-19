pipeline {
    agent any

    environment {
        BMC_URL = 'https://localhost:2443'
        BMC_USER = 'root'
        BMC_PASS = '0penBmc'
    }

    stages {
        stage('Start OpenBMC') {
            steps {
                script {
                    sh 'docker rm -f openbmc || true'
                    sh 'docker build -t openbmc-qemu .'
                    sh 'docker run -d --name openbmc -p 2222:22 -p 2443:443 openbmc-qemu'
                    sh 'sleep 45'
                }
            }
        }

        stage('Install Python') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run WebUI Tests (Selenium)') {
            steps {
                sh 'python3 openbmc_auth_tests.py'
            }
        }

        stage('Run API Tests') {
            steps {
                sh 'python3 -m pytest test_redfish.py -v --tb=short'
            }
        }

        stage('Run Load Tests (Locust)') {
            steps {
                script {
                    sh 'locust -f locustfile.py --headless -u 3 -r 1 -t 30s &'
                    sleep(35)
                }
            }
        }
    }

    post {
        always {
            sh 'docker stop openbmc || true'
            sh 'docker rm openbmc || true'
        }
    }
}
