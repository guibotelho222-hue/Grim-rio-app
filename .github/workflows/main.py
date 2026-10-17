"""
Grimório - Versão Final e Definitiva
Aplicativo de Produtividade & Gestão Pessoal Dark Fantasy Moderno
Arquitetura 100% Síncrona, Resolução de Caminhos com sys._MEIPASS
"""

import os
import sys
import flet as ft

# Configuração de Caminhos de Assets com suporte a PyInstaller e Executável
def resolve_path(relative_path: str) -> str:
    """Resolve caminhos absolutos em modo Dev, Executável PyInstaller (_MEIPASS) e Pacote Mobile."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

# Módulos do Grimório
from theme import (
    BG_DARK, BG_SURFACE, GOLD_PRIMARY, GOLD_LIGHT,
    PURPLE_PRIMARY, PURPLE_LIGHT, TEXT_PRIMARY, get_dark_theme, get_theme_colors
)
from storage import storage
from components.common_ui import criar_cabecalho_reino, abrir_modal_configuracoes
from splash_screen import criar_splash_screen

# Abas do Aplicativo
from tabs.tab_trono import criar_aba_trono
from tabs.tab_quests import criar_aba_quests
from tabs.tab_cofre import criar_aba_cofre
from tabs.tab_forja import criar_aba_forja
from tabs.tab_foco import criar_aba_foco

def main(page: ft.Page):
    """Ponto de Entrada Oficial Síncrono do Grimório."""
    
    cfg = storage.obter_configuracoes()
    tema_atual = cfg.get("tema_atual", "Dark Fantasy Dourado")
    cores = get_theme_colors(tema_atual)

    # 1. Configurações Oficiais da Janela
    page.title = "Grimório"
    page.theme = get_dark_theme(tema_atual)
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = cores["bg_dark"]
    page.padding = 0
    page.spacing = 0

    caminho_icone = resolve_path("assets/logo.ico")
    
    # Ícone da janela e executável
    if hasattr(page, "window"):
        page.window.width = 440
        page.window.height = 860
        page.window.min_width = 380
        page.window.min_height = 680
        if os.path.exists(caminho_icone):
            try:
                page.window.icon = caminho_icone
            except Exception:
                pass
                
    if hasattr(page, "window_icon") and os.path.exists(caminho_icone):
        try:
            page.window_icon = caminho_icone
        except Exception:
            pass

    # 2. Inicialização dos Controles de Áudio Síncronos em page.overlay
    audio_foco = ft.Audio(src=resolve_path("assets/som_foco.mp3"), autoplay=False)
    audio_alerta = ft.Audio(src=resolve_path("assets/som_alerta.mp3"), autoplay=False)
    page.overlay.append(audio_foco)
    page.overlay.append(audio_alerta)
    page.audio_foco = audio_foco
    page.audio_alerta = audio_alerta

    # 3. Gerenciamento de Estado de Abas
    estado_app = {
        "aba_atual": 0,
        "em_splash": True
    }

    # Contêineres Principais
    area_cabecalho = ft.Container()
    area_conteudo = ft.Container(expand=True)

    def recarregar_layout():
        """Recarrega cabeçalho, cores do tema, nomes de abas e a aba ativa."""
        cfg_atual = storage.obter_configuracoes()
        tema_novo = cfg_atual.get("tema_atual", "Dark Fantasy Dourado")
        novas_cores = get_theme_colors(tema_novo)
        nomes_abas = cfg_atual.get("nomes_abas", {})

        from theme import aplicar_tema
        aplicar_tema(tema_novo)

        page.theme = get_dark_theme(tema_novo)
        page.bgcolor = novas_cores["bg_dark"]

        # Atualiza os labels e cores da barra de navegação
        nav_bar.destinations[0].label = nomes_abas.get("trono", "Trono")
        nav_bar.destinations[1].label = nomes_abas.get("quests", "Quests")
        nav_bar.destinations[2].label = nomes_abas.get("cofre", "Cofre")
        nav_bar.destinations[3].label = nomes_abas.get("forja", "Forja")
        nav_bar.destinations[4].label = nomes_abas.get("foco", "Foco")
        nav_bar.bgcolor = novas_cores["bg_surface"]
        nav_bar.indicator_color = novas_cores["container"]

        atualizar_cabecalho()
        trocar_aba(estado_app["aba_atual"])
        page.update()

    def acao_abrir_configuracoes(e):
        abrir_modal_configuracoes(page, on_saved=recarregar_layout)

    def atualizar_cabecalho():
        """Atualiza sincronamente os valores de Ouro, EXP, Lua e Runa do cabeçalho real."""
        area_cabecalho.content = criar_cabecalho_reino(
            page=page,
            on_refresh=atualizar_cabecalho,
            on_settings_click=acao_abrir_configuracoes
        )
        try:
            area_cabecalho.update()
        except Exception:
            pass

    def trocar_aba(indice: int):
        """Alterna entre as 5 abas com rolagem independente e zero travamentos."""
        estado_app["aba_atual"] = indice
        atualizar_cabecalho()
        
        if indice == 0:
            area_conteudo.content = criar_aba_trono(page, on_update_callback=atualizar_cabecalho)
        elif indice == 1:
            area_conteudo.content = criar_aba_quests(page, on_update_callback=atualizar_cabecalho)
        elif indice == 2:
            area_conteudo.content = criar_aba_cofre(page, on_update_callback=atualizar_cabecalho)
        elif indice == 3:
            area_conteudo.content = criar_aba_forja(page, on_update_callback=atualizar_cabecalho)
        elif indice == 4:
            area_conteudo.content = criar_aba_foco(page, on_update_callback=atualizar_cabecalho)
            
        try:
            area_conteudo.update()
        except Exception:
            pass

    # 3. Barra de Navegação Inferior das 5 Abas
    nomes_abas_iniciais = cfg.get("nomes_abas", {})
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.FORT_OUTLINED,
                selected_icon=ft.Icons.FORT,
                label=nomes_abas_iniciais.get("trono", "Trono")
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.AUTO_AWESOME_OUTLINED,
                selected_icon=ft.Icons.AUTO_AWESOME,
                label=nomes_abas_iniciais.get("quests", "Quests")
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SAVINGS_OUTLINED,
                selected_icon=ft.Icons.SAVINGS,
                label=nomes_abas_iniciais.get("cofre", "Cofre")
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BUILD_OUTLINED,
                selected_icon=ft.Icons.BUILD,
                label=nomes_abas_iniciais.get("forja", "Forja")
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SCIENCE_OUTLINED,
                selected_icon=ft.Icons.SCIENCE,
                label=nomes_abas_iniciais.get("foco", "Foco")
            ),
        ],
        selected_index=0,
        bgcolor=cores["bg_surface"],
        indicator_color="#4C1D9580",
        on_change=lambda e: trocar_aba(e.control.selected_index)
    )

    # 4. Transição Fluida da Splash Screen para a Tela Principal
    def entrar_no_reino():
        estado_app["em_splash"] = False
        page.clean()
        
        atualizar_cabecalho()
        area_conteudo.content = criar_aba_trono(page, on_update_callback=atualizar_cabecalho)
        
        layout_principal = ft.Column(
            controls=[
                area_cabecalho,
                area_conteudo
            ],
            expand=True,
            spacing=0
        )
        
        page.navigation_bar = nav_bar
        page.add(layout_principal)
        page.update()

    # Inicia exibindo a Splash Screen com o Gatinho Cavaleiro
    tela_splash = criar_splash_screen(on_entrar_click=entrar_no_reino)
    page.add(tela_splash)
    page.update()

if __name__ == "__main__":
    assets_dir_path = resolve_path("assets")
    
    if hasattr(ft, "run"):
        ft.run(main, assets_dir=assets_dir_path)
    elif hasattr(ft, "app"):
        ft.app(target=main, assets_dir=assets_dir_path)
