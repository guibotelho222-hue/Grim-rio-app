"""
Grimório Mobile - Splash Screen (Tela de Início Oficial para Android)
Card com Logo do Gatinho Cavaleiro, Borda Dourada e Transição Direta ao Toque.
"""

import os
import flet as ft
from theme import (
    BG_DARK, BG_SURFACE, GOLD_PRIMARY, GOLD_LIGHT,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_DARK,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    border_all, border_radius_all, padding_symmetric, icon_nobre,
    resolve_path
)

def criar_splash_screen(on_entrar_click) -> ft.Control:
    """
    Constrói a Splash Screen oficial do Grimório Mobile:
    - Card refinado com a arte oficial do Gatinho Cavaleiro
    - Borda dourada (#D4AF37) com iluminação sutil
    - Título 'GRIMÓRIO' e subtítulo 'Dark Fantasy & Gestão do Reino'
    - Totalmente adaptada para telas verticais de smartphone (Portrait)
    """

    # Busca a logo oficial
    caminho_logo = resolve_path("assets/logo.png")
    if not os.path.exists(caminho_logo):
        caminho_logo = resolve_path("assets/gatinho_cavaleiro.png")
    if not os.path.exists(caminho_logo):
        caminho_logo = resolve_path("assets/logo.ico")

    # Card Nobre do Gatinho Cavaleiro (Tamanho ideal para celular: 170x170)
    card_gatinho_logo = ft.Container(
        content=ft.Image(
            src=caminho_logo,
            width=150,
            height=150,
            fit="contain"
        ),
        width=176,
        height=176,
        alignment=ft.Alignment(0, 0),
        border_radius=border_radius_all(24),
        bgcolor="#181524",
        border=border_all(2, GOLD_PRIMARY),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=18,
            color="#D4AF3740",
            offset=ft.Offset(0, 4)
        )
    )

    # Título Principal
    titulo = ft.Text(
        "GRIMÓRIO",
        size=34,
        weight=ft.FontWeight.BOLD,
        color=GOLD_LIGHT,
        text_align=ft.TextAlign.CENTER
    )

    # Subtítulo Oficial
    subtitulo = ft.Text(
        "Dark Fantasy & Gestão do Reino",
        size=13,
        color=TEXT_SECONDARY,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_400
    )

    # Botão de Entrada Mobile (Touch Target Amplo e Confortável)
    btn_entrar = ft.Container(
        content=ft.Row(
            controls=[
                icon_nobre(ft.Icons.AUTO_AWESOME, color="#121214", size=18),
                ft.Text("Toque para Entrar", color="#121214", weight=ft.FontWeight.BOLD, size=15),
                icon_nobre(ft.Icons.ARROW_FORWARD, color="#121214", size=18)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        ),
        height=52,
        padding=padding_symmetric(horizontal=32, vertical=12),
        border_radius=border_radius_all(26),
        gradient=ft.LinearGradient(
            colors=[GOLD_LIGHT, GOLD_PRIMARY, "#B8860B"]
        ),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=14,
            color="#D4AF3780",
            offset=ft.Offset(0, 4)
        ),
        on_click=lambda e: on_entrar_click(),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
    )

    rodape = ft.Text(
        "Crônicas e Glórias de Eldoria • v2.0",
        size=11,
        color=TEXT_MUTED,
        italic=True,
        text_align=ft.TextAlign.CENTER
    )

    conteudo_splash = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                card_gatinho_logo,
                ft.Container(height=16),
                titulo,
                ft.Container(height=4),
                subtitulo,
                ft.Container(height=28),
                btn_entrar,
                ft.Container(expand=True),
                rodape,
                ft.Container(height=16)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        ),
        gradient=ft.RadialGradient(
            colors=["#1D1530", "#14141B", BG_DARK],
            center=ft.Alignment(0, -0.2),
            radius=1.2
        ),
        expand=True,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: on_entrar_click()
    )

    return conteudo_splash
