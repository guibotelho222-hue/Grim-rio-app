"""
Grimório V2.0 - Aba 5: Foco (Poção Alquímica Pomodoro)
Frasco com Nível Líquido Dinâmico, Ciclos de Foco/Descanso, Timer Síncrono Seguro e Tema Dinâmico
"""

import time
import threading
import flet as ft
from theme import (
    BG_DARK, BG_SURFACE, BG_CARD, BG_CARD_LIGHT, BG_INPUT,
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_CONTAINER, BORDER_GOLD,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_DARK, PURPLE_CONTAINER, BORDER_PURPLE,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS_GREEN, DANGER_RED, MANA_BLUE, BORDER_RADIUS,
    border_all, border_radius_all, border_radius_only, padding_all, padding_symmetric, padding_only, icon_nobre,
    get_theme_colors
)
from storage import storage
from components.common_ui import criar_card_nobre, criar_botao_primario, mostrar_notificacao

def criar_aba_foco(page: ft.Page, on_update_callback=None) -> ft.Control:
    """Retorna a visão interativa da Aba Foco Alquímico com tema dinâmico."""

    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))

    estado = {
        "modo": "foco",
        "minutos_foco": 25,
        "minutos_descanso": 5,
        "segundos_restantes": 25 * 60,
        "segundos_totais": 25 * 60,
        "em_execucao": False,
        "thread_ativa": False
    }

    lbl_tempo = ft.Text("25:00", size=44, weight=ft.FontWeight.BOLD, color=cores["light"])
    lbl_modo = ft.Text("🧪 Poção de Foco Arcano", size=15, weight=ft.FontWeight.BOLD, color=cores["secondary_light"])
    lbl_status_detalhe = ft.Text("Canalize sua atenção para erguer as defesas do reino.", size=11, color=cores.get("text_secondary", TEXT_SECONDARY), text_align=ft.TextAlign.CENTER)
    
    ALTURA_FRASCO = 160
    LARGURA_FRASCO = 120
    
    liquido_container = ft.Container(
        width=LARGURA_FRASCO - 12,
        height=int(ALTURA_FRASCO * 0.9),
        border_radius=border_radius_only(
            bottom_left=30,
            bottom_right=30,
            top_left=8,
            top_right=8
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, 1),
            end=ft.Alignment(0, -1),
            colors=[PURPLE_DARK, cores["secondary"], cores["secondary_light"]]
        ),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    )

    bolhas_magicas = ft.Row(
        controls=[
            ft.Text("✨", size=14),
            ft.Text("🫧", size=16),
            ft.Text("✨", size=12),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
    )

    frasco_corpo = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    width=LARGURA_FRASCO,
                    height=ALTURA_FRASCO,
                    border_radius=border_radius_only(
                        top_left=12,
                        top_right=12,
                        bottom_left=34,
                        bottom_right=34
                    ),
                    bgcolor=cores["bg_input"],
                    border=border_all(2, cores["primary"]),
                    alignment=ft.Alignment(0, 1)
                ),
                ft.Container(
                    content=liquido_container,
                    width=LARGURA_FRASCO,
                    height=ALTURA_FRASCO,
                    alignment=ft.Alignment(0, 1),
                    padding=padding_only(bottom=4, left=6, right=6)
                ),
                ft.Container(
                    width=LARGURA_FRASCO,
                    height=ALTURA_FRASCO,
                    alignment=ft.Alignment(0, 0),
                    content=bolhas_magicas
                )
            ]
        ),
        width=LARGURA_FRASCO,
        height=ALTURA_FRASCO,
        alignment=ft.Alignment(0, 0)
    )

    gargalo_frasco = ft.Container(
        content=ft.Container(
            width=32,
            height=14,
            bgcolor="#854D0E",
            border_radius=border_radius_all(3),
            border=border_all(1, cores["light"])
        ),
        alignment=ft.Alignment(0, 0)
    )

    composicao_frasco = ft.Column(
        controls=[
            gargalo_frasco,
            frasco_corpo
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    def atualizar_interface():
        mins = estado["segundos_restantes"] // 60
        segs = estado["segundos_restantes"] % 60
        lbl_tempo.value = f"{mins:02d}:{segs:02d}"
        
        total = max(1, estado["segundos_totais"])
        prop = max(0.08, min(1.0, estado["segundos_restantes"] / total))
        liquido_container.height = int((ALTURA_FRASCO - 16) * prop)
        
        if estado["modo"] == "foco":
            lbl_modo.value = "🧪 Poção de Foco Arcano"
            lbl_modo.color = cores["secondary_light"]
            liquido_container.gradient = ft.LinearGradient(
                begin=ft.Alignment(0, 1),
                end=ft.Alignment(0, -1),
                colors=[PURPLE_DARK, cores["secondary"], cores["secondary_light"]]
            )
            lbl_status_detalhe.value = "Canalize sua atenção para erguer as defesas do reino."
        else:
            lbl_modo.value = "🍵 Elixir de Descanso Real"
            lbl_modo.color = SUCCESS_GREEN
            liquido_container.gradient = ft.LinearGradient(
                begin=ft.Alignment(0, 1),
                end=ft.Alignment(0, -1),
                colors=["#064E3B", "#10B981", "#34D399"]
            )
            lbl_status_detalhe.value = "Beba um gole de serenidade. Sua mente forjou grandes feitos."

        try:
            lbl_tempo.update()
            lbl_modo.update()
            lbl_status_detalhe.update()
            liquido_container.update()
        except Exception:
            pass

    def concluir_ciclo():
        from theme import disparar_notificacao_sistema
        if estado["modo"] == "foco":
            storage.registrar_foco_concluido(estado["minutos_foco"])
            if hasattr(page, "audio_alerta") and page.audio_alerta:
                page.audio_alerta.play()
            mostrar_notificacao(page, f"Poção consumida com louvor! +{estado['minutos_foco']} min de foco e +25 EXP!", sucesso=True)
            disparar_notificacao_sistema(
                titulo="Grimório • Foco Concluído!",
                mensagem=f"Poção de foco concluída! Você canalizou {estado['minutos_foco']} minutos de pura sabedoria régia."
            )
            estado["modo"] = "descanso"
            estado["segundos_restantes"] = estado["minutos_descanso"] * 60
            estado["segundos_totais"] = estado["minutos_descanso"] * 60
        else:
            if hasattr(page, "audio_foco") and page.audio_foco:
                page.audio_foco.play()
            mostrar_notificacao(page, "Descanso finalizado. Preparada para a próxima jornada, Soberana?", sucesso=True)
            disparar_notificacao_sistema(
                titulo="Grimório • Descanso Finalizado!",
                mensagem="Seu descanso terminou. O Pequeno Rei aguarda sua presença na corte para novas glórias!"
            )
            estado["modo"] = "foco"
            estado["segundos_restantes"] = estado["minutos_foco"] * 60
            estado["segundos_totais"] = estado["minutos_foco"] * 60
            
        estado["em_execucao"] = False
        btn_play_pause.content.controls[0].name = ft.Icons.PLAY_ARROW
        btn_play_pause.content.controls[1].value = "Iniciar Foco"
        try:
            btn_play_pause.update()
        except Exception:
            pass
        atualizar_interface()
        if on_update_callback:
            on_update_callback()

    def loop_temporizador():
        while estado["thread_ativa"]:
            if estado["em_execucao"]:
                if estado["segundos_restantes"] > 0:
                    estado["segundos_restantes"] -= 1
                    atualizar_interface()
                else:
                    concluir_ciclo()
            time.sleep(1)

    def alternar_play_pause(e):
        estado["em_execucao"] = not estado["em_execucao"]
        if estado["em_execucao"]:
            btn_play_pause.content.controls[0].name = ft.Icons.PAUSE
            btn_play_pause.content.controls[1].value = "Pausar"
            btn_play_pause.bgcolor = cores["secondary"]
        else:
            btn_play_pause.content.controls[0].name = ft.Icons.PLAY_ARROW
            btn_play_pause.content.controls[1].value = "Retomar"
            btn_play_pause.bgcolor = cores["primary"]
        btn_play_pause.update()

    def reiniciar_timer(e):
        estado["em_execucao"] = False
        if estado["modo"] == "foco":
            estado["segundos_restantes"] = estado["minutos_foco"] * 60
            estado["segundos_totais"] = estado["minutos_foco"] * 60
        else:
            estado["segundos_restantes"] = estado["minutos_descanso"] * 60
            estado["segundos_totais"] = estado["minutos_descanso"] * 60
            
        btn_play_pause.content.controls[0].name = ft.Icons.PLAY_ARROW
        btn_play_pause.content.controls[1].value = "Iniciar Foco"
        btn_play_pause.bgcolor = cores["primary"]
        btn_play_pause.update()
        atualizar_interface()

    def pular_ciclo(e):
        estado["em_execucao"] = False
        if estado["modo"] == "foco":
            estado["modo"] = "descanso"
            estado["segundos_restantes"] = estado["minutos_descanso"] * 60
            estado["segundos_totais"] = estado["minutos_descanso"] * 60
        else:
            estado["modo"] = "foco"
            estado["segundos_restantes"] = estado["minutos_foco"] * 60
            estado["segundos_totais"] = estado["minutos_foco"] * 60
            
        btn_play_pause.content.controls[0].name = ft.Icons.PLAY_ARROW
        btn_play_pause.content.controls[1].value = "Iniciar Foco"
        btn_play_pause.bgcolor = cores["primary"]
        btn_play_pause.update()
        atualizar_interface()

    def definir_tempo(min_foco: int, min_descanso: int):
        estado["em_execucao"] = False
        estado["modo"] = "foco"
        estado["minutos_foco"] = min_foco
        estado["minutos_descanso"] = min_descanso
        estado["segundos_restantes"] = min_foco * 60
        estado["segundos_totais"] = min_foco * 60
        
        btn_play_pause.content.controls[0].name = ft.Icons.PLAY_ARROW
        btn_play_pause.content.controls[1].value = "Iniciar Foco"
        btn_play_pause.bgcolor = cores["primary"]
        btn_play_pause.update()
        atualizar_interface()
        mostrar_notificacao(page, f"Ritmo ajustado: {min_foco} min de foco arcano / {min_descanso} min de descanso real.", sucesso=True)

    btn_play_pause = ft.Container(
        content=ft.Row(
            controls=[
                icon_nobre(ft.Icons.PLAY_ARROW, color="#121214", size=20),
                ft.Text("Iniciar Foco", color="#121214", weight=ft.FontWeight.BOLD, size=13)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6
        ),
        padding=padding_symmetric(horizontal=20, vertical=12),
        border_radius=border_radius_all(10),
        bgcolor=cores["primary"],
        on_click=alternar_play_pause,
        expand=True
    )

    btn_reiniciar = ft.Container(
        content=icon_nobre(ft.Icons.REPLAY, color=cores.get("text_primary", TEXT_PRIMARY), size=20),
        padding=padding_all(12),
        border_radius=border_radius_all(10),
        bgcolor=cores["bg_input"],
        border=border_all(1, cores.get("border_subtle", "#36364A")),
        on_click=reiniciar_timer,
        tooltip="Reiniciar Poção Atual"
    )

    btn_pular = ft.Container(
        content=icon_nobre(ft.Icons.SKIP_NEXT, color=cores.get("text_primary", TEXT_PRIMARY), size=20),
        padding=padding_all(12),
        border_radius=border_radius_all(10),
        bgcolor=cores["bg_input"],
        border=border_all(1, cores.get("border_subtle", "#36364A")),
        on_click=pular_ciclo,
        tooltip="Avançar para Próximo Ciclo"
    )

    botoes_predefinidos = ft.Row(
        controls=[
            ft.TextButton(
                "15/3 min",
                on_click=lambda e: definir_tempo(15, 3),
                style=ft.ButtonStyle(color=cores.get("text_secondary", TEXT_SECONDARY))
            ),
            ft.TextButton(
                "25/5 min (Padrão)",
                on_click=lambda e: definir_tempo(25, 5),
                style=ft.ButtonStyle(color=cores["light"])
            ),
            ft.TextButton(
                "45/10 min",
                on_click=lambda e: definir_tempo(45, 10),
                style=ft.ButtonStyle(color=cores.get("text_secondary", TEXT_SECONDARY))
            ),
            ft.TextButton(
                "50/10 min",
                on_click=lambda e: definir_tempo(50, 10),
                style=ft.ButtonStyle(color=cores.get("text_secondary", TEXT_SECONDARY))
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True
    )

    estado["thread_ativa"] = True
    t = threading.Thread(target=loop_temporizador, daemon=True)
    t.start()

    secao_pomodoro = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.SCIENCE, size=20, color=cores["light"]),
                        lbl_modo
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6
                ),
                ft.Container(height=8),
                composicao_frasco,
                ft.Container(height=4),
                ft.Row(
                    controls=[lbl_tempo],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                lbl_status_detalhe,
                ft.Container(height=6),
                ft.Row(
                    controls=[
                        btn_play_pause,
                        btn_reiniciar,
                        btn_pular
                    ],
                    spacing=8
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                botoes_predefinidos
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        borda_dourada=True
    )

    total_pom = storage.data["foco"].get("total_pomodoros", 0)
    total_min = storage.data["foco"].get("tempo_total_minutos", 0)
    
    secao_estatisticas = criar_card_nobre(
        conteudo=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            icon_nobre(ft.Icons.CHECK_CIRCLE, size=18, color=SUCCESS_GREEN),
                            ft.Text(f"{total_pom}", weight=ft.FontWeight.BOLD, size=16, color=cores.get("text_primary", TEXT_PRIMARY)),
                            ft.Text("Poções Consumadas", size=10, color=cores.get("text_muted", TEXT_MUTED))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2
                    ),
                    expand=True,
                    padding=10,
                    border_radius=border_radius_all(8),
                    bgcolor=cores["bg_input"]
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            icon_nobre(ft.Icons.HOURGLASS_FULL, size=18, color=cores["secondary_light"]),
                            ft.Text(f"{total_min} min", weight=ft.FontWeight.BOLD, size=16, color=cores.get("text_primary", TEXT_PRIMARY)),
                            ft.Text("Tempo em Foco Total", size=10, color=cores.get("text_muted", TEXT_MUTED))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2
                    ),
                    expand=True,
                    padding=10,
                    border_radius=border_radius_all(8),
                    bgcolor=cores["bg_input"]
                )
            ],
            spacing=10
        ),
        borda_roxa=True
    )

    return ft.ListView(
        controls=[
            secao_pomodoro,
            secao_estatisticas,
            ft.Container(height=30)
        ],
        spacing=14,
        padding=12,
        expand=True
    )
