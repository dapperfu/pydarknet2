pipeline {
  agent any
  stages {
    stage('Setup') {
      environment {
        FOO = 'BAR'
      }
      parallel {
        stage('Submodules') {
          steps {
            sh 'git submodule update --init; git submodule foreach "git submodule update --init"'
            sh 'make clean'
          }
        }
        stage('Bootstrap Python') {
          steps {
            sh 'make env.python'
          }
        }
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