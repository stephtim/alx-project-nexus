pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test') { steps { sh 'python -m pip install -r ecommerce-backend/requirements.txt && cd ecommerce-backend && python manage.py test' } }
    stage('Build') { steps { sh 'docker build -t ecommerce-backend:latest ecommerce-backend' } }
  }
}
