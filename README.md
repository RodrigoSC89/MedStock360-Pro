# 🏥 MedStock360 Advanced

## Sistema Hospitalar Completo Multi-usuário

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)

### 📋 Descrição

O **MedStock360** é um sistema completo de gestão hospitalar que oferece controle de medicamentos, estoque, pacientes, consultas e receitas médicas. Desenvolvido para ser simples de usar, mas poderoso em funcionalidades.

**🌟 NOVIDADE:** Agora disponível na nuvem via Railway! ☁️

---

## 🚀 **DUAS FORMAS DE USAR:**

### 🌐 **OPÇÃO 1: SISTEMA NA NUVEM (RECOMENDADO)**
- ✅ **Acesso de qualquer lugar** 24/7
- ✅ **Múltiplos usuários** simultâneos
- ✅ **HTTPS automático** (seguro)
- ✅ **Backup automático**
- ✅ **Zero instalação**

### 💻 **OPÇÃO 2: SISTEMA LOCAL**
- ✅ **Controle total** dos dados
- ✅ **Funciona offline**
- ✅ **Personalização** completa
- ✅ **Gratuito para sempre**

---

## ✨ Funcionalidades Principais

### 🔐 **Sistema de Usuários**
- ✅ Login seguro com diferentes perfis
- ✅ Perfis: Administrador, Médico, Farmacêutico, Enfermeiro
- ✅ Permissões específicas por perfil
- ✅ Multi-usuário simultâneo

### 💊 **Gestão de Medicamentos**
- ✅ Cadastro completo de medicamentos
- ✅ Controle de princípio ativo, fabricante, categoria
- ✅ Informações de apresentação (comprimido, xarope, etc.)
- ✅ Via de administração (oral, intramuscular, etc.)
- ✅ Medicamentos controlados
- ✅ Registro ANVISA

### 📦 **Controle de Estoque Inteligente**
- ✅ Gestão por lotes com validade
- ✅ Controle de localização física
- ✅ Alertas automáticos de estoque baixo
- ✅ Alertas de medicamentos próximos ao vencimento
- ✅ **🔮 Análise Preditiva de Consumo**
- ✅ Histórico completo de movimentações

### 🔮 **Análise Preditiva (DESTAQUE!)**
- ✅ Previsão de quando medicamentos vão acabar
- ✅ Cálculo baseado no consumo histórico
- ✅ Sugestões automáticas de reposição
- ✅ Alertas inteligentes por prioridade
- ✅ Gráficos de consumo em tempo real

### 👥 **Gestão de Pacientes**
- ✅ Cadastro completo de pacientes
- ✅ Histórico médico
- ✅ Informações de convênio
- ✅ Contatos de emergência

### 📅 **Agendamento de Consultas**
- ✅ Agenda por médico
- ✅ Controle de status das consultas
- ✅ Histórico de consultas
- ✅ Integração com receitas

### 📝 **Receitas Médicas Digitais**
- ✅ Prescrição eletrônica
- ✅ Controle de medicamentos prescritos
- ✅ Dosagem e instruções de uso
- ✅ Histórico de receitas por paciente

### 📊 **Relatórios e Dashboard**
- ✅ Dashboard executivo com gráficos
- ✅ Relatórios de medicamentos
- ✅ Relatórios de estoque
- ✅ Relatórios de pacientes e consultas
- ✅ Exportação de dados

---

## 🌐 **DEPLOY NA NUVEM (RAILWAY)**

### 🚀 **Deploy Automático (1 Clique):**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/medstock360)

### 🛠️ **Deploy Manual:**

