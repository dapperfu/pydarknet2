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
    stage('') {
      steps {
        ws(dir: 'MahWorkspace') {
          sh 'pwd'
        }

      }
    }
  }
}