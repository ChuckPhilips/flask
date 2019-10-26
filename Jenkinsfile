pipeline {

  	environment {
    		flask_app = "zgchuck/flask_app"
    		flask_mysql = "zgchuck/flask_mysql"
    		registryCredential = 'dockerhub'
		ssh_creds = credentials('osboxes')
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

            	stage('Generating secrets') {
                	steps {

                        	sh '''
                            		if [ ! -d ./secrets ]
                            		then
                                		mkdir ./secrets
                            		fi
                        	'''
                    
                
                    		withCredentials([string(credentialsId: 'flask_mysql_root_password', variable: 'mysql_root_password')]) {
                    	    		sh 'echo $mysql_root_password > ./secrets/mysql_root_pass.txt'
                    		}
                    	
                    		withCredentials([string(credentialsId: 'flask_db_user', variable: 'db_user')]) {
                    	    		sh 'echo $db_user > ./secrets/db_user.txt'
                    		}
                    	
                    		withCredentials([string(credentialsId: 'flask_db_password', variable: 'db_pass')]) {
                    	    		sh 'echo $db_pass > ./secrets/db_pass.txt'
                    		}
                    	
                    		withCredentials([string(credentialsId: 'flask_db_name', variable: 'db_name')]) {
                    	    		sh 'echo $db_name > ./secrets/db_name.txt'
                    		}
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
