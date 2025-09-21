# 🚀 Deploy MedStock360 no Railway

## 🌐 **TRANSFORME SEU SISTEMA LOCAL EM SISTEMA NA NUVEM!**

---

## 📋 **O que é o Railway?**

O **Railway** é uma plataforma de cloud que permite hospedar aplicações web de forma simples e gratuita. Perfeito para o MedStock360!

### ✨ **Vantagens:**
- ✅ **Gratuito** até 500 horas/mês
- ✅ **Deploy automático** via GitHub
- ✅ **HTTPS automático** (SSL grátis)
- ✅ **Banco de dados** na nuvem
- ✅ **Acesso global** 24/7
- ✅ **Backup automático**

---

## 🎯 **PASSO A PASSO COMPLETO:**

### **1️⃣ Preparar o Projeto para Railway**

Você vai precisar adicionar estes arquivos ao seu repositório GitHub:

```
📄 railway.json                    # Configuração principal do Railway
📄 Procfile                        # Comando de inicialização
📄 runtime.txt                     # Versão do Python
📄 requirements.txt                # Dependências otimizadas
📄 app_railway.py                  # Versão otimizada (renomear para app.py)
📁 .railway/railway.toml           # Configurações avançadas
📁 .streamlit/config.toml          # Configurações do Streamlit
📄 .env.example                    # Exemplo de variáveis de ambiente
```

**IMPORTANTE:** Substitua o `app.py` atual pelo `app_railway.py` (renomeie)

### **2️⃣ Criar Conta no Railway**

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Conecte com sua conta do GitHub
4. Autorize o Railway a acessar seus repositórios

### **3️⃣ Fazer Deploy**

1. **Selecione:** "Deploy from GitHub repo"
2. **Escolha:** seu repositório `medstock360`
3. **Configure:** as variáveis de ambiente
4. **Deploy:** automático!

---

## 📁 **ARQUIVOS NECESSÁRIOS (criar no GitHub):**

### **1. railway.json**
```json
{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
  }
}
```

### **2. Procfile**
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

### **3. runtime.txt**
```
python-3.11.6
```

### **4. requirements.txt (atualizado para Railway)**
```
streamlit==1.28.0
pandas==2.0.3
plotly==5.17.0
python-dateutil==2.8.2
```

### **5. .railway/railway.toml**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"

[env]
PORT = "8080"
```

---

## ⚙️ **CONFIGURAÇÕES NECESSÁRIAS:**

### **Variáveis de Ambiente no Railway:**

```
PORT=8080
ENVIRONMENT=production
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

---

## 🔧 **MODIFICAÇÕES NO CÓDIGO:**

### **app.py - Ajustes para Produção:**

Adicione no início do `app.py`:

```python
import os

# Configurações para produção no Railway
if os.getenv('ENVIRONMENT') == 'production':
    st.set_page_config(
        page_title="MedStock360 Advanced",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "MedStock360 - Sistema Hospitalar na Nuvem"
        }
    )
```

---

## 🗄️ **BANCO DE DADOS NA NUVEM:**

### **Opção 1: Railway PostgreSQL (Recomendado)**

1. No Railway Dashboard
2. Clique em "Add Service" 
3. Selecione "PostgreSQL"
4. Conecte ao seu projeto

### **Opção 2: Manter SQLite (Mais Simples)**

O SQLite funciona no Railway, mas os dados são perdidos a cada deploy. Para desenvolvimento está OK.

---

## 🌐 **ACESSO AO SISTEMA:**

Após o deploy, você terá:

```
URL: https://medstock360-production.up.railway.app
```

**Exemplo de como ficará:**
- ✅ Acesso via internet de qualquer lugar
- ✅ HTTPS automático (seguro)
- ✅ Funcionando 24/7
- ✅ Múltiplos usuários simultâneos

---

## 📱 **VANTAGENS DO SISTEMA NA NUVEM:**

### **Para Hospitais:**
- 👨‍⚕️ **Médicos acessam de casa**
- 💊 **Farmacêuticos acessam de qualquer local**
- 📱 **Funciona no celular**
- 🔒 **Dados seguros na nuvem**

### **Para Clínicas:**
- 🌐 **Filiais acessam o mesmo sistema**
- 📊 **Relatórios centralizados**
- 💾 **Backup automático**
- 🚀 **Sem necessidade de servidor próprio**

---

## 💰 **CUSTOS:**

### **Plano Gratuito Railway:**
- ✅ 500 horas/mês (suficiente para uso moderado)
- ✅ 1GB RAM
- ✅ 1GB armazenamento
- ✅ Banda ilimitada

### **Plano Pro ($5/mês):**
- ✅ Ilimitado
- ✅ 8GB RAM
- ✅ 100GB armazenamento
- ✅ Domínio customizado

---

## 🔐 **SEGURANÇA NA NUVEM:**

### **O que o Railway oferece:**
- ✅ **HTTPS automático** (SSL)
- ✅ **Firewall** integrado
- ✅ **Backup automático**
- ✅ **Monitoramento** 24/7
- ✅ **Logs** de acesso

### **Recomendações adicionais:**
- 🔑 **Mude a senha padrão** imediatamente
- 🔒 **Use senhas fortes** para todos os usuários
- 📊 **Monitor logs** regularmente
- 🔄 **Atualizações** regulares

---

## 🚀 **PRÓXIMOS PASSOS:**

1. **Adicione os arquivos** listados acima ao seu GitHub
2. **Crie conta** no Railway
3. **Conecte** seu repositório
4. **Configure** variáveis de ambiente
5. **Deploy!** 🎉

---

## 🆘 **SUPORTE:**

### **Se der erro no deploy:**
1. Verifique os logs no Railway Dashboard
2. Confirme se todos os arquivos estão no GitHub
3. Verifique as variáveis de ambiente

### **Problemas comuns:**
- **Port error:** Certifique-se que `$PORT` está configurado
- **Module error:** Verifique o requirements.txt
- **Database error:** Configure o banco corretamente

---

**🌟 Em poucos minutos seu sistema estará rodando na nuvem! 🌟**