variable "aiven_api_token" {
  description = "Token de API para autenticação na Aiven"
  type        = string
  sensitive   = true
}

variable "aiven_project_name" {
  description = "Nome exato do projeto criado no console da Aiven"
  type        = string
}