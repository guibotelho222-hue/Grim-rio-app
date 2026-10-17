"""
Grimório Mobile - Mascote Guardião Alado
Composição vetorial e imagem do gato em armadura com asas.
"""

import os
import flet as ft
from theme import (
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_CONTAINER,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_DARK,
    TEXT_PRIMARY, TEXT_SECONDARY, BG_CARD,
    border_all, border_radius_only, border_radius_all,
    padding_all, padding_only, icon_nobre, resolve_path
)

def criar_mascote_vetorial(tamanho: int = 160, animar_aura: bool = True) -> ft.Control:
    """
    Constrói o Mascote Guardião Alado diretamente em código Flet:
    - Felino sagrado com armadura de prata e ouro
    - Asas arcanas de éter e iluminação de fundo
    - Escudo do reino e espada mística
    """
    scale = tamanho / 180.0
    
    aura_fundo = ft.Container(
        width=int(170 * scale),
        height=int(170 * scale),
        border_radius=int(85 * scale),
        gradient=ft.RadialGradient(
            colors=["#3B1F6E", "#1F1238", "transparent"],
            center=ft.Alignment(0, 0),
            radius=0.9
        ),
        opacity=0.85
    )
    
    asa_esquerda = ft.Container(
        content=icon_nobre(
            ft.Icons.AIR,
            size=int(48 * scale),
            color=PURPLE_LIGHT,
        ),
        rotate=ft.Rotate(-0.4),
        offset=ft.Offset(x=-0.45 * scale, y=-0.15 * scale),
        opacity=0.9
    )
    
    asa_direita = ft.Container(
        content=icon_nobre(
            ft.Icons.AIR,
            size=int(48 * scale),
            color=PURPLE_LIGHT,
        ),
        rotate=ft.Rotate(0.4),
        offset=ft.Offset(x=0.45 * scale, y=-0.15 * scale),
        opacity=0.9
    )
    
    asa_dourada_esq = ft.Container(
        content=icon_nobre(
            ft.Icons.AUTO_AWESOME,
            size=int(24 * scale),
            color=GOLD_LIGHT,
        ),
        offset=ft.Offset(x=-0.55 * scale, y=-0.35 * scale),
    )
    
    asa_dourada_dir = ft.Container(
        content=icon_nobre(
            ft.Icons.AUTO_AWESOME,
            size=int(24 * scale),
            color=GOLD_LIGHT,
        ),
        offset=ft.Offset(x=0.55 * scale, y=-0.35 * scale),
    )

    peitoral_armadura = ft.Container(
        width=int(74 * scale),
        height=int(78 * scale),
        border_radius=border_radius_only(
            top_left=int(16 * scale),
            top_right=int(16 * scale),
            bottom_left=int(26 * scale),
            bottom_right=int(26 * scale)
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#3A3A4C", "#20202E", "#151520"]
        ),
        border=border_all(int(2 * scale), GOLD_PRIMARY),
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color="#D4AF3740",
            offset=ft.Offset(0, 2)
        )
    )

    brasao_escudo = ft.Container(
        content=icon_nobre(
            ft.Icons.SHIELD,
            size=int(32 * scale),
            color=GOLD_PRIMARY,
        ),
        offset=ft.Offset(0, 0.18 * scale)
    )
    
    gema_coracao = ft.Container(
        width=int(12 * scale),
        height=int(12 * scale),
        border_radius=int(6 * scale),
        bgcolor=PURPLE_LIGHT,
        border=border_all(1, "#FFFFFF"),
        offset=ft.Offset(0, 0.18 * scale),
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=6, color="#A78BFA")
    )

    cabeca_gato = ft.Container(
        width=int(68 * scale),
        height=int(64 * scale),
        border_radius=int(32 * scale),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=["#47475E", "#2E2E3E"]
        ),
        border=border_all(int(2 * scale), "#6E6E8A"),
        alignment=ft.Alignment(0, 0),
        offset=ft.Offset(0, -0.32 * scale)
    )

    orelha_esq = ft.Container(
        width=int(18 * scale),
        height=int(18 * scale),
        border_radius=border_radius_only(top_left=int(12 * scale)),
        gradient=ft.LinearGradient(colors=[GOLD_PRIMARY, "#3A3A4C"]),
        rotate=ft.Rotate(-0.3),
        offset=ft.Offset(x=-0.22 * scale, y=-0.56 * scale)
    )

    orelha_dir = ft.Container(
        width=int(18 * scale),
        height=int(18 * scale),
        border_radius=border_radius_only(top_right=int(12 * scale)),
        gradient=ft.LinearGradient(colors=[GOLD_PRIMARY, "#3A3A4C"]),
        rotate=ft.Rotate(0.3),
        offset=ft.Offset(x=0.22 * scale, y=-0.56 * scale)
    )
    
    rosto_felino = ft.Container(
        content=icon_nobre(
            ft.Icons.PETS,
            size=int(26 * scale),
            color="#E2E8F0"
        ),
        offset=ft.Offset(0, -0.32 * scale)
    )

    espada_sagrada = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    width=int(5 * scale),
                    height=int(55 * scale),
                    gradient=ft.LinearGradient(
                        colors=["#FFFFFF", "#CBD5E1", "#94A3B8"]
                    ),
                    border_radius=int(2 * scale),
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color="#FFFFFF80")
                ),
                ft.Container(
                    width=int(22 * scale),
                    height=int(5 * scale),
                    bgcolor=GOLD_PRIMARY,
                    border_radius=int(2 * scale)
                ),
                ft.Container(
                    width=int(4 * scale),
                    height=int(14 * scale),
                    bgcolor="#78350F"
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        offset=ft.Offset(x=0.36 * scale, y=-0.08 * scale)
    )

    mascote_stack = ft.Stack(
        controls=[
            aura_fundo,
            asa_esquerda,
            asa_direita,
            asa_dourada_esq,
            asa_dourada_dir,
            orelha_esq,
            orelha_dir,
            peitoral_armadura,
            brasao_escudo,
            gema_coracao,
            cabeca_gato,
            rosto_felino,
            espada_sagrada
        ],
        alignment=ft.Alignment(0, 0),
        width=int(170 * scale),
        height=int(170 * scale)
    )

    return ft.Container(
        content=mascote_stack,
        alignment=ft.Alignment(0, 0),
        padding=padding_all(int(4 * scale))
    )

def criar_card_mascote_interativo(tamanho: int = 140, exibir_foto: bool = True) -> ft.Control:
    caminho_imagem = resolve_path("assets/mascote.png")
    if not os.path.exists(caminho_imagem):
        caminho_imagem = resolve_path("assets/gatinho_cavaleiro.png")
    
    if exibir_foto and os.path.exists(caminho_imagem):
        return ft.Container(
            content=ft.Image(
                src=caminho_imagem,
                width=tamanho,
                height=tamanho,
                fit="contain"
            ),
            width=tamanho + 16,
            height=tamanho + 16,
            alignment=ft.Alignment(0, 0),
            border_radius=border_radius_all(16),
            gradient=ft.RadialGradient(
                colors=["#2D1B4E80", "transparent"],
                center=ft.Alignment(0, 0)
            )
        )
    
    return criar_mascote_vetorial(tamanho=tamanho)
