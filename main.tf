terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.1"
    }
  }
}

# AWS Provider Configuration
provider "aws" {
  region = var.aws_region
}

# Networking Module
module "networking" {
  source = "./modules/networking"

  app_name               = var.app_name
  environment           = var.environment
  vpc_cidr              = var.vpc_cidr
  availability_zones    = var.availability_zones
  public_subnet_cidrs   = var.public_subnet_cidrs
  private_subnet_cidrs  = var.private_subnet_cidrs
}

# Security Module
module "security" {
  source = "./modules/security"

  app_name         = var.app_name
  environment      = var.environment
  vpc_id           = module.networking.vpc_id
  vpc_cidr_block   = module.networking.vpc_cidr_block
  app_port         = var.app_port
}

# ECR Module
module "ecr" {
  source = "./modules/ecr"

  app_name                    = var.app_name
  environment                 = var.environment
  ecr_image_retention_count   = var.ecr_image_retention_count
  ecr_untagged_retention_days = var.ecr_untagged_retention_days
}

# ALB Module
module "alb" {
  source = "./modules/alb"

  app_name                = var.app_name
  environment            = var.environment
  vpc_id                 = module.networking.vpc_id
  public_subnet_ids      = module.networking.public_subnet_ids
  alb_security_group_id  = module.security.alb_security_group_id
  app_port               = var.app_port
  health_check_path      = var.health_check_path
}

# ECS Module
module "ecs" {
  source = "./modules/ecs"

  app_name                        = var.app_name
  environment                     = var.environment
  vpc_id                          = module.networking.vpc_id
  private_subnet_ids              = module.networking.private_subnet_ids
  ecs_tasks_security_group_id     = module.security.ecs_tasks_security_group_id
  ecs_task_execution_role_arn     = module.security.ecs_task_execution_role_arn
  ecs_task_role_arn               = module.security.ecs_task_role_arn
  ecr_repository_url              = module.ecr.repository_url
  target_group_arn                = module.alb.target_group_arn
  task_cpu                        = var.ecs_task_cpu
  task_memory                     = var.ecs_task_memory
  service_desired_count           = var.ecs_service_desired_count
  app_port                        = var.app_port
  health_check_path               = var.health_check_path
  log_retention_days              = var.log_retention_days
}

# CloudFront Module
module "cloudfront" {
  source = "./modules/cloudfront"

  app_name        = var.app_name
  environment     = var.environment
  alb_dns_name    = module.alb.dns_name
}

# CodePipeline Module
module "codepipeline" {
  source = "./modules/codepipeline"

  app_name               = var.app_name
  environment            = var.environment
  ecr_repository_name    = module.ecr.repository_name
  ecs_cluster_name       = module.ecs.cluster_name
  ecs_service_name       = module.ecs.service_name
  codebuild_role_arn     = module.security.codebuild_role_arn
  codepipeline_role_arn  = module.security.codepipeline_role_arn
  log_retention_days     = var.log_retention_days
} 