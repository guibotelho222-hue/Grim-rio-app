"""
Grimório Mobile - Aba 3: Cofre (Finanças & Gestão Financeira para Android)
Gestão do Cofre, Edição Direta de Teto e Reserva, Saúde Financeira, Categorias e Projeção Inteligente.
"""

from datetime import datetime, date
import flet as ft
from theme import (
    BG_DARK, BG_SURFACE, BG_CARD, BG_CARD_LIGHT, BG_INPUT,
    GOLD_PRIMARY, GOLD_LIGHT, GOLD_MUTED, GOLD_CONTAINER, BORDER_GOLD,
    PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_CONTAINER, BORDER_PURPLE,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS_GREEN, DANGER_RED, BORDER_RADIUS,
    border_all, border_radius_all, padding_all, padding_symmetric, icon_nobre, botao_preenchido,
    get_theme_colors
)
from storage import storage
from components.common_ui import criar_card_nobre, criar_botao_primario, mostrar_notificacao

CORES_CATEGORIAS = {
    "Alimentação": "#F59E0B",
    "Moradia": "#8B5CF6",
    "Lazer": "#EC4899",
    "Saúde": "#10B981",
    "Investimentos": "#D4AF37",
    "Essenciais": "#3B82F6",
    "Tributos": "#EF4444",
    "Reino & Armas": "#9333EA",
    "Poupança": "#14B8A6",
    "Outros": "#94A3B8"
}

ICONES_CATEGORIAS = {
    "Alimentação": ft.Icons.RESTAURANT,
    "Moradia": ft.Icons.HOME,
    "Lazer": ft.Icons.ATTRACTIONS,
    "Saúde": ft.Icons.FAVORITE,
    "Investimentos": ft.Icons.TRENDING_UP,
    "Essenciais": ft.Icons.LOCAL_GROCERY_STORE,
    "Tributos": ft.Icons.ACCOUNT_BALANCE,
    "Reino & Armas": ft.Icons.SHIELD,
    "Poupança": ft.Icons.SAVINGS,
    "Outros": ft.Icons.CATEGORY
}

