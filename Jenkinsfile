pipeline {
    agent any

    environment {
        // --- CONFIGURATION ---
        // Replace with your actual Docker Hub username and image name
        DOCKER_IMAGE = 'ravindukuruppuarachchi/inventory_project_api'
        DOCKER_TAG   = "${BUILD_NUMBER}" // Creates tags like v1, v2, v3 based on run number
        NAMESPACE    = 'inventory-ns'
        RELEASE_NAME = 'app-release'
    }

    stages {
        stage('Checkout') {
            steps {
                // Get code from the Git repo configured in the job
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Unit Tests...'
                // If you have python tests, uncomment the next line:
                // sh 'python3 -m pytest tests/'
                sh 'echo "Tests passed (Simulation)"'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // Build command using the Dockerfile in current folder (.)
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Also tag as 'latest' for convenience
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing to Registry...'
                    // Login using the credentials ID we created in Phase 1
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to K8s (Helm)') {
            steps {
                script {
                    echo 'Deploying Application Layer...'
                    // We use the Secret File credential to give Helm access to K8s
                    withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                        
                        // 1. Upgrade the App Release
                        // We use --set to dynamically inject the NEW image tag we just built
                        sh """
                            helm upgrade --install ${RELEASE_NAME} ./helm/inventory-app \
                            -f ./helm/inventory-app/values-app.yaml \
                            --set image.tag=${DOCKER_TAG} \
                            --namespace ${NAMESPACE} \
                            --create-namespace
                        """
                        
                        // 2. Verify rollout status
                        sh "kubectl rollout status deployment/inventory-app -n ${NAMESPACE}"
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup Docker images to save disk space
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}:latest || true"
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check logs.'
        }
    }
}