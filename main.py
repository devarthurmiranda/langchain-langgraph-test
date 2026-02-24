"""Interface CLI para o sistema multiagentes."""

import os
from dotenv import load_dotenv
from graph.workflow import MultiAgentWorkflow


def exibir_banner():
    """Exibe o banner de boas-vindas."""
    print("=" * 60)
    print(" Sistema Multiagentes - LangChain + LangGraph")
    print("=" * 60)
    print("\nAgentes disponíveis:")
    print("  1. Categorizador: Identifica o tipo de conversa")
    print("  2. Conversação: Responde com personalidade adequada")
    print("\nCategorias: técnico | comercial | suporte | geral")
    print("\nDigite 'sair' ou 'exit' para encerrar.")
    print("=" * 60)
    print()


def main():
    """Função principal da aplicação CLI."""
    # Carrega variáveis de ambiente
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("ERRO: GOOGLE_API_KEY não encontrada!")
        print("Por favor, crie um arquivo .env baseado no .env.example")
        print("e adicione sua chave da API do Google.")
        return

    # Inicializa o workflow
    print("Inicializando sistema multiagentes...")
    try:
        workflow = MultiAgentWorkflow(api_key)
        print("Sistema pronto!\n")
    except Exception as e:
        print(f"ERRO ao inicializar: {e}")
        return

    # Exibe banner
    exibir_banner()

    # Histórico da conversa
    historico = []

    # Loop principal
    while True:
        try:
            # Recebe entrada do usuário
            mensagem = input("\nVocê: ").strip()

            # Verifica se quer sair
            if mensagem.lower() in ["sair", "exit", "quit"]:
                print("\nEncerrando... Até logo!")
                break

            # Ignora mensagens vazias
            if not mensagem:
                continue

            # Processa a mensagem
            print("\nProcessando...", end="\r")
            resultado = workflow.processar_mensagem(mensagem, historico)

            # Atualiza o histórico
            historico = resultado["historico"]

            # Exibe a categoria identificada
            categoria = resultado["categoria"].upper()
            print(f"[Categoria: {categoria}]")

            # Exibe a resposta
            print(f"\nAssistente: {resultado['resposta']}")

        except KeyboardInterrupt:
            print("\n\nEncerrando... Até logo!")
            break
        except Exception as e:
            print(f"\nERRO: {e}")
            print("Tente novamente.")


if __name__ == "__main__":
    main()
