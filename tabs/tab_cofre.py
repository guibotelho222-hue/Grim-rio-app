"""
Grimório V2.0 - Aba 3: Cofre (Finanças Inteligentes & Gestão Financeira Real)
Gestão Real do Cofre, Edição Direta de Teto de Gastos e Reserva Guardada,
Barra de Progresso Orçamentária, Dashboard por Categoria e Projeção Inteligente.
"""

from datetime import datetime, date
import math
import flet as ft
import flet.canvas as cv
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
    """Retorna a visão completa da Aba Cofre com edição direta de teto/reserva e tema dinâmico."""

    cfg = storage.obter_configuracoes()
    cores = get_theme_colors(cfg.get("tema_atual", "Dark Fantasy Dourado"))

    mes_atual_iso = datetime.now().strftime("%Y-%m")
    
    resumo_container = ft.Column(spacing=8)
    teto_container = ft.Column(spacing=6)
    saude_container = ft.Column(spacing=6)
    dashboard_categorias_container = ft.Column(spacing=8)
    projecao_container = ft.Column(spacing=8)
    lista_transacoes_col = ft.Column(spacing=6)
    alerta_divida_container = ft.Column(spacing=4, visible=False)

    def formatar_moeda(val: float) -> str:
        s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{s} Ouro"

    # ==================== MODAL DE EDIÇÃO DE RESERVA ====================
    def abrir_modal_editar_reserva(e):
        reserva_atual = storage.data["cofre"].get("reserva_do_reino", 0.0)
        
        txt_reserva = ft.TextField(
            label="Reserva Guardada (Ouro)",
            value=f"{reserva_atual:.2f}".replace(".", ","),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            color=cores.get("text_primary", TEXT_PRIMARY),
            text_size=14
        )

        def salvar_reserva(e_salvar):
            try:
                val = float(txt_reserva.value.replace(" ", "").replace(".", "").replace(",", "."))
                if val < 0:
                    raise ValueError
            except Exception:
                txt_reserva.error_text = "Informe um valor numérico válido (ex: 1500,00)!"
                txt_reserva.update()
                return

            storage.atualizar_reserva_guardada(val)
            fechar_modal(dialogo_reserva)
            mostrar_notificacao(page, f"Reserva Guardada ajustada para {formatar_moeda(val)}!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()
            page.update()

        dialogo_reserva = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.SHIELD_MOON, color=cores["light"], size=20),
                    ft.Text("Ajustar Reserva Guardada", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Column(
                controls=[
                    ft.Text("Defina o montante real preservado nas arcas do reino:", size=11, color=cores.get("text_secondary", TEXT_SECONDARY)),
                    txt_reserva
                ],
                spacing=10,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo_reserva)),
                botao_preenchido(
                    texto="Salvar Reserva",
                    bgcolor=cores["primary"],
                    color="#121214",
                    on_click=salvar_reserva
                )
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )

        abrir_dialogo(dialogo_reserva)

    # ==================== MODAL DE EDIÇÃO DE TETO ====================
    def abrir_modal_editar_teto(e):
        teto_atual = storage.data["cofre"].get("teto_gastos_mes", 3000.0)
        
        txt_teto = ft.TextField(
            label="Teto de Gastos Mensal (Ouro)",
            value=f"{teto_atual:.2f}".replace(".", ","),
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor=cores["bg_input"],
            border_color=cores.get("border_subtle", "#36364A"),
            focused_border_color=cores["primary"],
            color=cores.get("text_primary", TEXT_PRIMARY),
            text_size=14
        )

        def salvar_teto(e_salvar):
            try:
                val = float(txt_teto.value.replace(" ", "").replace(".", "").replace(",", "."))
                if val <= 0:
                    raise ValueError
            except Exception:
                txt_teto.error_text = "Informe um teto positivo válido (ex: 2500,00)!"
                txt_teto.update()
                return

            storage.atualizar_teto_gastos(val)
            fechar_modal(dialogo_teto)
            mostrar_notificacao(page, f"Teto de gastos ajustado para {formatar_moeda(val)}!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()
            page.update()

        dialogo_teto = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.SPEED, color=cores["light"], size=20),
                    ft.Text("Ajustar Teto de Gastos do Mês", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Column(
                controls=[
                    ft.Text("Defina o limite máximo de despesas para o ciclo atual:", size=11, color=cores.get("text_secondary", TEXT_SECONDARY)),
                    txt_teto
                ],
                spacing=10,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo_teto)),
                botao_preenchido(
                    texto="Salvar Teto",
                    bgcolor=cores["primary"],
                    color="#121214",
                    on_click=salvar_teto
                )
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )

        abrir_dialogo(dialogo_teto)

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

    # ==================== RENDERIZAÇÃO DO RESUMO & TETO ====================
    def renderizar_resumo():
        resumo = storage.calcular_resumo_mes(mes_atual_iso)
        
        divida = resumo["divida"]
        if divida > 0:
            alerta_divida_container.controls = [
                ft.Container(
                    content=ft.Row(
                        controls=[
                            icon_nobre(ft.Icons.WARNING_AMBER_ROUNDED, color=DANGER_RED, size=24),
                            ft.Column(
                                controls=[
                                    ft.Text("Alerta Real: Dívida da Coroa!", weight=ft.FontWeight.BOLD, color=DANGER_RED, size=13),
                                    ft.Text(f"Estouro anterior consolidado: {formatar_moeda(divida)}. Economize nas despesas deste mês para amortizar a dívida.", size=11, color=cores.get("text_secondary", TEXT_SECONDARY))
                                ],
                                spacing=2,
                                expand=True
                            )
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=10,
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
                                    icon_nobre(ft.Icons.ARROW_UPWARD, size=14, color=SUCCESS_GREEN),
                                    ft.Text("Entradas Reais", size=11, color=cores.get("text_muted", TEXT_MUTED))
                                ],
                                spacing=4
                            ),
                            ft.Text(formatar_moeda(resumo["entradas"]), size=13, weight=ft.FontWeight.BOLD, color=SUCCESS_GREEN)
                        ],
                        spacing=3
                    ),
                    expand=True,
                    padding=10,
                    border_radius=border_radius_all(10),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, "#183827")
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    icon_nobre(ft.Icons.ARROW_DOWNWARD, size=14, color=DANGER_RED),
                                    ft.Text("Saídas Reais", size=11, color=cores.get("text_muted", TEXT_MUTED))
                                ],
                                spacing=4
                            ),
                            ft.Text(formatar_moeda(resumo["saidas"]), size=13, weight=ft.FontWeight.BOLD, color=DANGER_RED)
                        ],
                        spacing=3
                    ),
                    expand=True,
                    padding=10,
                    border_radius=border_radius_all(10),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, "#3A1B22")
                )
            ],
            spacing=8
        )

        card_saldo_mes = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Saldo do Ciclo Atual", size=11, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text(formatar_moeda(resumo["saldo"]), size=17, weight=ft.FontWeight.BOLD, color=cor_saldo)
                        ],
                        spacing=2
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                icon_nobre(ft.Icons.SHIELD_MOON, size=14, color=cores["light"]),
                                                ft.Text("Reserva Guardada", size=10, color=cores.get("text_muted", TEXT_MUTED))
                                            ],
                                            spacing=4
                                        ),
                                        ft.Text(formatar_moeda(resumo["reserva"]), size=13, weight=ft.FontWeight.BOLD, color=cores["light"])
                                    ],
                                    spacing=1,
                                    horizontal_alignment=ft.CrossAxisAlignment.END
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_size=16,
                                    icon_color=cores["light"],
                                    tooltip="Editar Reserva Guardada",
                                    on_click=abrir_modal_editar_reserva
                                )
                            ],
                            spacing=2,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=12,
            border_radius=border_radius_all(10),
            bgcolor=cores["container"],
            border=border_all(1, cores["border_color"])
        )

        # Barra e Cartão de Teto de Gastos do Mês
        teto = resumo.get("teto_gastos", 3000.0)
        saidas = resumo["saidas"]
        pct_teto = (saidas / teto * 100) if teto > 0 else 0.0
        barra_teto_val = min(1.0, max(0.0, saidas / teto if teto > 0 else 0.0))

        if pct_teto <= 75:
            cor_teto = SUCCESS_GREEN
        elif pct_teto <= 100:
            cor_teto = "#F59E0B" # Alerta Laranja/Dourado
        else:
            cor_teto = DANGER_RED

        aviso_estouro = None
        if saidas > teto:
            estouro = saidas - teto
            aviso_estouro = ft.Text(f"⚠️ Atenção Real: Teto ultrapassado em {formatar_moeda(estouro)}!", size=11, color=DANGER_RED, weight=ft.FontWeight.BOLD)

        card_teto = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    icon_nobre(ft.Icons.SPEED, size=16, color=cores["light"]),
                                    ft.Text("Teto de Gastos do Mês", size=12, weight=ft.FontWeight.BOLD, color=cores["light"]),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_size=16,
                                        icon_color=cores["light"],
                                        tooltip="Editar Teto de Gastos",
                                        on_click=abrir_modal_editar_teto
                                    )
                                ],
                                spacing=4,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Text(f"{formatar_moeda(teto)}", size=12, weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.ProgressBar(
                        value=barra_teto_val,
                        color=cor_teto,
                        bgcolor=cores["bg_input"],
                        height=8,
                        border_radius=border_radius_all(4)
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"Consumido: {formatar_moeda(saidas)} ({pct_teto:.1f}%)", size=10, color=cor_teto, weight=ft.FontWeight.W_500),
                            ft.Text(f"Disponível: {formatar_moeda(max(0.0, teto - saidas))}", size=10, color=cores.get("text_muted", TEXT_MUTED))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    aviso_estouro if aviso_estouro else ft.Container()
                ],
                spacing=4
            ),
            padding=10,
            border_radius=border_radius_all(10),
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
                    icon_nobre(ft.Icons.HEALTH_AND_SAFETY_ROUNDED, size=18, color=cor_badge),
                    ft.Text("Saúde Financeira do Reino", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=13),
                    ft.Container(
                        content=ft.Text(saude["status"], size=10, color=cor_badge, weight=ft.FontWeight.BOLD),
                        padding=padding_symmetric(horizontal=8, vertical=3),
                        border_radius=border_radius_all(6),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cor_badge)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Text(saude["descricao"], size=11, color=cores.get("text_secondary", TEXT_SECONDARY))
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
                        icon_nobre(ft.Icons.CATEGORY_ROUNDED, size=18, color=cores["light"]),
                        ft.Text("Distribuição de Gastos do Reino", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=13),
                    ],
                    spacing=6
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                ft.Container(
                    content=ft.Text("Nenhum custo registrado neste mês. O ouro do reino permanece sob guarda inviolável nas arcas reais.", size=11, color=cores.get("text_muted", TEXT_MUTED), italic=True),
                    padding=padding_symmetric(horizontal=8, vertical=6)
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
                                        icon_nobre(icone, size=14, color=cor),
                                        ft.Text(cat_nome, size=12, weight=ft.FontWeight.W_500, color=cores.get("text_primary", TEXT_PRIMARY))
                                    ],
                                    spacing=6
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(f"{pct:.1f}%", size=11, weight=ft.FontWeight.BOLD, color=cor),
                                        ft.Text(f"({formatar_moeda(val)})", size=11, color=cores.get("text_muted", TEXT_MUTED))
                                    ],
                                    spacing=4
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.ProgressBar(
                            value=barra_frac,
                            color=cor,
                            bgcolor="#222230",
                            height=6,
                            border_radius=border_radius_all(3)
                        )
                    ],
                    spacing=3
                )
                linhas_barras.append(linha_item)

            dashboard_categorias_container.controls = [
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                icon_nobre(ft.Icons.BAR_CHART_ROUNDED, size=18, color=cores["light"]),
                                ft.Text("Distribuição de Gastos por Categoria", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=13),
                            ],
                            spacing=6
                        ),
                        ft.Text(f"Total: {formatar_moeda(total_saidas)}", size=11, weight=ft.FontWeight.BOLD, color=DANGER_RED)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                ft.Column(controls=linhas_barras, spacing=8)
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
        
        cor_saldo_dia = SUCCESS_GREEN if proj["saldo_diario"] >= 0 else DANGER_RED
        sinal_dia = "+" if proj["saldo_diario"] >= 0 else ""

        projecao_container.controls = [
            ft.Row(
                controls=[
                    icon_nobre(ft.Icons.AUTO_AWESOME_ROUNDED, size=18, color=cores["light"]),
                    ft.Text("Engine de Projeção Inteligente do Tesouro", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=13),
                ],
                spacing=6
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("30 Dias", size=10, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD),
                                ft.Text(formatar_moeda(proj["projecao_30d"]), size=12, weight=ft.FontWeight.BOLD, color=cor_30)
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=8,
                        border_radius=border_radius_all(8),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores.get("border_subtle", "#26263A"))
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("60 Dias", size=10, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD),
                                ft.Text(formatar_moeda(proj["projecao_60d"]), size=12, weight=ft.FontWeight.BOLD, color=cor_60)
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=8,
                        border_radius=border_radius_all(8),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores.get("border_subtle", "#26263A"))
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("90 Dias", size=10, color=cores.get("text_muted", TEXT_MUTED), weight=ft.FontWeight.BOLD),
                                ft.Text(formatar_moeda(proj["projecao_90d"]), size=12, weight=ft.FontWeight.BOLD, color=cor_90)
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=8,
                        border_radius=border_radius_all(8),
                        bgcolor=cores["bg_input"],
                        border=border_all(1, cores.get("border_subtle", "#26263A"))
                    )
                ],
                spacing=6
            ),
            ft.Row(
                controls=[
                    ft.Text(f"Fluxo Diário Médio: {sinal_dia}{formatar_moeda(proj['saldo_diario'])}/dia", size=10, color=cor_saldo_dia, weight=ft.FontWeight.W_500),
                    ft.Text("Base: Saldo Real + Reserva", size=10, color=cores["light"])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.FORMAT_QUOTE_ROUNDED, size=20, color=cores["light"]),
                        ft.Column(
                            controls=[
                                ft.Text("Palavra do Rei Joaquim:", size=11, weight=ft.FontWeight.BOLD, color=cores["light"]),
                                ft.Text(proj["mensagem_rei"], size=11, color=cores.get("text_primary", TEXT_PRIMARY), italic=True)
                            ],
                            spacing=2,
                            expand=True
                        )
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                padding=10,
                border_radius=border_radius_all(8),
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
        mostrar_notificacao(page, "Transação removida do livro-caixa.", sucesso=True)
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
                            icon_nobre(ft.Icons.RECEIPT_LONG, size=28, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Nenhum lançamento no ciclo atual.", size=12, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Registre receitas ou despesas reais no botão acima.", size=11, color=cores["light"])
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4
                    ),
                    padding=16,
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
                            icon_nobre(icone, color=cor_val, size=24),
                            ft.Column(
                                controls=[
                                    ft.Text(t["titulo"], size=13, weight=ft.FontWeight.W_500, color=cores.get("text_primary", TEXT_PRIMARY)),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Text(cat_nome, size=10, color=cor_cat),
                                                padding=padding_symmetric(horizontal=4, vertical=1),
                                                border_radius=border_radius_all(3),
                                                bgcolor=cores["bg_input"]
                                            ),
                                            ft.Text(f"• {dt_formatada}", size=11, color=cores.get("text_muted", TEXT_MUTED))
                                        ],
                                        spacing=4
                                    )
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Text(f"{sinal} {formatar_moeda(t['valor'])}", size=13, weight=ft.FontWeight.BOLD, color=cor_val),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_size=18,
                                icon_color="#64748B",
                                on_click=lambda e, tid=t["id"]: excluir_transacao(tid)
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=6
                    ),
                    padding=padding_symmetric(horizontal=10, vertical=6),
                    border_radius=border_radius_all(8),
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
            hint_text="Ex: Feira Nobre, Armas, Aluguel",
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
            content=ft.Text("Despesa (Saída)", size=12, color=cores.get("text_primary", TEXT_PRIMARY), weight=ft.FontWeight.BOLD),
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
                btn_tipo_entrada.bgcolor = cores["bg_input"]
            else:
                btn_tipo_saida.bgcolor = cores["bg_input"]
                btn_tipo_entrada.bgcolor = SUCCESS_GREEN
            btn_tipo_saida.update()
            btn_tipo_entrada.update()

        btn_tipo_saida.on_click = lambda e: set_tipo("saida")
        btn_tipo_entrada.on_click = lambda e: set_tipo("entrada")

        def salvar_transacao(e_salvar):
            if not txt_titulo.value or not txt_titulo.value.strip():
                txt_titulo.error_text = "Informe a descrição!"
                txt_titulo.update()
                return
            try:
                val = float(txt_valor.value.replace(" ", "").replace(".", "").replace(",", "."))
                if val <= 0:
                    raise ValueError
            except Exception:
                txt_valor.error_text = "Informe um valor numérico válido!"
                txt_valor.update()
                return
                
            storage.adicionar_transacao(
                tipo=tipo_selecionado["valor"],
                titulo=txt_titulo.value.strip(),
                valor=val,
                categoria=dropdown_categoria.value,
                data_str=date.today().isoformat()
            )
            
            fechar_modal(dialogo)
            mostrar_notificacao(page, "Lançamento computado com honra no livro do Cofre!", sucesso=True)
            renderizar_tudo()
            if on_update_callback:
                on_update_callback()
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.ATTACH_MONEY, color=cores["light"], size=20),
                    ft.Text("Registrar no Livro-Caixa", size=16, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Column(
                controls=[
                    ft.Row(controls=[btn_tipo_saida, btn_tipo_entrada], spacing=8),
                    txt_titulo,
                    txt_valor,
                    dropdown_categoria
                ],
                spacing=12,
                tight=True,
                width=340
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(dialogo)),
                botao_preenchido(
                    texto="Registrar",
                    bgcolor=cores["primary"],
                    color="#121214",
                    on_click=salvar_transacao
                )
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )

        abrir_dialogo(dialogo)

    def abrir_modal_historico(e):
        historico = storage.data["cofre"].get("historico_fechamentos", {})
        
        itens_historico = []
        if not historico:
            itens_historico.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            icon_nobre(ft.Icons.MENU_BOOK, size=32, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("Nenhum ciclo anterior fechado ainda.", size=12, color=cores.get("text_muted", TEXT_MUTED)),
                            ft.Text("O fechamento consolida automaticamente na virada de cada mês.", size=11, color=cores["light"], text_align=ft.TextAlign.CENTER)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4
                    ),
                    padding=20,
                    alignment=ft.Alignment(0, 0)
                )
            )
        else:
            for mes_chave in sorted(historico.keys(), reverse=True):
                info = historico[mes_chave]
                status = info.get("status", "neutro")
                cor_status = SUCCESS_GREEN if status == "superavit" else (DANGER_RED if status == "deficit" else cores.get("text_muted", TEXT_MUTED))
                status_label = "Superávit (+Reserva)" if status == "superavit" else ("Déficit (Dívida)" if status == "deficit" else "Equilibrado")
                
                card_mes = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(f"Ciclo {mes_chave}", weight=ft.FontWeight.BOLD, color=cores["light"], size=13),
                                    ft.Container(
                                        content=ft.Text(status_label, size=10, color=cor_status, weight=ft.FontWeight.BOLD),
                                        padding=padding_symmetric(horizontal=6, vertical=2),
                                        border_radius=border_radius_all(4),
                                        bgcolor=cores["bg_input"],
                                        border=border_all(1, cor_status)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                            ft.Row(
                                controls=[
                                    ft.Text(f"Entradas: {formatar_moeda(info.get('total_entradas', 0.0))}", size=11, color=SUCCESS_GREEN),
                                    ft.Text(f"Saídas: {formatar_moeda(info.get('total_saidas', 0.0))}", size=11, color=DANGER_RED),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Saldo Consolidado:", size=11, color=cores.get("text_muted", TEXT_MUTED)),
                                    ft.Text(formatar_moeda(info.get("saldo_final", 0.0)), size=12, weight=ft.FontWeight.BOLD, color=cor_status)
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Text(f"Fechado em: {info.get('data_fechamento', '')}", size=10, color=cores.get("text_muted", TEXT_MUTED), italic=True)
                        ],
                        spacing=4
                    ),
                    padding=10,
                    border_radius=border_radius_all(8),
                    bgcolor=cores["bg_input"],
                    border=border_all(1, cores.get("border_subtle", "#36364A"))
                )
                itens_historico.append(card_mes)

        dialogo_hist = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    icon_nobre(ft.Icons.MENU_BOOK, color=cores["light"], size=20),
                    ft.Text("📜 Histórico & Balanços Anteriores", size=15, weight=ft.FontWeight.BOLD, color=cores["light"])
                ],
                spacing=8
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=itens_historico,
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO
                ),
                width=350,
                height=300
            ),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: fechar_modal(dialogo_hist))
            ],
            bgcolor=cores["bg_card"],
            shape=ft.RoundedRectangleBorder(radius=BORDER_RADIUS)
        )

        abrir_dialogo(dialogo_hist)

    botoes_acao_row = ft.Row(
        controls=[
            criar_botao_primario(
                texto="➕ Nova Transação",
                icone=ft.Icons.ADD_CIRCLE,
                on_click=abrir_modal_transacao,
                cor_fundo=cores["primary"],
                expand=True
            ),
            criar_botao_primario(
                texto="📜 Balanços Anteriores",
                icone=ft.Icons.HISTORY,
                on_click=abrir_modal_historico,
                cor_fundo=cores["secondary"],
                cor_texto="#FFFFFF",
                expand=True
            )
        ],
        spacing=8
    )

    secao_principal = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.SAVINGS, size=18, color=cores["light"]),
                        ft.Text(f"Cofre Real • Mês {mes_atual_iso}", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=14)
                    ],
                    spacing=6
                ),
                resumo_container,
                botoes_acao_row
            ],
            spacing=10
        ),
        borda_dourada=True
    )

    secao_saude = criar_card_nobre(
        conteudo=saude_container
    )

    secao_categorias = criar_card_nobre(
        conteudo=dashboard_categorias_container,
        borda_dourada=False
    )

    secao_projecao = criar_card_nobre(
        conteudo=projecao_container,
        borda_roxa=True
    )

    secao_transacoes = criar_card_nobre(
        conteudo=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        icon_nobre(ft.Icons.RECEIPT_LONG, size=18, color=cores["light"]),
                        ft.Text("Lançamentos do Mês Atual", weight=ft.FontWeight.BOLD, color=cores.get("text_primary", TEXT_PRIMARY), size=14)
                    ],
                    spacing=6
                ),
                ft.Divider(height=1, color=cores.get("border_subtle", "#2C2C3D")),
                lista_transacoes_col
            ],
            spacing=10
        )
    )

    renderizar_tudo()

    return ft.ListView(
        controls=[
            secao_principal,
            secao_saude,
            secao_categorias,
            secao_projecao,
            secao_transacoes,
            ft.Container(height=30)
        ],
        spacing=14,
        padding=12,
        expand=True
    )
