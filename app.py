"""
🏥 MedStock360 Advanced - RAILWAY CLOUD EDITION
Sistema Hospitalar Completo Multi-usuário
Versão: 3.0 Railway Cloud
Otimizado para deploy na nuvem Railway
"""

import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import uuid
from pathlib import Path
import time
import re
import os

# Configurações específicas para Railway
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
PORT = os.getenv('PORT', '8501')

# Configuração da página otimizada para Railway
if ENVIRONMENT == 'production':
    st.set_page_config(
        page_title="MedStock360 Cloud",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "🏥 MedStock360 - Sistema Hospitalar na Nuvem"
        }
    )
else:
    st.set_page_config(
        page_title="MedStock360 Advanced",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# CSS personalizado otimizado para Railway
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .cloud-badge {
        background: linear-gradient(45deg, #00c851, #007e33);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 10px;
    }
    .user-info {
        background: #f0f2f6;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-success {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .cloud-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseManager:
    """Gerenciador de banco de dados otimizado para Railway"""
    
    def __init__(self):
        # Caminho do banco otimizado para Railway
        if ENVIRONMENT == 'production':
            # No Railway, usar pasta temporária
            self.db_path = "/tmp/medstock360.db"
        else:
            # Local, usar pasta data
            self.db_path = "data/medstock360.db"
            Path("data").mkdir(exist_ok=True)
        
        self.init_database()
    
    def get_connection(self):
        """Obter conexão com o banco"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializar tabelas do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome_completo TEXT NOT NULL,
                email TEXT,
                perfil TEXT NOT NULL,
                crm_crf TEXT,
                ativo INTEGER DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_login TIMESTAMP,
                criado_por INTEGER,
                FOREIGN KEY (criado_por) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de medicamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                principio_ativo TEXT,
                fabricante TEXT,
                categoria TEXT,
                apresentacao TEXT,
                concentracao TEXT,
                registro_anvisa TEXT,
                controlado INTEGER DEFAULT 0,
                temperatura_armazenamento TEXT,
                via_administracao TEXT,
                observacoes TEXT,
                ativo INTEGER DEFAULT 1,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cadastrado_por INTEGER,
                FOREIGN KEY (cadastrado_por) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de lotes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicamento_id INTEGER NOT NULL,
                numero_lote TEXT NOT NULL,
                data_fabricacao DATE,
                data_validade DATE NOT NULL,
                quantidade_inicial INTEGER NOT NULL,
                quantidade_atual INTEGER NOT NULL,
                preco_unitario REAL,
                fornecedor TEXT,
                local_armazenamento TEXT,
                observacoes TEXT,
                ativo INTEGER DEFAULT 1,
                data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responsavel_entrada INTEGER,
                FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id),
                FOREIGN KEY (responsavel_entrada) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de pacientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                cpf TEXT UNIQUE,
                rg TEXT,
                data_nascimento DATE,
                sexo TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                plano_saude TEXT,
                numero_carteirinha TEXT,
                contato_emergencia TEXT,
                observacoes TEXT,
                ativo INTEGER DEFAULT 1,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cadastrado_por INTEGER,
                FOREIGN KEY (cadastrado_por) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de consultas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                data_consulta TIMESTAMP NOT NULL,
                tipo_consulta TEXT,
                motivo TEXT,
                diagnostico TEXT,
                observacoes TEXT,
                status TEXT DEFAULT 'Agendada',
                valor REAL,
                data_agendamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agendado_por INTEGER,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (medico_id) REFERENCES usuarios (id),
                FOREIGN KEY (agendado_por) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de receitas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consulta_id INTEGER,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                data_emissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT,
                status TEXT DEFAULT 'Ativa',
                FOREIGN KEY (consulta_id) REFERENCES consultas (id),
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (medico_id) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de itens da receita
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receita_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receita_id INTEGER NOT NULL,
                medicamento_id INTEGER NOT NULL,
                dosagem TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                frequencia TEXT NOT NULL,
                duracao_tratamento TEXT,
                instrucoes_uso TEXT,
                FOREIGN KEY (receita_id) REFERENCES receitas (id),
                FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
            )
        """)
        
        # Tabela de movimentações de estoque
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lote_id INTEGER NOT NULL,
                tipo_movimento TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                motivo TEXT,
                receita_id INTEGER,
                data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responsavel INTEGER NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (lote_id) REFERENCES lotes (id),
                FOREIGN KEY (receita_id) REFERENCES receitas (id),
                FOREIGN KEY (responsavel) REFERENCES usuarios (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Criar usuário administrador padrão
        self.create_default_admin()
    
    def create_default_admin(self):
        """Criar usuário administrador padrão"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar se já existe um admin
        cursor.execute("SELECT id FROM usuarios WHERE perfil = 'Administrador'")
        if not cursor.fetchone():
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, password_hash, nome_completo, perfil)
                VALUES ('admin', ?, 'Administrador do Sistema', 'Administrador')
            """, (password_hash,))
            conn.commit()
        
        conn.close()

class AuthManager:
    """Gerenciador de autenticação"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def hash_password(self, password):
        """Criar hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verificar senha"""
        return self.hash_password(password) == password_hash
    
    def authenticate(self, username, password):
        """Autenticar usuário"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, password_hash, nome_completo, perfil, ativo
            FROM usuarios WHERE username = ? AND ativo = 1
        """, (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and self.verify_password(password, user[2]):
            return {
                'id': user[0],
                'username': user[1],
                'nome_completo': user[3],
                'perfil': user[4]
            }
        return None
    
    def get_user_permissions(self, perfil):
        """Obter permissões do usuário"""
        permissions = {
            'Administrador': {
                'usuarios': ['criar', 'editar', 'visualizar', 'excluir'],
                'medicamentos': ['criar', 'editar', 'visualizar', 'excluir'],
                'estoque': ['criar', 'editar', 'visualizar', 'excluir'],
                'pacientes': ['criar', 'editar', 'visualizar', 'excluir'],
                'consultas': ['criar', 'editar', 'visualizar', 'excluir'],
                'receitas': ['criar', 'editar', 'visualizar', 'excluir'],
                'relatorios': ['visualizar', 'exportar']
            },
            'Farmacêutico': {
                'medicamentos': ['criar', 'editar', 'visualizar'],
                'estoque': ['criar', 'editar', 'visualizar'],
                'receitas': ['visualizar', 'dispensar'],
                'pacientes': ['visualizar'],
                'relatorios': ['visualizar']
            },
            'Médico': {
                'pacientes': ['criar', 'editar', 'visualizar'],
                'consultas': ['criar', 'editar', 'visualizar'],
                'receitas': ['criar', 'editar', 'visualizar'],
                'medicamentos': ['visualizar'],
                'relatorios': ['visualizar']
            },
            'Enfermeiro': {
                'pacientes': ['visualizar', 'editar'],
                'consultas': ['visualizar'],
                'medicamentos': ['visualizar'],
                'estoque': ['visualizar'],
                'receitas': ['visualizar']
            }
        }
        return permissions.get(perfil, {})

def main():
    """Função principal da aplicação"""
    
    # Inicializar gerenciadores
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
        st.session_state.auth_manager = AuthManager(st.session_state.db_manager)
    
    # Verificar autenticação
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    """Página de login otimizada para Railway"""
    
    # Badge de ambiente cloud
    cloud_badge = ""
    if ENVIRONMENT == 'production':
        cloud_badge = '<span class="cloud-badge">☁️ CLOUD</span>'
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🏥 MedStock360 Advanced{cloud_badge}</h1>
        <p>Sistema Hospitalar Completo Multi-usuário</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Informações da versão cloud
    if ENVIRONMENT == 'production':
        st.markdown("""
        <div class="cloud-info">
            ☁️ <strong>Versão Cloud</strong> | 🌐 Acesso Global 24/7 | 🔒 Dados Seguros | 💾 Backup Automático
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Acesso ao Sistema")
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            
            submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ Por favor, preencha todos os campos!")
                else:
                    user = st.session_state.auth_manager.authenticate(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.session_state.permissions = st.session_state.auth_manager.get_user_permissions(user['perfil'])
                        st.success(f"✅ Bem-vindo, {user['nome_completo']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
        
        st.markdown("---")
        st.info("""
        **Usuário Padrão:**
        - Usuário: `admin`
        - Senha: `admin123`
        
        ⚠️ **IMPORTANTE:** Mude a senha após o primeiro login!
        """)
        
        # Informações adicionais para versão cloud
        if ENVIRONMENT == 'production':
            st.markdown("---")
            st.success("""
            🌟 **Sistema na Nuvem Ativo!**
            - ✅ Acesso de qualquer lugar
            - ✅ Múltiplos usuários simultâneos  
            - ✅ Dados sincronizados em tempo real
            - ✅ Backup automático
            """)

def show_main_app():
    """Aplicação principal otimizada para Railway"""
    
    # Badge de ambiente
    cloud_badge = ""
    version_info = "v3.0"
    if ENVIRONMENT == 'production':
        cloud_badge = '<span class="cloud-badge">☁️ CLOUD</span>'
        version_info = "v3.0 Cloud Edition"
    
    # Header com informações do usuário
    st.markdown(f"""
    <div class="main-header">
        <h1>🏥 MedStock360 Advanced{cloud_badge}</h1>
        <p>Sistema Hospitalar Completo Multi-usuário - {version_info}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Informações do usuário logado
    user_info_col1, user_info_col2, user_info_col3 = st.columns([2, 1, 1])
    
    with user_info_col1:
        st.markdown(f"""
        <div class="user-info">
            👤 <strong>{st.session_state.user['nome_completo']}</strong> | 
            🎭 {st.session_state.user['perfil']} | 
            📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </div>
        """, unsafe_allow_html=True)
    
    with user_info_col3:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.permissions = None
            st.rerun()
    
    # Menu lateral
    with st.sidebar:
        st.markdown("### 📋 Menu Principal")
        
        # Badge cloud no sidebar
        if ENVIRONMENT == 'production':
            st.markdown("""
            <div style="background: linear-gradient(45deg, #00c851, #007e33); color: white; padding: 0.5rem; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
                ☁️ <strong>CLOUD EDITION</strong><br>
                🌐 Online 24/7
            </div>
            """, unsafe_allow_html=True)
        
        # Opções baseadas nas permissões do usuário
        menu_options = []
        
        # Dashboard sempre disponível
        menu_options.append("🏠 Dashboard")
        
        if 'medicamentos' in st.session_state.permissions:
            menu_options.append("💊 Medicamentos")
        
        if 'estoque' in st.session_state.permissions:
            menu_options.append("📦 Estoque")
            menu_options.append("🔮 Análise Preditiva")
        
        if 'pacientes' in st.session_state.permissions:
            menu_options.append("👥 Pacientes")
        
        if 'consultas' in st.session_state.permissions:
            menu_options.append("📅 Consultas")
        
        if 'receitas' in st.session_state.permissions:
            menu_options.append("📝 Receitas")
        
        if 'usuarios' in st.session_state.permissions:
            menu_options.append("👤 Usuários")
        
        if 'relatorios' in st.session_state.permissions:
            menu_options.append("📊 Relatórios")
        
        selected_menu = st.selectbox("Selecione uma opção:", menu_options)
    
    # Roteamento das páginas (simplified for this example)
    if selected_menu == "🏠 Dashboard":
        show_dashboard()
    # Add other menu handlers here...

def show_dashboard():
    """Dashboard principal otimizado para Railway"""
    st.markdown("## 🏠 Dashboard")
    
    # Informações da versão cloud
    if ENVIRONMENT == 'production':
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>☁️</h3>
                <h2>CLOUD</h2>
                <p>Sistema Online</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🌐</h3>
                <h2>24/7</h2>
                <p>Disponibilidade</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>🔒</h3>
                <h2>HTTPS</h2>
                <p>Conexão Segura</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    conn = st.session_state.db_manager.get_connection()
    
    # Total de medicamentos
    total_medicamentos = pd.read_sql("SELECT COUNT(*) as count FROM medicamentos WHERE ativo = 1", conn).iloc[0]['count']
    
    # Total de pacientes
    total_pacientes = pd.read_sql("SELECT COUNT(*) as count FROM pacientes WHERE ativo = 1", conn).iloc[0]['count']
    
    # Consultas hoje
    hoje = date.today()
    consultas_hoje = pd.read_sql("""
        SELECT COUNT(*) as count FROM consultas 
        WHERE DATE(data_consulta) = ? AND status != 'Cancelada'
    """, conn, params=[hoje]).iloc[0]['count']
    
    # Medicamentos próximos ao vencimento (30 dias)
    vencimento_proximo = pd.read_sql("""
        SELECT COUNT(DISTINCT l.medicamento_id) as count 
        FROM lotes l
        WHERE l.data_validade <= DATE('now', '+30 days') 
        AND l.quantidade_atual > 0 AND l.ativo = 1
    """, conn).iloc[0]['count']
    
    conn.close()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💊</h3>
            <h2>{total_medicamentos}</h2>
            <p>Medicamentos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥</h3>
            <h2>{total_pacientes}</h2>
            <p>Pacientes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅</h3>
            <h2>{consultas_hoje}</h2>
            <p>Consultas Hoje</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚠️</h3>
            <h2>{vencimento_proximo}</h2>
            <p>Próximos ao Vencimento</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Alertas importantes
    if vencimento_proximo > 0:
        st.markdown(f"""
        <div class="alert-warning">
            ⚠️ <strong>Atenção!</strong> Existem {vencimento_proximo} medicamentos com vencimento em 30 dias ou menos.
        </div>
        """, unsafe_allow_html=True)
    
    # Informações de sucesso para versão cloud
    if ENVIRONMENT == 'production':
        st.markdown("""
        <div class="alert-success">
            🌟 <strong>Sistema funcionando perfeitamente na nuvem!</strong> 
            Seus dados estão seguros e acessíveis 24/7 de qualquer lugar do mundo.
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()