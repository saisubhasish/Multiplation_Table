# Problem statement
A tool for multiplication table is required because it allows for quick and accurate multiplication calculations. It eliminates the need for manual calculations, which can be time-consuming and prone to errors. A calculator can handle large numbers and complicated calculations with ease, making it an essential tool for students, professionals, and anyone who needs to perform multiplication frequently. Additionally, a calculator provides instant results, allowing for efficient problem-solving and decision-making. Overall, a multiplication calculator simplifies the process and saves valuable time, making it an indispensable tool in various fields.  

# RegressionModel_MultiplicationTable
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/9e58da18-5b10-4ee0-9c67-68ce9d236937)

HLD Document: https://docs.google.com/document/d/151DYibsWqod1YxlJ_7fdzIWa-O9YnBTN/edit?usp=sharing&ouid=114030088195074570088&rtpof=true&sd=true 

# Model Archtecture
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/c3ecfd88-fb99-4347-8c5f-0dfcb2d65692)

# Deployment Process
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/dd86bad3-3611-4888-ab81-def81128a985)

# Model workflow
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/2759f2ae-69b2-4dca-a2f9-24cb81d967e8)


# Model UI
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/cba489fd-6ebf-42fc-ab87-745d83460320)
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/c1a890e6-3ea7-40ff-aa3f-3a0e30b046e3)
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/71ff918f-a3e0-4dcd-bc6b-9944f60ababb)
![image](https://github.com/saisubhasish/Multiplation_Table/assets/102937478/c1d7af28-685b-4ff2-90a9-ea6989d20847)

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

- Save the URI: 832383300965.dkr.ecr.ap-south-1.amazonaws.com/mlproj

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

AWS_REGION = ap-south-1

AWS_ECR_LOGIN_URI = 832383300965.dkr.ecr.ap-south-1.amazonaws.com

ECR_REPOSITORY_NAME = mlproj
