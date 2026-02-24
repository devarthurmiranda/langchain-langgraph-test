# Sistema Multiagentes com LangChain e LangGraph

Sistema de conversação inteligente que utiliza dois agentes cooperativos:
1. **Agente Categorizador**: Identifica o tipo de conversa
2. **Agente de Conversação**: Responde com personalidade adequada à categoria

## Arquitetura

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Categorizador      │ → Classifica em: técnico, comercial, suporte, geral
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Conversação        │ → Ajusta personalidade baseada na categoria
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  Resposta   │
└─────────────┘
```

### Tecnologias

- **LangChain**: Framework para desenvolvimento de aplicações com LLMs
- **LangGraph**: Orquestração de workflows multiagentes
- **Google Gemini**: Modelo de linguagem (via API)

## Categorias e Personalidades

| Categoria  | Personalidade | Características |
|-----------|---------------|-----------------|
| **Técnico** | Especialista técnico | Objetivo, preciso, foca em soluções técnicas |
| **Comercial** | Consultor comercial | Persuasivo, profissional, destaca valor |
| **Suporte** | Agente de suporte | Paciente, didático, explicações passo a passo |
| **Geral** | Assistente versátil | Amigável, conversacional, adaptável |

## Instalação

### 1. Pré-requisitos

- Python 3.10 ou superior
- Chave de API do Google (Gemini)

### 2. Clonar/baixar o projeto

```bash
cd LangChain
```

### 3. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Copiar o exemplo
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edite o arquivo `.env` e adicione sua chave:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

**Como obter a chave da API do Google:**
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

## Uso

### Executar o sistema

```bash
python main.py
```

### Exemplos de interação

```
Você: Como configurar SSL no servidor?
[Categoria: TECNICO]
Assistente: Para configurar SSL no servidor, você precisará...

Você: Quanto custa seu produto?
[Categoria: COMERCIAL]
Assistente: Nossos planos oferecem excelente custo-benefício...

Você: Como faço login no sistema?
[Categoria: SUPORTE]
Assistente: Vou te ajudar passo a passo com o login...

Você: Olá!
[Categoria: GERAL]
Assistente: Olá! Como posso ajudar você hoje?
```

### Sair do sistema

Digite `sair`, `exit` ou `quit`, ou pressione `Ctrl+C`.

## Estrutura do Projeto

```
LangChain/
├── agents/
│   ├── __init__.py
│   ├── categorizer.py      # Agente categorizador
│   └── conversation.py     # Agente de conversação
├── graph/
│   ├── __init__.py
│   └── workflow.py         # Orquestração LangGraph
├── .env                    # Variáveis de ambiente (não versionado)
├── .env.example            # Exemplo de configuração
├── .gitignore
├── main.py                 # Interface CLI
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## Funcionamento do Workflow

1. **Entrada**: Usuário envia mensagem
2. **Categorização**:
   - Agente categorizador analisa a mensagem
   - Classifica em uma das 4 categorias
3. **Conversação**:
   - Agente de conversação recebe a categoria
   - Ajusta personalidade conforme categoria
   - Acessa histórico de mensagens anteriores
   - Gera resposta apropriada
4. **Saída**: Resposta é exibida ao usuário
5. **Memória**: Histórico é mantido para contexto contínuo

## Personalização

### Adicionar novas categorias

Edite `agents/categorizer.py` e `agents/conversation.py`:

```python
# Em categorizer.py
CATEGORIAS = ["tecnico", "comercial", "suporte", "geral", "nova_categoria"]

# Em conversation.py
PERSONALIDADES = {
    # ... categorias existentes
    "nova_categoria": "Descrição da personalidade..."
}
```

### Ajustar temperatura do modelo

Em `agents/categorizer.py` ou `agents/conversation.py`:

```python
self.llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7  # Ajuste entre 0.0 (mais determinístico) e 1.0 (mais criativo)
)
```

### Usar modelo diferente

Substitua `"gemini-1.5-flash"` por:
- `"gemini-1.5-pro"` (mais poderoso, mais lento)
- `"gemini-pro"` (alternativa)

## Troubleshooting

### Erro: "GOOGLE_API_KEY não encontrada"

- Verifique se o arquivo `.env` existe na raiz do projeto
- Confirme que a variável está definida: `GOOGLE_API_KEY=sua_chave`

### Erro de importação

```bash
# Reinstale as dependências
pip install -r requirements.txt --upgrade
```

### Erro de API

- Verifique se a chave da API está correta
- Confirme que a API do Gemini está ativada
- Verifique limites de uso da API gratuita

## Melhorias Futuras

- [ ] Interface web com Streamlit/Gradio
- [ ] Persistência de histórico em banco de dados
- [ ] Métricas e analytics das conversas
- [ ] Mais agentes especializados
- [ ] Integração com ferramentas externas (APIs, bancos de dados)
- [ ] Testes automatizados

## Licença

Projeto livre para uso educacional e comercial.

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
