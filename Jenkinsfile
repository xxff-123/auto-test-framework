pipeline {
    agent any
    stages {
        stage('拉取代码') {
            steps {
                // 国内网络访问 GitHub 不稳定，使用加速地址
                git 'https://gitclone.com/github.com/xxff-123/auto-test-framework.git'
            }
        }
        stage('构建镜像') {
            steps {
                sh 'docker build -t auto-test-framework .'
            }
        }
        stage('运行测试') {
            steps {
                sh 'docker run --rm auto-test-framework'
            }
        }
    }
}
