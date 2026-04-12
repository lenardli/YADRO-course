pipeline {
    agent any

    options {
        gitLabConnection('YADRO')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Quality Checks') {
            parallel {
                stage('Lint') {
                    agent {
                        docker {
                            image 'python:3.13-slim-trixie@sha256:739e7213785e88c0f702dcdc12c0973afcbd606dbf021a589cab77d6b00b579d'
                            args "-e HOME=${env.WORKSPACE} -e PATH=/var/lib/jenkins/workspace/YADRO@2/.local/bin:$PATH"
                            reuseNode true
                        }
                    }
                    steps {
                        gitlabCommitStatus(name: 'lint') {
                            echo "Linting code"
                            sh '''
                                pip install flake8==7.3.0
                                flake8 . --exclude=venv,.env,__pycache__,.local --max-line-length=90
                            '''
                        }
                    }
                }
                stage('SAST') {
                    agent {
                        docker {
                            image 'python:3.13-slim-trixie@sha256:739e7213785e88c0f702dcdc12c0973afcbd606dbf021a589cab77d6b00b579d'
                            args "-e HOME=${env.WORKSPACE} -e PATH=/var/lib/jenkins/workspace/YADRO@2/.local/bin:$PATH"
                            reuseNode true
                        }
                    }
                    steps {
                        gitlabCommitStatus(name: 'SAST') {
                            echo "Running security checks..."
                            sh '''
                                pip install -r requirements-test.txt
                                bandit -r . -f html -o bandit-report.html

                            '''
                            archiveArtifacts artifacts: 'bandit-report.html'
                        }
                    }
                }
            }
            failFast true
        }

        stage('Build') {
            steps {
                gitlabCommitStatus(name: 'build') {
                    echo 'Building and pushing Docker image to Docker Hub'
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_PASS'
                    )]) {
                        sh """
                            echo \$DOCKERHUB_PASS | docker login -u \$DOCKERHUB_USER --password-stdin
                            docker build -t ${env.DOCKER_NAMESPACE}/${env.DOCKER_REPO}:${env.BUILD_NUMBER} .
                            docker push ${env.DOCKER_NAMESPACE}/${env.DOCKER_REPO}:${env.BUILD_NUMBER}
                        """
                    }
                }
            }
            post {
                always {
                    sh "docker logout"
                }
            }   
        }

        stage('Deploy') {
            when {
                allOf {
                    expression { env.GIT_BRANCH == 'origin/a.sheynova/main' }
                    expression { currentBuild.buildCauses.toString().contains('UserIdCause') }
                }
            }
            steps {
                gitlabCommitStatus(name: 'deploy') {
                    echo "Deploy to host ${params.DEPLOY_USER}@${params.DEPLOY_HOST}"
                    withCredentials([sshUserPrivateKey(
                            credentialsId: 'deploy-ssh',
                            keyFileVariable: 'SSH_KEY'
                        )]) {
                        sh """
                            chmod 600 "\$SSH_KEY" 2>/dev/null || true
                            ssh -i "\$SSH_KEY" -o StrictHostKeyChecking=accept-new -o IdentitiesOnly=yes -o BatchMode=yes ${params.DEPLOY_USER}@${params.DEPLOY_HOST} 'docker pull ${env.DOCKER_NAMESPACE}/${env.DOCKER_REPO}:${env.BUILD_NUMBER} && (docker stop yadro-app || true) && (docker rm yadro-app || true) && docker run -d --name yadro-app -p 8000:8000 --restart unless-stopped ${env.DOCKER_NAMESPACE}/${env.DOCKER_REPO}:${env.BUILD_NUMBER}'
                        """
                    }
                }
            }
            post {
                failure {
                    updateGitlabCommitStatus name: 'deploy', state: 'failed'
                }
                aborted {
                    updateGitlabCommitStatus name: 'deploy', state: 'canceled'
                }
            }
        }
    }
    post {
        always {
            script {
                def state = [
                    'SUCCESS' : 'success',
                    'FAILURE' : 'failed',
                    'ABORTED' : 'canceled'
                ][currentBuild.currentResult] ?: 'failed'
                updateGitlabCommitStatus name: 'pipeline', state: state
            }
        }
        failure {
            echo "Pipeline failed!"
        }
        success {
            echo "Pipeline succeeded!"
        }
        aborted {
            echo "Pipeline was aborted!"
        }
    }
}