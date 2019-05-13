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
    stage('Python Run') {
      steps {
        sh 'bin/python --version'
      }
    }
  }
}