// Filename: Jenkinsfile.app
pipeline {
    agent any
    environment {
        // CI SETTINGS
        DOCKER_IMAGE = 'ravindukuruppuarachchi/inventory_project_api'
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') { steps { checkout scm } }

        stage('Unit Tests') {
            steps {
                echo "Running tests..."
                // sh 'pip install pytest && pytest' // Uncomment when ready
            }
        }
        
        stage('Build & Push Docker') {
            steps {
                script {
                    echo "Building Artifact: ${DOCKER_TAG}"
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        
                        // We also push 'latest' so developers can pull it easily
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
    }
    post {
        success {
            echo "SUCCESS: Image ${DOCKER_IMAGE}:${DOCKER_TAG} is ready for deployment."
        }
    }
}