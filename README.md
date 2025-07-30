# ECS Playground - Serverless Container Demo

> Simple AWS Fargate deployment with Terraform and CI/CD pipeline

## 📍 Repository
**Clone the repository**:
```bash
git clone https://github.com/toasobi-lab/terraform-ecs-pipeline.git
cd terraform-ecs-pipeline
```

---

## 🚀 Quick Start

1. **Configure**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars if needed (defaults work for Tokyo region)
   ```

2. **Deploy Infrastructure**
   ```bash
   terraform init
   terraform apply
   ```

3. **Deploy Application**
   ```bash
   cd app && zip -r ../source.zip . && cd ..
   aws s3 cp source.zip s3://$(terraform output -raw s3_source_bucket_name)/source.zip
   ```

4. **Approve Deployment**
   - Go to AWS Console → CodePipeline
   - Approve the deployment when pipeline pauses

5. **Access Application**
   ```bash
   echo "Application URL: https://$(terraform output -raw cloudfront_domain_name)"
   ```

## 🏗️ Architecture

**Flow**: User → CloudFront → ALB → Fargate Tasks  
**Region**: Tokyo (ap-northeast-1)  
**Compute**: AWS Fargate (serverless containers)  
**Network**: Private subnets across 2 AZs  
**CI/CD**: S3 → CodeBuild → Manual Approval → ECS Deploy  

## 📦 What's Included

- **VPC**: Multi-AZ network with public/private subnets
- **ECS Fargate**: Serverless container hosting
- **ALB**: Load balancer with health checks
- **CloudFront**: Global CDN with HTTPS
- **ECR**: Private container registry
- **CI/CD**: CodePipeline with manual approval
- **Monitoring**: CloudWatch logs and metrics

## 🧹 Cleanup

```bash
terraform destroy
```

### State Cleanup
```bash
# Remove Terraform state files
rm -rf .terraform
rm -f .terraform.lock.hcl
rm -f terraform.tfstate
rm -f terraform.tfstate.backup
```

---

**Tech Stack**: Python 3.12 • Flask • Docker • AWS Fargate • Terraform  
