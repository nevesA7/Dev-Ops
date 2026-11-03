output "service_uri" {
  description = "URI de conexão completa do PostgreSQL para ser cadastrada no Render"
  value       = aiven_pg.dashboard_pg.service_uri
  sensitive   = true
}