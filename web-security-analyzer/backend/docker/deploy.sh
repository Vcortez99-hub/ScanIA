#!/bin/bash

# Configurar variáveis
REGION="us-east-1"  # Altere para sua região AWS
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPOSITORY="web-security-analyzer-api"
TAG="latest"

# Logar no ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build da imagem
docker build -t $REPOSITORY .

# Taggear a imagem com o repositório do ECR
docker tag $REPOSITORY:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY:$TAG

# Push para o ECR
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY:$TAG