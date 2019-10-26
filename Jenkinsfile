pipeline {

  	environment {
    		flask_app = "zgchuck/flask_app"
    		flask_mysql = "zgchuck/flask_mysql"
    		registryCredential = 'dockerhub'
		ssh_creds = credentials('osboxes')
  	}

  	agent any

	parameters {
		booleanParam(name: 'PUSH_DOCKER_IMAGES', defaultValue: true, description: '')
		booleanParam(name: 'DELETE_DOCKER_IMAGES', defaultValue: true, description: '')
		booleanParam(name: 'UPDATE_KUBERNETES_DEPLOYMENT', defaultValue: false, description: '')
	}

  	stages {
   		stage('Cloning Git') {
      			steps {
        			git 'https://github.com/ChuckPhilips/flask'
      			}
    		}

    		stage('Building image') {
      			steps {
        			script {
          				dockerFlaskbuild = docker.build(flask_app + ":$BUILD_NUMBER", "./app")
          				dockerFlask = docker.build(flask_app + ":latest", "./app")
          				dockerMysqlbuild = docker.build(flask_mysql + ":$BUILD_NUMBER", "./mysql")
          				dockerMysql = docker.build(flask_mysql + ":latest", "./mysql")
        			}
      			}
    		}

		stage('Create secrets') {
			sh 'echo "Checking if secrets files exist."'
		}
	
    		stage('Deploy Image') {
	    		when {
		    		expression{
			    		return params.PUSH_DOCKER_IMAGES
		    		}
	    		}
      			steps {
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
	    		when {
		    		expression{
			    		return params.DELETE_DOCKER_IMAGES
		    		}
	    		}
      			steps{
        			sh "docker rmi $flask_app:$BUILD_NUMBER"
        			sh "docker rmi $flask_app:latest"
        			sh "docker rmi $flask_mysql:$BUILD_NUMBER"
        			sh "docker rmi $flask_mysql:latest"
      			}
    		}

    		stage('Updated kubernetes deployment') {
	    		when {
		    		expression{
			    		return params.UPDATE_KUBERNETES_DEPLOYMENT
		    		}
	    		}
    			steps {
				sh "ssh -i $ssh_creds $ssh_creds_usr@kubemaster 'kubectl set image deployment/flask-app-deployment flask-app=zgchuck/flask_app:$BUILD_NUMBER'"
			}
    		}
  	}
}
