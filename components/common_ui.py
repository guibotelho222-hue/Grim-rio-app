"""
Grimório - Componentes de UI Comuns, Header Fixo, Influência Lunar & Configurações
Header Fixo: [Engrenagem Configs] + [Fase da Lua Interativa] + [Runa Diária] + [Nível/Reserva de Ouro]
Pop-up da Influência Lunar & Módulo de Configurações Dinâmico
"""

import flet as ft
from theme import (
    BG_CARD, BG_CARD_LIGHT, BG_SURFACE, BG_INPUT,
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_CONTAINER, BORDER_GOLD,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_CONTAINER, BORDER_PURPLE,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS_GREEN, DANGER_RED, BORDER_RADIUS, TEMAS,
    border_all, border_only, border_radius_all,
    padding_all, padding_symmetric, padding_only, icon_nobre,
    botao_preenchido, calcular_fase_lua, obter_influencia_lunar,
    get_theme_colors, aplicar_tema
)
from storage import storage
from oracle import sortear_runa

def criar_card_nobre(
    conteudo: ft.Control,
    padding: int = 16,
    borda_dourada: bool = False,
    borda_roxa: bool = False,
    bgcolor: str = None
) -> ft.Container:
    """Card padrão Dark Fantasy com cantos arredondados e borda sutil dependente do tema ativo."""
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    
    cor_fundo = bgcolor if bgcolor is not None else cores["bg_card"]
    
    border = None
    if borda_dourada:
        border = border_all(1, cores["border_color"])
    elif borda_roxa:
        border = border_all(1, cores["secondary"])
    else:
        border = border_all(1, cores.get("border_subtle", "#262636"))
        
    return ft.Container(
        content=conteudo,
        padding=padding_all(padding),
        border_radius=border_radius_all(BORDER_RADIUS),
        bgcolor=cor_fundo,
        border=border,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color="#00000040",
            offset=ft.Offset(0, 3)
        )
    )

