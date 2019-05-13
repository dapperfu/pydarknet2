pipeline {
  agent any
  stages {
    stage('Clean') {
      steps {
        script {
          properties([pipelineTriggers([pollSCM('H/5 * * * *')])])
        }

        sh 'make clean'
      }
    }
    stage('Git') {
      steps {
        sh 'git submodule update --init'
      }
    }
    stage('Python Environment') {
      steps {
        sh 'make env.python'
      }
    }
    stage('Python') {
      parallel {
        stage('version') {
          steps {
            sh 'bin/python --version'
          }
        }
        stage('build') {
          steps {
            sh 'bin/python setup.py build'
            sh 'bin/python setup.py install'
          }
        }
      }
    }
  }
}