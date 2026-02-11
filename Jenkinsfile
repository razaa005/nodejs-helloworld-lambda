pipeline {
  agent any

  environment {
    COMPONENT_NAME = "NodeJS-HelloWord-ahmadraza"
    PROJECT_PATH   = "developer"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build and Release to Cosmos') {
      steps {
        withCredentials([
          file(credentialsId: 'certee-client-crt', variable: 'CERT'),
          file(credentialsId: 'certee-client-key', variable: 'KEY')
        ]) {
          sh '''
            set -e
            echo "Using CERT=$CERT"
            echo "Using KEY=$KEY"
            make in_container/build_and_release
          '''
        }
      }
    }
  }
}
