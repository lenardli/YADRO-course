pipeline {
    agent any

    triggers {
        gitlab(triggerOnPush: true, triggerOnMergeRequest: false)
    }
    
    // 2. Добавляем опции для получения информации о push
    options {
        gitLabConnection('YADRO MULTI') // имя подключения из настроек Jenkins
    }
    
    stages {
        stage('Hello') {
            steps {
                conditionalStage('Ana')
            }
        }
    }
    
}