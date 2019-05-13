pipeline {
  agent any
  stages {
    stage('Bootstrap') {
      steps {
        sh 'git submodule update --init; git submodule foreach "git submodule update --init"'
      }
    }
  }
}