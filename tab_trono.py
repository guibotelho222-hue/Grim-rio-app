"""
Grimório - Aba 1: Trono Real (Dedicada Exclusivamente ao Rei Joaquim)
Ilustração Nobre do Rei Joaquim no Trono, Balão de Afeto e Audiência Real com Acolhimento Imediato
"""

import os
import random
import flet as ft
from theme import (
    BG_DARK, BG_SURFACE, BG_CARD, BG_CARD_LIGHT, BG_INPUT,
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_CONTAINER, BORDER_GOLD,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_CONTAINER, BORDER_PURPLE,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS_GREEN, HP_RED, MANA_BLUE, BORDER_RADIUS,
    border_all, border_radius_all, padding_all, padding_symmetric, icon_nobre,
    botao_preenchido, get_theme_colors, resolve_path
)
from storage import storage
from oracle import FRASES_REI_ACOLHEDORAS, gerar_resposta_rei
from components.common_ui import criar_card_nobre, mostrar_notificacao

def criar_aba_trono(page: ft.Page, on_update_callback=None) -> ft.Control:
    """
    Retorna a Sala do Trono reformulada:
    Ambiente visualmente lindo, acolhedor e cheio de afeto,
    homenageando o filho (Pequeno Rei Joaquim) e a esposa (a Rainha).
    """

    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    nome_rainha = cfg.get("nome_rainha", "Minha Rainha")

    # Estado local da aba
    humor_selecionado = {"valor": "Tranquila"}
    frase_rei_atual = {"texto": random.choice(FRASES_REI_ACOLHEDORAS)}
    
    balao_dialogo_txt = ft.Text(
        frase_rei_atual["texto"],
        color=cores.get("text_primary", TEXT_PRIMARY),
        size=13,
        italic=True,
        weight=ft.FontWeight.W_400
    )
    
    resposta_rei_container = ft.Column(visible=False, spacing=6)
    
    txt_desabafo = ft.TextField(
        hint_text=f"Conte ao Pequeno Joaquim o que está no seu coração hoje, {nome_rainha}... Ele está pronto para te ouvir e te abraçar.",
        hint_style=ft.TextStyle(color=cores.get("text_muted", TEXT_MUTED), size=12),
        multiline=True,
        min_lines=2,
        max_lines=5,
        bgcolor=cores["bg_input"],
        border_color=cores.get("border_subtle", "#36364A"),
        focused_border_color=cores["primary"],
        text_size=13,
        color=cores.get("text_primary", TEXT_PRIMARY),
        border_radius=10
    )

    # 1. Ilustração Central: Nova Imagem do Pequeno Rei no Trono em Cartão Pergaminho com Luz Dourada
    caminho_rei_trono = resolve_path("assets/rei_joaquim_trono.png")
    
    card_rei_destaque = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=caminho_rei_trono,
                        height=195,
                        fit="cover",
                        border_radius=border_radius_all(14)
                    ),
                    alignment=ft.Alignment(0, 0),
                    border_radius=border_radius_all(16),
                    bgcolor="#181424",
                    border=border_all(2, "#D4AF37"),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=20,
                        color="#D4AF3740",
                        offset=ft.Offset(0, 4)
                    )
                ),
                ft.Text(
                    "Sua Majestade, Rei Joaquim • O Pequeno Guardião do Nosso Reino",
                    weight=ft.FontWeight.BOLD,
                    size=13,
                    color=cores["light"],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Onde habita o amor mais puro do nosso castelo e a fortaleza da nossa família",
                    size=11,
                    color=cores.get("text_secondary", TEXT_SECONDARY),
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6
        ),
        alignment=ft.Alignment(0, 0),
        padding=padding_symmetric(vertical=4)
    )
    
    # 2. Mensagem do Pequeno Rei: Balão de Diálogo Elegante & Destacado
    def mudar_frase_rei():
        nova_frase = random.choice(FRASES_REI_ACOLHEDORAS)
        balao_dialogo_txt.value = nova_frase
        balao_dialogo_txt.update()

    btn_ouvir_rei = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("💖", size=14),
                ft.Text("Ouvir o Pequeno Rei", size=12, weight=ft.FontWeight.BOLD, color="#121214")
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=padding_symmetric(horizontal=16, vertical=8),
        border_radius=border_radius_all(18),
        bgcolor=cores["primary"],
        on_click=lambda e: mudar_frase_rei(),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color="#D4AF3740",
            offset=ft.Offset(0, 2)
        ),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
    )

    balao_dialogo = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("💖", size=15),
                        ft.Text(f"Voz do Pequeno Rei Joaquim à {nome_rainha}", weight=ft.FontWeight.BOLD, color=cores["light"], size=13),
                    ],
                    spacing=6
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#3A3422")),
                balao_dialogo_txt,
                ft.Row(
                    controls=[btn_ouvir_rei],
                    alignment=ft.MainAxisAlignment.END
                )
            ],
            spacing=8
        ),
        padding=12,
        borda_dourada=True
    )

    # 3. Espaço de Audiência Íntima: Expressar sentimentos e receber carinho
    humores = [
        ("Tranquila", "🌿", "#10B981"),
        ("Radiante", "☀️", "#EAB308"),
        ("Cansada", "🌙", "#64748B"),
        ("Ansiosa", "🌪️", "#8B5CF6"),
        ("Sobrecarregada", "⚡", "#F97316"),
        ("Com Saudade", "💖", "#EC4899")
    ]
    
    humor_buttons = []
    
    def selecionar_humor(nome_humor):
        humor_selecionado["valor"] = nome_humor
        for btn, h_nome in humor_buttons:
            is_sel = (h_nome == nome_humor)
            btn.bgcolor = cores["primary"] if is_sel else cores["bg_input"]
            btn.border = border_all(1, cores["light"] if is_sel else cores.get("border_subtle", "#2C2C3D"))
            btn.update()

    botoes_humor_row = ft.Row(wrap=True, spacing=6)
    
    for nome, emoji, cor in humores:
        is_sel = (nome == humor_selecionado["valor"])
        btn_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(emoji, size=13),
                    ft.Text(nome, size=11, color=cores.get("text_primary", TEXT_PRIMARY), weight=ft.FontWeight.W_500)
                ],
                spacing=4,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=padding_symmetric(horizontal=10, vertical=6),
            border_radius=border_radius_all(8),
            bgcolor=cores["primary"] if is_sel else cores["bg_input"],
            border=border_all(1, cores["light"] if is_sel else cores.get("border_subtle", "#2C2C3D")),
            on_click=lambda e, n=nome: selecionar_humor(n),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
        )
        humor_buttons.append((btn_container, nome))
        botoes_humor_row.controls.append(btn_container)

    def enviar_audiencia(e):
        texto = txt_desabafo.value or ""
        humor = humor_selecionado["valor"]
        resposta = gerar_resposta_rei(humor, texto)
        
        storage.registrar_emocional(humor, texto, resposta)
        
        balao_dialogo_txt.value = resposta
        balao_dialogo_txt.update()
        
        resposta_rei_container.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("💖", size=16),
                                ft.Text("Palavras Reconfortantes do Pequeno Joaquim:", weight=ft.FontWeight.BOLD, color=cores["light"], size=13)
                            ],
                            spacing=6
                        ),
                        ft.Text(resposta, color=cores.get("text_primary", TEXT_PRIMARY), size=12, italic=True)
                    ],
                    spacing=6
                ),
                padding=12,
                border_radius=border_radius_all(10),
                bgcolor=cores["container"],
                border=border_all(1, cores["secondary"])
            )
        ]
        resposta_rei_container.visible = True
        txt_desabafo.value = ""
        txt_desabafo.update()
        resposta_rei_container.update()
        
        mostrar_notificacao(page, f"O Pequeno Joaquim acolheu seu coração com todo o amor, {nome_rainha}!", sucesso=True)
        if on_update_callback:
            on_update_callback()

    btn_solicitar_audiencia = botao_preenchido(
        texto="Pedir Acolhimento do Pequeno Rei",
        icon=ft.Icons.FAVORITE,
        bgcolor=cores["primary"],
        color="#121214",
        on_click=enviar_audiencia
    )

    secao_audiencia = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.FAVORITE_BORDER, size=18, color=HP_RED),
                        ft.Text("Audiência Íntima do Castelo", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=14)
                    ],
                    spacing=6
                ),
                ft.Text("Como está o coração da Rainha hoje?", size=12, color=cores.get("text_secondary", TEXT_SECONDARY), weight=ft.FontWeight.W_500),
                botoes_humor_row,
                ft.Container(height=4),
                txt_desabafo,
                ft.Row(controls=[btn_solicitar_audiencia], alignment=ft.MainAxisAlignment.CENTER),
                resposta_rei_container
            ],
            spacing=10
        ),
        borda_roxa=True
    )

    return ft.ListView(
        controls=[
            card_rei_destaque,
            balao_dialogo,
            secao_audiencia,
            ft.Container(height=30)
        ],
        spacing=14,
        padding=12,
        expand=True
    )
