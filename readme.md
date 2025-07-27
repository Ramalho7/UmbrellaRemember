# 🌂 Umbrella Remember

Aplicação web que permite aos usuários se cadastrarem com suas cidades e receberem notificações personalizadas por e-mail sobre a previsão do tempo diariamente.

## 📋 Descrição

O **Umbrella Remember** é uma aplicação Flask que oferece:

- **Sistema de cadastro e autenticação de usuários** com criptografia segura de senhas
- **Banco de dados completo** com todas as cidades brasileiras (integração com API do IBGE)
- **Verificação automática do clima** via API OpenWeatherMap
- **Envio personalizado de e-mails** com previsão do tempo baseada na localização do usuário
- **Sistema de sessões** para controle de acesso às páginas

## 🌐 Funcionalidades Web

### Sistema de Usuários

- **Cadastro**: Registre-se com nome, e-mail, senha e cidade
- **Login/Logout**: Sistema de autenticação seguro
- **Perfil**: Visualize e edite seus dados pessoais
- **Exclusão de conta**: Remova sua conta quando desejar

### Localização Inteligente

- **Seleção de cidades**: Escolha entre todas as cidades brasileiras
- **Interface intuitiva**: Digite ou selecione sua cidade em um dropdown sincronizado
- **Dados atualizados**: Base de dados com informações do IBGE

## 🔧 Configuração

### 1. Pré-requisitos

- Python 3.13+
- MySQL ou outro banco de dados compatível com SQLAlchemy
- Conta no [OpenWeatherMap](https://openweathermap.org/api) (gratuita)

### 2. Dependências

```bash
pip install flask flask-session sqlalchemy pymysql python-dotenv argon2-cffi requests
```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Banco de Dados
DB_USER=seu_usuario_db
DB_PASSWORD=sua_senha_db
DB_HOST=localhost
DB_NAME=umbrella_remember

# Chave secreta da aplicação Flask
SECRET_KEY=sua_chave_secreta_super_segura

# API do OpenWeatherMap
OPENWEATHER_API_KEY=sua_chave_api_aqui

# Configurações de E-mail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
```

### 4. Configuração do Banco de Dados

Execute o script para criar as tabelas e popular com dados das cidades brasileiras:

```bash
python models/model.py
```

## 🚀 Como Usar

### Execução da Aplicação Web

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

### Execução do Sistema de Notificações

Para enviar notificações de clima para todos os usuários:

```bash
python utils/checkRain.py
```

## 🌐 Páginas da Aplicação

### Página Inicial (`/`)

- Formulário de cadastro com seleção de cidade
- Interface responsiva e amigável

### Login (`/login`)

- Autenticação segura de usuários
- Redirecionamento automático após login

### Perfil (`/profile`)

- Visualização dos dados do usuário
- Botões para editar ou excluir conta

### Edição de Perfil (`/update`)

- Atualização de dados pessoais
- Mudança de cidade

## 📧 Sistema de Notificações

### Tipos de E-mail Enviados

**🌧️ Quando há previsão de chuva:**

- **Assunto**: "Dia de chuva!"
- **Conteúdo**: E-mail personalizado com o nome do usuário e cidade
- **Visual**: Imagem de guarda-chuva e design responsivo

**☀️ Quando não há previsão de chuva:**

- **Assunto**: "Dia de sol!"
- **Conteúdo**: E-mail motivacional sobre o dia ensolarado
- **Visual**: Imagem de dia ensolarado e cores vibrantes

### Personalização

- E-mails são enviados individualmente para cada usuário
- Conteúdo personalizado com nome e cidade do usuário
- Design HTML responsivo com imagens do Unsplash

## 📁 Estrutura do Projeto

```txt
UmbrellaRemember/
├── app.py                      # Aplicação Flask principal
├── generate_app_key.py         # Gerador de chave secreta
├── .env                        # Variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
├── LICENSE                     # Licença do projeto
├── README.md                   # Documentação
├── models/                     # Modelos do banco de dados
│   ├── model.py               # Classes SQLAlchemy e configuração DB
│   ├── get_user_by_id.py      # Função para buscar usuário por ID
│   └── update_user.py         # Função para atualizar dados do usuário
├── utils/                      # Utilitários
│   ├── checkRain.py           # Script de verificação do clima
│   ├── email_exists.py        # Verificação de e-mail existente
│   ├── login_verify.py        # Verificação de login
│   └── send_email.py          # Envio de e-mails
├── templates/                  # Templates HTML
│   ├── layout.html            # Layout base
│   ├── index.html             # Página inicial
│   ├── login.html             # Página de login
│   ├── profile.html           # Página de perfil
│   └── editUserPage.html      # Página de edição
├── static/                     # Arquivos estáticos
│   ├── syncCityInput.js       # JavaScript para seleção de cidades
│   └── css/
│       ├── layout.css         # Estilos gerais
│       ├── index.css          # Estilos da página inicial
│       └── profile.css        # Estilos do perfil
├── flask_session/              # Sessões do Flask
```

## ⚙️ Funcionamento

### Fluxo da Aplicação Web

1. **Registro**: Usuário acessa `/` e se cadastra escolhendo sua cidade
2. **Autenticação**: Sistema criptografa senha com Argon2 e armazena no banco
3. **Login**: Usuário faz login em `/login` com e-mail e senha
4. **Perfil**: Acesso à página de perfil com dados pessoais
5. **Edição**: Possibilidade de atualizar dados ou excluir conta

### Sistema de Notificações Automáticas

1. **Execução diária**: Script `checkRain.py` verifica clima para todos os usuários
2. **Geolocalização**: Converte cidade do usuário em coordenadas (lat/lon)
3. **Consulta API**: Obtém previsão do tempo via OpenWeatherMap
4. **Análise**: Verifica se há chuva prevista para o dia atual
5. **E-mail personalizado**: Envia notificação específica para cada usuário

### Banco de Dados

- **Países, Estados e Cidades**: Base completa com dados do IBGE
- **Usuários**: Informações pessoais e referência à cidade
- **Relacionamentos**: Estrutura normalizada com chaves estrangeiras
- **Segurança**: Senhas criptografadas com Argon2

## 🛠️ Tecnologias Utilizadas

- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para banco de dados
- **MySQL**: Sistema de gerenciamento de banco de dados
- **Argon2**: Criptografia de senhas
- **Flask-Session**: Gerenciamento de sessões
- **OpenWeatherMap API**: Dados meteorológicos
- **IBGE API**: Dados geográficos do Brasil
- **HTML/CSS/JavaScript**: Interface do usuário
- **SMTP**: Envio de e-mails
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🔒 Segurança

### Autenticação

- Senhas criptografadas com **Argon2**
- Verificação segura de credenciais
- Sistema de sessões para controle de acesso

### Proteção de Dados

- Validação de entrada de dados
- Sanitização de e-mails
- Tratamento de exceções para evitar vazamentos de informações

### Variáveis de Ambiente

- Credenciais sensíveis armazenadas em arquivo `.env`
- Separação entre configuração e código

## 📊 Status

- ✅ Sistema web funcionando completamente
- ✅ Banco de dados com todas as cidades brasileiras
- ✅ Autenticação segura de usuários
- ✅ Notificações personalizadas por e-mail
- ✅ Interface responsiva e amigável
- ✅ Sistema de gerenciamento de perfil

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**🌦️ Nunca mais esqueça o guarda-chuva!**