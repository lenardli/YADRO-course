pipeline {
    agent any

    options {
        gitLabConnection('YADRO MULTI')
    }

    stage('Checkout') {
        steps { echo 'Checkout stage' }
        if (conditionalStage.isMain()) {
            echo "a.sheynova/hw5 is success"
        }
    }
    stage('Lint') {
        steps { echo 'Lint stage' }
    }
    stage('SAST') {
        steps { echo 'SAST stage' }
    }
    stage('Build') {
        steps { echo 'Build stage' }
    }
    stage('Push') {
        steps { echo 'Push stage' }
    }
    stage('Deploy') {
        steps { echo 'Deploy stage' }
    }
    stage('Smoke Test') {
        steps { echo 'Smoke Test stage' }
    }
}