"""
Grimório Mobile - Dark Fantasy Modern Theme & Engine de Temas
Paletas dinâmicas, cálculo de fase lunar, estilos mobile e áudio seguro para Android.
"""

import sys
import os
from datetime import datetime
import flet as ft

def resolve_path(relative_path: str) -> str:
    """Resolve caminhos em modo Dev, Executável e Pacote Mobile Android."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

# Compatibilidade e Engine de Áudio Segura para Mobile
try:
    import winsound
except ImportError:
    winsound = None

class FletAudioCompat(ft.Container):
    """Fallback simples caso ft.Audio não esteja disponível."""
    def __init__(self, src: str, autoplay: bool = False, volume: float = 1.0):
        super().__init__(visible=False, width=0, height=0)
        self.src = src
        self.autoplay = autoplay
        self.volume = volume

    def play(self):
        try:
            if winsound and os.path.exists(self.src):
                winsound.PlaySound(self.src, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def release(self):
        pass

if not hasattr(ft, "Audio"):
    ft.Audio = FletAudioCompat

def disparar_notificacao_sistema(titulo: str, mensagem: str, app_icon: str = None) -> bool:
    """Dispara notificação com fallback seguro para não quebrar em Mobile."""
    try:
        from plyer import notification
        icone = app_icon if (app_icon and os.path.exists(app_icon)) else resolve_path("assets/logo.png")
        notification.notify(
            title=titulo,
            message=mensagem,
            app_name="Grimório",
            app_icon=icone if (icone and os.path.exists(icone)) else None,
            timeout=5
        )
        return True
    except Exception as e:
        print(f"[Notificação Mobile] Fallback: {e}")
        return False

# Paletas Pré-definidas do Grimório Mobile
TEMAS = {
    "Dark Fantasy Dourado": {
        "bg_dark": "#121214",
        "bg_surface": "#181820",
        "bg_card": "#21212D",
        "bg_card_light": "#2A2A3B",
        "bg_input": "#16161E",
        "primary": "#D4AF37",
        "light": "#FFD700",
        "secondary": "#8B5CF6",
        "secondary_light": "#A78BFA",
        "container": "#2E2612",
        "border_color": "#D4AF37",
        "border_subtle": "#3D3418",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B"
    },
    "Roxo Arcano": {
        "bg_dark": "#0D0915",
        "bg_surface": "#150F24",
        "bg_card": "#1E1633",
        "bg_card_light": "#281E44",
        "bg_input": "#130E20",
        "primary": "#A855F7",
        "light": "#C084FC",
        "secondary": "#E879F9",
        "secondary_light": "#F0ABFC",
        "container": "#291340",
        "border_color": "#A855F7",
        "border_subtle": "#581C87",
        "text_primary": "#FAF5FF",
        "text_secondary": "#D8B4FE",
        "text_muted": "#7E22CE"
    },
    "Esmeralda Obscura": {
        "bg_dark": "#0B1411",
        "bg_surface": "#0F1E19",
        "bg_card": "#152C25",
        "bg_card_light": "#1C3A31",
        "bg_input": "#0D1814",
        "primary": "#10B981",
        "light": "#34D399",
        "secondary": "#059669",
        "secondary_light": "#6EE7B7",
        "container": "#063323",
        "border_color": "#10B981",
        "border_subtle": "#065F46",
        "text_primary": "#F0FDF4",
        "text_secondary": "#A7F3D0",
        "text_muted": "#047857"
    },
    "Chumbo Sóbrio": {
        "bg_dark": "#0F1115",
        "bg_surface": "#161920",
        "bg_card": "#1F232D",
        "bg_card_light": "#282E3B",
        "bg_input": "#14171E",
        "primary": "#94A3B8",
        "light": "#E2E8F0",
        "secondary": "#64748B",
        "secondary_light": "#CBD5E1",
        "container": "#1E293B",
        "border_color": "#94A3B8",
        "border_subtle": "#334155",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B"
    }
}

# Funções de Compatibilidade Flet
def border_all(width: float = 1, color: str = "#3D3418") -> ft.Border:
    if hasattr(ft, "Border") and hasattr(ft.Border, "all"):
        return ft.Border.all(width=width, color=color)
    return ft.border.all(width, color)

def border_only(**kwargs) -> ft.Border:
    if hasattr(ft, "Border") and hasattr(ft.Border, "only"):
        return ft.Border.only(**kwargs)
    return ft.border.only(**kwargs)

def border_radius_all(radius: float) -> ft.BorderRadius:
    if hasattr(ft, "BorderRadius") and hasattr(ft.BorderRadius, "all"):
        return ft.BorderRadius.all(radius)
    return ft.border_radius.all(radius)

def border_radius_only(**kwargs) -> ft.BorderRadius:
    if hasattr(ft, "BorderRadius") and hasattr(ft.BorderRadius, "only"):
        return ft.BorderRadius.only(**kwargs)
    return ft.border_radius.only(**kwargs)

def padding_all(pad: float) -> ft.Padding:
    if hasattr(ft, "Padding") and hasattr(ft.Padding, "all"):
        return ft.Padding.all(pad)
    return ft.padding.all(pad)

def padding_symmetric(horizontal: float = 0, vertical: float = 0) -> ft.Padding:
    if hasattr(ft, "Padding") and hasattr(ft.Padding, "symmetric"):
        return ft.Padding.symmetric(horizontal=horizontal, vertical=vertical)
    return ft.padding.symmetric(horizontal=horizontal, vertical=vertical)

def padding_only(left: float = 0, top: float = 0, right: float = 0, bottom: float = 0) -> ft.Padding:
    if hasattr(ft, "Padding") and hasattr(ft.Padding, "only"):
        return ft.Padding.only(left=left, top=top, right=right, bottom=bottom)
    return ft.padding.only(left=left, top=top, right=right, bottom=bottom)

def icon_nobre(icone_data, size=None, color=None) -> ft.Icon:
    kwargs = {}
    if size is not None:
        kwargs["size"] = size
    if color is not None:
        kwargs["color"] = color
    return ft.Icon(icone_data, **kwargs)

# Paleta Ativa Global
TEMA_ATIVO = "Dark Fantasy Dourado"
TEMA_PADRAO = TEMAS[TEMA_ATIVO]
BG_DARK = TEMA_PADRAO["bg_dark"]
BG_SURFACE = TEMA_PADRAO["bg_surface"]
BG_CARD = TEMA_PADRAO["bg_card"]
BG_CARD_LIGHT = TEMA_PADRAO["bg_card_light"]
BG_INPUT = TEMA_PADRAO["bg_input"]

GOLD_PRIMARY = TEMA_PADRAO["primary"]
GOLD_LIGHT = TEMA_PADRAO["light"]
GOLD_MUTED = "#9A8132"
GOLD_CONTAINER = TEMA_PADRAO["container"]

PURPLE_PRIMARY = TEMA_PADRAO["secondary"]
PURPLE_LIGHT = TEMA_PADRAO["secondary_light"]
PURPLE_DARK = "#4C1D95"
PURPLE_CONTAINER = "#261B40"

BORDER_GOLD = border_all(1, TEMA_PADRAO["border_color"])
BORDER_PURPLE = border_all(1, TEMA_PADRAO["secondary"])
BORDER_SUBTLE = border_all(1, TEMA_PADRAO["border_subtle"])

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#64748B"
SUCCESS_GREEN = "#10B981"
DANGER_RED = "#EF4444"
MANA_BLUE = "#38BDF8"
HP_RED = "#F43F5E"

BORDER_RADIUS = 14

def get_theme_colors(nome_tema: str = "Dark Fantasy Dourado") -> dict:
    return TEMAS.get(nome_tema, TEMAS["Dark Fantasy Dourado"])

def aplicar_tema(nome_tema: str):
    """Atualiza as variáveis globais de cor para recoloração instantânea."""
    global TEMA_ATIVO, BG_DARK, BG_SURFACE, BG_CARD, BG_CARD_LIGHT, BG_INPUT
    global GOLD_PRIMARY, GOLD_LIGHT, GOLD_CONTAINER, BORDER_GOLD
    global PURPLE_PRIMARY, PURPLE_LIGHT, PURPLE_CONTAINER, BORDER_PURPLE, BORDER_SUBTLE
    global TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED

    cores = get_theme_colors(nome_tema)
    TEMA_ATIVO = nome_tema
    BG_DARK = cores["bg_dark"]
    BG_SURFACE = cores["bg_surface"]
    BG_CARD = cores["bg_card"]
    BG_CARD_LIGHT = cores["bg_card_light"]
    BG_INPUT = cores["bg_input"]

    GOLD_PRIMARY = cores["primary"]
    GOLD_LIGHT = cores["light"]
    GOLD_CONTAINER = cores["container"]

    PURPLE_PRIMARY = cores["secondary"]
    PURPLE_LIGHT = cores["secondary_light"]
    PURPLE_CONTAINER = cores["container"]

    BORDER_GOLD = border_all(1, cores["border_color"])
    BORDER_PURPLE = border_all(1, cores["secondary"])
    BORDER_SUBTLE = border_all(1, cores["border_subtle"])

    TEXT_PRIMARY = cores.get("text_primary", "#F8FAFC")
    TEXT_SECONDARY = cores.get("text_secondary", "#94A3B8")
    TEXT_MUTED = cores.get("text_muted", "#64748B")

def botao_preenchido(
    texto: str,
    on_click=None,
    bgcolor: str = None,
    color: str = "#121214",
    icon=None
) -> ft.Control:
    """Botão preenchido ergonômico para telas mobile."""
    if bgcolor is None:
        bgcolor = GOLD_PRIMARY
        
    kwargs = {
        "on_click": on_click,
        "bgcolor": bgcolor,
        "color": color
    }
    if icon:
        kwargs["icon"] = icon
        
    if hasattr(ft, "FilledButton"):
        return ft.FilledButton(texto, height=44, **kwargs)
    elif hasattr(ft, "ElevatedButton"):
        return getattr(ft, "ElevatedButton")(texto, height=44, **kwargs)
    return ft.Container(
        content=ft.Text(texto, color=color, weight=ft.FontWeight.BOLD, size=14),
        bgcolor=bgcolor,
        on_click=on_click,
        padding=padding_symmetric(horizontal=18, vertical=12),
        border_radius=border_radius_all(10),
        alignment=ft.Alignment(0, 0)
    )

def get_dark_theme(nome_tema: str = "Dark Fantasy Dourado") -> ft.Theme:
    cores = get_theme_colors(nome_tema)
    try:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                surface=cores["bg_surface"],
                primary=cores["primary"],
                secondary=cores["secondary"],
                on_surface=cores.get("text_primary", TEXT_PRIMARY),
            )
        )
    except Exception:
        return ft.Theme()

# ==================== CÁLCULO E INFLUÊNCIA LUNAR ====================
def calcular_fase_lua(dt: datetime = None) -> tuple:
    """Calcula a fase lunar baseada no ciclo sinódico aproximado de 29.53 dias."""
    if dt is None:
        dt = datetime.now()

    # Referência de Lua Nova conhecida: 11 de Janeiro de 2024
    ref = datetime(2024, 1, 11, 11, 57)
    dias = (dt - ref).total_seconds() / 86400.0
    ciclo = 29.53058867
    fase_dias = dias % ciclo

    if fase_dias < 1.84:
        return ("Lua Nova", ft.Icons.CIRCLE_OUTLINED, "🌑", "Renovação e Silêncio Arcano")
    elif fase_dias < 7.38:
        return ("Lua Crescente", ft.Icons.BRIGHTNESS_3, "🌒", "Expansão e Semeadura de Metas")
    elif fase_dias < 9.23:
        return ("Quarto Crescente", ft.Icons.BRIGHTNESS_2, "🌓", "Ação Firme e Superação")
    elif fase_dias < 14.77:
        return ("Crescente Gibosa", ft.Icons.BRIGHTNESS_2, "🌔", "Lapidação e Foco nas Tarefas")
    elif fase_dias < 16.61:
        return ("Lua Cheia", ft.Icons.BRIGHTNESS_1, "🌕", "Plenitude, Poder e Colheita")
    elif fase_dias < 22.15:
        return ("Minguante Gibosa", ft.Icons.BRIGHTNESS_3, "🌖", "Gratidão e Compartilhamento")
    elif fase_dias < 23.99:
        return ("Quarto Minguante", ft.Icons.BRIGHTNESS_2, "🌗", "Desapego e Limpeza do Castelo")
    else:
        return ("Lua Minguante", ft.Icons.BRIGHTNESS_3, "🌘", "Descanso Sagrado e Introspecção")

def obter_influencia_lunar() -> dict:
    """Retorna os dados completos da fase lunar para os modais e alertas."""
    nome, icone, emoji, descricao = calcular_fase_lua()

    influencias = {
        "Lua Nova": {
            "influencia": "Início de Novos Ciclos e Planejamento Real",
            "orientacao": "Momento ideal para traçar novas quests e semear hábitos na Forja.",
            "bonus_magico": "+15% de Foco nas primeiras sessões de estudo."
        },
        "Lua Crescente": {
            "influencia": "Crescimento Rápido e Fortalecimento de Vínculos",
            "orientacao": "Avance nas quests principais e cuide do afeto com Sir Fagulha.",
            "bonus_magico": "+20% de EXP ao concluir hábitos diários."
        },
        "Quarto Crescente": {
            "influencia": "Decisões Corajosas e Quebra de Obstáculos",
            "orientacao": "Enfrente as tarefas mais desafiadoras com a proteção do Pequeno Joaquim.",
            "bonus_magico": "Resistência mental ampliada nas sessões de foco."
        },
        "Crescente Gibosa": {
            "influencia": "Paciência, Refinamento e Lapidação",
            "orientacao": "Revise o planejamento do cofre e finalize detalhes pendentes.",
            "bonus_magico": "Economia mágica: clareza nos cálculos da Coroa."
        },
        "Lua Cheia": {
            "influencia": "Poder Máximo, Vitalidade e Clarividência",
            "orientacao": "O castelo brilha sob a luz prateada. Celebre suas vitórias e conquistas!",
            "bonus_magico": "Bônus de +25 Ouros em recompensas de quests concluídas hoje."
        },
        "Minguante Gibosa": {
            "influencia": "Partilha de Sabedoria e Reconhecimento",
            "orientacao": "Agradeça pelas bênçãos do reino e desabafe na Sala do Trono.",
            "bonus_magico": "Restauração emocional dobrada na Audiência Real."
        },
        "Quarto Minguante": {
            "influencia": "Expurgo de Cansaço e Eliminação do Supérfluo",
            "orientacao": "Remova cobranças excessivas da sua mente e ajuste os gastos secundários.",
            "bonus_magico": "Alívio de dívidas emocionais e mente desanuviada."
        },
        "Lua Minguante": {
            "influencia": "Regeneração Vital e Sono Reparador",
            "orientacao": "Permita-se descansar. Até os maiores guerreiros embainham a espada.",
            "bonus_magico": "Recuperação total dos pontos de HP e Mana ao dormir."
        }
    }

    dados = influencias.get(nome, influencias["Lua Nova"])
    return {
        "nome": nome,
        "icone": icone,
        "emoji": emoji,
        "descricao": descricao,
        "influencia": dados["influencia"],
        "orientacao": dados["orientacao"],
        "bonus_magico": dados["bonus_magico"]
    }
