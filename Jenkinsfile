properties([
    pipelineTriggers([
        gitlab(triggerOnPush: true)
    ]),
    parameters([
        choice(name: 'NODE', 
               choices: ['master', 'worker-1', 'worker-2'], 
               description: 'Available nodes')
    ])
])

node(params.NODE) {
    Boolean IsTag = env.TAG_NAME != null
    Boolean IsMR = env.CHANGE_ID != null
    Boolean IsMain = env.BRANCH_NAME == 'a.sheynova/main'

    Boolean shouldBuild = IsMain || IsMR || IsTag
    Boolean shouldPush = IsMain || IsTag
    Boolean shouldStaging = IsMain
    Boolean shouldProduction = IsTag

    def imageTag
    def imageName
    def commit
    def version
    def timestamp 

    try {
        stage('Checkout') {
            checkout scm
            commit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
            version = readFile('VERSION').trim()
            timestamp = sh(script: "date +'%Y%m%d%H%M%S'", returnStdout: true).trim()
            imageTag = env.TAG_NAME ?: "v${version}-${commit}-${timestamp}"
            imageName = "${env.DOCKER_NAMESPACE}/${env.DOCKER_REPO}:${imageTag}"
        }

        stage('Checks') {
            parallel(
                lint: {
                    echo "Linting code"
                    def dockerImage = docker.image('python:3.13-slim-trixie@sha256:739e7213785e88c0f702dcdc12c0973afcbd606dbf021a589cab77d6b00b579d')
                    dockerImage.inside(
                    "-e HOME=${env.WORKSPACE} -e PATH=${env.WORKSPACE}/.local/bin:$PATH"
                    ) {
                    sh '''
                        pip install flake8==7.3.0
                        flake8 . --exclude=venv,.env,__pycache__,.local,.ansible --max-line-length=90
                    '''
                    }
                },
                sast: {
                    echo "SAST checking"
                    def dockerImage = docker.image('python:3.13-slim-trixie@sha256:739e7213785e88c0f702dcdc12c0973afcbd606dbf021a589cab77d6b00b579d')
                    dockerImage.inside(
                    "-e HOME=${env.WORKSPACE} -e PATH=${env.WORKSPACE}/.local/bin:$PATH"
                    ) {
                    sh '''
                        pip install bandit==1.9.4
                        bandit -r .  --severity-level=high --exclude=./.local -f json -o sast-report.json
                    '''
                    archiveArtifacts artifacts: 'sast-report.json', allowEmptyArchive: true
                    }
                }
            )
        }

        conditionalStage(name: 'Build', condition: shouldBuild) {
            echo "Building ${imageName}"
            sh """
                docker build -t ${imageName} .
            """
        }

        conditionalStage(name: 'Push', condition: shouldPush) {
            echo "Pushing ${imageName} to Docker Hub"
            withCredentials([usernamePassword(
                credentialsId: 'docker-hub',
                usernameVariable: 'DOCKERHUB_USER',
                passwordVariable: 'DOCKERHUB_PASS'
            )]) {
                sh """
                    echo \$DOCKERHUB_PASS | docker login -u \$DOCKERHUB_USER --password-stdin
                    docker push ${imageName}
                """
                }
            }

        conditionalStage(name: 'Deploy staging', condition: shouldStaging) {
            build job: 'YADRO', parameters: [
                string(name: 'IMAGE_TAG', value: imageTag),
                string(name: 'ENVIRONMENT', value: 'staging')
            ]
        }

        conditionalStage(name: 'Deploy production', condition: shouldProduction) {
            build job: 'YADRO', parameters: [
                string(name: 'IMAGE_TAG', value: imageTag),
                string(name: 'ENVIRONMENT', value: 'production')
            ]
        }

    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        throw e

    } finally {
        sh "docker logout"
    }
}