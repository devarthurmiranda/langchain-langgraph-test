"""Agente de conversação - responde ao usuário baseado na categoria."""

from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


class ConversationAgent:
    """Agente responsável por conversar com o usuário baseado na categoria."""

    # Personalidades diferentes para cada categoria
    PERSONALIDADES = {
        "tecnico": """Você é um assistente técnico especializado. Suas características:
- Objetivo e preciso nas respostas
- Foca em soluções técnicas e detalhes de implementação
- Usa terminologia técnica apropriada
- Fornece exemplos de código quando relevante
- Analisa problemas de forma sistemática""",

        "comercial": """Você é um consultor comercial profissional. Suas características:
- Persuasivo e focado em valor
- Destaca benefícios e retorno sobre investimento
- Profissional e cortês
- Identifica oportunidades de negócio
- Busca entender necessidades do cliente""",

        "suporte": """Você é um agente de suporte dedicado. Suas características:
- Paciente e empático
- Didático e claro nas explicações
- Fornece instruções passo a passo
- Confirma compreensão do usuário
- Oferece ajuda adicional proativamente""",

        "geral": """Você é um assistente amigável e versátil. Suas características:
- Conversacional e natural
- Adapta-se ao tom da conversa
- Responde de forma clara e concisa
- Mantém interações agradáveis
- Pode discutir diversos assuntos"""
    }

    def __init__(self, api_key: str):
        """
        Inicializa o agente de conversação.

        Args:
            api_key: Chave da API do Google para usar o Gemini
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7  # Temperatura moderada para respostas naturais
        )

    def _create_prompt(self, categoria: str) -> ChatPromptTemplate:
        """
        Cria o prompt baseado na categoria.

        Args:
            categoria: Categoria da conversa (tecnico, comercial, suporte, geral)

        Returns:
            Template de prompt configurado
        """
        personalidade = self.PERSONALIDADES.get(categoria, self.PERSONALIDADES["geral"])

        return ChatPromptTemplate.from_messages([
            ("system", personalidade),
            MessagesPlaceholder(variable_name="historico"),
            ("user", "{mensagem}")
        ])

    def responder(
        self,
        mensagem: str,
        categoria: str,
        historico: List[Dict[str, str]] = None
    ) -> str:
        """
        Gera uma resposta baseada na mensagem, categoria e histórico.

        Args:
            mensagem: Mensagem atual do usuário
            categoria: Categoria identificada (tecnico, comercial, suporte, geral)
            historico: Lista de mensagens anteriores [{"role": "user"/"assistant", "content": "..."}]

        Returns:
            Resposta do agente
        """
        if historico is None:
            historico = []

        # Converte histórico para formato LangChain
        mensagens_historico = []
        for msg in historico:
            if msg["role"] == "user":
                mensagens_historico.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                mensagens_historico.append(AIMessage(content=msg["content"]))

        # Cria o prompt com a personalidade apropriada
        prompt = self._create_prompt(categoria)
        chain = prompt | self.llm

        # Gera resposta
        resposta = chain.invoke({
            "mensagem": mensagem,
            "historico": mensagens_historico
        })

        return resposta.content
