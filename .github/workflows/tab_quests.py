"""
Grimório Mobile - Aba 2: Quests (Calendário & Missões para Android)
Calendário Dinâmico Mobile, Mural de Missões com Checkbox Tátil e Recompensas.
"""

import calendar
from datetime import datetime, date
import flet as ft
from theme import (
    BG_DARK, BG_SURFACE, BG_CARD, BG_CARD_LIGHT, BG_INPUT,
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_MUTED, GOLD_CONTAINER, BORDER_GOLD,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_CONTAINER, BORDER_PURPLE,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS_GREEN, DANGER_RED, HP_RED, MANA_BLUE, BORDER_RADIUS,
    border_all, border_radius_all, padding_all, padding_symmetric, icon_nobre, botao_preenchido,
    get_theme_colors
)
from storage import storage
from components.common_ui import criar_card_nobre, criar_botao_primario, mostrar_notificacao

def criar_aba_quests(page: ft.Page, on_update_callback=None) -> ft.Control:
    """Retorna a visão interativa completa da Aba Quests adaptada para telas de smartphone."""
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))

    hoje = date.today()
    estado = {
        "ano": hoje.year,
        "mes": hoje.month,
        "dia_selecionado": hoje.isoformat()
    }

    lista_quests_col = ft.Column(spacing=6)
    
    lbl_data_selecionada = ft.Text(
        f"Missões de {hoje.strftime('%d/%m/%Y')}",
        weight=ft.FontWeight.BOLD,
        color=cores["light"],
        size=13
    )

    lbl_mes_ano = ft.Text(
        f"{calendar.month_name[estado['mes']].capitalize()} {estado['ano']}",
        weight=ft.FontWeight.BOLD,
        color=cores.get("text_primary", TEXT_PRIMARY),
        size=13
    )
    
    grade_dias_container = ft.Column(spacing=2)

    def formatar_nome_mes(ano, mes):
        meses_pt = [
            "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        return f"{meses_pt[mes]} {ano}"

    def renderizar_calendario():
        ano = estado["ano"]
        mes = estado["mes"]
        lbl_mes_ano.value = formatar_nome_mes(ano, mes)
        
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        header_dias = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(d, size=10, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    expand=True,
                    alignment=ft.Alignment(0, 0)
                )
                for d in dias_semana
            ],
            spacing=1
        )
        
        cal = calendar.monthcalendar(ano, mes)
        linhas_dias = [header_dias]
        
        for semana in cal:
            row_controles = []
            for dia in semana:
                if dia == 0:
                    row_controles.append(ft.Container(expand=True))
                else:
                    data_iso = f"{ano:04d}-{mes:02d}-{dia:02d}"
                    is_sel = (data_iso == estado["dia_selecionado"])
                    is_hoje = (data_iso == hoje.isoformat())
                    
                    quests_do_dia = [q for q in storage.data["quests"] if q.get("data_limite") == data_iso]
                    tem_pendente = any(not q["concluida"] for q in quests_do_dia)
                    
                    bg_btn = cores["secondary"] if is_sel else (cores["container"] if is_hoje else cores["bg_input"])
                    border_btn = border_all(1, cores["light"] if is_sel else (cores["border_color"] if is_hoje else cores.get("border_subtle", "#282838")))
                    
                    dot_quest = None
                    if quests_do_dia:
                        dot_cor = cores["light"] if tem_pendente else SUCCESS_GREEN
                        dot_quest = ft.Container(
                            width=4, height=4, border_radius=border_radius_all(2), bgcolor=dot_cor
                        )

                    dia_btn = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    str(dia),
                                    size=11,
                                    color=cores.get("text_primary", TEXT_PRIMARY) if (is_sel or is_hoje) else cores.get("text_secondary", TEXT_SECONDARY),
                                    weight=ft.FontWeight.BOLD if (is_sel or is_hoje) else ft.FontWeight.NORMAL,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                dot_quest if dot_quest else ft.Container(height=4)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=1
                        ),
                        expand=True,
                        height=32,
                        border_radius=border_radius_all(6),
                        bgcolor=bg_btn,
                        border=border_btn,
                        on_click=lambda e, dt=data_iso: selecionar_data(dt)
                    )
                    row_controles.append(dia_btn)
                    
            linhas_dias.append(ft.Row(controls=row_controles, spacing=1))
            
        grade_dias_container.controls = linhas_dias
        try:
            grade_dias_container.update()
            lbl_mes_ano.update()
        except Exception:
            pass

    def mudar_mes(delta: int):
        novo_mes = estado["mes"] + delta
        novo_ano = estado["ano"]
        if novo_mes > 12:
            novo_mes = 1
            novo_ano += 1
        elif novo_mes < 1:
            novo_mes = 12
            novo_ano -= 1
        estado["ano"] = novo_ano
        estado["mes"] = novo_mes
        renderizar_calendario()

    def selecionar_data(dt_iso: str):
        estado["dia_selecionado"] = dt_iso
        dt_obj = datetime.strptime(dt_iso, "%Y-%m-%d").date()
        lbl_data_selecionada.value = f"Missões de {dt_obj.strftime('%d/%m/%Y')}"
        lbl_data_selecionada.update()
        renderizar_calendario()
        renderizar_quests()

    calendario_card = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_LEFT,
                            icon_color=cores["light"],
                            icon_size=20,
                            on_click=lambda e: mudar_mes(-1)
                        ),
                        lbl_mes_ano,
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_RIGHT,
                            icon_color=cores["light"],
                            icon_size=20,
                            on_click=lambda e: mudar_mes(1)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                grade_dias_container
            ],
            spacing=4
        ),
        borda_dourada=True,
        padding=8
    )

    def alternar_conclusao_quest(quest_id: str):
        q = storage.alternar_conclusao_quest(quest_id)
        if q:
            if q["concluida"]:
                mostrar_notificacao(page, f"Quest Concluída! +{q.get('recompensa_exp', 25)} EXP e +{q.get('recompensa_ouro', 15):.0f} Ouro!", sucesso=True)
            else:
                mostrar_notificacao(page, "Quest reaberta.", sucesso=False)
        renderizar_quests()
        renderizar_calendario()
        if on_update_callback:
            on_update_callback()

    def excluir_quest(quest_id: str):
        storage.remover_quest(quest_id)
        mostrar_notificacao(page, "Missão removida do mural.", sucesso=True)
        renderizar_quests()
        renderizar_calendario()
        if on_update_callback:
            on_update_callback()

    def renderizar_quests():
        data_sel = estado["dia_selecionado"]
        quests = storage.obter_quests_por_data(data_sel)
        
        if not quests:
            lista_quests_col.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            icon_nobre(ft.Icons.AUTO_AWESOME_OUTLINED, size=28, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Nenhuma missão para este dia.", color=cores.get("text_muted", TEXT_MUTED), size=12),
                            ft.Text("Toque acima para convocar uma nova quest!", color=cores["light"], size=11)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=3
                    ),
                    padding=16,
                    alignment=ft.Alignment(0, 0)
                )
            ]
        else:
            cards = []
            for q in quests:
                concluida = q.get("concluida", False)
                cor_cat = {
                    "Principal": cores["primary"],
                    "Diária": cores["secondary_light"],
                    "Coroa": HP_RED,
                    "Secundária": MANA_BLUE
                }.get(q.get("categoria", "Diária"), cores.get("text_secondary", TEXT_SECONDARY))
                
                check_icon = ft.Icons.CHECK_BOX if concluida else ft.Icons.CHECK_BOX_OUTLINE_BLANK
                cor_check = SUCCESS_GREEN if concluida else cores.get("text_muted", TEXT_MUTED)
                
                txt_titulo = ft.Text(
                    q["titulo"],
                    size=12,
                    color=cores.get("text_muted", TEXT_MUTED) if concluida else cores.get("text_primary", TEXT_PRIMARY),
                    weight=ft.FontWeight.W_500,
                    style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH if concluida else ft.TextDecoration.NONE),
                    expand=True
                )
                
                badge_cat = ft.Container(
                    content=ft.Text(q.get("categoria", "Diária"), size=9, color=cor_cat, weight=ft.FontWeight.BOLD),
                    padding=padding_symmetric(horizontal=5, vertical=2),
                    border_radius=border_radius_all(4),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, cor_cat)
                )
                
                badge_recompensa = ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.AUTO_AWESOME, size=12, color=cores["light"]),
                        ft.Text(f"+{q.get('recompensa_exp', 25)} EXP", size=10, color=cores["light"], weight=ft.FontWeight.BOLD)
                    ],
                    spacing=2
                )
                
                badge_ouro = ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.SAVINGS, size=12, color=GOLD_LIGHT),
                        ft.Text(f"+{q.get('recompensa_ouro', 15):.0f} O", size=10, color=GOLD_LIGHT, weight=ft.FontWeight.BOLD)
                    ],
                    spacing=2
                )

                itens_rodape_quest = [badge_cat, badge_ouro, badge_recompensa]
                if q.get("horario"):
                    badge_horario = ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("⏰", size=10),
                                ft.Text(q["horario"], size=10, weight=ft.FontWeight.BOLD, color=cores["light"])
                            ],
                            spacing=2
                        ),
                        padding=padding_symmetric(horizontal=4, vertical=2),
                        border_radius=border_radius_all(4),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores["primary"])
                    )
                    itens_rodape_quest.append(badge_horario)

                card_quest = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=check_icon,
                                icon_color=cor_check,
                                icon_size=22,
                                on_click=lambda e, qid=q["id"]: alternar_conclusao_quest(qid),
                                style=ft.ButtonStyle(padding=padding_all(4))
                            ),
                            ft.Column(
                                controls=[
                                    txt_titulo,
                                    ft.Row(
                                        controls=itens_rodape_quest,
                                        spacing=4,
                                        wrap=True,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    )
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color="#64748B",
                                icon_size=18,
                                on_click=lambda e, qid=q["id"]: excluir_quest(qid),
                                style=ft.ButtonStyle(padding=padding_all(4))
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2
                    ),
                    padding=padding_symmetric(horizontal=6, vertical=4),
                    border_radius=border_radius_all(8),
                    bgcolor=cores["bg_input"] if concluida else cores["bg_card"],
                    border=border_all(1, "#1E3A2F" if concluida else cores.get("border_subtle", "#2D2D3D"))
                )
                cards.append(card_quest)
                
            lista_quests_col.controls = cards

        try:
            lista_quests_col.update()
        except Exception:
            pass

    def abrir_modal_nova_quest(e):
        txt_novo_titulo = ft.TextField(
            label="Título da Missão",
            hint_text="Ex: Ler 10 páginas arcanas",
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            text_size=13,
            color=cores.get("text_primary", TEXT_PRIMARY)
        )
        
        dropdown_categoria = ft.Dropdown(
            label="Categoria da Missão",
            options=[
                ft.dropdown.Option("Principal"),
                ft.dropdown.Option("Diária"),
                ft.dropdown.Option("Coroa"),
                ft.dropdown.Option("Secundária")
            ],
            value="Diária",
            bgcolor=cores["bg_surface"],
            border_color=cores.get("border_subtle", "#36364A"),
            color=cores.get("text_primary", TEXT_PRIMARY)
        )
        
        dropdown_dificuldade = ft.Dropdown(
            label="Dificuldade / Recompensa",
            options=[
                ft.dropdown.Option("Fácil", "Fácil (+15 Ouro, +20 EXP)"),
                ft.dropdown.Option("Média", "Média (+30 Ouro, +40 EXP)"),
                ft.dropdown.Option("Difícil", "Difícil (+50 Ouro, +70 EXP)"),
                ft.dropdown.Option("Lendária", "Lendária (+100 Ouro, +150 EXP)")
            ],
            value="Média",
            bgcolor=cores["bg_surface"],
            border_color=cores.get("border_subtle", "#36364A"),
            color=cores.get("text_primary", TEXT_PRIMARY)
        )

        txt_horario = ft.TextField(
            label="Horário (Opcional)",
            hint_text="Ex: 14:30",
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            text_size=13,
            color=cores.get("text_primary", TEXT_PRIMARY)
        )

        def salvar_nova_quest(e_salvar):
            titulo = txt_novo_titulo.value
            if not titulo or not titulo.strip():
                txt_novo_titulo.error_text = "Dê um nome à sua missão régia!"
                txt_novo_titulo.update()
                return
                
            storage.adicionar_quest(
                titulo=titulo.strip(),
                categoria=dropdown_categoria.value,
                dificuldade=dropdown_dificuldade.value,
                data_limite=estado["dia_selecionado"],
                horario=txt_horario.value.strip() if txt_horario.value else None
            )
            
            fechar_modal(dialogo)
            mostrar_notificacao(page, "Nova missão proclamada no reino!", sucesso=True)
            renderizar_quests()
            renderizar_calendario()
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
                    icon_nobre(ft.Icons.AUTO_AWESOME, color=cores["light"], size=20),
                    ft.Text("Proclamar Nova Quest", size=15, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        txt_novo_titulo,
                        dropdown_categoria,
                        dropdown_dificuldade,
                        txt_horario
                    ],
                    spacing=8,
                    tight=True,
                    scroll=ft.ScrollMode.ADAPTIVE
                ),
                width=320,
                constraints=ft.BoxConstraints(max_height=380)
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo)),
                botao_preenchido("Salvar Quest", on_click=salvar_nova_quest, bgcolor=cores["primary"])
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

    btn_nova_quest = criar_botao_primario(
        texto="Proclamar Nova Quest",
        icone=ft.Icons.ADD_TASK,
        on_click=abrir_modal_nova_quest,
        expand=True
    )

    mural_quests = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        lbl_data_selecionada,
                        icon_nobre(ft.Icons.SWORDS, size=16, color=cores["light"]) if hasattr(ft.Icons, "SWORDS") else icon_nobre(ft.Icons.SHIELD, size=16, color=cores["light"])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#36364A")),
                lista_quests_col,
                ft.Container(height=4),
                ft.Row(controls=[btn_nova_quest])
            ],
            spacing=8
        ),
        borda_roxa=True,
        padding=10
    )

    renderizar_calendario()
    renderizar_quests()

    return ft.ListView(
        controls=[
            calendario_card,
            mural_quests,
            ft.Container(height=24)
        ],
        spacing=10,
        padding=10,
        expand=True
    )
