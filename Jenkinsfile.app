// Filename: Jenkinsfile.app
pipeline {
    agent any
    environment {
        // Update with your actual Docker Hub username
        DOCKER_IMAGE = 'ravindukuruppuarachchi/inventory_project_api'
        DOCKER_TAG   = "${BUILD_NUMBER}"
        NAMESPACE    = 'inventory-ns'
        RELEASE_NAME = 'app-release'
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        
        stage('Build & Push Docker') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    }
                }
            }
        }

        stage('Deploy App') {
            steps {
                script {
                    // 1. Wrap the command in 'withCredentials' to get the secret
                    withCredentials([string(credentialsId: 'app-admin-password', variable: 'ADMIN_PASS'),
                                    file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                        
                        // 2. Add the --set flag to inject the password dynamically
                        sh """
                            helm upgrade --install ${RELEASE_NAME} ./helm/inventory-app \
                            -f ./helm/inventory-app/values-app.yaml \
                            --set image.tag=${DOCKER_TAG} \
                            --set secrets.adminPassword=${ADMIN_PASS} \
                            --namespace ${NAMESPACE} \
                            --create-namespace
                        """
                        
                        sh "kubectl rollout status deployment/inventory-app -n ${NAMESPACE}"
                    }
                }
            }
        }
    }
}