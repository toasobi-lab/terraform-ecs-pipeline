variable "app_name" {
  description = "Name of the application"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "ecr_image_retention_count" {
  description = "Number of ECR images to retain"
  type        = number
  default     = 30
}

variable "ecr_untagged_retention_days" {
  description = "Days to retain untagged ECR images"
  type        = number
  default     = 1
} 