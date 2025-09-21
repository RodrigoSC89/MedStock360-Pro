# MedStock360 - Variáveis de Ambiente
# Copie para .env e configure conforme necessário

# Ambiente de execução
ENVIRONMENT=production

# Porta da aplicação (Railway define automaticamente)
PORT=8080

# Configurações do Streamlit
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Banco de dados (opcional - usar PostgreSQL no Railway)
# DATABASE_URL=postgresql://user:password@host:port/database

# Configurações de segurança (opcional)
# SECRET_KEY=sua-chave-secreta-aqui
# JWT_SECRET=sua-chave-jwt-aqui

# Configurações de email (opcional)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=seu-email@gmail.com
# SMTP_PASSWORD=sua-senha-app

# Configurações de backup (opcional)
# BACKUP_ENABLED=true
# BACKUP_INTERVAL_HOURS=6

# Configurações de logs (opcional)
# LOG_LEVEL=INFO
# LOG_TO_FILE=true