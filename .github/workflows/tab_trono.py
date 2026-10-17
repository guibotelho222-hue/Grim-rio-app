"""
Grimório Mobile - Aba 1: Trono Real (Dedicada ao Rei Joaquim & Sir Fagulha)
Ilustração Nobre do Rei Joaquim, Balão de Afeto, Audiência Real e Cuidados com o Pet Guardião.
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
    """Retorna a Sala do Trono Mobile com responsividade vertical e toque suave."""
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    nome_rainha = cfg.get("nome_rainha", "Minha Rainha")

    # Estado local
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
        hint_text=f"Conte ao Pequeno Joaquim o que está no seu coração hoje, {nome_rainha}...",
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

    # 1. Ilustração do Pequeno Rei no Trono
    caminho_rei_trono = resolve_path("assets/rei_joaquim_trono.png")
    
    card_rei_destaque = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=caminho_rei_trono,
                        height=180,
                        fit="contain",
                        border_radius=border_radius_all(14)
                    ),
                    alignment=ft.Alignment(0, 0),
                    border_radius=border_radius_all(16),
                    bgcolor="#181424",
                    border=border_all(2, "#D4AF37"),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=18,
                        color="#D4AF3740",
                        offset=ft.Offset(0, 4)
                    )
                ),
                ft.Text(
                    "Sua Majestade, Rei Joaquim • O Pequeno Guardião",
                    weight=ft.FontWeight.BOLD,
                    size=13,
                    color=cores["light"],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "O amor mais puro do nosso castelo e a fortaleza da nossa família",
                    size=11,
                    color=cores.get("text_secondary", TEXT_SECONDARY),
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4
        ),
        alignment=ft.Alignment(0, 0),
        padding=padding_symmetric(vertical=2)
    )
    
    # 2. Balão de Diálogo do Rei
    def mudar_frase_rei():
        nova_frase = random.choice(FRASES_REI_ACOLHEDORAS)
        balao_dialogo_txt.value = nova_frase
        balao_dialogo_txt.update()

    btn_ouvir_rei = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("👑", size=14),
                ft.Text("Ouvir o Pequeno Rei", size=11, weight=ft.FontWeight.BOLD, color="#121214")
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=padding_symmetric(horizontal=12, vertical=6),
        border_radius=border_radius_all(16),
        bgcolor=cores["primary"],
        on_click=lambda e: mudar_frase_rei(),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color="#D4AF3740",
            offset=ft.Offset(0, 2)
        )
    )

    balao_dialogo = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("👑", size=15),
                        ft.Text(f"Voz do Pequeno Rei Joaquim • {nome_rainha}", weight=ft.FontWeight.BOLD, color=cores["light"], size=12),
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
            spacing=6
        ),
        padding=10,
        borda_dourada=True
    )

    # 3. Audiência Real com Seleção de Humor
    humores = [
        ("Tranquila", "🌿", "#10B981"),
        ("Radiante", "✨", "#EAB308"),
        ("Cansada", "🌙", "#64748B"),
        ("Ansiosa", "🔮", "#8B5CF6"),
        ("Sobrecarregada", "🔥", "#F97316"),
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
                    ft.Text(emoji, size=12),
                    ft.Text(nome, size=11, color=cores.get("text_primary", TEXT_PRIMARY), weight=ft.FontWeight.W_500)
                ],
                spacing=4,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=padding_symmetric(horizontal=8, vertical=6),
            border_radius=border_radius_all(8),
            bgcolor=cores["primary"] if is_sel else cores["bg_input"],
            border=border_all(1, cores["light"] if is_sel else cores.get("border_subtle", "#2C2C3D")),
            on_click=lambda e, n=nome: selecionar_humor(n)
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
                                ft.Text("👑", size=15),
                                ft.Text("Palavras do Pequeno Joaquim:", weight=ft.FontWeight.BOLD, color=cores["light"], size=12)
                            ],
                            spacing=6
                        ),
                        ft.Text(resposta, color=cores.get("text_primary", TEXT_PRIMARY), size=12, italic=True)
                    ],
                    spacing=4
                ),
                padding=10,
                border_radius=border_radius_all(10),
                bgcolor=cores["container"],
                border=border_all(1, cores["secondary"])
            )
        ]
        resposta_rei_container.visible = True
        txt_desabafo.value = ""
        txt_desabafo.update()
        resposta_rei_container.update()
        
        mostrar_notificacao(page, f"O Pequeno Joaquim acolheu seu coração, {nome_rainha}!", sucesso=True)
        if on_update_callback:
            on_update_callback()

    btn_solicitar_audiencia = botao_preenchido(
        texto="Pedir Acolhimento do Rei",
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
                        icon_nobre(ft.Icons.FAVORITE_BORDER, size=16, color=HP_RED),
                        ft.Text("Audiência Íntima do Castelo", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=13)
                    ],
                    spacing=6
                ),
                ft.Text("Como está o coração da Rainha hoje?", size=11, color=cores.get("text_secondary", TEXT_SECONDARY)),
                botoes_humor_row,
                ft.Container(height=2),
                txt_desabafo,
                ft.Row(controls=[btn_solicitar_audiencia], alignment=ft.MainAxisAlignment.CENTER),
                resposta_rei_container
            ],
            spacing=8
        ),
        borda_roxa=True
    )

    # 4. Card do Mascote Sir Fagulha (Cuidados Rápidos)
    pet = storage.data["pet"]
    afeto = pet.get("nivel_afeto", 100)
    energia = pet.get("energia", 80)
    fome = pet.get("fome", 90)

    lbl_pet_status = ft.Text(
        f"Sir Fagulha • Afeto {afeto}% | Energia {energia}% | Saciedade {fome}%",
        size=11,
        color=cores.get("text_secondary", TEXT_SECONDARY),
        weight=ft.FontWeight.W_500
    )

    def acao_alimentar(e):
        novo = storage.alimentar_pet()
        lbl_pet_status.value = f"Sir Fagulha • Afeto {novo['nivel_afeto']}% | Energia {novo['energia']}% | Saciedade {novo['fome']}%"
        lbl_pet_status.update()
        mostrar_notificacao(page, "Sir Fagulha saboreou o banquete real (+10 EXP)!", sucesso=True)
        if on_update_callback:
            on_update_callback()

    def acao_brincar(e):
        novo = storage.brincar_pet()
        lbl_pet_status.value = f"Sir Fagulha • Afeto {novo['nivel_afeto']}% | Energia {novo['energia']}% | Saciedade {novo['fome']}%"
        lbl_pet_status.update()
        mostrar_notificacao(page, "Sir Fagulha voou pelos salões e está radiante (+15 EXP)!", sucesso=True)
        if on_update_callback:
            on_update_callback()

    card_pet = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.PETS, size=16, color=cores["light"]),
                        ft.Text("Sir Fagulha • Gatinho Alado Guardião", weight=ft.FontWeight.BOLD, color=cores["light"], size=12),
                    ],
                    spacing=6
                ),
                lbl_pet_status,
                ft.Row(
                    controls=[
                        ft.OutlinedButton("Alimentar", icon=ft.Icons.RESTAURANT, on_click=acao_alimentar),
                        ft.OutlinedButton("Brincar", icon=ft.Icons.AUTO_AWESOME, on_click=acao_brincar),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8
                )
            ],
            spacing=8
        )
    )

    return ft.ListView(
        controls=[
            card_rei_destaque,
            balao_dialogo,
            card_pet,
            secao_audiencia,
            ft.Container(height=24)
        ],
        spacing=10,
        padding=10,
        expand=True
    )
