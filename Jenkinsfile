pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'make env'
      }
    }
    stage('Build') {
      steps {
        sh './bin/python setup.py build'
        sh './bin/python setup.py install'
      }
    }
  }
  environment {
    DARKNET_FORCE = '1'
  }
}
