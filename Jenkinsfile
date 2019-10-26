pipeline {

  	environment {
    		flask_app = "zgchuck/flask_app"
    		flask_mysql = "zgchuck/flask_mysql"
    		registryCredential = 'dockerhub'
		ssh_creds = credentials('osboxes')
		flask_mysql_root_pass = credentials('flask_mysql_root_password')
  	}

  	agent any

	parameters {
		booleanParam(name: 'BUILD_DOCKER_IMAGES', defaultValue: true, description: '')
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
	    		when {
		    		expression{
			    		return params.BUILD_DOCKER_IMAGES
		    		}
	    		}
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
			steps {

				sh '''
					if test ! -d './secrets'; then
						mkdir ./secrets;
					fi
				'''

				sh '''
					if test ! -f './secrets/mysql_root_pass.txt'; then
						echo 'MySQL password file does not exist, building...'
  						withCredentials([usernameColonPassword(credentialsId: 'flask_mysql_root_password', variable: 'mysql_root_pass')]) {
							echo $mysql_root_pass > ./secrets/mysql_root_pass2.txt
						}
					fi
				'''
			}
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
