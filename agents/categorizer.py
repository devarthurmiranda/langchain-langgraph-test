"""Agente categorizador - classifica a mensagem do usuário em categorias."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class CategorizerAgent:
    """Agente responsável por categorizar mensagens do usuário."""

    CATEGORIAS = ["tecnico", "comercial", "suporte", "geral"]

    def __init__(self, api_key: str):
        """
        Inicializa o agente categorizador.

        Args:
            api_key: Chave da API do Google para usar o Gemini
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.1  # Baixa temperatura para respostas mais determinísticas
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um categorizador especializado. Sua única função é classificar mensagens em uma das seguintes categorias:

- tecnico: Questões técnicas, problemas de sistema, erros, bugs, configurações, código
- comercial: Vendas, preços, orçamentos, propostas, negociações, produtos/serviços
- suporte: Ajuda com uso, dúvidas sobre funcionalidades, tutoriais, como fazer algo
- geral: Conversas casuais, saudações, agradecimentos, outros tópicos não específicos

Responda APENAS com o nome da categoria, sem explicações adicionais.
Use EXATAMENTE um destes nomes: tecnico, comercial, suporte, geral"""),
            ("user", "Mensagem: {message}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def categorize(self, message: str) -> str:
        """
        Categoriza uma mensagem do usuário.

        Args:
            message: Mensagem do usuário para categorizar

        Returns:
            Nome da categoria (tecnico, comercial, suporte ou geral)
        """
        categoria = self.chain.invoke({"message": message}).strip().lower()

        # Valida que a categoria está entre as permitidas
        if categoria not in self.CATEGORIAS:
            # Se a LLM retornar algo inválido, usa 'geral' como fallback
            return "geral"

        return categoria