def abrir_modal_influencia_lunar(page: ft.Page):
    """
    Pop-up/Modal com a Influência Lunar do Reino:
    1. Fase da Lua Atual (com ícone e nome).
    2. Influência Lunar do Dia (clareza, foco e abundância).
    3. Orientação Arcana (dica prática de produtividade/bem-estar).
    Botão de fechamento: 'Abençoado seja o Luar Arcano'
    """
    if not page:
        return

    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    dados_lua = obter_influencia_lunar()

    def fechar_modal(dlg):
        if hasattr(page, "pop_dialog"):
            page.pop_dialog()
        else:
            dlg.open = False
            page.update()

    card_fase_atual = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(dados_lua["emoji"], size=36),
                ft.Column(
                    controls=[
                        ft.Text(dados_lua["nome"], size=16, weight=ft.FontWeight.BOLD, color=cores["light"]),
                        ft.Text("Fase Celeste Ativa sobre o Reino", size=11, color=cores.get("text_secondary", TEXT_SECONDARY))
                    ],
                    spacing=2
                )
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=12,
        border_radius=border_radius_all(10),
        bgcolor=cores["bg_input"],
        border=border_all(1, cores["border_color"])
    )

    card_influencia = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.AUTO_AWESOME, size=16, color=cores["light"]),
                        ft.Text("Influência Lunar do Dia", weight=ft.FontWeight.BOLD, color=cores["light"], size=13),
                    ],
                    spacing=6
                ),
                ft.Text(
                    dados_lua["influencia"],
                    size=12,
                    color=cores.get("text_primary", TEXT_PRIMARY)
                )
            ],
            spacing=6
        ),
        padding=12,
        border_radius=border_radius_all(10),
        bgcolor=cores["bg_card_light"],
        border=border_all(1, cores.get("border_subtle", "#36364A"))
    )

    card_orientacao = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.COMPASS_CALIBRATION, size=16, color=cores["secondary_light"]),
                        ft.Text("Orientação Arcana", weight=ft.FontWeight.BOLD, color=cores["secondary_light"], size=13),
                    ],
                    spacing=6
                ),
                ft.Text(
                    dados_lua["orientacao"],
                    size=12,
                    color=cores.get("text_primary", TEXT_PRIMARY),
                    italic=True
                )
            ],
            spacing=6
        ),
        padding=12,
        border_radius=border_radius_all(10),
        bgcolor=cores["container"],
        border=border_all(1, cores["secondary"])
    )

    btn_fechar = botao_preenchido(
        texto="Abençoado seja o Luar Arcano",
        bgcolor=cores["primary"],
        color="#121214",
        icon=ft.Icons.CHECK,
        on_click=lambda e: fechar_modal(dialogo_lua)
    )

    dialogo_lua = ft.AlertDialog(
        title=ft.Row(
            controls=[
                icon_nobre(ft.Icons.NIGHTLIGHT_ROUND, color=cores["light"], size=22),
                ft.Text("Influência Lunar do Reino", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
            ],
            spacing=8
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    card_fase_atual,
                    card_influencia,
                    card_orientacao
                ],
                spacing=12,
                tight=True
            ),
            width=360
        ),
        actions=[
            ft.Row(
                controls=[btn_fechar],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=cores["bg_card"],
        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
    )

    if hasattr(page, "show_dialog"):
        page.show_dialog(dialogo_lua)
    else:
        page.dialog = dialogo_lua
        dialogo_lua.open = True
        page.update()

def abrir_modal_oraculo_runas(page: ft.Page, on_update_callback=None):
    """
    Pop-up/Pergaminho 'Oráculo Sagrado das Runas':
    - Exibe a Runa Diária com frase poética e medieval profunda e reflexiva (SEM BUFFS OU XP).
    - Botão '🔮 Tirar Runa do Dia' para sortear nova leitura arcana em tempo real.
    - Botão de fechamento estilizado com o texto: 'Agradeço aos Deuses Arcanos'.
    """
    if not page:
        return

    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    
    ultima_runa = storage.data.get("emocional", {}).get("ultima_runa", {})
    if not ultima_runa or "simbolo" not in ultima_runa:
        ultima_runa = sortear_runa()
        storage.salvar_runa(ultima_runa)

    txt_simbolo = ft.Text(ultima_runa.get("simbolo", "ᛉ"), size=52, color=cores["light"], weight=ft.FontWeight.BOLD)
    txt_nome = ft.Text(ultima_runa.get("nome", "Runa Sagrada"), size=17, weight=ft.FontWeight.BOLD, color=cores["light"])
    txt_elemento = ft.Text(f"✦ {ultima_runa.get('elemento', 'Essência Mística')} ✦", size=11, color=cores.get("text_secondary", TEXT_SECONDARY), italic=True)
    txt_mensagem = ft.Text(
        f"\"{ultima_runa.get('mensagem', '')}\"",
        size=13,
        color=cores.get("text_primary", TEXT_PRIMARY),
        italic=True,
        text_align=ft.TextAlign.CENTER
    )

    def fechar_modal(dlg):
        if hasattr(page, "pop_dialog"):
            page.pop_dialog()
        else:
            dlg.open = False
            page.update()

    def sortear_nova_runa(e):
        nova = sortear_runa()
        storage.salvar_runa(nova)
        txt_simbolo.value = nova.get("simbolo", "ᛉ")
        txt_nome.value = nova.get("nome", "Runa Sagrada")
        txt_elemento.value = f"✦ {nova.get('elemento', 'Essência Mística')} ✦"
        txt_mensagem.value = f"\"{nova.get('mensagem', '')}\""
        page.update()
        if on_update_callback:
            on_update_callback()

    card_runa_destaque = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=txt_simbolo,
                    alignment=ft.Alignment(0, 0),
                    width=90,
                    height=90,
                    border_radius=border_radius_all(45),
                    bgcolor=cores["bg_input"],
                    border=border_all(2, cores["border_color"]),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=14,
                        color="#D4AF3740",
                        offset=ft.Offset(0, 3)
                    )
                ),
                txt_nome,
                txt_elemento,
                ft.Divider(height=1, color=cores.get("border_subtle", "#36364A")),
                ft.Container(
                    content=txt_mensagem,
                    padding=padding_all(10),
                    border_radius=border_radius_all(10),
                    bgcolor=cores["bg_card_light"],
                    border=border_all(1, cores.get("border_subtle", "#3A3422"))
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=14,
        border_radius=border_radius_all(14),
        bgcolor=cores["bg_surface"],
        border=border_all(1, cores["border_color"])
    )

    btn_tirar_runa = ft.Container(
        content=ft.Row(
            controls=[
                icon_nobre(ft.Icons.AUTO_AWESOME, color="#121214", size=16),
                ft.Text("🔮 Tirar Runa do Dia", color="#121214", weight=ft.FontWeight.BOLD, size=13)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6
        ),
        padding=padding_symmetric(horizontal=18, vertical=10),
        border_radius=border_radius_all(10),
        bgcolor=cores["primary"],
        on_click=sortear_nova_runa,
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
    )

    btn_fechar = botao_preenchido(
        texto="Agradeço aos Deuses Arcanos",
        bgcolor=cores["primary"],
        color="#121214",
        icon=ft.Icons.CHECK,
        on_click=lambda e: fechar_modal(dialogo_runas)
    )

    dialogo_runas = ft.AlertDialog(
        title=ft.Row(
            controls=[
                icon_nobre(ft.Icons.AUTO_AWESOME_MOTION, color=cores["light"], size=22),
                ft.Text("Oráculo Sagrado das Runas", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
            ],
            spacing=8
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    card_runa_destaque,
                    ft.Row(controls=[btn_tirar_runa], alignment=ft.MainAxisAlignment.CENTER)
                ],
                spacing=14,
                tight=True
            ),
            width=360
        ),
        actions=[
            ft.Row(
                controls=[btn_fechar],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=cores["bg_card"],
        shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
    )

    if hasattr(page, "show_dialog"):
        page.show_dialog(dialogo_runas)
    else:
        page.dialog = dialogo_runas
        dialogo_runas.open = True
        page.update()

def criar_cabecalho_reino(page: ft.Page = None, on_refresh=None, on_settings_click=None) -> ft.Container:
    """
    Header Fixo no topo de todas as abas:
    [Engrenagem Configs] + [Fase da Lua Interativa] + [Runa Diária] + [Nível/Reserva de Ouro]
    """
    reino = storage.data["reino"]
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    
    nome_rainha = cfg.get("nome_rainha", reino.get("nome_rainha", "Minha Rainha"))
    ouro = reino.get("ouro_tesouro", 0.0)
    nivel = reino.get("nivel", 1)
    titulo = reino.get("titulo_nivel", "Vilarejo Inicial")
    exp_atual = reino.get("exp_atual", 0)
    exp_prox = reino.get("exp_proximo", 100)
    progresso_exp = min(1.0, max(0.0, exp_atual / exp_prox if exp_prox > 0 else 0.0))

    # 1. Fase Atual da Lua (Cálculo Astronômico com Modal Místico ao clicar)
    nome_lua, emoji_lua = calcular_fase_lua()
    
    def on_click_lua(e):
        if page:
            abrir_modal_influencia_lunar(page)

    badge_lua = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(emoji_lua, size=14),
                ft.Text(nome_lua, size=11, color=cores.get("text_secondary", TEXT_SECONDARY), weight=ft.FontWeight.W_500)
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=padding_symmetric(horizontal=8, vertical=4),
        border_radius=border_radius_all(14),
        bgcolor=cores["bg_input"],
        border=border_all(1, cores["border_color"]),
        on_click=on_click_lua,
        tooltip="Toque para consultar a Influência Lunar do Reino"
    )

    # 2. Runa Sagrada Diária (100% Clicável - Abre o Oráculo Sagrado das Runas)
    ultima_runa = storage.data.get("emocional", {}).get("ultima_runa", {})
    simbolo_runa = ultima_runa.get("simbolo", "ᛉ")
    nome_runa = ultima_runa.get("nome", "Runa da Proteção").split()[0]
    
    def on_click_runa(e):
        if page:
            abrir_modal_oraculo_runas(page, on_refresh)

    badge_runa = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(simbolo_runa, size=13, color=cores["light"], weight=ft.FontWeight.BOLD),
                ft.Text(nome_runa, size=11, color=cores["secondary_light"], weight=ft.FontWeight.W_500)
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=padding_symmetric(horizontal=8, vertical=4),
        border_radius=border_radius_all(14),
        bgcolor=cores["container"],
        border=border_all(1, cores["border_color"]),
        on_click=on_click_runa,
        tooltip="Toque para consultar o Oráculo Sagrado das Runas"
    )

    # 3. Nível e Ouro do Reino
    badge_status = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(f"Nv.{nivel}", size=11, color=cores.get("text_primary", TEXT_PRIMARY), weight=ft.FontWeight.BOLD),
                icon_nobre(ft.Icons.SAVINGS, size=14, color=cores["light"]),
                ft.Text(f"{ouro:,.0f}".replace(",", "."), size=11, color=cores["light"], weight=ft.FontWeight.BOLD)
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=padding_symmetric(horizontal=8, vertical=4),
        border_radius=border_radius_all(14),
        bgcolor=cores["bg_input"],
        border=border_all(1, cores["border_color"])
    )

    # 4. Ícone de Engrenagem (Configs)
    btn_engrenagem = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        icon_color=cores["light"],
        icon_size=20,
        tooltip="Configurações do Reino",
        on_click=on_settings_click
    )

    # Barra de Progresso de EXP
    barra_exp = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text(f"👑 {nome_rainha} • {titulo}", size=11, color=cores["light"], weight=ft.FontWeight.BOLD),
                    ft.Text(f"{exp_atual}/{exp_prox} EXP ({int(progresso_exp * 100)}%)", size=10, color=cores.get("text_muted", TEXT_MUTED))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.ProgressBar(
                value=progresso_exp,
                color=cores["primary"],
                bgcolor="#1C182A",
                height=4
            )
        ],
        spacing=3
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        btn_engrenagem,
                        badge_lua,
                        badge_runa,
                        badge_status
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                barra_exp
            ],
            spacing=6
        ),
        padding=padding_only(left=8, right=12, top=6, bottom=8),
        bgcolor=cores["bg_surface"],
        border=border_only(bottom=ft.BorderSide(1, cores["border_color"]))
    )

