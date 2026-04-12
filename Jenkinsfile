node {
    def conditions = conditionalStage()
    
    def shouldRunCheckout = conditions.isCheckout
    def shouldRunLint = conditions.isLint
    def shouldRunSAST = conditions.isSAST
    def shouldRunBuild = conditions.isBuild
    def shouldRunPush = conditions.isPush
    def shouldRunDeployStaging = conditions.isDeployStaging
    def shouldRunSmokeTest = conditions.isSmokeTest
    def shouldRunDeployProduction = conditions.isDeployProduction
    
    if (shouldRunCheckout) {
        stage('Checkout') {
            echo 'Checkout stage'
        }
    }
    
    if (shouldRunLint) {
        stage('Lint') {
            echo 'Lint stage'
        }
    }
    
    if (shouldRunSAST) {
        stage('SAST') {
            echo 'SAST stage'
        }
    }
    
    if (shouldRunBuild) {
        stage('Build') {
            echo 'Build stage'
        }
    }
    
    if (shouldRunPush) {
        stage('Push') {
            echo 'Push stage'
        }
    }
    
    if (shouldRunDeployStaging) {
        stage('Deploy Staging') {
            echo 'Deploy stage to Staging'
        }
    }
    
    if (shouldRunSmokeTest) {
        stage('Smoke Test') {
            echo 'Smoke Test stage'
        }
    }
    
    if (shouldRunDeployProduction) {
        stage('Deploy Production') {
            echo 'Deploy stage to Production'
        }
    }
}