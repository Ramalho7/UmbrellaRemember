# 🌂 Umbrella Remember

Sistema automatizado de lembrete de guarda-chuva que verifica a previsão do tempo diariamente e envia notificações push quando há possibilidade de chuva.

## 📋 Descrição

O **Umbrella Remember** é um script Python que:
- Consulta a API do OpenWeatherMap para obter a previsão do tempo
- Analisa se há possibilidade de chuva no dia atual
- Envia notificações push via [ntfy.sh](https://ntfy.sh) para lembrar de levar o guarda-chuva
- Executa automaticamente todos os dias às 6h da manhã via GitHub Actions

## 🏙️ Localização

Atualmente configurado para **João Pessoa, Paraíba, Brasil**.

## 🔧 Configuração

### 1. Pré-requisitos

- Python 3.11+
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
```

### 4. Configuração no GitHub

1. Vá em **Settings** > **Secrets and variables** > **Actions**
2. Adicione um novo secret:
   - **Name**: `OPENWEATHER_API_KEY`
   - **Value**: Sua chave da API do OpenWeatherMap

## 🚀 Como Usar

### Execução Local
```bash
python umbrellaRemember.py
```

### Execução Automática
O GitHub Actions executará automaticamente todos os dias às **6h da manhã** (horário brasileiro).

### Execução Manual no GitHub
1. Vá na aba **Actions** do repositório
2. Selecione o workflow **Umbrella Reminder**
3. Clique em **Run workflow**

## 📱 Notificações

As notificações são enviadas via **ntfy.sh** no tópico `RainInJpCity`.

### Para receber notificações:
1. Instale o app [ntfy](https://ntfy.sh/app) no seu celular
2. Inscreva-se no tópico: `RainInJpCity`

### Tipos de notificação:

**🌧️ Quando vai chover:**
- **Título**: "Importante: Chuva HOJE!"
- **Mensagem**: "Leve um guarda-chuva!"
- **Prioridade**: Alta
- **Tags**: warning, rain

**☀️ Quando não vai chover:**
- **Mensagem**: "Sem chuva para hoje!"

## 📁 Estrutura do Projeto

```
UmbrellaRemember/
├── .github/
│   └── workflows/
│       └── umbrella.yml        # Configuração do GitHub Actions
├── umbrellaRemember.py         # Script principal
├── .env                        # Variáveis de ambiente (não commitado)
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

## ⚙️ Funcionamento

1. **6h da manhã**: GitHub Actions executa o script automaticamente
2. **Geocodificação**: Converte "João Pessoa" em coordenadas (lat/lon)
3. **Previsão**: Consulta API do OpenWeatherMap para previsão do dia
4. **Análise**: Verifica se há chuva prevista para hoje
5. **Notificação**: Envia alerta via ntfy.sh

## 🔄 Personalização

### Alterar Cidade
Modifique as constantes no arquivo `umbrellaRemember.py`:

```python
CITY = 'Sua Cidade'
STATE_CODE = 'Seu Estado'
COUNTY_CODE = 'BR'  # ou outro país
```

### Alterar Horário
Edite o cron no arquivo `.github/workflows/umbrella.yml`:

```yaml
schedule:
  - cron: '0 09 * * *'  # UTC (ajuste conforme seu fuso)
```

### Alterar Tópico de Notificação
Modifique a URL no script:

```python
'https://ntfy.sh/SeuTopicoPersonalizado'
```

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal
- **OpenWeatherMap API**: Dados meteorológicos
- **ntfy.sh**: Serviço de notificações push
- **GitHub Actions**: Automação e agendamento
- **requests**: Requisições HTTP
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 📊 Status

- ✅ Funcionando automaticamente
- ✅ Notificações em português
- ✅ Execução diária às 6h
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