def criar_aba_cofre(page: ft.Page, on_update_callback=None) -> ft.Control:
    """Retorna a visão completa da Aba Cofre adaptada para toque e rolagem vertical em smartphone."""
    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))

    mes_atual_iso = datetime.now().strftime("%Y-%m")
    
    resumo_container = ft.Column(spacing=6)
    saude_container = ft.Column(spacing=4)
    dashboard_categorias_container = ft.Column(spacing=6)
    projecao_container = ft.Column(spacing=6)
    lista_transacoes_col = ft.Column(spacing=4)
    alerta_divida_container = ft.Column(spacing=4, visible=False)

    def formatar_moeda(val: float) -> str:
        s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{s} Ouro"

    def fechar_modal(dlg):
        if hasattr(page, "pop_dialog"):
            page.pop_dialog()
        else:
            dlg.open = False
            page.update()

    def abrir_dialogo(dlg):
        if hasattr(page, "show_dialog"):
            page.show_dialog(dlg)
        else:
            page.dialog = dlg
            dlg.open = True
            page.update()

    # ==================== MODAL DE EDIÇÃO DE RESERVA ====================
    def abrir_modal_editar_reserva(e):
        reserva_atual = storage.obter_reserva_reino()
        
        txt_reserva = ft.TextField(
            label="Reserva Guardada (Ouro)",
            value=f"{reserva_atual:.2f}".replace(".", ","),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            color=cores.get("text_primary", TEXT_PRIMARY),
            text_size=13
        )

        def salvar_reserva(e_salvar):
            try:
                val = float(txt_reserva.value.replace(" ", "").replace(".", "").replace(",", "."))
                if val < 0:
                    raise ValueError
            except Exception:
                txt_reserva.error_text = "Informe um valor numérico válido!"
                txt_reserva.update()
                return

            storage.atualizar_reserva_guardada(val)
            fechar_modal(dialogo_reserva)
            mostrar_notificacao(page, f"Reserva ajustada para {formatar_moeda(val)}!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()
            page.update()

        dialogo_reserva = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.SHIELD_MOON, color=cores["light"], size=20),
                    ft.Text("Ajustar Reserva", size=15, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Defina o tesouro reservado nas arcas do reino:", size=11, color=cores.get("text_secondary", TEXT_SECONDARY)),
                        txt_reserva
                    ],
                    spacing=8,
                    tight=True
                ),
                width=300
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo_reserva)),
                botao_preenchido("Salvar", bgcolor=cores["primary"], on_click=salvar_reserva)
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )
        abrir_dialogo(dialogo_reserva)

    # ==================== MODAL DE EDIÇÃO DE TETO ====================
    def abrir_modal_editar_teto(e):
        teto_atual = storage.obter_teto_gastos()
        
        txt_teto = ft.TextField(
            label="Teto de Gastos Mensal (Ouro)",
            value=f"{teto_atual:.2f}".replace(".", ","),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            color=cores.get("text_primary", TEXT_PRIMARY),
            text_size=13
        )

        def salvar_teto(e_salvar):
            try:
                val = float(txt_teto.value.replace(" ", "").replace(".", "").replace(",", "."))
                if val <= 0:
                    raise ValueError
            except Exception:
                txt_teto.error_text = "Informe um teto válido!"
                txt_teto.update()
                return

            storage.atualizar_teto_gastos(val)
            fechar_modal(dialogo_teto)
            mostrar_notificacao(page, f"Teto ajustado para {formatar_moeda(val)}!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()
            page.update()

        dialogo_teto = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.SPEED, color=cores["light"], size=20),
                    ft.Text("Ajustar Teto de Gastos", size=15, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Defina o limite máximo de despesas do ciclo:", size=11, color=cores.get("text_secondary", TEXT_SECONDARY)),
                        txt_teto
                    ],
                    spacing=8,
                    tight=True
                ),
                width=300
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo_teto)),
                botao_preenchido("Salvar Teto", bgcolor=cores["primary"], on_click=salvar_teto)
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )
        abrir_dialogo(dialogo_teto)

    # ==================== RENDERIZAÇÃO DO RESUMO & TETO ====================
    def renderizar_resumo():
        resumo = storage.calcular_resumo_mes(mes_atual_iso)
        
        divida = resumo.get("divida", 0.0)
        if divida > 0:
            alerta_divida_container.controls = [
                ft.Container(
                    content=ft.Row(
                        controls=[
                            icon_nobre(ft.Icons.WARNING_AMBER_ROUNDED, color=DANGER_RED, size=20),
                            ft.Column(
                                controls=[
                                    ft.Text("Alerta Real: Dívida da Coroa!", weight=ft.FontWeight.BOLD, color=DANGER_RED, size=12),
                                    ft.Text(f"Estouro anterior: {formatar_moeda(divida)}.", size=10, color=cores.get("text_secondary", TEXT_SECONDARY))
                                ],
                                spacing=1,
                                expand=True
                            )
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=8,
                    border_radius=border_radius_all(8),
                    bgcolor="#3A141A",
                    border=border_all(1, DANGER_RED)
                )
            ]
            alerta_divida_container.visible = True
        else:
            alerta_divida_container.visible = False

        cor_saldo = SUCCESS_GREEN if resumo["saldo"] >= 0 else DANGER_RED

        cards_kpi = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    icon_nobre(ft.Icons.ARROW_UPWARD, size=13, color=SUCCESS_GREEN),
                                    ft.Text("Entradas", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                ],
                                spacing=2
                            ),
                            ft.Text(formatar_moeda(resumo["entradas"]), size=12, weight=ft.FontWeight.BOLD, color=SUCCESS_GREEN)
                        ],
                        spacing=2
                    ),
                    expand=True,
                    padding=8,
                    border_radius=border_radius_all(8),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, "#183827")
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    icon_nobre(ft.Icons.ARROW_DOWNWARD, size=13, color=DANGER_RED),
                                    ft.Text("Saídas", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                ],
                                spacing=2
                            ),
                            ft.Text(formatar_moeda(resumo["saidas"]), size=12, weight=ft.FontWeight.BOLD, color=DANGER_RED)
                        ],
                        spacing=2
                    ),
                    expand=True,
                    padding=8,
                    border_radius=border_radius_all(8),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, "#3A1B22")
                )
            ],
            spacing=6
        )

        card_saldo_mes = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Saldo do Ciclo Atual", size=10, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text(formatar_moeda(resumo["saldo"]), size=15, weight=ft.FontWeight.BOLD, color=cor_saldo)
                        ],
                        spacing=1
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                icon_nobre(ft.Icons.SHIELD_MOON, size=13, color=cores["light"]),
                                                ft.Text("Reserva", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                            ],
                                            spacing=2
                                        ),
                                        ft.Text(formatar_moeda(resumo.get("reserva", 0.0)), size=12, weight=ft.FontWeight.BOLD, color=cores["light"])
                                    ],
                                    spacing=1,
                                    horizontal_alignment=ft.CrossAxisAlignment.END
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_size=15,
                                    icon_color=cores["light"],
                                    tooltip="Editar Reserva",
                                    on_click=abrir_modal_editar_reserva,
                                    style=ft.ButtonStyle(padding=padding_all(2))
                                )
                            ],
                            spacing=1,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=10,
            border_radius=border_radius_all(8),
            bgcolor=cores["container"],
            border=border_all(1, cores["border_color"])
        )

        # Barra de Teto de Gastos
        teto = resumo.get("teto", 3000.0)
        saidas = resumo["saidas"]
        pct_teto = (saidas / teto * 100) if teto > 0 else 0.0
        barra_teto_val = min(1.0, max(0.0, saidas / teto if teto > 0 else 0.0))

        if pct_teto <= 75:
            cor_teto = SUCCESS_GREEN
        elif pct_teto <= 100:
            cor_teto = "#F59E0B"
        else:
            cor_teto = DANGER_RED

        aviso_estouro = None
        if saidas > teto:
            estouro = saidas - teto
            aviso_estouro = ft.Text(f"⚠️ Teto ultrapassado em {formatar_moeda(estouro)}!", size=10, color=DANGER_RED, weight=ft.FontWeight.BOLD)

        card_teto = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    icon_nobre(ft.Icons.SPEED, size=15, color=cores["light"]),
                                    ft.Text("Teto Mensal", size=11, weight=ft.FontWeight.BOLD, color=cores["light"]),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_size=14,
                                        icon_color=cores["light"],
                                        tooltip="Editar Teto",
                                        on_click=abrir_modal_editar_teto,
                                        style=ft.ButtonStyle(padding=padding_all(2))
                                    )
                                ],
                                spacing=2,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Text(f"{formatar_moeda(teto)}", size=11, weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.ProgressBar(
                        value=barra_teto_val,
                        color=cor_teto,
                        bgcolor=cores["bg_input"],
                        height=6,
                        border_radius=border_radius_all(3)
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"Gasto: {formatar_moeda(saidas)} ({pct_teto:.1f}%)", size=9, color=cor_teto, weight=ft.FontWeight.W_500),
                            ft.Text(f"Livre: {formatar_moeda(max(0.0, teto - saidas))}", size=9, color=cores.get("text_muted", TEXT_MUTED))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    aviso_estouro if aviso_estouro else ft.Container()
                ],
                spacing=3
            ),
            padding=8,
            border_radius=border_radius_all(8),
            bgcolor=cores["bg_input"],
            border=border_all(1, cor_teto if saidas > teto else cores.get("border_subtle", "#2C2C3D"))
        )

        resumo_container.controls = [
            alerta_divida_container,
            card_saldo_mes,
            card_teto,
            cards_kpi
        ]
        try:
            resumo_container.update()
        except Exception:
            pass

    def renderizar_saude_financeira():
        saude = storage.calcular_saude_financeira(mes_atual_iso)
        cor_badge = saude["cor"]
        
        saude_container.controls = [
            ft.Row(
                controls=[
                    icon_nobre(ft.Icons.HEALTH_AND_SAFETY_ROUNDED, size=16, color=cor_badge),
                    ft.Text("Saúde Financeira", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=12),
                    ft.Container(
                        content=ft.Text(saude["status"], size=9, color=cor_badge, weight=ft.FontWeight.BOLD),
                        padding=padding_symmetric(horizontal=6, vertical=2),
                        border_radius=border_radius_all(4),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cor_badge)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Text(saude["descricao"], size=10, color=cores.get("text_secondary", TEXT_SECONDARY))
        ]
        try:
            saude_container.update()
        except Exception:
            pass

    def renderizar_dashboard_categorias():
        dados_cat = storage.calcular_gastos_por_categoria(mes_atual_iso)
        total_saidas = dados_cat["total_saidas"]
        categorias = dados_cat["categorias"]

        if total_saidas <= 0 or not categorias:
            dashboard_categorias_container.controls = [
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.CATEGORY_ROUNDED, size=16, color=cores["light"]),
                        ft.Text("Distribuição de Gastos", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=12),
                    ],
                    spacing=4
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                ft.Container(
                    content=ft.Text("Nenhum custo registrado neste mês.", size=10, color=cores.get("text_muted", TEXT_MUTED), italic=True),
                    padding=padding_symmetric(horizontal=6, vertical=4)
                )
            ]
        else:
            linhas_barras = []
            for item in categorias:
                cat_nome = item["categoria"]
                val = item["valor"]
                pct = item["porcentagem"]
                cor = CORES_CATEGORIAS.get(cat_nome, cores["primary"])
                icone = ICONES_CATEGORIAS.get(cat_nome, ft.Icons.CATEGORY)

                barra_frac = min(1.0, max(0.02, pct / 100.0))

                linha_item = ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        icon_nobre(icone, size=13, color=cor),
                                        ft.Text(cat_nome, size=11, weight=ft.FontWeight.W_500, color=cores.get("text_primary", TEXT_PRIMARY))
                                    ],
                                    spacing=4
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(f"{pct:.1f}%", size=10, weight=ft.FontWeight.BOLD, color=cor),
                                        ft.Text(f"({formatar_moeda(val)})", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                    ],
                                    spacing=2
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.ProgressBar(
                            value=barra_frac,
                            color=cor,
                            bgcolor="#222230",
                            height=5,
                            border_radius=border_radius_all(3)
                        )
                    ],
                    spacing=2
                )
                linhas_barras.append(linha_item)

            dashboard_categorias_container.controls = [
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                icon_nobre(ft.Icons.BAR_CHART_ROUNDED, size=16, color=cores["light"]),
                                ft.Text("Gastos por Categoria", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=12),
                            ],
                            spacing=4
                        ),
                        ft.Text(f"Total: {formatar_moeda(total_saidas)}", size=10, weight=ft.FontWeight.BOLD, color=DANGER_RED)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                ft.Column(controls=linhas_barras, spacing=6)
            ]

        try:
            dashboard_categorias_container.update()
        except Exception:
            pass

    def renderizar_projecao():
        proj = storage.calcular_projecao()
        
        cor_30 = SUCCESS_GREEN if proj["projecao_30d"] >= 0 else DANGER_RED
        cor_60 = SUCCESS_GREEN if proj["projecao_60d"] >= 0 else DANGER_RED
        cor_90 = SUCCESS_GREEN if proj["projecao_90d"] >= 0 else DANGER_RED

        projecao_container.controls = [
            ft.Row(
                controls=[
                    icon_nobre(ft.Icons.AUTO_AWESOME_ROUNDED, size=16, color=cores["light"]),
                    ft.Text("Projeção do Tesouro", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=12),
                ],
                spacing=4
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("30 Dias", size=9, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD),
                                ft.Text(formatar_moeda(proj["projecao_30d"]), size=10, weight=ft.FontWeight.BOLD, color=cor_30)
                            ],
                            spacing=1,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=6,
                        border_radius=border_radius_all(6),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores.get("border_subtle", "#26263A"))
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("60 Dias", size=9, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD),
                                ft.Text(formatar_moeda(proj["projecao_60d"]), size=10, weight=ft.FontWeight.BOLD, color=cor_60)
                            ],
                            spacing=1,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=6,
                        border_radius=border_radius_all(6),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores.get("border_subtle", "#26263A"))
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("90 Dias", size=9, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD),
                                ft.Text(formatar_moeda(proj["projecao_90d"]), size=10, weight=ft.FontWeight.BOLD, color=cor_90)
                            ],
                            spacing=1,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=6,
                        border_radius=border_radius_all(6),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores.get("border_subtle", "#26263A"))
                    )
                ],
                spacing=4
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.FORMAT_QUOTE_ROUNDED, size=18, color=cores["light"]),
                        ft.Column(
                            controls=[
                                ft.Text("Palavra do Rei Joaquim:", size=10, weight=ft.FontWeight.BOLD, color=cores["light"]),
                                ft.Text(proj["mensagem_rei"], size=10, color=cores.get("text_primary", TEXT_PRIMARY), italic=True)
                            ],
                            spacing=1,
                            expand=True
                        )
                    ],
                    spacing=6,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                padding=8,
                border_radius=border_radius_all(6),
                bgcolor=cores["container"],
                border=border_all(1, cores["border_color"])
            )
        ]
        try:
            projecao_container.update()
        except Exception:
            pass

    def excluir_transacao(tid: str):
        storage.remover_transacao(tid)
        mostrar_notificacao(page, "Transação removida com sucesso.", sucesso=True)
        renderizar_tudo()
        if on_update_callback:
            on_update_callback()
        page.update()

    def renderizar_transacoes():
        txs = storage.obter_transacoes_mes(mes_atual_iso)
        if not txs:
            lista_transacoes_col.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            icon_nobre(ft.Icons.RECEIPT_LONG, size=24, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Nenhum lançamento neste ciclo.", size=11, color=cores.get("text_muted", TEXT_MUTED)),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2
                    ),
                    padding=12,
                    alignment=ft.Alignment(0, 0)
                )
            ]
        else:
            cards = []
            for t in reversed(txs):
                is_entrada = (t["tipo"] == "entrada")
                cor_val = SUCCESS_GREEN if is_entrada else DANGER_RED
                sinal = "+" if is_entrada else "-"
                icone = ft.Icons.ARROW_DROP_UP if is_entrada else ft.Icons.ARROW_DROP_DOWN
                
                dt_formatada = t.get("data", "")
                try:
                    dt_obj = datetime.strptime(dt_formatada, "%Y-%m-%d")
                    dt_formatada = dt_obj.strftime("%d/%m")
                except Exception:
                    pass

                cat_nome = t.get("categoria", "Geral")
                cor_cat = CORES_CATEGORIAS.get(cat_nome, cores["primary"])

                card = ft.Container(
                    content=ft.Row(
                        controls=[
                            icon_nobre(icone, color=cor_val, size=20),
                            ft.Column(
                                controls=[
                                    ft.Text(t["titulo"], size=12, weight=ft.FontWeight.W_500, color=cores.get("text_primary", TEXT_PRIMARY)),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Text(cat_nome, size=9, color=cor_cat),
                                                padding=padding_symmetric(horizontal=4, vertical=1),
                                                border_radius=border_radius_all(3),
                                                bgcolor=cores["bg_input"]
                                            ),
                                            ft.Text(f"• {dt_formatada}", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                        ],
                                        spacing=4
                                    )
                                ],
                                spacing=1,
                                expand=True
                            ),
                            ft.Text(f"{sinal} {formatar_moeda(t['valor'])}", size=11, weight=ft.FontWeight.BOLD, color=cor_val),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_size=16,
                                icon_color="#64748B",
                                on_click=lambda e, tid=t["id"]: excluir_transacao(tid),
                                style=ft.ButtonStyle(padding=padding_all(2))
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4
                    ),
                    padding=padding_symmetric(horizontal=8, vertical=4),
                    border_radius=border_radius_all(6),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, cores.get("border_subtle", "#262636"))
                )
                cards.append(card)
            lista_transacoes_col.controls = cards
            
        try:
            lista_transacoes_col.update()
        except Exception:
            pass

    def renderizar_tudo():
        renderizar_resumo()
        renderizar_saude_financeira()
        renderizar_dashboard_categorias()
        renderizar_projecao()
        renderizar_transacoes()

    def abrir_modal_transacao(e):
        tipo_selecionado = {"valor": "saida"}
        
        txt_titulo = ft.TextField(
            label="Título / Motivo",
            hint_text="Ex: Banquete Nobre, Armaduras",
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            text_size=13,
            color=cores.get("text_primary", TEXT_PRIMARY)
        )
        
        txt_valor = ft.TextField(
            label="Valor em Ouro",
            hint_text="Ex: 150.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            text_size=13,
            color=cores.get("text_primary", TEXT_PRIMARY)
        )
        
        dropdown_categoria = ft.Dropdown(
            label="Categoria",
            options=[
                ft.dropdown.Option("Alimentação"),
                ft.dropdown.Option("Moradia"),
                ft.dropdown.Option("Lazer"),
                ft.dropdown.Option("Saúde"),
                ft.dropdown.Option("Investimentos"),
                ft.dropdown.Option("Essenciais"),
                ft.dropdown.Option("Tributos"),
                ft.dropdown.Option("Reino & Armas"),
                ft.dropdown.Option("Poupança"),
                ft.dropdown.Option("Outros")
            ],
            value="Alimentação",
            bgcolor=cores["bg_surface"],
            border_color=cores.get("border_subtle", "#36364A"),
            color=cores.get("text_primary", TEXT_PRIMARY)
        )

        btn_tipo_saida = ft.Container(
            content=ft.Text("Despesa (Saída)", size=12, color="#FFFFFF", weight=ft.FontWeight.BOLD),
            padding=padding_symmetric(horizontal=12, vertical=8),
            border_radius=border_radius_all(8),
            bgcolor=DANGER_RED,
            expand=True,
            alignment=ft.Alignment(0, 0)
        )
        
        btn_tipo_entrada = ft.Container(
            content=ft.Text("Receita (Entrada)", size=12, color=cores.get("text_primary", TEXT_PRIMARY), weight=ft.FontWeight.BOLD),
            padding=padding_symmetric(horizontal=12, vertical=8),
            border_radius=border_radius_all(8),
            bgcolor=cores["bg_input"],
            expand=True,
            alignment=ft.Alignment(0, 0)
        )

        def set_tipo(t):
            tipo_selecionado["valor"] = t
            if t == "saida":
                btn_tipo_saida.bgcolor = DANGER_RED
                btn_tipo_saida.content.color = "#FFFFFF"
                btn_tipo_entrada.bgcolor = cores["bg_input"]
                btn_tipo_entrada.content.color = cores.get("text_primary", TEXT_PRIMARY)
            else:
                btn_tipo_entrada.bgcolor = SUCCESS_GREEN
                btn_tipo_entrada.content.color = "#FFFFFF"
                btn_tipo_saida.bgcolor = cores["bg_input"]
                btn_tipo_saida.content.color = cores.get("text_primary", TEXT_PRIMARY)
            btn_tipo_saida.update()
            btn_tipo_entrada.update()

        btn_tipo_saida.on_click = lambda e: set_tipo("saida")
        btn_tipo_entrada.on_click = lambda e: set_tipo("entrada")

        seletor_tipo = ft.Row(
            controls=[btn_tipo_saida, btn_tipo_entrada],
            spacing=8
        )

        def salvar_transacao(e_salvar):
            titulo = txt_titulo.value
            if not titulo or not titulo.strip():
                txt_titulo.error_text = "Informe o título do lançamento!"
                txt_titulo.update()
                return

            try:
                val = float(txt_valor.value.replace(" ", "").replace(".", "").replace(",", "."))
                if val <= 0:
                    raise ValueError
            except Exception:
                txt_valor.error_text = "Informe um valor positivo válido!"
                txt_valor.update()
                return

            storage.adicionar_transacao(
                tipo=tipo_selecionado["valor"],
                titulo=titulo.strip(),
                valor=val,
                categoria=dropdown_categoria.value,
                data_str=date.today().isoformat()
            )

            fechar_modal(dialogo_transacao)
            mostrar_notificacao(page, "Lançamento registrado nas arcas do reino!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()
            page.update()

        dialogo_transacao = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.RECEIPT, color=cores["light"], size=20),
                    ft.Text("Novo Lançamento Real", size=15, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        seletor_tipo,
                        txt_titulo,
                        txt_valor,
                        dropdown_categoria
                    ],
                    spacing=8,
                    tight=True,
                    scroll=ft.ScrollMode.ADAPTIVE
                ),
                width=300,
                constraints=ft.BoxConstraints(max_height=380)
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo_transacao)),
                botao_preenchido("Registrar", bgcolor=cores["primary"], on_click=salvar_transacao)
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )
        abrir_dialogo(dialogo_transacao)

    btn_nova_transacao = criar_botao_primario(
        texto="Novo Lançamento Real",
        icone=ft.Icons.ADD,
        on_click=abrir_modal_transacao,
        expand=True
    )

    card_resumo = criar_card_nobre(conteudo=resumo_container, borda_dourada=True, padding=8)
    card_saude = criar_card_nobre(conteudo=saude_container, borda_roxa=True, padding=8)
    card_categorias = criar_card_nobre(conteudo=dashboard_categorias_container, padding=8)
    card_projecao = criar_card_nobre(conteudo=projecao_container, borda_dourada=True, padding=8)
    
    card_transacoes = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                icon_nobre(ft.Icons.HISTORY, size=16, color=cores["light"]),
                                ft.Text("Livro-Caixa do Reino", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=12),
                            ],
                            spacing=4
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                            icon_color=cores["primary"],
                            icon_size=20,
                            tooltip="Adicionar Lançamento",
                            on_click=abrir_modal_transacao,
                            style=ft.ButtonStyle(padding=padding_all(2))
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                lista_transacoes_col,
                ft.Container(height=4),
                ft.Row(controls=[btn_nova_transacao])
            ],
            spacing=6
        ),
        padding=8
    )

    renderizar_tudo()

    return ft.ListView(
        controls=[
            card_resumo,
            card_saude,
            card_categorias,
            card_projecao,
            card_transacoes,
            ft.Container(height=24)
        ],
        spacing=8,
        padding=10,
        expand=True
    )
