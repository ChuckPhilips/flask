pipeline {
  environment {
    flask_app = "zgchuck/flask_app"
    flask_mysql = "zgchuck/flask_mysql"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git 'https://github.com/ChuckPhilips/flask'
      }
    }
    stage('Building image') {
      steps{
        script {
          dockerFlask = docker.build flask_app + ":$BUILD_NUMBER"
           dockerMysql = docker.build(flask_mysql + ":$BUILD_NUMBER", "./mysql")
        }
      }
    }
    stage('Deploy Image') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerFlask.push()
            dockerMysql.push()
          }
        }
      }
    }
    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $flask_app:$BUILD_NUMBER"
        sh "docker rmi $flask_mysql:$BUILD_NUMBER"
      }
    }
  }
}
