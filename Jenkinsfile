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
            sh 'make env.python'
          }
        }
        stage('Bootstrap Python') {
          steps {
            sh 'make env.python'
          }
        }
      }
    }
  }
}