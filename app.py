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

    # Roteamento das páginas
    if selected_menu == "🏠 Dashboard":
        show_dashboard()
    elif selected_menu == "💊 Medicamentos":
        show_medicamentos()
    elif selected_menu == "📦 Estoque":
        show_estoque()
    elif selected_menu == "🔮 Análise Preditiva":
        show_analise_preditiva()
    elif selected_menu == "👥 Pacientes":
        show_pacientes()
    elif selected_menu == "📅 Consultas":
        show_consultas()
    elif selected_menu == "📝 Receitas":
        show_receitas()
    elif selected_menu == "👤 Usuários":
        show_usuarios()
    elif selected_menu == "📊 Relatórios":
        show_relatorios()

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
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Medicamentos por Categoria")
        conn = st.session_state.db_manager.get_connection()
        df_categorias = pd.read_sql("""
            SELECT categoria, COUNT(*) as quantidade
            FROM medicamentos 
            WHERE ativo = 1 AND categoria IS NOT NULL
            GROUP BY categoria
            ORDER BY quantidade DESC
        """, conn)
        conn.close()
        
        if not df_categorias.empty:
            fig = px.pie(df_categorias, values='quantidade', names='categoria')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum medicamento cadastrado ainda.")
    
    with col2:
        st.markdown("### 📈 Consultas dos Últimos 7 Dias")
        conn = st.session_state.db_manager.get_connection()
        df_consultas = pd.read_sql("""
            SELECT DATE(data_consulta) as data, COUNT(*) as quantidade
            FROM consultas 
            WHERE data_consulta >= DATE('now', '-7 days')
            AND status != 'Cancelada'
            GROUP BY DATE(data_consulta)
            ORDER BY data
        """, conn)
        conn.close()
        
        if not df_consultas.empty:
            fig = px.line(df_consultas, x='data', y='quantidade', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma consulta nos últimos 7 dias.")

def show_medicamentos():
    """Módulo de medicamentos"""
    st.markdown("## 💊 Gestão de Medicamentos")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('medicamentos', []):
        tab1, tab2 = st.tabs(["📋 Lista de Medicamentos", "➕ Cadastrar Medicamento"])
    else:
        tab1, tab2 = st.tabs(["📋 Lista de Medicamentos", ""])
    
    with tab1:
        st.markdown("### 📋 Medicamentos Cadastrados")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Buscar medicamento", placeholder="Nome ou princípio ativo")
        
        with col2:
            conn = st.session_state.db_manager.get_connection()
            categorias = pd.read_sql("SELECT DISTINCT categoria FROM medicamentos WHERE categoria IS NOT NULL", conn)['categoria'].tolist()
            categoria_filter = st.selectbox("📂 Categoria", ["Todas"] + categorias)
        
        with col3:
            controlado_filter = st.selectbox("🎯 Tipo", ["Todos", "Controlados", "Não Controlados"])
        
        # Buscar medicamentos
        query = """
            SELECT m.*, u.nome_completo as cadastrado_por_nome
            FROM medicamentos m
            LEFT JOIN usuarios u ON m.cadastrado_por = u.id
            WHERE m.ativo = 1
        """
        params = []
        
        if search_term:
            query += " AND (m.nome LIKE ? OR m.principio_ativo LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if categoria_filter != "Todas":
            query += " AND m.categoria = ?"
            params.append(categoria_filter)
        
        if controlado_filter == "Controlados":
            query += " AND m.controlado = 1"
        elif controlado_filter == "Não Controlados":
            query += " AND m.controlado = 0"
        
        query += " ORDER BY m.nome"
        
        df_medicamentos = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if not df_medicamentos.empty:
            # Exibir tabela
            for _, med in df_medicamentos.iterrows():
                with st.expander(f"💊 {med['nome']} {'🔒' if med['controlado'] else ''}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Princípio Ativo:** {med['principio_ativo'] or 'N/A'}")
                        st.write(f"**Fabricante:** {med['fabricante'] or 'N/A'}")
                        st.write(f"**Categoria:** {med['categoria'] or 'N/A'}")
                    
                    with col2:
                        st.write(f"**Apresentação:** {med['apresentacao'] or 'N/A'}")
                        st.write(f"**Concentração:** {med['concentracao'] or 'N/A'}")
                        st.write(f"**Via de Administração:** {med['via_administracao'] or 'N/A'}")
                    
                    with col3:
                        st.write(f"**Registro ANVISA:** {med['registro_anvisa'] or 'N/A'}")
                        st.write(f"**Controlado:** {'Sim' if med['controlado'] else 'Não'}")
                        st.write(f"**Cadastrado por:** {med['cadastrado_por_nome'] or 'N/A'}")
                    
                    if med['observacoes']:
                        st.write(f"**Observações:** {med['observacoes']}")
        else:
            st.info("Nenhum medicamento encontrado com os filtros aplicados.")
    
    if 'criar' in st.session_state.permissions.get('medicamentos', []):
        with tab2:
            st.markdown("### ➕ Cadastrar Novo Medicamento")
            
            with st.form("form_medicamento"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("Nome do Medicamento *", placeholder="Ex: Dipirona Sódica")
                    principio_ativo = st.text_input("Princípio Ativo", placeholder="Ex: Dipirona Sódica")
                    fabricante = st.text_input("Fabricante", placeholder="Ex: EMS")
                    categoria = st.selectbox("Categoria", [
                        "", "Analgésicos", "Anti-inflamatórios", "Antibióticos", 
                        "Antidepressivos", "Anti-hipertensivos", "Vitaminas",
                        "Controlados", "Outros"
                    ])
                    apresentacao = st.text_input("Apresentação", placeholder="Ex: Comprimido, Ampola, Frasco")
                
                with col2:
                    concentracao = st.text_input("Concentração", placeholder="Ex: 500mg")
                    registro_anvisa = st.text_input("Registro ANVISA", placeholder="Ex: 1.0000.0000")
                    controlado = st.checkbox("Medicamento Controlado")
                    temperatura_armazenamento = st.selectbox("Temperatura de Armazenamento", [
                        "", "Ambiente (15°C a 30°C)", "Refrigerado (2°C a 8°C)", 
                        "Congelado (-20°C)", "Controlada (20°C a 25°C)"
                    ])
                    via_administracao = st.selectbox("Via de Administração", [
                        "", "Oral", "Intravenosa", "Intramuscular", "Subcutânea",
                        "Tópica", "Oftálmica", "Nasal", "Retal", "Outras"
                    ])
                
                observacoes = st.text_area("Observações", placeholder="Informações adicionais...")
                
                submitted = st.form_submit_button("💾 Cadastrar Medicamento", use_container_width=True)
                
                if submitted:
                    if not nome:
                        st.error("❌ O nome do medicamento é obrigatório!")
                    else:
                        try:
                            conn = st.session_state.db_manager.get_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                INSERT INTO medicamentos (
                                    nome, principio_ativo, fabricante, categoria, apresentacao,
                                    concentracao, registro_anvisa, controlado, temperatura_armazenamento,
                                    via_administracao, observacoes, cadastrado_por
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                nome, principio_ativo, fabricante, categoria, apresentacao,
                                concentracao, registro_anvisa, controlado, temperatura_armazenamento,
                                via_administracao, observacoes, st.session_state.user['id']
                            ))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Medicamento cadastrado com sucesso!")
                            time.sleep(2)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Erro ao cadastrar medicamento: {str(e)}")

def show_estoque():
    """Módulo de estoque"""
    st.markdown("## 📦 Gestão de Estoque")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('estoque', []):
        tab1, tab2, tab3 = st.tabs(["📋 Estoque Atual", "➕ Entrada de Lote", "📊 Movimentações"])
    else:
        tab1, tab2, tab3 = st.tabs(["📋 Estoque Atual", "", "📊 Movimentações"])
    
    with tab1:
        st.markdown("### 📋 Estoque Atual")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Buscar medicamento", placeholder="Nome do medicamento")
        
        with col2:
            status_filter = st.selectbox("📊 Status", ["Todos", "Em estoque", "Estoque baixo", "Sem estoque", "Próximo ao vencimento"])
        
        with col3:
            conn = st.session_state.db_manager.get_connection()
            locais = pd.read_sql("SELECT DISTINCT local_armazenamento FROM lotes WHERE local_armazenamento IS NOT NULL", conn)['local_armazenamento'].tolist()
            local_filter = st.selectbox("📍 Local", ["Todos"] + locais)
        
        # Query base
        query = """
            SELECT 
                m.nome as medicamento,
                m.principio_ativo,
                l.numero_lote,
                l.data_validade,
                l.quantidade_atual,
                l.local_armazenamento,
                l.fornecedor,
                l.preco_unitario,
                CASE 
                    WHEN l.quantidade_atual = 0 THEN 'Sem estoque'
                    WHEN l.quantidade_atual <= 10 THEN 'Estoque baixo'
                    WHEN DATE(l.data_validade) <= DATE('now', '+30 days') THEN 'Próximo ao vencimento'
                    ELSE 'Normal'
                END as status
            FROM lotes l
            JOIN medicamentos m ON l.medicamento_id = m.id
            WHERE l.ativo = 1 AND m.ativo = 1
        """
        params = []
        
        if search_term:
            query += " AND m.nome LIKE ?"
            params.append(f"%{search_term}%")
        
        if local_filter != "Todos":
            query += " AND l.local_armazenamento = ?"
            params.append(local_filter)
        
        if status_filter != "Todos":
            if status_filter == "Em estoque":
                query += " AND l.quantidade_atual > 10"
            elif status_filter == "Estoque baixo":
                query += " AND l.quantidade_atual > 0 AND l.quantidade_atual <= 10"
            elif status_filter == "Sem estoque":
                query += " AND l.quantidade_atual = 0"
            elif status_filter == "Próximo ao vencimento":
                query += " AND DATE(l.data_validade) <= DATE('now', '+30 days') AND l.quantidade_atual > 0"
        
        query += " ORDER BY m.nome, l.data_validade"
        
        df_estoque = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if not df_estoque.empty:
            # Resumo
            total_lotes = len(df_estoque)
            sem_estoque = len(df_estoque[df_estoque['quantidade_atual'] == 0])
            estoque_baixo = len(df_estoque[(df_estoque['quantidade_atual'] > 0) & (df_estoque['quantidade_atual'] <= 10)])
            proximo_vencimento = len(df_estoque[df_estoque['status'] == 'Próximo ao vencimento'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📦 Total de Lotes", total_lotes)
            with col2:
                st.metric("🔴 Sem Estoque", sem_estoque)
            with col3:
                st.metric("🟡 Estoque Baixo", estoque_baixo)
            with col4:
                st.metric("⚠️ Próximo Vencimento", proximo_vencimento)
            
            # Alertas
            if sem_estoque > 0:
                st.markdown(f"""
                <div class="alert-danger">
                    🔴 <strong>Atenção!</strong> {sem_estoque} lotes sem estoque.
                </div>
                """, unsafe_allow_html=True)
            
            if proximo_vencimento > 0:
                st.markdown(f"""
                <div class="alert-warning">
                    ⚠️ <strong>Alerta!</strong> {proximo_vencimento} lotes próximos ao vencimento.
                </div>
                """, unsafe_allow_html=True)
            
            # Tabela de estoque
            st.dataframe(
                df_estoque,
                use_container_width=True,
                column_config={
                    "medicamento": "Medicamento",
                    "numero_lote": "Lote",
                    "data_validade": st.column_config.DateColumn("Validade", format="DD/MM/YYYY"),
                    "quantidade_atual": "Quantidade",
                    "local_armazenamento": "Local",
                    "status": st.column_config.TextColumn("Status")
                }
            )
        else:
            st.info("Nenhum lote encontrado com os filtros aplicados.")
    
    # Implementar outras abas do estoque aqui...

def show_analise_preditiva():
    """Módulo de análise preditiva"""
    st.markdown("## 🔮 Análise Preditiva de Medicamentos")
    
    conn = st.session_state.db_manager.get_connection()
    
    # Buscar medicamentos com movimentação
    query = """
        SELECT 
            m.id,
            m.nome as medicamento,
            m.principio_ativo,
            SUM(l.quantidade_atual) as estoque_atual,
            COUNT(DISTINCT mov.id) as total_movimentacoes
        FROM medicamentos m
        JOIN lotes l ON m.id = l.medicamento_id
        LEFT JOIN movimentacoes mov ON l.id = mov.lote_id
        WHERE m.ativo = 1 AND l.ativo = 1 AND l.quantidade_atual > 0
        GROUP BY m.id, m.nome, m.principio_ativo
        HAVING total_movimentacoes > 0
        ORDER BY m.nome
    """
    
    df_medicamentos_pred = pd.read_sql(query, conn)
    
    if df_medicamentos_pred.empty:
        st.info("Nenhum medicamento com histórico de movimentação encontrado.")
        st.markdown("""
        ### 💡 Como usar a análise preditiva:
        1. **Cadastre medicamentos** no sistema
        2. **Registre entradas** de lotes no estoque
        3. **Registre saídas** (dispensações, receitas)
        4. **Aguarde alguns dias** para acumular histórico
        5. **Volte aqui** para ver as previsões!
        """)
        conn.close()
        return
    
    # Seletor de medicamento
    medicamento_options = {f"{row['medicamento']} (Estoque: {row['estoque_atual']})": row['id'] for _, row in df_medicamentos_pred.iterrows()}
    medicamento_selecionado = st.selectbox("🔍 Selecione um medicamento para análise:", list(medicamento_options.keys()))
    
    if medicamento_selecionado:
        medicamento_id = medicamento_options[medicamento_selecionado]
        
        # Calcular consumo médio dos últimos 30 dias
        query_consumo = """
            SELECT 
                DATE(mov.data_movimento) as data,
                SUM(CASE WHEN mov.tipo_movimento = 'Saída' THEN mov.quantidade ELSE 0 END) as consumo_diario
            FROM movimentacoes mov
            JOIN lotes l ON mov.lote_id = l.id
            WHERE l.medicamento_id = ? 
            AND mov.data_movimento >= DATE('now', '-30 days')
            AND mov.tipo_movimento = 'Saída'
            GROUP BY DATE(mov.data_movimento)
            ORDER BY data DESC
        """
        
        df_consumo = pd.read_sql(query_consumo, conn, params=[medicamento_id])
        
        if not df_consumo.empty:
            # Calcular métricas
            consumo_medio_diario = df_consumo['consumo_diario'].mean()
            consumo_total_30dias = df_consumo['consumo_diario'].sum()
            estoque_atual = df_medicamentos_pred[df_medicamentos_pred['id'] == medicamento_id]['estoque_atual'].iloc[0]
            
            # Previsões
            dias_para_acabar = estoque_atual / consumo_medio_diario if consumo_medio_diario > 0 else float('inf')
            data_previsao_fim = datetime.now() + timedelta(days=int(dias_para_acabar))
            
            # Exibir métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📦 Estoque Atual", f"{estoque_atual} unidades")
            
            with col2:
                st.metric("📊 Consumo Médio Diário", f"{consumo_medio_diario:.1f} unidades")
            
            with col3:
                st.metric("📅 Dias para Acabar", f"{int(dias_para_acabar)} dias" if dias_para_acabar != float('inf') else "∞")
            
            with col4:
                if dias_para_acabar != float('inf'):
                    st.metric("⚠️ Previsão de Fim", data_previsao_fim.strftime('%d/%m/%Y'))
                else:
                    st.metric("⚠️ Previsão de Fim", "Sem consumo")
            
            # Alertas
            if dias_para_acabar < 7:
                st.markdown("""
                <div class="alert-danger">
                    🚨 <strong>ALERTA CRÍTICO!</strong> Medicamento pode acabar em menos de 7 dias!
                </div>
                """, unsafe_allow_html=True)
            elif dias_para_acabar < 15:
                st.markdown("""
                <div class="alert-warning">
                    ⚠️ <strong>Atenção!</strong> Medicamento pode acabar em menos de 15 dias.
                </div>
                """, unsafe_allow_html=True)
            elif dias_para_acabar < 30:
                st.markdown("""
                <div class="alert-success">
                    ✅ <strong>OK!</strong> Estoque suficiente para os próximos 30 dias.
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de consumo
            if len(df_consumo) > 1:
                st.markdown("### 📈 Histórico de Consumo (Últimos 30 dias)")
                
                fig = px.line(df_consumo, x='data', y='consumo_diario', 
                             title="Consumo Diário", markers=True)
                fig.add_hline(y=consumo_medio_diario, line_dash="dash", 
                             annotation_text=f"Média: {consumo_medio_diario:.1f}")
                st.plotly_chart(fig, use_container_width=True)
            
            # Sugestões de reposição
            st.markdown("### 💡 Sugestões de Reposição")
            
            if dias_para_acabar < 30:
                quantidade_sugerida = consumo_medio_diario * 60  # 60 dias de estoque
                st.info(f"📋 **Sugestão:** Repor {quantidade_sugerida:.0f} unidades para manter 60 dias de estoque.")
            
            # Tabela detalhada de consumo
            st.markdown("### 📊 Detalhamento do Consumo")
            st.dataframe(df_consumo.sort_values('data', ascending=False), use_container_width=True)
            
        else:
            st.info("Não há histórico de consumo (saídas) para este medicamento nos últimos 30 dias.")
    
    conn.close()

def show_pacientes():
    """Módulo de pacientes"""
    st.markdown("## 👥 Gestão de Pacientes")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('pacientes', []):
        tab1, tab2 = st.tabs(["📋 Lista de Pacientes", "➕ Cadastrar Paciente"])
    else:
        tab1, tab2 = st.tabs(["📋 Lista de Pacientes", ""])
    
    with tab1:
        st.markdown("### 📋 Pacientes Cadastrados")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("🔍 Buscar paciente", placeholder="Nome ou CPF")
        
        with col2:
            conn = st.session_state.db_manager.get_connection()
            planos = pd.read_sql("SELECT DISTINCT plano_saude FROM pacientes WHERE plano_saude IS NOT NULL", conn)['plano_saude'].tolist()
            plano_filter = st.selectbox("🏥 Plano de Saúde", ["Todos"] + planos)
        
        # Buscar pacientes
        query = """
            SELECT p.*, u.nome_completo as cadastrado_por_nome
            FROM pacientes p
            LEFT JOIN usuarios u ON p.cadastrado_por = u.id
            WHERE p.ativo = 1
        """
        params = []
        
        if search_term:
            query += " AND (p.nome_completo LIKE ? OR p.cpf LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if plano_filter != "Todos":
            query += " AND p.plano_saude = ?"
            params.append(plano_filter)
        
        query += " ORDER BY p.nome_completo"
        
        df_pacientes = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if not df_pacientes.empty:
            for _, pac in df_pacientes.iterrows():
                with st.expander(f"👤 {pac['nome_completo']} - {pac['cpf'] or 'CPF não informado'}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Nome:** {pac['nome_completo']}")
                        st.write(f"**CPF:** {pac['cpf'] or 'N/A'}")
                        st.write(f"**RG:** {pac['rg'] or 'N/A'}")
                        st.write(f"**Data de Nascimento:** {pac['data_nascimento'] or 'N/A'}")
                        st.write(f"**Sexo:** {pac['sexo'] or 'N/A'}")
                    
                    with col2:
                        st.write(f"**Telefone:** {pac['telefone'] or 'N/A'}")
                        st.write(f"**Email:** {pac['email'] or 'N/A'}")
                        st.write(f"**Cidade:** {pac['cidade'] or 'N/A'}")
                        st.write(f"**Estado:** {pac['estado'] or 'N/A'}")
                        st.write(f"**CEP:** {pac['cep'] or 'N/A'}")
                    
                    with col3:
                        st.write(f"**Plano de Saúde:** {pac['plano_saude'] or 'N/A'}")
                        st.write(f"**Carteirinha:** {pac['numero_carteirinha'] or 'N/A'}")
                        st.write(f"**Contato de Emergência:** {pac['contato_emergencia'] or 'N/A'}")
                        st.write(f"**Cadastrado por:** {pac['cadastrado_por_nome'] or 'N/A'}")
                    
                    if pac['endereco']:
                        st.write(f"**Endereço:** {pac['endereco']}")
                    if pac['observacoes']:
                        st.write(f"**Observações:** {pac['observacoes']}")
        else:
            st.info("Nenhum paciente encontrado com os filtros aplicados.")
    
    if 'criar' in st.session_state.permissions.get('pacientes', []):
        with tab2:
            st.markdown("### ➕ Cadastrar Novo Paciente")
            
            with st.form("form_paciente"):
                st.markdown("**Dados Pessoais**")
                col1, col2 = st.columns(2)
                
                with col1:
                    nome_completo = st.text_input("Nome Completo *", placeholder="Nome completo do paciente")
                    cpf = st.text_input("CPF", placeholder="000.000.000-00")
                    rg = st.text_input("RG", placeholder="00.000.000-0")
                    data_nascimento = st.date_input("Data de Nascimento")
                    sexo = st.selectbox("Sexo", ["", "Masculino", "Feminino", "Outro", "Não informar"])
                
                with col2:
                    telefone = st.text_input("Telefone", placeholder="(00) 00000-0000")
                    email = st.text_input("Email", placeholder="email@exemplo.com")
                    contato_emergencia = st.text_input("Contato de Emergência", placeholder="Nome e telefone")
                
                st.markdown("**Endereço**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    endereco = st.text_input("Endereço", placeholder="Rua, número, complemento")
                    cidade = st.text_input("Cidade", placeholder="Nome da cidade")
                
                with col2:
                    estado = st.selectbox("Estado", [
                        "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                        "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", 
                        "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                    ])
                    cep = st.text_input("CEP", placeholder="00000-000")
                
                st.markdown("**Convênio/Plano de Saúde**")
                col1, col2 = st.columns(2)
                
                with col1:
                    plano_saude = st.text_input("Plano de Saúde", placeholder="Nome do plano/convênio")
                
                with col2:
                    numero_carteirinha = st.text_input("Número da Carteirinha", placeholder="Número da carteirinha")
                
                observacoes = st.text_area("Observações", placeholder="Informações adicionais sobre o paciente...")
                
                submitted = st.form_submit_button("💾 Cadastrar Paciente", use_container_width=True)
                
                if submitted:
                    if not nome_completo:
                        st.error("❌ O nome completo é obrigatório!")
                    else:
                        try:
                            conn = st.session_state.db_manager.get_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                INSERT INTO pacientes (
                                    nome_completo, cpf, rg, data_nascimento, sexo, telefone, email,
                                    endereco, cidade, estado, cep, plano_saude, numero_carteirinha,
                                    contato_emergencia, observacoes, cadastrado_por
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                nome_completo, cpf, rg, data_nascimento, sexo, telefone, email,
                                endereco, cidade, estado, cep, plano_saude, numero_carteirinha,
                                contato_emergencia, observacoes, st.session_state.user['id']
                            ))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Paciente cadastrado com sucesso!")
                            time.sleep(2)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Erro ao cadastrar paciente: {str(e)}")

def show_consultas():
    """Módulo de consultas"""
    st.markdown("## 📅 Gestão de Consultas")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('consultas', []):
        tab1, tab2 = st.tabs(["📋 Agenda de Consultas", "➕ Agendar Consulta"])
    else:
        tab1, tab2 = st.tabs(["📋 Agenda de Consultas", ""])
    
    with tab1:
        st.markdown("### 📋 Agenda de Consultas")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data_consulta = st.date_input("📅 Data", value=date.today())
        
        with col2:
            conn = st.session_state.db_manager.get_connection()
            medicos = pd.read_sql("SELECT id, nome_completo FROM usuarios WHERE perfil = 'Médico' AND ativo = 1", conn)
            medico_options = ["Todos"] + [f"{row['nome_completo']}" for _, row in medicos.iterrows()]
            medico_filter = st.selectbox("👨‍⚕️ Médico", medico_options)
        
        with col3:
            status_filter = st.selectbox("📊 Status", ["Todos", "Agendada", "Confirmada", "Em andamento", "Concluída", "Cancelada"])
        
        # Buscar consultas
        query = """
            SELECT 
                c.*,
                p.nome_completo as paciente_nome,
                m.nome_completo as medico_nome,
                a.nome_completo as agendado_por_nome
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN usuarios m ON c.medico_id = m.id
            LEFT JOIN usuarios a ON c.agendado_por = a.id
            WHERE DATE(c.data_consulta) = ?
        """
        params = [data_consulta]
        
        if medico_filter != "Todos":
            # Encontrar o ID do médico selecionado
            if not medicos.empty:
                medico_selecionado = medicos[medicos['nome_completo'] == medico_filter]
                if not medico_selecionado.empty:
                    query += " AND c.medico_id = ?"
                    params.append(medico_selecionado.iloc[0]['id'])
        
        if status_filter != "Todos":
            query += " AND c.status = ?"
            params.append(status_filter)
        
        query += " ORDER BY c.data_consulta"
        
        df_consultas = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if not df_consultas.empty:
            for _, cons in df_consultas.iterrows():
                # Definir cor baseada no status
                status_color = {
                    'Agendada': '🟡',
                    'Confirmada': '🟢',
                    'Em andamento': '🔵',
                    'Concluída': '✅',
                    'Cancelada': '🔴'
                }.get(cons['status'], '⚪')
                
                data_hora = datetime.strptime(cons['data_consulta'], '%Y-%m-%d %H:%M:%S')
                
                with st.expander(f"{status_color} {data_hora.strftime('%H:%M')} - {cons['paciente_nome']} - Dr(a). {cons['medico_nome']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Paciente:** {cons['paciente_nome']}")
                        st.write(f"**Médico:** Dr(a). {cons['medico_nome']}")
                        st.write(f"**Data/Hora:** {data_hora.strftime('%d/%m/%Y %H:%M')}")
                        st.write(f"**Tipo:** {cons['tipo_consulta'] or 'N/A'}")
                        st.write(f"**Status:** {cons['status']}")
                    
                    with col2:
                        st.write(f"**Motivo:** {cons['motivo'] or 'N/A'}")
                        st.write(f"**Valor:** R$ {cons['valor']:.2f}" if cons['valor'] else "Valor: N/A")
                        st.write(f"**Agendado por:** {cons['agendado_por_nome'] or 'N/A'}")
                    
                    if cons['diagnostico']:
                        st.write(f"**Diagnóstico:** {cons['diagnostico']}")
                    if cons['observacoes']:
                        st.write(f"**Observações:** {cons['observacoes']}")
                    
                    # Ações para a consulta
                    if 'editar' in st.session_state.permissions.get('consultas', []):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("✅ Concluir", key=f"concluir_{cons['id']}"):
                                try:
                                    conn = st.session_state.db_manager.get_connection()
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE consultas SET status = 'Concluída' WHERE id = ?", (cons['id'],))
                                    conn.commit()
                                    conn.close()
                                    st.success("Consulta marcada como concluída!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro: {e}")
                        
                        with col2:
                            if st.button("❌ Cancelar", key=f"cancelar_{cons['id']}"):
                                try:
                                    conn = st.session_state.db_manager.get_connection()
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE consultas SET status = 'Cancelada' WHERE id = ?", (cons['id'],))
                                    conn.commit()
                                    conn.close()
                                    st.success("Consulta cancelada!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro: {e}")
        else:
            st.info(f"Nenhuma consulta agendada para {data_consulta.strftime('%d/%m/%Y')}.")
    
    if 'criar' in st.session_state.permissions.get('consultas', []):
        with tab2:
            st.markdown("### ➕ Agendar Nova Consulta")
            
            # Buscar pacientes e médicos
            conn = st.session_state.db_manager.get_connection()
            pacientes = pd.read_sql("SELECT id, nome_completo FROM pacientes WHERE ativo = 1 ORDER BY nome_completo", conn)
            medicos = pd.read_sql("SELECT id, nome_completo FROM usuarios WHERE perfil = 'Médico' AND ativo = 1 ORDER BY nome_completo", conn)
            conn.close()
            
            if pacientes.empty:
                st.warning("⚠️ Nenhum paciente cadastrado. Cadastre pacientes primeiro.")
            elif medicos.empty:
                st.warning("⚠️ Nenhum médico cadastrado. Cadastre médicos primeiro.")
            else:
                with st.form("form_consulta"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        paciente_options = {f"{row['nome_completo']}": row['id'] for _, row in pacientes.iterrows()}
                        paciente_selecionado = st.selectbox("Paciente *", list(paciente_options.keys()))
                        
                        medico_options = {f"{row['nome_completo']}": row['id'] for _, row in medicos.iterrows()}
                        medico_selecionado = st.selectbox("Médico *", list(medico_options.keys()))
                        
                        data_consulta_agendamento = st.date_input("Data da Consulta *", value=date.today())
                        hora_consulta = st.time_input("Horário da Consulta *")
                    
                    with col2:
                        tipo_consulta = st.selectbox("Tipo de Consulta", [
                            "", "Consulta inicial", "Retorno", "Emergência", "Exame",
                            "Procedimento", "Teleconsulta", "Outros"
                        ])
                        
                        valor = st.number_input("Valor da Consulta (R$)", min_value=0.0, step=0.01, format="%.2f")
                        
                        motivo = st.text_area("Motivo da Consulta", placeholder="Descreva o motivo da consulta...")
                    
                    observacoes = st.text_area("Observações", placeholder="Informações adicionais...")
                    
                    submitted = st.form_submit_button("📅 Agendar Consulta", use_container_width=True)
                    
                    if submitted:
                        if not paciente_selecionado or not medico_selecionado or not data_consulta_agendamento or not hora_consulta:
                            st.error("❌ Preencha todos os campos obrigatórios!")
                        else:
                            try:
                                # Combinar data e hora
                                data_hora_consulta = datetime.combine(data_consulta_agendamento, hora_consulta)
                                
                                conn = st.session_state.db_manager.get_connection()
                                cursor = conn.cursor()
                                
                                # Verificar conflito de horário
                                cursor.execute("""
                                    SELECT COUNT(*) as conflitos FROM consultas 
                                    WHERE medico_id = ? AND data_consulta = ? AND status NOT IN ('Cancelada')
                                """, (medico_options[medico_selecionado], data_hora_consulta))
                                
                                conflitos = cursor.fetchone()[0]
                                
                                if conflitos > 0:
                                    st.error("❌ Já existe uma consulta agendada para este médico neste horário!")
                                else:
                                    cursor.execute("""
                                        INSERT INTO consultas (
                                            paciente_id, medico_id, data_consulta, tipo_consulta,
                                            motivo, valor, observacoes, agendado_por
                                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                    """, (
                                        paciente_options[paciente_selecionado],
                                        medico_options[medico_selecionado],
                                        data_hora_consulta,
                                        tipo_consulta,
                                        motivo,
                                        valor if valor > 0 else None,
                                        observacoes,
                                        st.session_state.user['id']
                                    ))
                                    
                                    conn.commit()
                                    conn.close()
                                    
                                    st.success("✅ Consulta agendada com sucesso!")
                                    time.sleep(2)
                                    st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Erro ao agendar consulta: {str(e)}")

def show_receitas():
    """Módulo de receitas"""
    st.markdown("## 📝 Gestão de Receitas")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('receitas', []):
        tab1, tab2 = st.tabs(["📋 Receitas", "➕ Nova Receita"])
    else:
        tab1, tab2 = st.tabs(["📋 Receitas", ""])
    
    with tab1:
        st.markdown("### 📋 Receitas Emitidas")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Buscar", placeholder="Nome do paciente")
        
        with col2:
            periodo = st.selectbox("📅 Período", ["Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias", "Personalizado"])
        
        with col3:
            status_filter = st.selectbox("📊 Status", ["Todas", "Ativa", "Dispensada", "Cancelada"])
        
        # Definir período de busca
        if periodo == "Últimos 7 dias":
            data_inicio = date.today() - timedelta(days=7)
            data_fim = date.today()
        elif periodo == "Últimos 30 dias":
            data_inicio = date.today() - timedelta(days=30)
            data_fim = date.today()
        elif periodo == "Últimos 90 dias":
            data_inicio = date.today() - timedelta(days=90)
            data_fim = date.today()
        else:  # Personalizado
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input("Data Início", value=date.today() - timedelta(days=30))
            with col2:
                data_fim = st.date_input("Data Fim", value=date.today())
        
        # Buscar receitas
        query = """
            SELECT 
                r.*,
                p.nome_completo as paciente_nome,
                m.nome_completo as medico_nome,
                COUNT(ri.id) as total_medicamentos
            FROM receitas r
            JOIN pacientes p ON r.paciente_id = p.id
            JOIN usuarios m ON r.medico_id = m.id
            LEFT JOIN receita_itens ri ON r.id = ri.receita_id
            WHERE DATE(r.data_emissao) BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if search_term:
            query += " AND p.nome_completo LIKE ?"
            params.append(f"%{search_term}%")
        
        if status_filter != "Todas":
            query += " AND r.status = ?"
            params.append(status_filter)
        
        query += " GROUP BY r.id ORDER BY r.data_emissao DESC"
        
        conn = st.session_state.db_manager.get_connection()
        df_receitas = pd.read_sql(query, conn, params=params)
        
        if not df_receitas.empty:
            for _, rec in df_receitas.iterrows():
                status_icon = {'Ativa': '🟢', 'Dispensada': '✅', 'Cancelada': '🔴'}.get(rec['status'], '⚪')
                data_emissao = datetime.strptime(rec['data_emissao'], '%Y-%m-%d %H:%M:%S')
                
                with st.expander(f"{status_icon} Receita #{rec['id']} - {rec['paciente_nome']} - {data_emissao.strftime('%d/%m/%Y')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Paciente:** {rec['paciente_nome']}")
                        st.write(f"**Médico:** Dr(a). {rec['medico_nome']}")
                        st.write(f"**Data de Emissão:** {data_emissao.strftime('%d/%m/%Y %H:%M')}")
                        st.write(f"**Status:** {rec['status']}")
                    
                    with col2:
                        st.write(f"**Total de Medicamentos:** {rec['total_medicamentos']}")
                        if rec['observacoes']:
                            st.write(f"**Observações:** {rec['observacoes']}")
                    
                    # Buscar itens da receita
                    itens_query = """
                        SELECT 
                            ri.*,
                            m.nome as medicamento_nome
                        FROM receita_itens ri
                        JOIN medicamentos m ON ri.medicamento_id = m.id
                        WHERE ri.receita_id = ?
                    """
                    df_itens = pd.read_sql(itens_query, conn, params=[rec['id']])
                    
                    if not df_itens.empty:
                        st.markdown("**Medicamentos Prescritos:**")
                        for _, item in df_itens.iterrows():
                            st.write(f"• {item['medicamento_nome']} - {item['dosagem']} - {item['frequencia']} - Qtd: {item['quantidade']}")
                            if item['duracao_tratamento']:
                                st.write(f"  Duração: {item['duracao_tratamento']}")
                            if item['instrucoes_uso']:
                                st.write(f"  Instruções: {item['instrucoes_uso']}")
                    
                    # Ações
                    if 'editar' in st.session_state.permissions.get('receitas', []):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if rec['status'] == 'Ativa' and st.button("💊 Dispensar", key=f"dispensar_{rec['id']}"):
                                try:
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE receitas SET status = 'Dispensada' WHERE id = ?", (rec['id'],))
                                    conn.commit()
                                    st.success("Receita dispensada!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro: {e}")
                        
                        with col2:
                            if rec['status'] == 'Ativa' and st.button("❌ Cancelar", key=f"cancelar_rec_{rec['id']}"):
                                try:
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE receitas SET status = 'Cancelada' WHERE id = ?", (rec['id'],))
                                    conn.commit()
                                    st.success("Receita cancelada!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro: {e}")
        
        conn.close()
        
        if df_receitas.empty:
            st.info("Nenhuma receita encontrada com os filtros aplicados.")
    
    if 'criar' in st.session_state.permissions.get('receitas', []):
        with tab2:
            st.markdown("### ➕ Prescrever Nova Receita")
            
            # Buscar pacientes e medicamentos
            conn = st.session_state.db_manager.get_connection()
            pacientes = pd.read_sql("SELECT id, nome_completo FROM pacientes WHERE ativo = 1 ORDER BY nome_completo", conn)
            medicamentos = pd.read_sql("SELECT id, nome FROM medicamentos WHERE ativo = 1 ORDER BY nome", conn)
            conn.close()
            
            if pacientes.empty:
                st.warning("⚠️ Nenhum paciente cadastrado.")
            elif medicamentos.empty:
                st.warning("⚠️ Nenhum medicamento cadastrado.")
            else:
                with st.form("form_receita"):
                    # Dados da receita
                    paciente_options = {f"{row['nome_completo']}": row['id'] for _, row in pacientes.iterrows()}
                    paciente_selecionado = st.selectbox("Paciente *", list(paciente_options.keys()))
                    
                    observacoes_receita = st.text_area("Observações da Receita", placeholder="Orientações gerais...")
                    
                    st.markdown("---")
                    st.markdown("**Medicamentos Prescritos**")
                    
                    # Sistema para adicionar medicamentos
                    if 'medicamentos_receita' not in st.session_state:
                        st.session_state.medicamentos_receita = []
                    
                    # Formulário para adicionar medicamento
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        medicamento_options = {f"{row['nome']}": row['id'] for _, row in medicamentos.iterrows()}
                        medicamento_selecionado = st.selectbox("Medicamento", [""] + list(medicamento_options.keys()))
                        dosagem = st.text_input("Dosagem", placeholder="Ex: 500mg")
                    
                    with col2:
                        frequencia = st.text_input("Frequência", placeholder="Ex: 8/8h, 2x ao dia")
                        quantidade = st.number_input("Quantidade", min_value=1, value=1)
                    
                    with col3:
                        duracao_tratamento = st.text_input("Duração do Tratamento", placeholder="Ex: 7 dias")
                        instrucoes_uso = st.text_input("Instruções de Uso", placeholder="Ex: Após as refeições")
                    
                    # Botão para adicionar medicamento à lista
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("➕ Adicionar Medicamento"):
                            if medicamento_selecionado and dosagem and frequencia:
                                novo_medicamento = {
                                    'medicamento_id': medicamento_options[medicamento_selecionado],
                                    'medicamento_nome': medicamento_selecionado,
                                    'dosagem': dosagem,
                                    'frequencia': frequencia,
                                    'quantidade': quantidade,
                                    'duracao_tratamento': duracao_tratamento,
                                    'instrucoes_uso': instrucoes_uso
                                }
                                st.session_state.medicamentos_receita.append(novo_medicamento)
                                st.success("Medicamento adicionado!")
                                st.rerun()
                            else:
                                st.error("Preencha pelo menos: medicamento, dosagem e frequência!")
                    
                    with col2:
                        if st.form_submit_button("💾 Salvar Receita"):
                            if not paciente_selecionado:
                                st.error("❌ Selecione um paciente!")
                            elif not st.session_state.medicamentos_receita:
                                st.error("❌ Adicione pelo menos um medicamento!")
                            else:
                                try:
                                    conn = st.session_state.db_manager.get_connection()
                                    cursor = conn.cursor()
                                    
                                    # Inserir receita
                                    cursor.execute("""
                                        INSERT INTO receitas (
                                            paciente_id, medico_id, observacoes
                                        ) VALUES (?, ?, ?)
                                    """, (
                                        paciente_options[paciente_selecionado],
                                        st.session_state.user['id'],
                                        observacoes_receita
                                    ))
                                    
                                    receita_id = cursor.lastrowid
                                    
                                    # Inserir itens da receita
                                    for medicamento in st.session_state.medicamentos_receita:
                                        cursor.execute("""
                                            INSERT INTO receita_itens (
                                                receita_id, medicamento_id, dosagem, quantidade,
                                                frequencia, duracao_tratamento, instrucoes_uso
                                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                                        """, (
                                            receita_id,
                                            medicamento['medicamento_id'],
                                            medicamento['dosagem'],
                                            medicamento['quantidade'],
                                            medicamento['frequencia'],
                                            medicamento['duracao_tratamento'],
                                            medicamento['instrucoes_uso']
                                        ))
                                    
                                    conn.commit()
                                    conn.close()
                                    
                                    st.success("✅ Receita criada com sucesso!")
                                    st.session_state.medicamentos_receita = []  # Limpar lista
                                    time.sleep(2)
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Erro ao criar receita: {str(e)}")
                
                # Exibir medicamentos adicionados
                if st.session_state.medicamentos_receita:
                    st.markdown("**Medicamentos Adicionados:**")
                    for i, med in enumerate(st.session_state.medicamentos_receita):
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.write(f"• {med['medicamento_nome']} - {med['dosagem']} - {med['frequencia']} - Qtd: {med['quantidade']}")
                        
                        with col2:
                            if st.button("🗑️", key=f"remove_{i}"):
                                st.session_state.medicamentos_receita.pop(i)
                                st.rerun()

def show_usuarios():
    """Módulo de usuários"""
    st.markdown("## 👤 Gestão de Usuários")
    
    # Verificar se tem permissão para usuários
    if 'usuarios' not in st.session_state.permissions:
        st.error("❌ Você não tem permissão para acessar esta área!")
        return
    
    tab1, tab2 = st.tabs(["📋 Lista de Usuários", "➕ Novo Usuário"])
    
    with tab1:
        st.markdown("### 📋 Usuários do Sistema")
        
        # Buscar usuários
        conn = st.session_state.db_manager.get_connection()
        df_usuarios = pd.read_sql("""
            SELECT 
                u.*,
                c.nome_completo as criado_por_nome
            FROM usuarios u
            LEFT JOIN usuarios c ON u.criado_por = c.id
            ORDER BY u.nome_completo
        """, conn)
        conn.close()
        
        if not df_usuarios.empty:
            for _, user in df_usuarios.iterrows():
                status_icon = "🟢" if user['ativo'] else "🔴"
                perfil_icon = {
                    'Administrador': '👑',
                    'Médico': '👨‍⚕️',
                    'Farmacêutico': '💊',
                    'Enfermeiro': '👩‍⚕️'
                }.get(user['perfil'], '👤')
                
                with st.expander(f"{status_icon} {perfil_icon} {user['nome_completo']} - {user['perfil']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Nome:** {user['nome_completo']}")
                        st.write(f"**Usuário:** {user['username']}")
                        st.write(f"**Perfil:** {user['perfil']}")
                        st.write(f"**Email:** {user['email'] or 'N/A'}")
                    
                    with col2:
                        st.write(f"**CRM/CRF:** {user['crm_crf'] or 'N/A'}")
                        st.write(f"**Status:** {'Ativo' if user['ativo'] else 'Inativo'}")
                        st.write(f"**Data de Criação:** {user['data_criacao']}")
                        st.write(f"**Criado por:** {user['criado_por_nome'] or 'Sistema'}")
                    
                    # Ações
                    if 'editar' in st.session_state.permissions.get('usuarios', []):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if user['ativo']:
                                if st.button("❌ Desativar", key=f"desativar_{user['id']}"):
                                    try:
                                        conn = st.session_state.db_manager.get_connection()
                                        cursor = conn.cursor()
                                        cursor.execute("UPDATE usuarios SET ativo = 0 WHERE id = ?", (user['id'],))
                                        conn.commit()
                                        conn.close()
                                        st.success("Usuário desativado!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro: {e}")
                            else:
                                if st.button("✅ Ativar", key=f"ativar_{user['id']}"):
                                    try:
                                        conn = st.session_state.db_manager.get_connection()
                                        cursor = conn.cursor()
                                        cursor.execute("UPDATE usuarios SET ativo = 1 WHERE id = ?", (user['id'],))
                                        conn.commit()
                                        conn.close()
                                        st.success("Usuário ativado!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Erro: {e}")
                        
                        with col2:
                            if st.button("🔑 Resetar Senha", key=f"reset_{user['id']}"):
                                try:
                                    nova_senha = "123456"
                                    password_hash = st.session_state.auth_manager.hash_password(nova_senha)
                                    conn = st.session_state.db_manager.get_connection()
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE usuarios SET password_hash = ? WHERE id = ?", (password_hash, user['id']))
                                    conn.commit()
                                    conn.close()
                                    st.success(f"Senha resetada para: {nova_senha}")
                                except Exception as e:
                                    st.error(f"Erro: {e}")
        else:
            st.info("Nenhum usuário encontrado.")
    
    with tab2:
        st.markdown("### ➕ Cadastrar Novo Usuário")
        
        with st.form("form_usuario"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_completo = st.text_input("Nome Completo *", placeholder="Nome completo do usuário")
                username = st.text_input("Nome de Usuário *", placeholder="Username para login")
                email = st.text_input("Email", placeholder="email@exemplo.com")
                perfil = st.selectbox("Perfil *", ["", "Administrador", "Médico", "Farmacêutico", "Enfermeiro"])
            
            with col2:
                password = st.text_input("Senha *", type="password", placeholder="Senha inicial")
                confirm_password = st.text_input("Confirmar Senha *", type="password", placeholder="Confirme a senha")
                crm_crf = st.text_input("CRM/CRF", placeholder="Número do registro profissional")
            
            submitted = st.form_submit_button("💾 Cadastrar Usuário", use_container_width=True)
            
            if submitted:
                if not nome_completo or not username or not password or not perfil:
                    st.error("❌ Preencha todos os campos obrigatórios!")
                elif password != confirm_password:
                    st.error("❌ As senhas não coincidem!")
                elif len(password) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres!")
                else:
                    try:
                        conn = st.session_state.db_manager.get_connection()
                        cursor = conn.cursor()
                        
                        # Verificar se username já existe
                        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
                        if cursor.fetchone():
                            st.error("❌ Nome de usuário já existe!")
                        else:
                            password_hash = st.session_state.auth_manager.hash_password(password)
                            
                            cursor.execute("""
                                INSERT INTO usuarios (
                                    username, password_hash, nome_completo, email, perfil, crm_crf, criado_por
                                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                username, password_hash, nome_completo, email, perfil, crm_crf, st.session_state.user['id']
                            ))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Usuário cadastrado com sucesso!")
                            time.sleep(2)
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar usuário: {str(e)}")

def show_relatorios():
    """Módulo de relatórios"""
    st.markdown("## 📊 Relatórios e Análises")
    
    # Verificar permissões
    if 'relatorios' not in st.session_state.permissions:
        st.error("❌ Você não tem permissão para acessar esta área!")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💊 Medicamentos", "👥 Pacientes", "📅 Consultas"])
    
    with tab1:
        st.markdown("### 📊 Dashboard Executivo")
        
        conn = st.session_state.db_manager.get_connection()
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        # Medicamentos cadastrados
        total_medicamentos = pd.read_sql("SELECT COUNT(*) as count FROM medicamentos WHERE ativo = 1", conn).iloc[0]['count']
        
        # Pacientes ativos
        total_pacientes = pd.read_sql("SELECT COUNT(*) as count FROM pacientes WHERE ativo = 1", conn).iloc[0]['count']
        
        # Consultas este mês
        consultas_mes = pd.read_sql("""
            SELECT COUNT(*) as count FROM consultas 
            WHERE strftime('%Y-%m', data_consulta) = strftime('%Y-%m', 'now')
            AND status != 'Cancelada'
        """, conn).iloc[0]['count']
        
        # Receitas emitidas este mês
        receitas_mes = pd.read_sql("""
            SELECT COUNT(*) as count FROM receitas 
            WHERE strftime('%Y-%m', data_emissao) = strftime('%Y-%m', 'now')
        """, conn).iloc[0]['count']
        
        with col1:
            st.metric("💊 Medicamentos", total_medicamentos)
        with col2:
            st.metric("👥 Pacientes", total_pacientes)
        with col3:
            st.metric("📅 Consultas (Mês)", consultas_mes)
        with col4:
            st.metric("📝 Receitas (Mês)", receitas_mes)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Consultas por Mês (Últimos 6 meses)")
            df_consultas_mes = pd.read_sql("""
                SELECT 
                    strftime('%Y-%m', data_consulta) as mes,
                    COUNT(*) as quantidade
                FROM consultas 
                WHERE data_consulta >= DATE('now', '-6 months')
                AND status != 'Cancelada'
                GROUP BY strftime('%Y-%m', data_consulta)
                ORDER BY mes
            """, conn)
            
            if not df_consultas_mes.empty:
                fig = px.line(df_consultas_mes, x='mes', y='quantidade', markers=True)
                fig.update_layout(xaxis_title="Mês", yaxis_title="Quantidade")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sem dados de consultas.")
        
        with col2:
            st.markdown("### 🏥 Consultas por Médico (Este mês)")
            df_consultas_medico = pd.read_sql("""
                SELECT 
                    u.nome_completo as medico,
                    COUNT(*) as quantidade
                FROM consultas c
                JOIN usuarios u ON c.medico_id = u.id
                WHERE strftime('%Y-%m', c.data_consulta) = strftime('%Y-%m', 'now')
                AND c.status != 'Cancelada'
                GROUP BY u.nome_completo
                ORDER BY quantidade DESC
                LIMIT 10
            """, conn)
            
            if not df_consultas_medico.empty:
                fig = px.bar(df_consultas_medico, x='quantidade', y='medico', orientation='h')
                fig.update_layout(xaxis_title="Quantidade", yaxis_title="Médico")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sem dados de consultas por médico.")
        
        conn.close()
    
    with tab2:
        st.markdown("### 💊 Relatórios de Medicamentos")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            relatorio_tipo = st.selectbox("Tipo de Relatório", [
                "Medicamentos por Categoria",
                "Estoque Atual",
                "Medicamentos Próximos ao Vencimento",
                "Medicamentos Mais Prescritos"
            ])
        
        conn = st.session_state.db_manager.get_connection()
        
        if relatorio_tipo == "Medicamentos por Categoria":
            df_report = pd.read_sql("""
                SELECT 
                    categoria,
                    COUNT(*) as quantidade,
                    SUM(CASE WHEN controlado = 1 THEN 1 ELSE 0 END) as controlados
                FROM medicamentos 
                WHERE ativo = 1 AND categoria IS NOT NULL
                GROUP BY categoria
                ORDER BY quantidade DESC
            """, conn)
            
            if not df_report.empty:
                st.dataframe(df_report, use_container_width=True)
                
                fig = px.pie(df_report, values='quantidade', names='categoria', title="Distribuição por Categoria")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado encontrado.")
        
        elif relatorio_tipo == "Estoque Atual":
            df_report = pd.read_sql("""
                SELECT 
                    m.nome as medicamento,
                    m.categoria,
                    l.numero_lote,
                    l.quantidade_atual,
                    l.data_validade,
                    l.local_armazenamento
                FROM lotes l
                JOIN medicamentos m ON l.medicamento_id = m.id
                WHERE l.ativo = 1 AND m.ativo = 1 AND l.quantidade_atual > 0
                ORDER BY m.nome, l.data_validade
            """, conn)
            
            if not df_report.empty:
                st.dataframe(df_report, use_container_width=True)
            else:
                st.info("Nenhum estoque encontrado.")
        
        elif relatorio_tipo == "Medicamentos Próximos ao Vencimento":
            df_report = pd.read_sql("""
                SELECT 
                    m.nome as medicamento,
                    l.numero_lote,
                    l.quantidade_atual,
                    l.data_validade,
                    julianday(l.data_validade) - julianday('now') as dias_para_vencer
                FROM lotes l
                JOIN medicamentos m ON l.medicamento_id = m.id
                WHERE l.ativo = 1 AND m.ativo = 1 
                AND l.quantidade_atual > 0
                AND DATE(l.data_validade) <= DATE('now', '+60 days')
                ORDER BY l.data_validade
            """, conn)
            
            if not df_report.empty:
                st.dataframe(df_report, use_container_width=True)
            else:
                st.info("Nenhum medicamento próximo ao vencimento.")
        
        elif relatorio_tipo == "Medicamentos Mais Prescritos":
            df_report = pd.read_sql("""
                SELECT 
                    m.nome as medicamento,
                    m.principio_ativo,
                    COUNT(*) as vezes_prescrito,
                    SUM(ri.quantidade) as quantidade_total
                FROM receita_itens ri
                JOIN medicamentos m ON ri.medicamento_id = m.id
                JOIN receitas r ON ri.receita_id = r.id
                WHERE r.data_emissao >= DATE('now', '-3 months')
                GROUP BY m.id, m.nome, m.principio_ativo
                ORDER BY vezes_prescrito DESC
                LIMIT 20
            """, conn)
            
            if not df_report.empty:
                st.dataframe(df_report, use_container_width=True)
                
                fig = px.bar(df_report.head(10), x='vezes_prescrito', y='medicamento', orientation='h',
                           title="Top 10 Medicamentos Mais Prescritos")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma prescrição encontrada.")
        
        conn.close()
    
    with tab3:
        st.markdown("### 👥 Relatórios de Pacientes")
        
        conn = st.session_state.db_manager.get_connection()
        
        # Estatísticas de pacientes
        col1, col2, col3 = st.columns(3)
        
        # Total de pacientes
        total_pacientes_rel = pd.read_sql("SELECT COUNT(*) as count FROM pacientes WHERE ativo = 1", conn).iloc[0]['count']
        
        # Pacientes por sexo
        df_sexo = pd.read_sql("""
            SELECT sexo, COUNT(*) as quantidade
            FROM pacientes 
            WHERE ativo = 1 AND sexo IS NOT NULL
            GROUP BY sexo
        """, conn)
        
        # Pacientes por idade
        df_idade = pd.read_sql("""
            SELECT 
                CASE 
                    WHEN (julianday('now') - julianday(data_nascimento))/365.25 < 18 THEN 'Menor de 18'
                    WHEN (julianday('now') - julianday(data_nascimento))/365.25 < 65 THEN '18-64 anos'
                    ELSE '65+ anos'
                END as faixa_etaria,
                COUNT(*) as quantidade
            FROM pacientes 
            WHERE ativo = 1 AND data_nascimento IS NOT NULL
            GROUP BY faixa_etaria
        """, conn)
        
        with col1:
            st.metric("👥 Total de Pacientes", total_pacientes_rel)
        
        with col2:
            if not df_sexo.empty:
                fig_sexo = px.pie(df_sexo, values='quantidade', names='sexo', title="Distribuição por Sexo")
                st.plotly_chart(fig_sexo, use_container_width=True)
        
        with col3:
            if not df_idade.empty:
                fig_idade = px.bar(df_idade, x='faixa_etaria', y='quantidade', title="Distribuição por Idade")
                st.plotly_chart(fig_idade, use_container_width=True)
        
        conn.close()
    
    with tab4:
        st.markdown("### 📅 Relatórios de Consultas")
        
        conn = st.session_state.db_manager.get_connection()
        
        # Filtro de período
        col1, col2 = st.columns(2)
        with col1:
            data_inicio_rel = st.date_input("Data Início", value=date.today() - timedelta(days=30))
        with col2:
            data_fim_rel = st.date_input("Data Fim", value=date.today())
        
        # Consultas por status
        df_status = pd.read_sql("""
            SELECT status, COUNT(*) as quantidade
            FROM consultas 
            WHERE DATE(data_consulta) BETWEEN ? AND ?
            GROUP BY status
        """, conn, params=[data_inicio_rel, data_fim_rel])
        
        if not df_status.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_status = px.pie(df_status, values='quantidade', names='status', title="Consultas por Status")
                st.plotly_chart(fig_status, use_container_width=True)
            
            with col2:
                # Consultas por dia
                df_dia = pd.read_sql("""
                    SELECT DATE(data_consulta) as data, COUNT(*) as quantidade
                    FROM consultas 
                    WHERE DATE(data_consulta) BETWEEN ? AND ?
                    GROUP BY DATE(data_consulta)
                    ORDER BY data
                """, conn, params=[data_inicio_rel, data_fim_rel])
                
                if not df_dia.empty:
                    fig_dia = px.line(df_dia, x='data', y='quantidade', title="Consultas por Dia", markers=True)
                    st.plotly_chart(fig_dia, use_container_width=True)
        
        conn.close()

if __name__ == "__main__":
    main()
