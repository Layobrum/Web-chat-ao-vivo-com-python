import flet as ft

# Definindo a função principal com as variaveis iniciais
def main(pagina):
    texto = ft.Text("Hashzap")
    chat = ft.Column()
    nomeUsuario = ft.TextField(label="Escreva seu nome")

    # Criando a função que irá conectar as mensagens de todos os usuários
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", 
                                         size=12, italic=True, color=ft.colors.ORANGE_500))
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    # Criando a função para um usuario enviar uma mensagem normalmente
    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nomeUsuario.value, "tipo": "mensagem"})
        campo_mensagem.value = ""
        pagina.update()

    # Criando
    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    # Criando a função de popup ao iniciar o programa
    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nomeUsuario.value, "tipo": "entrada"})
        pagina.add(chat)
        popup.open = False
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))
        pagina.update()

    # Configurando o popup
    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Bem vindo ao Hashzap"),
        content=nomeUsuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
        )

    # Definindo a função para um usuário entrar no chat
    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    # Criando o botão para entrar no chat
    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    # Adicionando os elementos a página
    pagina.add(texto)
    pagina.add(botao_iniciar)

# Rodando o programa e configurando a visualização para o navegador
ft.app(target=main, view="web_browser", port=8000)