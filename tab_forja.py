"""
Grimório V2.0 - Aba 4: Forja (Hábitos & Evolução)
Rastreador de Hábitos Estilo Mana/HP, Fogo de Sequência (Streak) e Níveis do Império com Tema Dinâmico
"""

from datetime import date
import flet as ft
from theme import (
    BG_DARK, BG_SURFACE, BG_CARD, BG_CARD_LIGHT, BG_INPUT,
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_MUTED, GOLD_CONTAINER, BORDER_GOLD,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_CONTAINER, BORDER_PURPLE,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS_GREEN, DANGER_RED, MANA_BLUE, HP_RED, BORDER_RADIUS,
    border_all, border_radius_all, padding_all, padding_symmetric, icon_nobre, botao_preenchido,
    get_theme_colors
)
from storage import storage
from components.common_ui import criar_card_nobre, criar_botao_primario, mostrar_notificacao

def criar_aba_forja(page: ft.Page, on_update_callback=None) -> ft.Control:
    """Retorna a visão completa da Aba Forja com suporte a tema dinâmico."""

    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))

    hoje_str = date.today().isoformat()
    lista_habitos_col = ft.Column(spacing=10)
    secao_evolucao_container = ft.Column(spacing=8)

    def renderizar_evolucao():
        reino = storage.data["reino"]
        nivel = reino.get("nivel", 1)
        titulo = reino.get("titulo_nivel", "Vilarejo Inicial")
        exp_atual = reino.get("exp_atual", 0)
        exp_prox = reino.get("exp_proximo", 100)
        progresso = min(1.0, max(0.0, exp_atual / exp_prox if exp_prox > 0 else 0.0))

        proximo_nivel_num = nivel + 1
        idx_prox = min(nivel, len(storage.TITULOS_NIVEL) - 1)
        proximo_titulo = storage.TITULOS_NIVEL[idx_prox]

        secao_evolucao_container.controls = [
            ft.Row(
                controls=[
                    ft.Container(
                        content=icon_nobre(ft.Icons.FORT, size=32, color=cores["light"]),
                        width=56,
                        height=56,
                        border_radius=border_radius_all(28),
                        bgcolor=cores["container"],
                        border=border_all(2, cores["primary"]),
                        alignment=ft.Alignment(0, 0)
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(f"Nível {nivel} • {titulo}", weight=ft.FontWeight.BOLD, color=cores["light"], size=15),
                                ],
                                spacing=4
                            ),
                            ft.Text(f"Próxima Fronteira: Nv. {proximo_nivel_num} - {proximo_titulo}", size=11, color=cores.get("text_secondary", TEXT_SECONDARY)),
                            ft.Row(
                                controls=[
                                    ft.Text(f"{exp_atual}/{exp_prox} EXP", size=10, color=cores.get("text_muted", TEXT_MUTED)),
                                    ft.Text(f"{int(progresso * 100)}%", size=10, color=cores["secondary_light"], weight=ft.FontWeight.BOLD)
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.ProgressBar(value=progresso, color=cores["primary"], bgcolor="#1E1E2C", height=7)
                        ],
                        spacing=3,
                        expand=True
                    )
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
        try:
            secao_evolucao_container.update()
        except Exception:
            pass

    def alternar_habito(hid: str):
        h = storage.alternar_habito_hoje(hid)
        if h:
            if h["concluido_hoje"]:
                mostrar_notificacao(page, f"Hábito cumprido! 🔥 {h['streak_atual']} dias de sequência! (+12 EXP, +5 Ouro)", sucesso=True)
            else:
                mostrar_notificacao(page, "Check-in do hábito desmarcado.", sucesso=False)
        renderizar_tudo()
        if on_update_callback:
            on_update_callback()

    def excluir_habito(hid: str):
        storage.remover_habito(hid)
        mostrar_notificacao(page, "Hábito removido da Forja.", sucesso=True)
        renderizar_tudo()
        if on_update_callback:
            on_update_callback()

    def renderizar_habitos():
        habitos = storage.data["forja"].get("habitos", [])
        if not habitos:
            lista_habitos_col.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            icon_nobre(ft.Icons.BUILD, size=32, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Nenhum hábito na Forja.", size=12, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Forje novas virtudes para fortalecer o Império!", size=11, color=cores["light"])
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4
                    ),
                    padding=20,
                    alignment=ft.Alignment(0, 0)
                )
            ]
        else:
            cards = []
            for h in habitos:
                datas = h.get("datas_concluidas", [])
                concluido_hoje = hoje_str in datas
                streak = h.get("streak_atual", 0)
                melhor = h.get("melhor_streak", 0)
                tipo = h.get("tipo", "HP")
                
                if tipo == "Mana":
                    cor_barra = MANA_BLUE
                    icone_tipo = ft.Icons.AUTO_AWESOME
                    label_tipo = "Mana / Mente"
                elif tipo == "Ouro":
                    cor_barra = cores["primary"]
                    icone_tipo = ft.Icons.LOCAL_FIRE_DEPARTMENT
                    label_tipo = "Ouro / Disciplina"
                else:
                    cor_barra = HP_RED
                    icone_tipo = ft.Icons.FAVORITE
                    label_tipo = "HP / Vitalidade"

                progresso_meta = min(1.0, streak / 21.0)
                
                check_btn = ft.Container(
                    content=icon_nobre(
                        ft.Icons.CHECK_CIRCLE if concluido_hoje else ft.Icons.RADIO_BUTTON_UNCHECKED,
                        size=28,
                        color=SUCCESS_GREEN if concluido_hoje else cores.get("text_muted", TEXT_MUTED)
                    ),
                    on_click=lambda e, hid=h["id"]: alternar_habito(hid),
                    padding=4
                )

                card = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    check_btn,
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                h["nome"],
                                                weight=ft.FontWeight.BOLD,
                                                size=13,
                                                color=cores.get("text_muted", TEXT_MUTED) if concluido_hoje else cores.get("text_primary", TEXT_PRIMARY),
                                                style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH if concluido_hoje else ft.TextDecoration.NONE)
                                            ),
                                            ft.Row(
                                                controls=[
                                                    icon_nobre(icone_tipo, size=12, color=cor_barra),
                                                    ft.Text(label_tipo, size=10, color=cor_barra, weight=ft.FontWeight.W_500),
                                                    ft.Text("•", size=10, color=cores.get("text_muted", TEXT_MUTED)),
                                                    ft.Text(f"🔥 {streak} dias", size=11, color="#FB923C", weight=ft.FontWeight.BOLD),
                                                    ft.Text(f"(Recorde: {melhor})", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                                ],
                                                spacing=4,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                                            )
                                        ],
                                        spacing=2,
                                        expand=True
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_size=18,
                                        icon_color="#64748B",
                                        on_click=lambda e, hid=h["id"]: excluir_habito(hid)
                                    )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=6
                            ),
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Forja Contínua (Rumo aos 21 dias)", size=9, color=cores.get("text_muted", TEXT_MUTED)),
                                            ft.Text(f"{streak}/21", size=9, color=cor_barra, weight=ft.FontWeight.BOLD)
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.ProgressBar(value=progresso_meta, color=cor_barra, bgcolor="#181822", height=5)
                                ],
                                spacing=2
                            )
                        ],
                        spacing=6
                    ),
                    padding=10,
                    border_radius=border_radius_all(10),
                    bgcolor=cores["bg_input"] if concluido_hoje else cores["bg_card"],
                    border=border_all(1, "#1E3A2F" if concluido_hoje else cores.get("border_subtle", "#2B2B3D"))
                )
                cards.append(card)
            lista_habitos_col.controls = cards

        try:
            lista_habitos_col.update()
        except Exception:
            pass

    def renderizar_tudo():
        renderizar_evolucao()
        renderizar_habitos()

    def abrir_modal_novo_habito(e):
        txt_nome = ft.TextField(
            label="Nome do Hábito / Virtude",
            hint_text="Ex: 30 min de Treino com Espada, Estudo Arcano",
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            text_size=13,
            color=cores.get("text_primary", TEXT_PRIMARY)
        )
        
        dropdown_tipo = ft.Dropdown(
            label="Tipo de Atributo",
            options=[
                ft.dropdown.Option("HP", "HP / Vitalidade (Saúde, Exercício, Sono)"),
                ft.dropdown.Option("Mana", "Mana / Mente (Estudo, Foco, Leitura)"),
                ft.dropdown.Option("Ouro", "Ouro / Disciplina (Finanças, Organização, Metas)")
            ],
            value="HP",
            bgcolor=cores["bg_surface"],
            border_color=cores.get("border_subtle", "#36364A"),
            color=cores.get("text_primary", TEXT_PRIMARY)
        )

        def salvar_habito(e_salvar):
            if not txt_nome.value or not txt_nome.value.strip():
                txt_nome.error_text = "Informe o nome da virtude!"
                txt_nome.update()
                return
                
            storage.adicionar_habito(
                nome=txt_nome.value.strip(),
                tipo=dropdown_tipo.value
            )
            
            fechar_modal(dialogo)
            mostrar_notificacao(page, "Nova virtude forjada no coração do reino!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()

        def fechar_modal(dlg):
            if hasattr(page, "pop_dialog"):
                page.pop_dialog()
            else:
                dlg.open = False
                page.update()

        dialogo = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.BUILD, color=cores["light"], size=20),
                    ft.Text("Forjar Nova Virtude", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Column(
                controls=[
                    txt_nome,
                    dropdown_tipo
                ],
                spacing=12,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo)),
                botao_preenchido(
                    texto="Forjar Virtude",
                    bgcolor=cores["primary"],
                    color="#121214",
                    on_click=salvar_habito
                )
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )

        if hasattr(page, "show_dialog"):
            page.show_dialog(dialogo)
        else:
            page.dialog = dialogo
            dialogo.open = True
            page.update()

    btn_novo_habito = criar_botao_primario(
        texto="➕ Forjar Nova Virtude",
        icone=ft.Icons.ADD_CIRCLE,
        on_click=abrir_modal_novo_habito,
        cor_fundo=cores["primary"],
        expand=True
    )

    secao_evolucao_card = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.AUTO_AWESOME, size=18, color=cores["light"]),
                        ft.Text("Evolução & Honra do Reino", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=14)
                    ],
                    spacing=6
                ),
                secao_evolucao_container
            ],
            spacing=10
        ),
        borda_dourada=True
    )

    secao_habitos_card = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.LOCAL_FIRE_DEPARTMENT, size=18, color="#FB923C"),
                        ft.Text("Virtudes Diárias • Hábitos da Coroa", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=14)
                    ],
                    spacing=6
                ),
                btn_novo_habito,
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                lista_habitos_col
            ],
            spacing=10
        ),
        borda_roxa=True
    )

    renderizar_tudo()

    return ft.ListView(
        controls=[
            secao_evolucao_card,
            secao_habitos_card,
            ft.Container(height=30)
        ],
        spacing=14,
        padding=12,
        expand=True
    )
