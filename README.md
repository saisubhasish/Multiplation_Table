# RegressionModel_MultiplicationTable

![HLD_MultiplicationTable](https://github.com/saisubhasish/MultiplationTable_RegressionModel/assets/102937478/c814f0d8-c0b5-4208-b60f-af9ac2ff324a)

# Model UI
![Screenshot (22)](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/c3b27abc-2d82-4fe8-9d73-c401ede66f8d)
![Screenshot (23)](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/1803f0a3-0b53-4362-9012-e1ffd9ebf9ba)
![Screenshot (24)](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/408f448d-8ed9-4990-8acd-8bda23131947)
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/ed1876b7-ff81-4191-a933-899077b1c547)



# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.
## 2. Create IAM user for deployment

#with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws


#Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

#Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess

## 3. Create ECR repo to store/save docker image

- Save the URI: 566373416292.dkr.ecr.ap-south-1.amazonaws.com/mlproj

## 4. Create EC2 machine (Ubuntu)
## 5. Open EC2 and Install docker in EC2 Machine:

#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

## 6. Configure EC2 as self-hosted runner:

setting>actions>runner>new self hosted runner> choose os> then run command one by one

## 7. Setup github secrets:

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

ECR_REPOSITORY_NAME = simple-app
