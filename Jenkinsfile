pipeline {
  agent any
  stages {
    stage('Clean') {
      steps {
        script {
            properties([pipelineTriggers([pollSCM('')])])
        }
        sh 'make clean'
      }
    }
  }
}
