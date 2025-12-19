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

    post {
        always {
            sh 'docker stop openbmc || true'
            sh 'docker rm openbmc || true'
        }
    }
}
