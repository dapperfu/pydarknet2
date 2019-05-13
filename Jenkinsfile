pipeline {
  agent any
  stages {
    stage('Setup') {
    environment {
      FOO = 'BAR'
    }
    stage('Submodules') {
        steps {
          sh 'git submodule update --init; git submodule foreach "git submodule update --init"'
          sh 'make clean'
        }
      }
    }
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
