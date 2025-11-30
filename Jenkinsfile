pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test') { steps { sh 'python -m pip install -r ecommerce-backend/requirements.txt && cd ecommerce-backend && python manage.py test' } }
    stage('Build') { steps { sh 'docker build -t ecommerce-backend:latest ecommerce-backend' } }
    stage('Deploy') {
      steps {
        withCredentials([string(credentialsId: 'DB_NAME', variable: 'DB_NAME'),
                         string(credentialsId: 'DB_USER', variable: 'DB_USER'),
                         string(credentialsId: 'DB_PASS', variable: 'DB_PASS'),
                         string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY')]) {
          sh '''
cat > ecommerce-backend/.env <<EOF
SECRET_KEY=${SECRET_KEY}
DEBUG=1
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASS=${DB_PASS}
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

docker-compose -f docker-compose.yml up --build -d
'''
        }
      }
    }
  }
}
