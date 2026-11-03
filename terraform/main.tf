terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aiven = {
      source  = "aiven/aiven"
      version = ">= 4.0.0"
    }
  }
}

provider "aiven" {
  api_token = var.aiven_api_token
}

resource "aiven_pg" "dashboard_pg" {
  project      = var.aiven_project_name
  service_name = "dashboard-pg"
  cloud_name   = "aws-sa-east-1"
  plan         = "startup-4"

  pg_user_config {
    pg_version = "15"
    public_access {
      pg = true
    }
  }
}