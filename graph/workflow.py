"""Grafo LangGraph para orquestração dos agentes."""

from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from agents.categorizer import CategorizerAgent
from agents.conversation import ConversationAgent


class Estado(TypedDict):
    """Estado compartilhado entre os nós do grafo."""
    mensagem: str  # Mensagem atual do usuário
    categoria: str  # Categoria identificada
    resposta: str  # Resposta gerada
    historico: List[Dict[str, str]]  # Histórico de mensagens


class MultiAgentWorkflow:
    """Workflow que orquestra os agentes usando LangGraph."""

    def __init__(self, api_key: str):
        """
        Inicializa o workflow com os agentes.

        Args:
            api_key: Chave da API do Google
        """
        self.categorizador = CategorizerAgent(api_key)
        self.conversacao = ConversationAgent(api_key)
        self.graph = self._criar_grafo()

    def _nodo_categorizar(self, state: Estado) -> Estado:
        """
        Nó que categoriza a mensagem do usuário.

        Args:
            state: Estado atual

        Returns:
            Estado atualizado com a categoria
        """
        mensagem = state["mensagem"]
        categoria = self.categorizador.categorize(mensagem)

        return {
            **state,
            "categoria": categoria
        }

    def _nodo_conversar(self, state: Estado) -> Estado:
        """
        Nó que gera a resposta baseada na categoria.

        Args:
            state: Estado atual

        Returns:
            Estado atualizado com a resposta
        """
        mensagem = state["mensagem"]
        categoria = state["categoria"]
        historico = state.get("historico", [])

        resposta = self.conversacao.responder(mensagem, categoria, historico)

        # Atualiza o histórico
        novo_historico = historico.copy()
        novo_historico.append({"role": "user", "content": mensagem})
        novo_historico.append({"role": "assistant", "content": resposta})

        return {
            **state,
            "resposta": resposta,
            "historico": novo_historico
        }

    def _criar_grafo(self) -> StateGraph:
        """
        Cria o grafo de workflow.

        Returns:
            Grafo compilado
        """
        # Cria o grafo
        workflow = StateGraph(Estado)

        # Adiciona os nós
        workflow.add_node("categorizar", self._nodo_categorizar)
        workflow.add_node("conversar", self._nodo_conversar)

        # Define as arestas (fluxo)
        workflow.set_entry_point("categorizar")
        workflow.add_edge("categorizar", "conversar")
        workflow.add_edge("conversar", END)

        # Compila o grafo
        return workflow.compile()

    def processar_mensagem(
        self,
        mensagem: str,
        historico: List[Dict[str, str]] = None
    ) -> Dict[str, any]:
        """
        Processa uma mensagem através do workflow.

        Args:
            mensagem: Mensagem do usuário
            historico: Histórico de mensagens anteriores

        Returns:
            Dicionário com categoria, resposta e histórico atualizado
        """
        if historico is None:
            historico = []

        # Estado inicial
        estado_inicial = {
            "mensagem": mensagem,
            "categoria": "",
            "resposta": "",
            "historico": historico
        }

        # Executa o grafo
        resultado = self.graph.invoke(estado_inicial)

        return {
            "categoria": resultado["categoria"],
            "resposta": resultado["resposta"],
            "historico": resultado["historico"]
        }
