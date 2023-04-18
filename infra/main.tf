terraform {
  required_version = "~> 1.3.7"

  backend "s3" {
    # aws s3 mb s3://kiba-infra-pablo-production
    key = "tf-state.json"
    region = "eu-west-1"
    bucket = "kiba-infra-pablo-production"
    profile = "kiba"
    encrypt = true
  }

  required_providers {
    aws = {
      version = "4.12.1"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  profile = "kiba"
}

provider "aws" {
  alias = "acm"
  region = "us-east-1"
  profile = "kiba"
}

locals {
  project = "pablo"
  root_domain_name = "pablo-images.kibalabs.com"
}