def criar_botao_primario(
    texto: str,
    icone = None,
    on_click = None,
    cor_fundo: str = None,
    cor_texto: str = "#121214",
    expand: bool = False
) -> ft.Container:
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    bg = cor_fundo if cor_fundo is not None else cores["primary"]

    itens = []
    if icone:
        itens.append(icon_nobre(icone, size=18, color=cor_texto))
    itens.append(
        ft.Text(texto, color=cor_texto, weight=ft.FontWeight.BOLD, size=13)
    )

    btn = ft.Container(
        content=ft.Row(
            controls=itens,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        ),
        padding=padding_symmetric(horizontal=16, vertical=12),
        border_radius=border_radius_all(10),
        bgcolor=bg,
        on_click=on_click,
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        expand=expand,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color="#00000050",
            offset=ft.Offset(0, 2)
        )
    )
    return btn

def mostrar_notificacao(page: ft.Page, mensagem: str, sucesso: bool = True):
    cor_bg = "#1B3A2B" if sucesso else "#3A1B22"
    cor_borda = SUCCESS_GREEN if sucesso else DANGER_RED
    icone = ft.Icons.CHECK_CIRCLE if sucesso else ft.Icons.ERROR
    
    snack = ft.SnackBar(
        content=ft.Row(
            controls=[
                icon_nobre(icone, color=cor_borda, size=20),
                ft.Text(mensagem, color="#FFFFFF", size=13, weight=ft.FontWeight.W_500, expand=True)
            ],
            spacing=10
        ),
        bgcolor=cor_bg,
        duration=3000,
        open=True
    )
    
    try:
        page.overlay.append(snack)
        snack.open = True
        page.update()
    except Exception:
        pass

