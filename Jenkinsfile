node {
    Boolean isTag = env.TAG_NAME != null
    Boolean isMR = env.CHANGE_ID != null
    Boolean isMain = env.BRANCH_NAME == 'main'

    Boolean shouldBuild = isMain || isMR || isTag
    Boolean shouldPush = isMain || isTag
    Boolean shouldStaging = isMain
    Boolean shouldProduction = isTag

    def imageTag
    def imageName

    try {
        stage('Checkout') {
            checkout scm
            imageTag = env.TAG_NAME ?: sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
            imageName = "dans-fake-app:${imageTag}"
            sleep 2
        }

        stage('Checks') {
            parallel(
                lint: {
                    echo "Running linter... [STUB]"
                    sleep 3
                },
                sast: {
                    echo "Running bandit/gosec... [STUB]"
                    sleep 4
                    archiveArtifacts artifacts: 'sast-report.json', allowEmptyArchive: true
                }
            )
        }
        stage(name: 'Build') {
            echo "Building ${imageName}... [STUB]"
            sleep 4
        }

        stage(name: 'Push') {
            echo "Pushing ${imageName} to registry... [STUB]"
            sleep 3
        }

        stage(name: 'Deploy staging') {
            build job: 'YADRO', parameters: [
                string(name: 'IMAGE_TAG', value: imageTag),
                string(name: 'ENVIRONMENT', value: 'staging')
            ]
        }

        stage(name: 'Deploy production') {
            build job: 'YADRO', parameters: [
                string(name: 'IMAGE_TAG', value: imageTag),
                string(name: 'ENVIRONMENT', value: 'production')
            ]
        }


        // conditionalStage(name: 'Build', condition: shouldBuild) {
        //     echo "Building ${imageName}... [STUB]"
        //     sleep 4
        // }

        // conditionalStage(name: 'Push', condition: shouldPush) {
        //     echo "Pushing ${imageName} to registry... [STUB]"
        //     sleep 3
        // }

        // conditionalStage(name: 'Deploy staging', condition: shouldStaging) {
        //     build job: 'deploy-fake-app', parameters: [
        //         string(name: 'IMAGE_TAG', value: imageTag),
        //         string(name: 'ENVIRONMENT', value: 'staging')
        //     ]
        // }

        // conditionalStage(name: 'Deploy production', condition: shouldProduction) {
        //     build job: 'deploy-fake-app', parameters: [
        //         string(name: 'IMAGE_TAG', value: imageTag),
        //         string(name: 'ENVIRONMENT', value: 'production')
        //     ]
        // }

    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        throw e

    } finally {
        echo "Cleanup... [STUB]"
        sleep 2
    }
}