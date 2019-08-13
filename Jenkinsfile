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
          dockerFlaskbuild = docker.build flask_app + ":$BUILD_NUMBER"
          dockerFlask = docker.build flask_app + ":latest"
          dockerMysqlbuild = docker.build(flask_mysql + ":$BUILD_NUMBER", "./mysql")
          dockerMysql = docker.build(flask_mysql + ":latest", "./mysql")
        }
      }
    }
    stage('Deploy Image') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerFlask.push()
            dockerFlaskbuild.push()
            dockerMysql.push()
            dockerMysqlbuild.push()
          }
        }
      }
    }
    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $flask_app:$BUILD_NUMBER"
        sh "docker rmi $flask_app:latest"
        sh "docker rmi $flask_mysql:$BUILD_NUMBER"
        sh "docker rmi $flask_mysql:latest"
      }
    }
    stage('Updated kubernetes deployment'){
    	steps{
		sh "ssh osboxes@kubemaster 'kubectl get all'"
	}
    }
  }
}