# ==================== MODAL DE CONFIGURAÇÕES ====================
def abrir_modal_configuracoes(page: ft.Page, on_saved=None):
    """
    Abre o Modal de Configurações com:
    1. Perfil do Personagem (Nome da Rainha).
    2. Personalização dos nomes das 5 abas.
    3. Seletor de Temas & Paletas Dark Fantasy com recoloração em tempo real.
    """
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))
    nomes_abas = cfg.get("nomes_abas", {})

    txt_nome_rainha = ft.TextField(
        label="Nome da Rainha / Personagem",
        value=cfg.get("nome_rainha", "Minha Rainha"),
        bgcolor=cores["bg_input"],
        border_color=cores.get("border_subtle", "#36364A"),
        focused_border_color=cores["primary"],
        color=cores.get("text_primary", TEXT_PRIMARY),
        text_size=13
    )

    # Campos de customização dos nomes das 5 abas
    txt_aba_trono = ft.TextField(label="Aba 1 (Trono)", value=nomes_abas.get("trono", "Trono"), bgcolor=cores["bg_input"], border_color=cores.get("border_subtle", "#36364A"), color=cores.get("text_primary", TEXT_PRIMARY), text_size=12, expand=True)
    txt_aba_quests = ft.TextField(label="Aba 2 (Quests)", value=nomes_abas.get("quests", "Quests"), bgcolor=cores["bg_input"], border_color=cores.get("border_subtle", "#36364A"), color=cores.get("text_primary", TEXT_PRIMARY), text_size=12, expand=True)
    txt_aba_cofre = ft.TextField(label="Aba 3 (Cofre)", value=nomes_abas.get("cofre", "Cofre"), bgcolor=cores["bg_input"], border_color=cores.get("border_subtle", "#36364A"), color=cores.get("text_primary", TEXT_PRIMARY), text_size=12, expand=True)
    txt_aba_forja = ft.TextField(label="Aba 4 (Forja)", value=nomes_abas.get("forja", "Forja"), bgcolor=cores["bg_input"], border_color=cores.get("border_subtle", "#36364A"), color=cores.get("text_primary", TEXT_PRIMARY), text_size=12, expand=True)
    txt_aba_foco = ft.TextField(label="Aba 5 (Foco)", value=nomes_abas.get("foco", "Foco"), bgcolor=cores["bg_input"], border_color=cores.get("border_subtle", "#36364A"), color=cores.get("text_primary", TEXT_PRIMARY), text_size=12, expand=True)

    def fechar_dialogo(dlg):
        if hasattr(page, "pop_dialog"):
            page.pop_dialog()
        else:
            dlg.open = False
            page.update()

    def mudar_tema_tempo_real(e):
        novo_tema = dropdown_tema.value or "Dark Fantasy Dourado"
        storage.salvar_configuracoes(tema_atual=novo_tema)
        aplicar_tema(novo_tema)
        if on_saved:
            on_saved()

    # Seletor de Temas com gatilho dinâmico imediato
    dropdown_tema = ft.Dropdown(
        label="Paleta & Tema Dark Fantasy",
        options=[
            ft.dropdown.Option("Dark Fantasy Dourado", "✨ Dark Fantasy Dourado (Padrão Real)"),
            ft.dropdown.Option("Roxo Arcano", "🔮 Roxo Arcano (Místico & Nobre)"),
            ft.dropdown.Option("Esmeralda Obscura", "🌿 Esmeralda Obscura (Alquimia Florestal)"),
            ft.dropdown.Option("Chumbo Sóbrio", "🛡️ Chumbo Sóbrio (Cavaleiro & Aço)"),
        ],
        value=cfg.get("tema_atual", "Dark Fantasy Dourado"),
        bgcolor=cores["bg_surface"],
        border_color=cores.get("border_subtle", "#36364A"),
        color=cores.get("text_primary", TEXT_PRIMARY)
    )
    dropdown_tema.on_change = mudar_tema_tempo_real

    def salvar_configs(e):
        novo_nome = txt_nome_rainha.value.strip() or "Minha Rainha"
        novos_nomes_abas = {
            "trono": txt_aba_trono.value.strip() or "Trono",
            "quests": txt_aba_quests.value.strip() or "Quests",
            "cofre": txt_aba_cofre.value.strip() or "Cofre",
            "forja": txt_aba_forja.value.strip() or "Forja",
            "foco": txt_aba_foco.value.strip() or "Foco"
        }
        novo_tema = dropdown_tema.value or "Dark Fantasy Dourado"

        storage.salvar_configuracoes(
            nome_rainha=novo_nome,
            tema_atual=novo_tema,
            nomes_abas=novos_nomes_abas
        )
        aplicar_tema(novo_tema)

        fechar_dialogo(dialogo)
        mostrar_notificacao(page, "Configurações e tema atualizados com honra!", sucesso=True)
        if on_saved:
            on_saved()

    def testar_alerta(e):
        if hasattr(page, "audio_alerta") and page.audio_alerta:
            page.audio_alerta.play()
        else:
            from theme import resolve_path, FletAudioCompat
            FletAudioCompat(resolve_path("assets/som_alerta.mp3")).play()
        mostrar_notificacao(page, "Som de Alerta reproduzido com sucesso!", sucesso=True)

    def testar_foco(e):
        if hasattr(page, "audio_foco") and page.audio_foco:
            page.audio_foco.play()
        else:
            from theme import resolve_path, FletAudioCompat
            FletAudioCompat(resolve_path("assets/som_foco.mp3")).play()
        mostrar_notificacao(page, "Som de Foco reproduzido com sucesso!", sucesso=True)

    def testar_notificacao(e):
        from theme import disparar_notificacao_sistema, resolve_path
        sucesso = disparar_notificacao_sistema(
            titulo="Grimório • Notificação Real",
            mensagem="O Pequeno Rei Joaquim e os Arcanos abençoam o seu reino!",
            app_icon=resolve_path("assets/logo.ico")
        )
        mostrar_notificacao(page, "Notificação de Sistema disparada no Windows!" if sucesso else "Notificação emitida!", sucesso=True)

    btn_teste_alerta = ft.OutlinedButton(
        content=ft.Row([ft.Text("🔊", size=13), ft.Text("Testar Som de Alerta", size=11, color=cores["light"])], spacing=4),
        on_click=testar_alerta,
        style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(1, cores.get("border_subtle", "#36364A"))})
    )
    btn_teste_foco = ft.OutlinedButton(
        content=ft.Row([ft.Text("⏱️", size=13), ft.Text("Testar Som de Foco", size=11, color=cores["light"])], spacing=4),
        on_click=testar_foco,
        style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(1, cores.get("border_subtle", "#36364A"))})
    )
    btn_teste_notif = ft.OutlinedButton(
        content=ft.Row([ft.Text("🔔", size=13), ft.Text("Testar Notificação (Toast)", size=11, color=cores["secondary_light"])], spacing=4),
        on_click=testar_notificacao,
        style=ft.ButtonStyle(side={ft.ControlState.DEFAULT: ft.BorderSide(1, cores["secondary"])})
    )

    dialogo = ft.AlertDialog(
        title=ft.Row(
            controls=[
                icon_nobre(ft.Icons.SETTINGS, color=cores["light"], size=20),
                ft.Text("Configurações do Reino", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
            ],
            spacing=8
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("👑 Perfil Real", weight=ft.FontWeight.BOLD, size=13, color=cores["light"]),
                    txt_nome_rainha,
                    ft.Divider(height=1, color=cores.get("border_subtle", "#36364A")),
                    ft.Text("🎨 Tema Visual da UI (Tempo Real)", weight=ft.FontWeight.BOLD, size=13, color=cores["light"]),
                    dropdown_tema,
                    ft.Divider(height=1, color=cores.get("border_subtle", "#36364A")),
                    ft.Text("📜 Personalização das Abas", weight=ft.FontWeight.BOLD, size=13, color=cores["light"]),
                    ft.Row(controls=[txt_aba_trono, txt_aba_quests], spacing=6),
                    ft.Row(controls=[txt_aba_cofre, txt_aba_forja], spacing=6),
                    txt_aba_foco,
                    ft.Divider(height=1, color=cores.get("border_subtle", "#36364A")),
                    ft.Text("🔊 Áudio & Notificações do Sistema", weight=ft.FontWeight.BOLD, size=13, color=cores["light"]),
                    ft.Row(controls=[btn_teste_alerta, btn_teste_foco], spacing=6, wrap=True),
                    ft.Row(controls=[btn_teste_notif], alignment=ft.MainAxisAlignment.CENTER)
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO
            ),
            width=360,
            height=430
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dialogo)),
            botao_preenchido(
                texto="Salvar Alterações",
                bgcolor=cores["primary"],
                color="#121214",
                on_click=salvar_configs
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
