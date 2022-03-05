pipeline {
	agent {
	  kubernetes {
		label 'pdme'  // all your pods will be named with this prefix, followed by a unique id
		idleMinutes 5  // how long the pod will live after no jobs have run on it
		yamlFile 'jenkins/ci-agent-pod.yaml'  // path to the pod definition relative to the root of our project
		defaultContainer 'poetry'  // define a default container if more than a few stages use it, will default to jnlp container
	  }
	}

	options {
		parallelsAlwaysFailFast()
	}

	stages {
		stage('Build') {
			steps {
				echo 'Building...'
				sh 'python --version'
				sh 'poetry --version'
				sh 'poetry install'
			}
		}
		stage('Test') {
			parallel{
				stage('pytest') {
					steps {
						sh 'poetry run pytest'
					}
				}
				stage('lint') {
					steps {
						sh 'poetry run flake8 pdme tests'
					}
				}
				stage('mypy') {
					steps {
						sh 'poetry run mypy pdme'
					}
				}
			}
		}

		stage('Deploy') {
			environment {
				PYPI=credentials("pypi-pdme")
			}

			when {
				buildingTag()
			}
			steps {
				echo 'Deploying...'
				sh '/poetry publish -u ${PYPI_USR} -p ${PYPI_PSW} --build'
			}
		}

	}
	post {
		always {
			echo 'This will always run'
			junit 'pytest.xml'
			cobertura coberturaReportFile: 'coverage.xml'
			mail (bcc: '',
				body: "Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> Build URL: ${env.BUILD_URL}", cc: '', charset: 'UTF-8', from: 'jenkins@jenkins.deepak.science', mimeType: 'text/html', replyTo: 'dmallubhotla+jenkins@gmail.com', subject: "${env.JOB_NAME} #${env.BUILD_NUMBER}: Build ${currentBuild.currentResult}", to: "dmallubhotla+ci@gmail.com")
		}
		success {
			echo 'This will run only if successful'
		}
		failure {
			echo 'This will run only if failed'
		}
		unstable {
			echo 'This will run only if the run was marked as unstable'
		}
		changed {
			echo 'This will run only if the state of the Pipeline has changed'
			echo 'For example, if the Pipeline was previously failing but is now successful'
		}
	}
}
