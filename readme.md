# 🌂 Umbrella Remember

Sistema automatizado de lembrete de guarda-chuva que verifica a previsão do tempo diariamente e envia notificações push quando há possibilidade de chuva.

## 📋 Descrição

O **Umbrella Remember** é um script Python que:
- Consulta a API do OpenWeatherMap para obter a previsão do tempo
- Analisa se há possibilidade de chuva no dia atual
- Envia notificações push via [ntfy.sh](https://ntfy.sh) e um e-mail para lembrar de levar o guarda-chuva 
- Executa automaticamente todos os dias às 5h30 da manhã via pythonAnyWhere

## 🏙️ Localização

Para configurar a localização da cidade, é necessário criar um arquivo `.env` na raiz do projeto. Este arquivo deve conter as seguintes variáveis:

```env
CITY=SuaCidade
STATE_CODE=SeuEstado
COUNTY_CODE=BR  # Código do país (exemplo: BR para Brasil)
```

Substitua `SuaCidade`, `SeuEstado` e `BR` pelos valores correspondentes à sua localização. Essas variáveis serão usadas pelo script para consultar a previsão do tempo na API do OpenWeatherMap.

## 🔧 Configuração

### 1. Pré-requisitos

- Python 3.13+
- Conta no [OpenWeatherMap](https://openweathermap.org/api) (gratuita)
- Repositório no GitHub (para automação)

### 2. Dependências

```bash
pip install requests python-dotenv 
```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENWEATHER_API_KEY=sua_chave_api_aqui
NTFY_CHANNEL=https://ntfy.sh/SeuTopicoPersonalizado
CITY=sua_cidade
STATE_CODE=seu_estado
COUNTY_CODE=seu_pais
RECIPIENTS=dest_email@gmail.com, dest_email2@outlook.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=app_password
```

## 🚀 Como Usar

### Execução Local
```bash
python umbrellaRemember.py
```

### Execução Automática
O pythonAnyWhere executará automaticamente todos os dias às **5h30 da manhã** (horário brasileiro).

## 📱 Notificações

As notificações são enviadas via **ntfy.sh** no tópico `seu_tópico`.

### Para receber notificações via ntfy:
1. Instale o app [ntfy](https://ntfy.sh/app) no seu celular
2. Inscreva-se no tópico: `seu_tópico`

### Para receber notificações via e-mail:

1. Configure as variáveis de ambiente no arquivo `.env`
```.env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
RECIPIENTS=dest_email@gmail.com,dest_email2@outlook.com
``` 
2. Certifique-se de que o e-mail configurado em SMTP_USER possui uma senha de aplicativo.
   1. Acesse Google App Passwords para gerar uma senha de aplicativo.
3. O script enviará e-mails automaticamente para os destinatários configurados em RECIPIENTS quando houver previsão de chuva ou dia ensolarado.
4. Para testar manualmente, execute o script:
```python
python umbrellaRemember.py
```
5. Verifique sua caixa de entrada para confirmar o recebimento das notificações.

### Tipos de notificação ntfy:

**🌧️ Quando vai chover:**
- **Título**: "Importante: Chuva HOJE!"
- **Mensagem**: "Leve um guarda-chuva!"
- **Prioridade**: Alta
- **Tags**: warning, rain

**☀️ Quando não vai chover:**
- **Mensagem**: "Dia de sol!"

### Tipos de notificação e-mail:

🌧️ Quando vai chover:

**Assunto:** "Leve um guarda-chuva!"
**Corpo do e-mail:**
```HTML
<div style="text-align:center; font-family:Roboto, sans-serif; padding:20px;">
<img src="https://images.unsplash.com/photo-1428592953211-077101b2021b?q=80&w=1000&auto=format&fit=crop" alt="Guarda-chuva" style="width:100%; max-width:600px; margin:20px auto; border-radius:10px; height:300px;">
<h1 style="color:blue;">☂️ Importante: Chuva HOJE!</h1>
<p style="font-size:18px;">Olá,</p>
<p style="font-size:16px;">Há previsão de chuva para hoje. Não se esqueça de levar um guarda-chuva!</p>
<p style="font-size:14px; color:gray;">Atenciosamente,<br><strong>Umbrella Remember</strong></p>
</div>
```

☀️ Quando não vai chover:

**Assunto:** "Dia de sol!"
***Corpo do e-mail:**
```HTML
<div style="text-align:center; font-family:Roboto, sans-serif; padding:20px; background-color:#f9f9f9; border-radius:10px;">
<img src="https://images.unsplash.com/photo-1464660439080-b79116909ce7?q=80&w=1502&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Dia ensolarado" style="width:100%; max-width:600px; margin:20px auto; border-radius:10px; height:300px;">
<h1 style="color:green;">☀️ Sem previsão de chuva hoje!</h1>
<p style="font
```

## 📁 Estrutura do Projeto

```
UmbrellaRemember/
├── umbrellaRemember.py         
├── .env                        
├── .gitignore                 
└── README.md 
```

## ⚙️ Funcionamento

1. **5h30 da manhã**: PythonAnyWhere executa o script automaticamente
2. **Geocodificação**: Converte "CITY" em coordenadas (lat/lon)
3. **Previsão**: Consulta API do OpenWeatherMap para previsão do dia
4. **Análise**: Verifica se há chuva prevista para hoje
5. **Notificação**: Envia alerta via ntfy.sh e e-mail

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal
- **OpenWeatherMap API**: Dados meteorológicos
- **ntfy.sh**: Serviço de notificações push
- **PythonAnyWhere**: Automação e agendamento
- **requests**: Requisições HTTP
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 📊 Status

- ✅ Funcionando automaticamente
- ✅ Notificações em português
- ✅ Execução diária às 5h30
- ✅ Prioridade alta para dias chuvosos

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