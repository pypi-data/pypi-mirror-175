terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data"
    key     = "terraform/ecs-cluster/dangolchain-cluster/task-def/dw-api/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    acl     = "bucket-owner-full-control"
  }
}

provider "aws" {
  region  = "ap-northeast-2"
}

variable "template_version" {
  default = "1"
}

variable "cluster_name" {
  default = "dangolchain-cluster"
}

# variables -----------------------------------------------
variable "awslog_region" {
  default = "ap-northeast-2"
}

variable "stages" {
  default = {
    default = {
        env_service_stage = "production"
        hosts = ["dangolchain.com"]
        listener_priority = 10
        service_name = "dw-api"
        task_definition_name = "dw-api"
    }
    qa = {
        env_service_stage = "qa"
        hosts = ["qa.dangolchain.com"]
        listener_priority = 20
        service_name = "dw-api--qa"
        task_definition_name = "dw-api--qa"
    }
  }
}

variable "service_auto_scaling" {
  default = {
    desired = 1
    memory = 80
    cpu = 400
    min = 1
    max = 3
  }
}

variable "exposed_container" {
  default = [{
    name = "dangolchain-api"
    port = 8080
  }]
}

variable "target_group" {
  default = {
    protocol = "HTTP"
    healthcheck = {
        path = "/management/server/status"
        matcher = "200,304"
        timeout = 10
        interval = 60
        healthy_threshold = 2
        unhealthy_threshold = 10
    }
  }
}

variable "loggings" {
  default = ["dangolchain-api"]
}

variable "loadbalancing_pathes" {
  default = ["/api/*", "/management/*"]
}

variable "requires_compatibilities" {
  default = ["EC2"]
}

variable "service_resources" {
  default = {
    memory = 0
    cpu = 0
  }
}