1. **Faça fork** deste repositório
2. **Acesse** [railway.app](https://railway.app)
3. **Conecte** sua conta GitHub
4. **Selecione** este repositório
5. **Deploy automático!** 🎉

### 🎯 **Resultado:**
```
🌐 URL: https://medstock360-production.up.railway.app
👤 Usuário: admin
🔒 Senha: admin123
```

### 💰 **Custos Railway:**
- **GRATUITO**: 500 horas/mês
- **PRO ($5/mês)**: Uso ilimitado

---

## 💻 **INSTALAÇÃO LOCAL**

### 📋 **Pré-requisitos**
- Python 3.8 ou superior
- Computador com Windows, Mac ou Linux

### 💻 **Instalação Simples**

#### **Windows:**
1. **Baixe o projeto:**
   ```bash
   git clone https://github.com/SEU_USUARIO/medstock360.git
   cd medstock360
   ```

2. **Execute a instalação automática:**
   ```bash
   INSTALAR_WINDOWS.bat
   ```

3. **Execute o sistema:**
   ```bash
   EXECUTAR_WINDOWS.bat
   ```

#### **Mac/Linux:**
1. **Baixe o projeto:**
   ```bash
   git clone https://github.com/SEU_USUARIO/medstock360.git
   cd medstock360
   ```

2. **Execute a instalação:**
   ```bash
   chmod +x instalar_mac.sh && ./instalar_mac.sh
   ```

3. **Execute o sistema:**
   ```bash
   ./executar_mac.sh
   ```

#### **Instalação Manual:**
```bash
pip install streamlit pandas plotly python-dateutil
streamlit run app.py
```

### 🌐 **Acesso Local:**
- **URL:** http://localhost:8501
- **Usuário:** `admin`
- **Senha:** `admin123`

---

## 👥 **Perfis de Usuário**

### 👑 **Administrador**
- Acesso total ao sistema
- Gerencia usuários
- Relatórios completos
- Configurações do sistema

### 👨‍⚕️ **Médico**
- Gestão de pacientes
- Agendamento de consultas
- Prescrição de receitas
- Consulta de medicamentos

### 💊 **Farmacêutico**
- Gestão de medicamentos
- Controle de estoque
- Dispensação de medicamentos
- Relatórios farmacêuticos

### 👩‍⚕️ **Enfermeiro**
- Consulta de pacientes
- Visualização de receitas
- Consulta de estoque
- Suporte às consultas

---

## 📁 **Estrutura do Projeto**

### **Para Uso Local:**
```
medstock360/
├── app.py                          # Aplicação principal
├── config.py                       # Configurações
├── requirements.txt                # Dependências
├── README.md                       # Este arquivo
├── INSTALACAO.md                   # Guia de instalação
├── INSTALAR_WINDOWS.bat           # Instalação Windows
├── EXECUTAR_WINDOWS.bat           # Execução Windows
├── instalar_mac.sh                # Instalação Mac/Linux
├── executar_mac.sh                # Execução Mac/Linux
├── data/                          # Banco de dados
├── logs/                          # Logs do sistema
└── backups/                       # Backups automáticos
```

### **Para Deploy Railway:**
```
medstock360/
├── app.py                          # Versão cloud otimizada
├── railway.json                    # Configuração Railway
├── Procfile                        # Comando de inicialização
├── runtime.txt                     # Versão Python
├── requirements.txt                # Dependências cloud
├── .railway/railway.toml           # Configurações Railway
├── .streamlit/config.toml          # Configurações Streamlit
├── .env.example                    # Variáveis de ambiente
├── DEPLOY_RAILWAY.md               # Guia de deploy
└── DEPLOY_RAPIDO.md                # Deploy em 5 minutos
```

---

## 🔧 **Configurações Importantes**

### 📊 **Análise Preditiva**
O sistema calcula automaticamente:
- **Consumo médio diário** baseado nos últimos 30 dias
- **Previsão de término** do estoque atual
- **Alertas inteligentes:**
  - 🚨 Crítico: menos de 7 dias
  - ⚠️ Atenção: menos de 15 dias
  - ✅ OK: mais de 30 dias

### 🔄 **Backup Automático**
- Backup automático a cada 6 horas
- Arquivos salvos na pasta `backups/`
- Retenção de 30 dias de backups

---

## 🎯 **Como Usar Cada Módulo**

### 1️⃣ **Cadastrar Medicamentos**
1. Acesse "💊 Medicamentos"
2. Clique em "➕ Cadastrar Medicamento"
3. Preencha todas as informações
4. Salve

### 2️⃣ **Controlar Estoque**
1. Acesse "📦 Estoque"
2. Para nova entrada: "➕ Entrada de Lote"
3. Monitore alertas automáticos
4. Use "🔮 Análise Preditiva" para previsões

### 3️⃣ **Cadastrar Pacientes**
1. Acesse "👥 Pacientes"
2. Clique em "➕ Cadastrar Paciente"
3. Complete todos os dados
4. Salve

### 4️⃣ **Agendar Consultas**
1. Acesse "📅 Consultas"
2. Clique em "➕ Agendar Consulta"
3. Selecione paciente e médico
4. Defina data/hora

### 5️⃣ **Prescrever Receitas**
1. Acesse "📝 Receitas"
2. Clique em "➕ Nova Receita"
3. Selecione paciente
4. Adicione medicamentos com dosagem
5. Salve a receita

---

## 📈 **Alertas Automáticos**

### 🔴 **Estoque Crítico**
- Medicamentos com quantidade ≤ 10 unidades
- Aparecem no dashboard principal

### ⚠️ **Próximo ao Vencimento**
- Medicamentos que vencem em 30 dias
- Alertas visuais em todas as telas

### 🔮 **Previsão de Término**
- Baseada no consumo histórico
- Cálculo automático diário
- Sugestões de reposição

---

## 🛠️ **Solução de Problemas**

### ❓ **Não consegue fazer login?**
- Verifique usuário e senha
- Use credenciais padrão: `admin` / `admin123`

### ❓ **Sistema lento?**
- Feche abas desnecessárias do navegador
- Reinicie o aplicativo

### ❓ **Erro ao instalar?**
- Verifique se o Python está instalado
- Execute: `pip install --upgrade pip`
- Tente novamente: `pip install -r requirements.txt`

### ❓ **Sistema na nuvem não abre?**
- Aguarde alguns minutos após deploy
- Verifique logs no Railway Dashboard
- Confirme se todos os arquivos estão no GitHub

### ❓ **Perdeu dados?**
- **Local:** Verifique a pasta `backups/`
- **Cloud:** Dados são persistidos automaticamente

---

## 🌐 **Comparação: Local vs Cloud**

| Recurso | Local 💻 | Cloud ☁️ |
|---------|----------|----------|
| **Acesso** | Apenas local | Global 24/7 |
| **Instalação** | Necessária | Zero |
| **Múltiplos usuários** | Limitado | Ilimitado |
| **Backup** | Manual | Automático |
| **Atualizações** | Manual | Automático |
| **Custo** | Gratuito | $0-5/mês |
| **Manutenção** | Você | Railway |
| **Dados** | Seu controle | Na nuvem |
| **Performance** | Depende do PC | Sempre rápido |
| **Segurança** | Sua responsabilidade | HTTPS automático |

---

## 📞 **Suporte**

### 🔧 **Problemas Técnicos**
1. Verifique a seção "Solução de Problemas"
2. Consulte os logs na pasta `logs/`
3. Abra uma issue no GitHub

### 💡 **Sugestões de Melhorias**
- Abra uma issue no GitHub com suas ideias
- Descreva detalhadamente a funcionalidade

---

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🎉 **Versão Atual: 3.0**

### ✨ **Novidades da v3.0:**
- 🔮 **Análise Preditiva de Medicamentos**
- ☁️ **Deploy na nuvem via Railway**
- 📊 **Dashboard melhorado com gráficos interativos**
- 🎯 **Alertas inteligentes por prioridade**
- 👥 **Sistema multi-usuário robusto**
- 📱 **Interface responsiva**
- 🔒 **Segurança aprimorada**

### 🗓️ **Próximas Atualizações (v3.1):**
- 📱 Notificações push
- 📧 Envio de alertas por email
- 📊 Relatórios em PDF
- 🔗 Integração com sistemas externos
- 📱 App mobile

---

## 🌟 **Contribua!**

Ajude a melhorar o MedStock360:
1. Faça um Fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

## 🚀 **Links Úteis**

- 🌐 **Demo Cloud:** [medstock360.railway.app](https://medstock360.railway.app)
- 📚 **Documentação:** [INSTALACAO.md](INSTALACAO.md)
- ☁️ **Deploy Railway:** [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)
- ⚡ **Deploy Rápido:** [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)
- 🐛 **Issues:** [GitHub Issues](https://github.com/SEU_USUARIO/medstock360/issues)
- 💬 **Discussões:** [GitHub Discussions](https://github.com/SEU_USUARIO/medstock360/discussions)

---

## 📸 **Screenshots**

### 🏠 **Dashboard Principal**
![Dashboard](screenshots/dashboard.png)

### 🔮 **Análise Preditiva**
![Análise Preditiva](screenshots/analise-preditiva.png)

### 💊 **Gestão de Medicamentos**
![Medicamentos](screenshots/medicamentos.png)

### ☁️ **Versão Cloud**
![Cloud Version](screenshots/cloud-version.png)

---

**Desenvolvido com ❤️ para facilitar a gestão hospitalar!**

**MedStock360 - Transformando a gestão hospitalar! 🏥✨**

---

## 🏆 **Estatísticas do Projeto**

![GitHub stars](https://img.shields.io/github/stars/SEU_USUARIO/medstock360)
![GitHub forks](https://img.shields.io/github/forks/SEU_USUARIO/medstock360)
![GitHub issues](https://img.shields.io/github/issues/SEU_USUARIO/medstock360)
![GitHub license](https://img.shields.io/github/license/SEU_USUARIO/medstock360)
![Railway Deploy](https://img.shields.io/badge/deploy-railway-blueviolet)

---

**⭐ Se este projeto te ajudou, dê uma estrela! ⭐**
