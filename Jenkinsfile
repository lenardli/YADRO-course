pipeline {
    agent any

    options {
        gitLabConnection('YADRO MULTI')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checkout stage'
                script {
                    // Получаем карту условий один раз
                    def conditions = conditionalStage()
                    
                    if (conditions.isMain) {
                        echo "a.sheynova/hw5 is success"
                    }
                    
                    // Сохраняем условия для использования в других stage
                    env.SHOULD_PUSH = conditions.shouldPush.toString()
                    env.SHOULD_STAGING = conditions.shouldStaging.toString()
                    env.SHOULD_PRODUCTION = conditions.shouldProduction.toString()
                }
            }
        }
        
        stage('Lint') {
            steps { 
                echo 'Lint stage' 
            }
        }
        
        stage('SAST') {
            steps { 
                echo 'SAST stage' 
            }
        }
        
        stage('Build') {
            steps { 
                echo 'Build stage' 
            }
        }
        
        stage('Push') {
            when {
                expression { env.SHOULD_PUSH == 'true' }
            }
            steps { 
                echo 'Push stage' 
            }
        }
        
        stage('Deploy') {
            when {
                expression { env.SHOULD_STAGING == 'true' }
            }
            steps { 
                echo 'Deploy stage to Staging' 
            }
        }
        
        stage('Smoke Test') {
            when {
                expression { env.SHOULD_PRODUCTION == 'true' }
            }
            steps { 
                echo 'Smoke Test stage for Production' 
            }
        }
    }
}