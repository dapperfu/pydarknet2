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
  }
}
