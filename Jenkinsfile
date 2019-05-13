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
        stage('Darknet') {
          steps {
            sh 'bin/python setup.py build'
            sh 'bin/python setup.py develop'
          }
        }
      }
    }
    stage('Darknet') {
      steps {
        sh 'export DARKNET_ROOT=`pwd`/darknet;rm -rf ${DARKNET_ROOT};bin/darknet.py darknet clone;bin/darknet.py darknet build'
      }
    }
    stage('Darknet Build') {
      steps {
        sh 'export DARKNET_ROOT=`pwd`/darknet;rm -rf ${DARKNET_ROOT};bin/darknet.py darknet build --force'
      }
    }
  }
}