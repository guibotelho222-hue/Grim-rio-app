"""
=============================================================================
  ⚔️ GRIMÓRIO - EDIÇÃO DEFINITIVA CONSOLIDADA (FLET 1.0+) ⚔️
=============================================================================
Aplicativo Dark Fantasy RPG Retrô / Moderno para Windows Desktop e Mobile Android.
Consolidação completa:
  1. Configurações da Janela, Identidade Visual & 4 Temas Dark Fantasy.
  2. Dashboard Unificado da Saúde do Reino (% dinâmico, Frases RPG, XP & Títulos).
  3. Visão do Oráculo (+65 Profecias Diárias Offline) & Sistema de 24 Runas Místicas.
  4. A Forja de Hábitos (CRUD Completo, Animação de Durabilidade em Tempo Real).
  5. O Cofre Preditivo (Projeção de Fim de Mês, Alerta do Guardião, Barras Estilo Enquete).
  6. Poção de Foco (Pomodoro Alquímico, Bolsa de Ingredientes Raros) & Crônicas.
  7. Almanaque Celestial (Calendário Flutuante Interativo com Histórico Diário).
  8. Persistência de Dados em JSON ('grimorio_mobile_dados.json' & 'widget_data.json').
=============================================================================
"""

import calendar
import json
import os
import random
import sys
import threading
import time
from datetime import datetime
import flet as ft

# -----------------------------------------------------------------------------
# PROTEÇÃO PARA EXECUÇÃO SEM CONSOLE NO WINDOWS (PYINSTALLER --NOCONSOLE)
# -----------------------------------------------------------------------------
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

# -----------------------------------------------------------------------------
# GARANTIA DE COMPATIBILIDADE SINTÁTICA FLET 1.0+ & POLIFILLS
# -----------------------------------------------------------------------------
if hasattr(ft, "Margin"):
    ft.margin = ft.Margin
if hasattr(ft, "Padding"):
    ft.padding = ft.Padding
if hasattr(ft, "Border"):
    ft.border = ft.Border
if hasattr(ft, "Alignment"):
    ft.alignment = ft.Alignment
if not hasattr(ft, "ElevatedButton"):
    ft.ElevatedButton = getattr(ft, "FilledButton", getattr(ft, "Button", None))

if not hasattr(ft.Page, "open"):
    def _compat_page_open(self, ctrl):
        if hasattr(self, "show_dialog") and hasattr(ctrl, "open"):
            try:
                self.show_dialog(ctrl)
                return
            except Exception:
                pass
        if hasattr(self, "overlay"):
            if ctrl not in self.overlay:
                self.overlay.append(ctrl)
        ctrl.open = True
        self.update()
    ft.Page.open = _compat_page_open

if not hasattr(ft.Page, "close"):
    def _compat_page_close(self, ctrl=None):
        if hasattr(self, "pop_dialog"):
            try:
                self.pop_dialog()
                return
            except Exception:
                pass
        if ctrl is not None and hasattr(ctrl, "open"):
            ctrl.open = False
        self.update()
    ft.Page.close = _compat_page_close

# -----------------------------------------------------------------------------
# DIRETÓRIOS E CONSTANTES DE PERSISTÊNCIA
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(BASE_DIR, "grimorio_mobile_dados.json")
ARQUIVO_WIDGET = os.path.join(BASE_DIR, "widget_data.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# -----------------------------------------------------------------------------
# 1. SISTEMA DE TEMAS PERSONALIZÁVEIS (4 PALETAS DARK FANTASY)
# -----------------------------------------------------------------------------
PALETAS = {
    "Obsidian Clássico": {
        "fundo": "#0F0F14",
        "card": "#181424",
        "card_borda": "#40C8AA6E",
        "primaria": "#C8AA6E",       # Ouro Místico Envelhecido
        "secundaria": "#7B2CBF",     # Roxo Místico Profundo
        "acento": "#2EC4B6",         # Ciano Neon / Verde Espectral
        "alerta": "#E63946",         # Vermelho Rubi
        "sucesso": "#2EC4B6",        # Verde Espectral
        "texto": "#F0EBD8",          # Pergaminho Claro
        "texto_muted": "#9C978D"
    },
    "Chama do Dragão": {
        "fundo": "#121214",          # Cinza Chumbo Escuro
        "card": "#1F1E24",          # Chumbo Profundo
        "card_borda": "#45E63946",
        "primaria": "#FF6B35",       # Laranja Vulcânico
        "secundaria": "#E63946",     # Carmesim do Dragão
        "acento": "#FFAA00",         # Fogo Rúnico
        "alerta": "#FF0054",
        "sucesso": "#38B000",
        "texto": "#F7F2E7",
        "texto_muted": "#A89F91"
    },
    "Mata dos Elfos": {
        "fundo": "#08100C",          # Escuro Profundo Élfico
        "card": "#0E1D17",          # Musgo Escuro
        "card_borda": "#4010B981",
        "primaria": "#10B981",       # Verde Esmeralda Neon
        "secundaria": "#059669",     # Copa da Floresta
        "acento": "#34D399",         # Orvalho Élfico
        "alerta": "#F43F5E",
        "sucesso": "#10B981",
        "texto": "#ECFDF5",
        "texto_muted": "#84A999"
    },
    "Paladin Gold": {
        "fundo": "#0A0F1D",          # Azul-Marinho Noturno
        "card": "#131C31",          # Azul Real da Cidadela
        "card_borda": "#45F39C12",
        "primaria": "#F39C12",       # Ouro Reluzente do Paladino
        "secundaria": "#2980B9",     # Azul Safira
        "acento": "#FFD166",         # Brilho Solar
        "alerta": "#E74C3C",
        "sucesso": "#2ECC71",
        "texto": "#F4F6F9",
        "texto_muted": "#8FA0BE"
    }
}

# -----------------------------------------------------------------------------
# 2. TÍTULOS EVOLUTIVOS RPG DA HEROÍNA
# -----------------------------------------------------------------------------
TITULOS_HEROINA = [
    "Aprendiz de Alquimia",
    "Guardiana do Tesouro",
    "Iniciada das Sombras",
    "Alquimista do Foco",
    "Guardiã do Castelo",
    "Mestra de Quests",
    "Arquimaga do Reino",
    "Lenda Imortal do Reino"
]

# -----------------------------------------------------------------------------
# 3. +60 PROFECIAS DIÁRIAS DO ORÁCULO (OFFLINE)
# -----------------------------------------------------------------------------
PROFECIAS_EXPANDIDAS = [
    "As estrelas arcanas sussurram: a disciplina de hoje forja o império de amanhã.",
    "Nenhum dragão é derrotado de uma só vez, mas sim a cada golpe lapidado na forja.",
    "O ouro resguardado no cofre é a muralha invisível que defende o seu castelo.",
    "Uma poção de foco bem destilada dissipa até a mais densa névoa de incerteza.",
    "Aquele que registra suas missões no grimório jamais se perde nos labirintos do destino.",
    "Pequenos rituais diários invocam os maiores milagres do reino.",
    "A paciência da arquimaga constrói torres que tempestade alguma consegue derrubar.",
    "Não tema o peso da armadura; tema a fragilidade de quem desiste antes da batalha.",
    "O verdadeiro tesouro não se mede apenas em moedas, mas na paz de um reino bem governado.",
    "Cada hábito mantido aceso é uma tocha contra a escuridão da procrastinação.",
    "Mesmo a mais longa das jornadas começou com um único passo além do portão de ferro.",
    "A magia mais poderosa é o foco canalizado em uma única tarefa com determinação.",
    "Crie alicerces tão profundos quanto as raízes da Árvore-Mundo.",
    "A água que molda a pedra o faz pela constância incessante, não pela fúria de um instante.",
    "Quando o vento sopra contra, a águia real usa as correntes para planar ainda mais alto.",
    "O silêncio antes do golpe é onde se esconde a mira mais perfeita.",
    "Descanse quando necessário, pois até a lâmina encantada precisa retornar à bainha.",
    "Quem domina a si mesmo governa qualquer reino sem precisar levantar um cetro.",
    "A sabedoria ancestral dorme nos livros esquecidos; desperte-a na leitura de hoje.",
    "A riqueza guardada com honra liberta o espírito para as grandes conquistas da vida.",
    "Uma missão concluída hoje vale mais do que cem promessas feitas ao vento de amanhã.",
    "Proteja suas horas mais produtivas como se fossem relíquias guardadas na torre mais alta.",
    "A forja exige calor, marteladas e tempo; o seu caráter é lapidado da mesma forma.",
    "A serenidade da mente é a poção mais rara do laboratório alquímico.",
    "Não espere a maré da sorte virar; pegue os remos e navegue rumo à terra prometida.",
    "O reino floresce quando a soberana honra sua própria palavra dada a si mesma.",
    "A cada quest riscada do pergaminho, o monstro da dúvida encolhe nas sombras.",
    "A disciplina é o feitiço que transforma ideias voláteis em ouro puro tangível.",
    "Quem sabe dizer 'não' às distrações preserva mana suficiente para os milagres reais.",
    "A luz que guia tua espada vem de dentro; nenhuma escuridão externa pode apagá-la.",
    "O cofre bem administrado permite à heroína sonhar com expedições cada vez mais audazes.",
    "O cansaço passa, mas a obra forjada com carinho permanece pelas eras.",
    "Nas montanhas mais íngremes encontram-se as ervas de cura mais poderosas.",
    "Um bom planejamento estratégico é metade da vitória antes mesmo de soar o clarim.",
    "Não conte a todos sobre suas poções secretas; mostre o brilho quando estiverem prontas.",
    "A glória não está em nunca cair, mas em erguer o escudo após cada investida do destino.",
    "Mantenha os olhos na bússola e os pés firmes no chão de pedra da fortaleza.",
    "A verdadeira nobreza está em ser hoje mais sábia e justa do que ontem.",
    "O tempo é o mais precioso ingrediente da criação; use cada gota com reverência.",
    "Seja implacável contra o desânimo, mas gentil com os seus momentos de recarga.",
    "A mente treinada é uma lâmina rúnica capaz de cortar qualquer emaranhado de problemas.",
    "A fortaleza mais inexpugnável é aquela cujos portões são vigiados pela consciência.",
    "Cada gota de suor derramada no treino economiza um rio de lágrimas no campo de prova.",
    "O sábio guarda provisões no verão para que o inverno seja uma estação de celebração.",
    "A constância dos dias simples é o solo onde brotam as lendas imortais.",
    "Concentre sua mana no presente; o passado é ruína e o futuro é névoa a desbravar.",
    "Celebre tua coragem de tentar novamente, pois recomeçar é o rito dos campeões.",
    "Um coração destemido e um grimório organizado são suficientes para mudar qualquer mundo.",
    "Colha os frutos do trabalho com gratidão e compartilhe prosperidade com teus aliados.",
    "A lua cheia clareia as rotas; aproveite o frescor da noite para meditar sobre tuas vitórias.",
    "A verdadeira mestria não tem pressa; ela se aprofunda até atingir as fontes eternas.",
    "Quando a névoa cobrir o vale, confie na bússola do teu propósito maior.",
    "Tu és a arquiteta do teu próprio destino; desenhe cada arco e ogiva com grandeza.",
    "Nenhuma sombra permanece para sempre diante da chama que queima sem hesitar.",
    "As runas se alinham para aqueles que mantêm a fé e a firmeza na própria jornada.",
    "A coroa mais pesada torna-se leve sobre a cabeça de quem governa com serenidade.",
    "Guarde suas palavras de poder para os momentos em que o silêncio não bastar.",
    "A flecha só avança para a frente após ser puxada para trás com força e concentração.",
    "Cultive teu santuário interior; é de lá que emana toda a magia do reino.",
    "O poço da sabedoria é profundo, mas cada balde retirado sacia a sede da alma.",
    "Quem respeita as próprias pausas retorna ao campo com o dobro do poder de ataque.",
    "Um reino organizado por dentro não teme o caos que ruge do lado de fora das muralhas.",
    "O mapa mais perfeito não substitui a coragem de cruzar a ponte levadiça.",
    "A cada amanhecer, o universo renova sua aliança com quem busca a excelência.",
    "Tua história está sendo talhada em pedra rúnica; faça de cada capítulo um épico memorável."
]

# -----------------------------------------------------------------------------
# 4. 24 RUNAS MÍSTICAS DO ELDER FUTHARK (COM CONSELHOS ARCANOS)
# -----------------------------------------------------------------------------
RUNAS_MISTICAS = [
    {
        "simbolo": "ᚠ",
        "nome": "Fehu",
        "arquetipo": "Runa da Abundância & Fortuna",
        "conselho": "O ouro circula como o sangue vital do reino. Invista hoje naquilo que nutre sua alma e fortaleça seus alicerces financeiros."
    },
    {
        "simbolo": "ᚢ",
        "nome": "Uruz",
        "arquetipo": "Runa da Força Primitiva & Vitalidade",
        "conselho": "A força indomável do touro selvagem reside em ti. Enfrente o maior obstáculo do dia com vigor inabalável e postura resoluta."
    },
    {
        "simbolo": "ᚦ",
        "nome": "Thurisaz",
        "arquetipo": "Runa da Proteção & Espinho Defensivo",
        "conselho": "Erigir limites sagrados é sabedoria, não fraqueza. Proteja sua energia de vampiros de tempo e preserve sua paz interior."
    },
    {
        "simbolo": "ᚨ",
        "nome": "Ansuz",
        "arquetipo": "Runa da Sabedoria Ancestral & Inspiração",
        "conselho": "As palavras têm poder de encantamento supremo. Escute a voz da intuição e expresse suas ideias com clareza e verdade."
    },
    {
        "simbolo": "ᚱ",
        "nome": "Raido",
        "arquetipo": "Runa da Jornada & Movimento Estratégico",
        "conselho": "A viagem é o próprio destino. Cada passo bem planejado na forja vence o mais traiçoeiro dos labirintos."
    },
    {
        "simbolo": "ᚲ",
        "nome": "Kenaz",
        "arquetipo": "Runa da Chama Criativa & Clareza",
        "conselho": "A tocha que arde na escuridão dissipa qualquer névoa de dúvida. Ilumine seus projetos com paixão e foco cirúrgico."
    },
    {
        "simbolo": "ᚷ",
        "nome": "Gebo",
        "arquetipo": "Runa da Generosidade & Trocas Justas",
        "conselho": "Um presente convoca outro presente. Mantenha o equilíbrio entre dar e receber para que a harmonia reine no castelo."
    },
    {
        "simbolo": "ᚹ",
        "nome": "Wunjo",
        "arquetipo": "Runa da Alegria Triunfante & Harmonia",
        "conselho": "Celebre os pequenos triunfos do dia. A alegria genuína é o escudo mais impenetrável contra a armadura pesada do estresse."
    },
    {
        "simbolo": "ᚺ",
        "nome": "Hagalaz",
        "arquetipo": "Runa da Transformação & Tempestade Libertadora",
        "conselho": "A chuva de granizo desfaz o velho para semear o novo. Abrace as mudanças inesperadas com serenidade e coragem."
    },
    {
        "simbolo": "ᚾ",
        "nome": "Nauthiz",
        "arquetipo": "Runa da Resiliência & Paciência na Escassez",
        "conselho": "A necessidade lapida o diamante. Transforme as limitações presentes em molas propulsoras de profunda criatividade."
    },
    {
        "simbolo": "ᛁ",
        "nome": "Isa",
        "arquetipo": "Runa da Quietude & Gelo Contemplativo",
        "conselho": "O lago congelado ensina o valor sagrado da pausa. Quando as águas agitarem, recue um momento para refletir antes de agir."
    },
    {
        "simbolo": "ᛃ",
        "nome": "Jera",
        "arquetipo": "Runa da Colheita Justa & Ciclos Férteis",
        "conselho": "Quem plantou com disciplina no inverno colherá banquetes no outono. Confie no ritmo natural do tempo e do esforço."
    },
    {
        "simbolo": "ᛇ",
        "nome": "Eihwaz",
        "arquetipo": "Runa do Teixo Sagrado & Longevidade",
        "conselho": "Como a árvore de teixo milenar, curve-se com a tempestade sem jamais quebrar. Tua determinação é inquebrantável."
    },
    {
        "simbolo": "ᛈ",
        "nome": "Perthro",
        "arquetipo": "Runa do Mistério & Destino Oculto",
        "conselho": "O copo de dados cósmicos foi lançado. Mantenha-se receptiva às sincronicidades e surpresas agradáveis do reino."
    },
    {
        "simbolo": "ᛉ",
        "nome": "Algiz",
        "arquetipo": "Runa da Guardiã & Proteção Espiritual",
        "conselho": "As hastes do cervo conectam a terra aos céus. Tua intuição é um escudo rúnico ativo contra qualquer má intenção."
    },
    {
        "simbolo": "ᛊ",
        "nome": "Sowilo",
        "arquetipo": "Runa da Vitória & Luz Solar Triunfante",
        "conselho": "A luz solar dissipa as sombras mais antigas. A vitória está ao alcance; tome posse do teu brilho sem receios."
    },
    {
        "simbolo": "ᛏ",
        "nome": "Tiwaz",
        "arquetipo": "Runa da Bravura & Lança da Justiça",
        "conselho": "A guerreira espiritual luta pela integridade. Mantenha teus princípios intactos mesmo diante dos maiores atalhos."
    },
    {
        "simbolo": "ᛒ",
        "nome": "Berkana",
        "arquetipo": "Runa do Renascimento & Primavera Fértil",
        "conselho": "Novos começos florescem em solo nutrido pelo autocuidado. É tempo de cultivar novos hábitos e regenerar a energia."
    },
    {
        "simbolo": "ᛖ",
        "nome": "Ehwaz",
        "arquetipo": "Runa da Lealdade & Movimento Ágil",
        "conselho": "O cavalo e a amazona movem-se como uma só mente. Valorize suas alianças fiéis e avance em harmonia com seu propósito."
    },
    {
        "simbolo": "ᛗ",
        "nome": "Mannaz",
        "arquetipo": "Runa do Autoconhecimento & Mente Iluminada",
        "conselho": "Conhece-te a ti mesma antes de governar qualquer império. Tua mente é a torre mais alta de toda a fortaleza."
    },
    {
        "simbolo": "ᛚ",
        "nome": "Laguz",
        "arquetipo": "Runa das Águas Profundas & Intuição",
        "conselho": "Deixe o fluxo da sabedoria interior te guiar através da névoa. Nem todas as decisões precisam ser tomadas apenas pela razão."
    },
    {
        "simbolo": "ᛝ",
        "nome": "Ingwaz",
        "arquetipo": "Runa da Conclusão Fértil & Descanso do Guerreiro",
        "conselho": "A semente descansa no escuro fértil antes de desabrochar. Conclua etapas pendentes e celebre o encerramento do ciclo."
    },
    {
        "simbolo": "ᛞ",
        "nome": "Dagaz",
        "arquetipo": "Runa do Despertar & Aurora Radiante",
        "conselho": "A noite mais longa sempre cede lugar à alvorada. Um novo horizonte de possibilidades mágicas se abre hoje para você."
    },
    {
        "simbolo": "ᛟ",
        "nome": "Othala",
        "arquetipo": "Runa do Legado & Herança Sagrada",
        "conselho": "Honre as lições do passado e construa uma fortaleza duradoura para o futuro. Teu legado ecoará através das eras."
    }
]

# Ícones temáticos para a Forja de Hábitos
ICONES_FORJA = [
    "⚔️ Espada de Batalha",
    "🛡️ Escudo de Mana",
    "🧪 Elixir da Mente",
    "📖 Tomo Sagrado",
    "🔥 Fogueira Sagrada",
    "🧘 Meditação Astral",
    "🔨 Martelo de Aço",
    "🏹 Mira Certeira",
    "🔮 Orbe de Vidência",
    "⚡ Raio Arcano",
    "🕯️ Vigília Noturna",
    "🗝️ Chave do Tesouro",
    "🌿 Erva Curativa",
    "💎 Joia da Alma"
]

INGREDIENTES_RAROS_POOL = [
    "Flor de Lótus Lunar",
    "Pó de Estrela Cadente",
    "Cristal de Éter Rúnico",
    "Lágrima de Fênix Dourada",
    "Orvalho da Floresta Espectral",
    "Fragmento de Meteorito Arcano"
]

MESES_PTBR = [
    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]


# -----------------------------------------------------------------------------
# FUNÇÕES DE LOCALIZAÇÃO DE ASSETS
# -----------------------------------------------------------------------------
def localizar_logo() -> str:
    """Localiza a imagem do logo da usuária em múltiplas fontes ('assets/logo.png', 'logo.png.jpeg', etc.)."""
    candidatos = [
        os.path.join(ASSETS_DIR, "logo.png"),
        os.path.join(ASSETS_DIR, "logo.png.jpeg"),
        os.path.join(BASE_DIR, "logo.png.jpeg"),
        os.path.join(BASE_DIR, "logo.png"),
        os.path.join(os.path.dirname(BASE_DIR), "logo.png.jpeg"),
        os.path.join(os.path.dirname(BASE_DIR), "logo.png"),
        "logo.png",
        "logo.png.jpeg",
        "assets/logo.png"
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    return ""


def localizar_ico() -> str:
    """Localiza o arquivo logo.ico para a janela Desktop do Windows."""
    candidatos = [
        os.path.join(BASE_DIR, "logo.ico"),
        os.path.join(ASSETS_DIR, "logo.ico"),
        os.path.join(BASE_DIR, "logo.ico (1).ico"),
        os.path.join(os.path.dirname(BASE_DIR), "logo.ico"),
        "logo.ico",
        "assets/logo.ico"
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    return ""


# -----------------------------------------------------------------------------
# 8. GERENCIADOR DE ESTADO E PERSISTÊNCIA JSON
# -----------------------------------------------------------------------------
class DadosManager:
    """Gerenciador centralizado de persistência em JSON e sincronização de widgets."""

    def __init__(self):
        self.dados = self._carregar_dados()

    def _dados_padrao(self) -> dict:
        return {
            "config": {
                "nome_personagem": "Lady Morgana",
                "titulo_personagem": "Aprendiz de Alquimia",
                "paleta": "Obsidian Clássico",
                "haptic": True,
                "sons": True,
                "titulos_abas": {
                    "quests": "📜 Quests",
                    "cofre": "💰 Cofre",
                    "forja": "⚒️ A Forja",
                    "cronicas": "📖 Crônicas",
                    "foco": "🧪 Poção de Foco"
                }
            },
            "gamificacao": {
                "nivel": 1,
                "xp": 35,
                "xp_proximo": 100,
                "pocoes_tomadas": 0,
                "ingredientes_raros": {
                    "Flor de Lótus Lunar": 1,
                    "Pó de Estrela Cadente": 0,
                    "Cristal de Éter Rúnico": 0,
                    "Lágrima de Fênix Dourada": 0,
                    "Orvalho da Floresta Espectral": 0,
                    "Fragmento de Meteorito Arcano": 0
                }
            },
            "quests": [
                {
                    "id": "q1",
                    "titulo": "Revisar os Tratados do Conselho Real",
                    "categoria": "Quest Principal",
                    "prioridade": "🔴 Crítico",
                    "data": datetime.now().strftime("%Y-%m-%d"),
                    "hora": "14:00",
                    "concluida": False,
                    "detalhes": "Assinar decretos e despachar mensageiros."
                },
                {
                    "id": "q2",
                    "titulo": "Coleta de Ervas e Flores Lunares",
                    "categoria": "Rituais",
                    "prioridade": "🟡 Importante",
                    "data": datetime.now().strftime("%Y-%m-%d"),
                    "hora": "17:30",
                    "concluida": False,
                    "detalhes": "Preparar infusão para o laboratório alquímico."
                },
                {
                    "id": "q3",
                    "titulo": "Organizar os Frascos da Dispensa",
                    "categoria": "Missão Secundária",
                    "prioridade": "🟢 Normal",
                    "data": datetime.now().strftime("%Y-%m-%d"),
                    "hora": "19:00",
                    "concluida": True,
                    "detalhes": "Limpar estantes do castelo."
                }
            ],
            "cofre": {
                "categorias": [
                    {"id": "c1", "nome": "Banquete & Alimentos", "limite_po": 1200.0, "gasto_po": 650.0},
                    {"id": "c2", "nome": "Manutenção da Fortaleza", "limite_po": 800.0, "gasto_po": 680.0},
                    {"id": "c3", "nome": "Vestimentas Nobres", "limite_po": 500.0, "gasto_po": 150.0},
                    {"id": "c4", "nome": "Poções & Cuidados", "limite_po": 400.0, "gasto_po": 120.0}
                ],
                "gastos": [
                    {"id": "g1", "categoria": "Manutenção da Fortaleza", "valor_po": 200.0, "desc": "Reparo nas muralhas", "data": datetime.now().strftime("%Y-%m-%d")},
                    {"id": "g2", "categoria": "Banquete & Alimentos", "valor_po": 150.0, "desc": "Especiarias do oriente", "data": datetime.now().strftime("%Y-%m-%d")}
                ]
            },
            "forja": {
                "habitos": [
                    {"id": "h1", "nome": "Meditação Arcana (20 min)", "icone": "🧘", "dias": 7, "alvo": 21, "ultimo_dia": ""},
                    {"id": "h2", "nome": "Treino com a Espada Rúnica", "icone": "⚔️", "dias": 14, "alvo": 30, "ultimo_dia": ""},
                    {"id": "h3", "nome": "Leitura do Livro das Sombras", "icone": "📖", "dias": 3, "alvo": 21, "ultimo_dia": ""}
                ],
                "historico_dias": {
                    datetime.now().strftime("%Y-%m-%d"): ["Meditação Arcana (20 min)"]
                }
            },
            "cronicas": [
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] ⭐ Início da jornada no Grimório & Caixa do Reino."
            ]
        }

    def _carregar_dados(self) -> dict:
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    # Migração defensiva de campos novos
                    if "ingredientes_raros" not in dados.get("gamificacao", {}):
                        dados.setdefault("gamificacao", {})["ingredientes_raros"] = {
                            "Flor de Lótus Lunar": 1,
                            "Pó de Estrela Cadente": 0,
                            "Cristal de Éter Rúnico": 0,
                            "Lágrima de Fênix Dourada": 0,
                            "Orvalho da Floresta Espectral": 0,
                            "Fragmento de Meteorito Arcano": 0
                        }
                    if "historico_dias" not in dados.get("forja", {}):
                        dados.setdefault("forja", {})["historico_dias"] = {}
                    return dados
            except Exception:
                pass
        dados = self._dados_padrao()
        self.salvar_dados(dados)
        return dados

    def salvar_dados(self, dados: dict = None):
        if dados is not None:
            self.dados = dados
        try:
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
            self.atualizar_widget_data()
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def atualizar_widget_data(self):
        """Gera um resumo compacto em widget_data.json para integração com o Android App Widget."""
        try:
            hoje = datetime.now().strftime("%Y-%m-%d")
            quests_hoje = [q for q in self.dados.get("quests", []) if q.get("data") == hoje and not q.get("concluida")]
            proximas_3 = [
                {"titulo": q.get("titulo"), "hora": q.get("hora"), "prioridade": q.get("prioridade")}
                for q in quests_hoje[:3]
            ]

            cats = self.dados.get("cofre", {}).get("categorias", [])
            total_limite = sum(c.get("limite_po", 0.0) for c in cats)
            total_gasto = sum(c.get("gasto_po", 0.0) for c in cats)
            pct_gasto = (total_gasto / total_limite * 100.0) if total_limite > 0 else 0.0

            habitos = self.dados.get("forja", {}).get("habitos", [])
            maior_streak = max([h.get("dias", 0) for h in habitos], default=0)

            widget_payload = {
                "atualizado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "titulos_abas": self.dados.get("config", {}).get("titulos_abas", {}),
                "personagem": {
                    "nome": self.dados.get("config", {}).get("nome_personagem"),
                    "titulo": self.dados.get("config", {}).get("titulo_personagem"),
                    "nivel": self.dados.get("gamificacao", {}).get("nivel", 1),
                    "xp": self.dados.get("gamificacao", {}).get("xp", 0)
                },
                "quests_proximas": proximas_3,
                "cofre_saude": {
                    "total_limite": round(total_limite, 2),
                    "total_gasto": round(total_gasto, 2),
                    "porcentagem_consumida": round(pct_gasto, 1),
                    "alerta_critico": pct_gasto >= 80.0
                },
                "fogo_streak": maior_streak
            }

            with open(ARQUIVO_WIDGET, "w", encoding="utf-8") as f:
                json.dump(widget_payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao gerar widget_data.json: {e}")


# -----------------------------------------------------------------------------
# APLICAÇÃO PRINCIPAL FLET (MAIN)
# -----------------------------------------------------------------------------
def main(page: ft.Page):
    # =========================================================================
    # 1. IDENTIDADE VISUAL & CONFIGURAÇÕES DA JANELA (WINDOWS & MOBILE)
    # =========================================================================
    page.title = "Grimório"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    # Configuração de Janela Desktop (simulando proporção mobile moderna 450x800)
    try:
        page.window.title = "Grimório"
        page.window.width = 450
        page.window.height = 800
        page.window.min_width = 380
        page.window.min_height = 650
        page.window.resizable = True

        caminho_ico = localizar_ico()
        if caminho_ico and os.path.exists(caminho_ico):
            page.window.icon = caminho_ico
    except Exception:
        pass

    # Inicialização dos dados
    db = DadosManager()
    dados = db.dados

    # Estado da paleta ativa
    nome_paleta = dados.get("config", {}).get("paleta", "Obsidian Clássico")
    paleta = PALETAS.get(nome_paleta, PALETAS["Obsidian Clássico"])
    page.bgcolor = paleta["fundo"]

    # Estado da Poção de Foco
    pomodoro_segundos = 25 * 60
    pomodoro_total = 25 * 60
    pomodoro_ativo = False
    pomodoro_thread = None

    # Estado de navegação do Almanaque Celestial
    agora_inicial = datetime.now()
    cal_ano = [agora_inicial.year]
    cal_mes = [agora_inicial.month]
    cal_dia_sel = [agora_inicial.day]

    # Sorteio diário da profecia (semente YYYY-MM-DD para consistência offline)
    hoje_str = datetime.now().strftime("%Y-%m-%d")
    random.seed(hoje_str)
    frase_oraculo = [random.choice(PROFECIAS_EXPANDIDAS)]
    random.seed()

    def vibrar():
        """Feedback sonoro e tátil de micro-interação."""
        try:
            if dados.get("config", {}).get("haptic", True):
                try:
                    import winsound
                    winsound.MessageBeep(winsound.MB_OK)
                except Exception:
                    pass
        except Exception:
            pass

    def exibir_notificacao(texto: str, cor_fundo=None):
        """Exibe SnackBar com feedback visual imediato."""
        page.open(
            ft.SnackBar(
                content=ft.Text(texto, color=paleta["texto"], weight=ft.FontWeight.W_500),
                bgcolor=cor_fundo if cor_fundo else paleta["secundaria"]
            )
        )

    def ganhar_xp(qtd: int, motivo: str):
        """Acumula XP, avalia subida de nível e atualiza títulos RPG da heroína."""
        g = dados["gamificacao"]
        g["xp"] += qtd
        prox = g["xp_proximo"]
        nivel_anterior = g["nivel"]

        while g["xp"] >= prox:
            g["xp"] -= prox
            g["nivel"] += 1
            g["xp_proximo"] = int(prox * 1.5)
            prox = g["xp_proximo"]

        agora = datetime.now().strftime("%Y-%m-%d %H:%M")
        dados["cronicas"].insert(0, f"[{agora}] ⭐ +{qtd} XP: {motivo}")

        if g["nivel"] > nivel_anterior:
            idx = min(g["nivel"] - 1, len(TITULOS_HEROINA) - 1)
            novo_tit = TITULOS_HEROINA[idx]
            dados["config"]["titulo_personagem"] = novo_tit
            dados["cronicas"].insert(0, f"[{agora}] ✨ SUBIU DE NÍVEL! {dados['config']['nome_personagem']} agora é Nível {g['nivel']} ({novo_tit})!")
            exibir_notificacao(f"✨ SUBIU DE NÍVEL! Agora és {novo_tit}!", paleta["secundaria"])

        db.salvar_dados()

    # =========================================================================
    # COMPONENTE CARD GLASSMORPHIC
    # =========================================================================
    def criar_card_glass(conteudo, padding=14, margin=None, border_color=None):
        return ft.Container(
            content=conteudo,
            bgcolor=paleta["card"],
            border_radius=16,
            padding=padding,
            margin=margin if margin else ft.Margin.only(left=14, right=14, bottom=10),
            border=ft.Border.all(1, border_color if border_color else paleta["card_borda"]),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color="#20000000",
                offset=ft.Offset(0, 4)
            )
        )

    # =========================================================================
    # 2. DASHBOARD DA SAÚDE GERAL DO REINO & 3. ORÁCULO E RUNAS
    # =========================================================================
    def construir_oraculo():
        hoje = datetime.now().strftime("%Y-%m-%d")

        # 1. Quests do dia
        quests_hoje = [q for q in dados["quests"] if q.get("data") == hoje]
        if not quests_hoje:
            quests_hoje = dados["quests"]
        total_q = len(quests_hoje)
        conc_q = sum(1 for q in quests_hoje if q.get("concluida"))
        pct_q = (conc_q / total_q) if total_q > 0 else 1.0
        saude_quests = pct_q * 100.0

        # 2. Saúde do Cofre (% de sobra orçamentária)
        cats = dados["cofre"]["categorias"]
        limite_tot = sum(c["limite_po"] for c in cats)
        gasto_tot = sum(c["gasto_po"] for c in cats)
        if limite_tot > 0:
            pct_gasto = (gasto_tot / limite_tot) * 100.0
            saude_cofre = max(0.0, min(100.0, 100.0 - pct_gasto))
        else:
            saude_cofre = 100.0

        # 3. Hábitos da Forja (Hábitos concluídos hoje)
        habitos = dados["forja"]["habitos"]
        maior_streak = max([h.get("dias", 0) for h in habitos], default=0)
        total_hab = len(habitos)
        hab_feitos = sum(1 for h in habitos if h.get("ultimo_dia") == hoje)
        saude_forja = (hab_feitos / total_hab * 100.0) if total_hab > 0 else 100.0

        # Fórmula Unificada: (Saúde do Cofre % * 0.4) + (Hábitos % * 0.4) + (Quests % * 0.2)
        saude_geral = round((saude_cofre * 0.4) + (saude_forja * 0.4) + (saude_quests * 0.2), 1)
        saude_geral = max(0.0, min(100.0, saude_geral))

        # Status Dinâmico por Frases de RPG
        if saude_geral >= 90:
            frase_status = "🌟 O Reino vive uma Era de Ouro!"
            cor_status = paleta["sucesso"]
        elif saude_geral >= 70:
            frase_status = "🛡️ A Fortaleza permanece firme e próspera."
            cor_status = paleta["primaria"]
        elif saude_geral >= 50:
            frase_status = "🌫️ Névoas de incerteza rondam as muralhas..."
            cor_status = "#F39C12"
        else:
            frase_status = "⚠️ Alerta Geral! Invasores e sombras ameaçam o Tesouro e a Forja!"
            cor_status = paleta["alerta"]

        def nova_profecia(e):
            vibrar()
            frase_oraculo[0] = random.choice(PROFECIAS_EXPANDIDAS)
            atualizar_interface()

        def tirar_runa_diaria(e):
            vibrar()
            runa = random.choice(RUNAS_MISTICAS)

            dlg_runa = None

            def fechar_runa(ev=None):
                page.close(dlg_runa)

            dlg_runa = ft.AlertDialog(
                title=ft.Row([
                    ft.Text(runa["simbolo"], size=28, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ft.Column([
                        ft.Text(f"Runa {runa['nome']}", size=15, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                        ft.Text(runa["arquetipo"], size=11, color=paleta["acento"])
                    ], spacing=1)
                ], spacing=12),
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f'"{runa["conselho"]}"', size=13, italic=True, color=paleta["texto"]),
                        ft.Divider(color=paleta["card_borda"]),
                        ft.Text("Presságio extraído do oráculo para orientar as suas decisões de hoje.", size=10, color=paleta["texto_muted"])
                    ], tight=True, spacing=8),
                    width=320
                ),
                actions=[
                    ft.FilledButton("Agradecer aos Deuses Arcanos", bgcolor=paleta["primaria"], color="#111116", on_click=fechar_runa)
                ],
                bgcolor=paleta["card"]
            )
            page.open(dlg_runa)

        return criar_card_glass(
            ft.Column([
                # Cabeçalho da Visão do Oráculo & Tiragem de Runas
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.AUTO_AWESOME, color=paleta["primaria"], size=18),
                        ft.Text("Visão do Oráculo", size=13, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ]),
                    ft.Row([
                        ft.TextButton(
                            "ᚱ Tirar Runa",
                            style=ft.ButtonStyle(color=paleta["acento"]),
                            on_click=tirar_runa_diaria
                        ),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH_ROUNDED,
                            icon_color=paleta["texto_muted"],
                            icon_size=18,
                            tooltip="Consultar nova profecia",
                            on_click=nova_profecia
                        )
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Profecia do Dia
                ft.Text(
                    f'"{frase_oraculo[0]}"',
                    size=12,
                    italic=True,
                    color=paleta["texto"],
                    max_lines=3,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                ft.Divider(color=paleta["card_borda"], height=10),

                # Medidor da Saúde Geral do Reino
                ft.Row([
                    ft.Column([
                        ft.Row([
                            ft.Text("Saúde Geral do Reino:", size=11, color=paleta["texto_muted"]),
                            ft.Text(f"{saude_geral:.1f}%", size=13, weight=ft.FontWeight.BOLD, color=cor_status)
                        ], spacing=6),
                        ft.Text(frase_status, size=11, weight=ft.FontWeight.W_500, color=cor_status)
                    ], spacing=2, expand=True),
                    ft.Container(
                        content=ft.ProgressRing(value=saude_geral / 100.0, stroke_width=4, color=cor_status, bgcolor="#201830", width=36, height=36),
                        alignment=ft.Alignment.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Métricas Componentes
                ft.Row([
                    ft.Column([
                        ft.Text("Quests Diárias", size=10, color=paleta["texto_muted"]),
                        ft.Text(f"{conc_q}/{total_q}", size=12, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                        ft.ProgressBar(value=pct_q, color=paleta["sucesso"], bgcolor="#252033", width=80, height=4)
                    ], spacing=2),
                    ft.Column([
                        ft.Text("Cofre Saudável", size=10, color=paleta["texto_muted"]),
                        ft.Text(f"{saude_cofre:.0f}%", size=12, weight=ft.FontWeight.BOLD, color=paleta["sucesso"] if saude_cofre >= 30 else paleta["alerta"]),
                        ft.ProgressBar(value=saude_cofre / 100.0, color=paleta["sucesso"] if saude_cofre >= 30 else paleta["alerta"], bgcolor="#252033", width=80, height=4)
                    ], spacing=2),
                    ft.Column([
                        ft.Text("Forja Ativa", size=10, color=paleta["texto_muted"]),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color="#FF6D00", size=16),
                            ft.Text(f"{maior_streak}d ({saude_forja:.0f}%)", size=11, weight=ft.FontWeight.BOLD, color="#FF6D00")
                        ], spacing=2),
                        ft.ProgressBar(value=saude_forja / 100.0, color="#FF6D00", bgcolor="#252033", width=80, height=4)
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ], spacing=6)
        )

    # =========================================================================
    # MÓDULO 1: QUESTS (COM SWIPE/DISMISSIBLE E FILTROS)
    # =========================================================================
    filtro_prioridade = ["Todas"]

    def construir_view_quests():
        hoje = datetime.now().strftime("%Y-%m-%d")

        def alternar_conclusao(q):
            vibrar()
            q["concluida"] = not q.get("concluida", False)
            if q["concluida"]:
                ganhar_xp(10, f"Conclusão da Quest '{q['titulo']}'")
            db.salvar_dados()
            atualizar_interface()

        def excluir_quest(q):
            vibrar()
            dados["quests"] = [item for item in dados["quests"] if item["id"] != q["id"]]
            db.salvar_dados()
            atualizar_interface()

        def set_filtro(prio):
            vibrar()
            filtro_prioridade[0] = prio
            atualizar_interface()

        botoes_filtro = ft.Row([
            ft.TextButton("Todas", on_click=lambda e: set_filtro("Todas")),
            ft.TextButton("🟢 Normal", on_click=lambda e: set_filtro("🟢 Normal")),
            ft.TextButton("🟡 Importante", on_click=lambda e: set_filtro("🟡 Importante")),
            ft.TextButton("🔴 Crítico", on_click=lambda e: set_filtro("🔴 Crítico")),
        ], scroll=ft.ScrollMode.AUTO)

        lista_cards = []
        for q in dados["quests"]:
            if filtro_prioridade[0] != "Todas" and q.get("prioridade") != filtro_prioridade[0]:
                continue

            concluida = q.get("concluida", False)
            prio = q.get("prioridade", "🟢 Normal")
            cor_prio = paleta["alerta"] if "Crítico" in prio else (paleta["primaria"] if "Importante" in prio else paleta["sucesso"])

            conteudo_item = ft.Container(
                content=ft.Row([
                    ft.Checkbox(
                        value=concluida,
                        fill_color={ft.ControlState.SELECTED: paleta["sucesso"], ft.ControlState.DEFAULT: paleta["card_borda"]},
                        on_change=lambda e, quest=q: alternar_conclusao(quest)
                    ),
                    ft.Column([
                        ft.Text(
                            q["titulo"],
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=paleta["texto_muted"] if concluida else paleta["texto"],
                            style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH) if concluida else None
                        ),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(prio, size=10, color=cor_prio, weight=ft.FontWeight.BOLD),
                                bgcolor="#20000000",
                                border=ft.Border.all(1, cor_prio),
                                border_radius=6,
                                padding=ft.Padding.symmetric(horizontal=6, vertical=2)
                            ),
                            ft.Text(f"⏰ {q.get('hora', '')} • {q.get('categoria', '')}", size=11, color=paleta["texto_muted"])
                        ], spacing=6)
                    ], expand=True, spacing=3),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                        icon_color=paleta["alerta"],
                        icon_size=18,
                        on_click=lambda e, quest=q: excluir_quest(quest)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=paleta["card"],
                padding=10,
                border_radius=12,
                border=ft.Border.all(1, paleta["card_borda"])
            )

            dismissible = ft.Dismissible(
                content=conteudo_item,
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                background=ft.Container(
                    bgcolor=paleta["sucesso"],
                    alignment=ft.Alignment.CENTER_LEFT,
                    padding=ft.Padding.only(left=20),
                    content=ft.Icon(ft.Icons.CHECK_ROUNDED, color="#FFFFFF")
                ),
                secondary_background=ft.Container(
                    bgcolor=paleta["alerta"],
                    alignment=ft.Alignment.CENTER_RIGHT,
                    padding=ft.Padding.only(right=20),
                    content=ft.Icon(ft.Icons.DELETE_ROUNDED, color="#FFFFFF")
                ),
                on_dismiss=lambda e, quest=q: alternar_conclusao(quest) if e.direction == ft.DismissDirection.START_TO_END else excluir_quest(quest)
            )
            lista_cards.append(dismissible)

        def abrir_modal_nova_quest(e):
            vibrar()
            tit_input = ft.TextField(label="Título da Quest", bgcolor=paleta["card"], color=paleta["texto"])
            hora_input = ft.TextField(label="Horário (HH:MM)", value=datetime.now().strftime("%H:%M"), bgcolor=paleta["card"], color=paleta["texto"])
            prio_drop = ft.Dropdown(
                label="Prioridade",
                value="🟢 Normal",
                options=[ft.dropdown.Option("🟢 Normal"), ft.dropdown.Option("🟡 Importante"), ft.dropdown.Option("🔴 Crítico")],
                bgcolor=paleta["card"]
            )
            cat_drop = ft.Dropdown(
                label="Categoria",
                value="Quest Principal",
                options=[ft.dropdown.Option("Quest Principal"), ft.dropdown.Option("Missão Secundária"), ft.dropdown.Option("Rituais"), ft.dropdown.Option("Estudo de Magia")],
                bgcolor=paleta["card"]
            )

            dialogo = None

            def fechar_quest(ev=None):
                page.close(dialogo)

            def salvar(ev):
                if tit_input.value:
                    dados["quests"].append({
                        "id": f"q_{int(time.time()*1000)}",
                        "titulo": tit_input.value.strip(),
                        "hora": hora_input.value.strip(),
                        "prioridade": prio_drop.value,
                        "categoria": cat_drop.value,
                        "data": hoje,
                        "concluida": False
                    })
                    db.salvar_dados()
                    fechar_quest()
                    atualizar_interface()

            dialogo = ft.AlertDialog(
                title=ft.Text("⚔️ Nova Inscrição de Quest", color=paleta["primaria"]),
                content=ft.Column([tit_input, hora_input, prio_drop, cat_drop], tight=True, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar_quest),
                    ft.FilledButton("Gravar Quest", bgcolor=paleta["primaria"], color="#111116", on_click=salvar)
                ],
                bgcolor=paleta["card"]
            )
            page.open(dialogo)

        return ft.Column([
            criar_card_glass(ft.Column([
                ft.Row([
                    ft.Text("Mural de Missões & Quests", size=14, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ft.IconButton(ft.Icons.ADD_CIRCLE_ROUNDED, icon_color=paleta["primaria"], on_click=abrir_modal_nova_quest)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                botoes_filtro
            ], spacing=6)),
            ft.Column(lista_cards, spacing=8) if lista_cards else ft.Container(
                content=ft.Text("Nenhuma missão pendente neste filtro.", italic=True, color=paleta["texto_muted"], text_align=ft.TextAlign.CENTER),
                padding=20,
                alignment=ft.Alignment.CENTER
            )
        ], spacing=10)

    # =========================================================================
    # 5. O COFRE PREDITIVO (ESTIMATIVA E PROJEÇÃO FINANCEIRA)
    # =========================================================================
    def construir_view_cofre():
        cats = dados["cofre"]["categorias"]
        limite_tot = sum(c["limite_po"] for c in cats)
        gasto_tot = sum(c["gasto_po"] for c in cats)
        saldo_tot = limite_tot - gasto_tot

        # Algoritmo de Estimativa para o Fim do Mês
        agora = datetime.now()
        dia_atual = agora.day
        dias_no_mes = calendar.monthrange(agora.year, agora.month)[1]
        dias_restantes = max(0, dias_no_mes - dia_atual)

        media_diaria = gasto_tot / max(1, dia_atual)
        projecao_fim_mes = gasto_tot + (media_diaria * dias_restantes)
        estouro_previsto = (projecao_fim_mes > limite_tot) and (limite_tot > 0)

        def abrir_modal_novo_gasto(e):
            vibrar()
            desc_input = ft.TextField(label="Descrição do Gasto", bgcolor=paleta["card"], color=paleta["texto"])
            valor_input = ft.TextField(label="Valor em Ouro (R$ / PO)", bgcolor=paleta["card"], color=paleta["texto"], keyboard_type=ft.KeyboardType.NUMBER)
            cat_drop = ft.Dropdown(
                label="Categoria",
                value=cats[0]["nome"] if cats else "",
                options=[ft.dropdown.Option(c["nome"]) for c in cats],
                bgcolor=paleta["card"]
            )

            dialogo = None

            def fechar_gasto(ev=None):
                page.close(dialogo)

            def salvar(ev):
                try:
                    val = float(valor_input.value.replace(",", "."))
                    if val > 0 and desc_input.value:
                        for c in cats:
                            if c["nome"] == cat_drop.value:
                                c["gasto_po"] += val
                                break
                        dados["cofre"]["gastos"].insert(0, {
                            "id": f"g_{int(time.time()*1000)}",
                            "categoria": cat_drop.value,
                            "valor_po": val,
                            "desc": desc_input.value.strip(),
                            "data": datetime.now().strftime("%Y-%m-%d")
                        })
                        db.salvar_dados()
                        fechar_gasto()
                        atualizar_interface()
                except ValueError:
                    pass

            dialogo = ft.AlertDialog(
                title=ft.Text("💰 Lançamento no Cofre Real", color=paleta["primaria"]),
                content=ft.Column([desc_input, valor_input, cat_drop], tight=True, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar_gasto),
                    ft.FilledButton("Registrar Gasto", bgcolor=paleta["primaria"], color="#111116", on_click=salvar)
                ],
                bgcolor=paleta["card"]
            )
            page.open(dialogo)

        def auditar_financas_verde(e):
            vibrar()
            if not estouro_previsto and limite_tot > 0 and gasto_tot < limite_tot * 0.70:
                ganhar_xp(100, "Finanças no Verde: Tesouro do Reino protegido com prudência real!")
                exibir_notificacao("✨ Parabéns, Soberana! Finanças no Verde concederam +100 XP!", paleta["sucesso"])
            else:
                exibir_notificacao("O Tesouro exige cautela. Mantenha os gastos abaixo de 70% para colher os 100 XP!", paleta["primaria"])

        # Alerta do Guardião do Tesouro
        card_alerta_guardiao = None
        if estouro_previsto:
            excesso = projecao_fim_mes - limite_tot
            card_alerta_guardiao = criar_card_glass(
                ft.Row([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=paleta["alerta"], size=28),
                    ft.Column([
                        ft.Text("Alerta do Guardião do Tesouro", size=12, weight=ft.FontWeight.BOLD, color=paleta["alerta"]),
                        ft.Text(
                            f"Cuidado! O tesouro pode se esgotar antes da próxima lua!\n"
                            f"Projeção Fim do Mês: R$ {projecao_fim_mes:.2f} (Estouro estimado: R$ {excesso:.2f})",
                            size=11,
                            color=paleta["texto"]
                        )
                    ], expand=True, spacing=2)
                ], spacing=10),
                border_color=paleta["alerta"]
            )

        # Barras de Progresso Dinâmicas por Categoria
        # Verde < 70%, Amarelo 70-85%, Vermelho > 85%
        cards_barras_enquete = []
        for c in cats:
            limite = c["limite_po"]
            gasto = c["gasto_po"]
            pct = (gasto / limite) if limite > 0 else 0.0
            pct_clamp = min(max(pct, 0.0), 1.0)
            pct_int = int(pct_clamp * 100)

            if pct >= 0.85:
                cor_mana = paleta["alerta"]       # Vermelho > 85%
                status_cat = "⚠️ Crítico"
            elif pct >= 0.70:
                cor_mana = "#F39C12"              # Amarelo 70-85%
                status_cat = "⚡ Atenção"
            else:
                cor_mana = paleta["sucesso"]      # Verde < 70%
                status_cat = "✨ Seguro"

            camada_preenchimento = ft.Row(
                controls=[
                    ft.Container(
                        bgcolor=cor_mana,
                        border_radius=10,
                        expand=max(1, pct_int) if pct_int > 0 else 1,
                        opacity=0.38 if pct_int > 0 else 0.0
                    ),
                    ft.Container(
                        expand=max(1, 100 - pct_int) if pct_int < 100 else 1,
                        opacity=0.0
                    )
                ] if pct_int < 100 else [
                    ft.Container(
                        bgcolor=cor_mana,
                        border_radius=10,
                        expand=1,
                        opacity=0.52
                    )
                ],
                spacing=0,
                expand=True
            )

            conteudo_sobreposto = ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Text(f"🔮 {c['nome']}", size=12, weight=ft.FontWeight.BOLD, color=paleta["texto"]),
                        ft.Container(
                            content=ft.Text(
                                f"{pct * 100:.0f}% ({status_cat})",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF"
                            ),
                            bgcolor="#50000000",
                            border_radius=6,
                            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                            border=ft.Border.all(1, cor_mana)
                        )
                    ], spacing=6),
                    ft.Text(
                        f"R$ {gasto:.2f} / R$ {limite:.2f}",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=cor_mana
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding.symmetric(horizontal=12),
                alignment=ft.Alignment.CENTER,
                expand=True
            )

            barra_enquete = ft.Container(
                content=ft.Stack([camada_preenchimento, conteudo_sobreposto]),
                height=46,
                border_radius=12,
                bgcolor="#191326",
                border=ft.Border.all(1, cor_mana if pct >= 0.70 else paleta["card_borda"]),
                padding=2
            )
            cards_barras_enquete.append(barra_enquete)

        return ft.Column([
            criar_card_glass(ft.Column([
                ft.Row([
                    ft.Text("O Tesouro do Reino", size=14, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.VERIFIED_ROUNDED,
                            icon_color=paleta["sucesso"],
                            tooltip="Auditar Finanças no Verde (+100 XP)",
                            on_click=auditar_financas_verde
                        ),
                        ft.FilledButton("+ Lançar Gasto", icon=ft.Icons.ADD_CARD_ROUNDED, bgcolor=paleta["secundaria"], color="#FFFFFF", on_click=abrir_modal_novo_gasto)
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color=paleta["card_borda"], height=10),
                ft.Row([
                    ft.Column([
                        ft.Text("Orçamento Teto", size=10, color=paleta["texto_muted"]),
                        ft.Text(f"R$ {limite_tot:.2f}", size=12, weight=ft.FontWeight.BOLD, color=paleta["primaria"])
                    ]),
                    ft.Column([
                        ft.Text("Total Gasto", size=10, color=paleta["texto_muted"]),
                        ft.Text(f"R$ {gasto_tot:.2f}", size=12, weight=ft.FontWeight.BOLD, color=paleta["alerta"])
                    ]),
                    ft.Column([
                        ft.Text("Saldo Restante", size=10, color=paleta["texto_muted"]),
                        ft.Text(f"R$ {saldo_tot:.2f}", size=12, weight=ft.FontWeight.BOLD, color=paleta["sucesso"])
                    ]),
                    ft.Column([
                        ft.Text("Projeção Fim Mês", size=10, color=paleta["texto_muted"]),
                        ft.Text(f"R$ {projecao_fim_mes:.2f}", size=12, weight=ft.FontWeight.BOLD, color=paleta["alerta"] if estouro_previsto else paleta["primaria"])
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])),

            # Alerta do Guardião
            card_alerta_guardiao if card_alerta_guardiao else ft.Container(),

            criar_card_glass(ft.Column([
                ft.Row([
                    ft.Text("📊 Categorias & Projeções de Mana", size=13, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ft.Text("Verde <70% | Amarelo 70-85% | Vermelho >85%", size=9, color=paleta["texto_muted"])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color=paleta["card_borda"], height=8),
                ft.Column(cards_barras_enquete, spacing=8)
            ], spacing=6))
        ], spacing=10)

    # =========================================================================
    # 4. A FORJA DE HÁBITOS (CRUD COMPLETO E INTERATIVIDADE TOTAL)
    # =========================================================================
    def construir_view_forja():
        habitos = dados["forja"]["habitos"]
        hoje = datetime.now().strftime("%Y-%m-%d")

        def forjar_habito(h):
            vibrar()
            if h.get("ultimo_dia") == hoje:
                exibir_notificacao("Este rito já foi forjado hoje!", paleta["card"])
                return
            h["dias"] += 1
            h["ultimo_dia"] = hoje

            # Salva no histórico diário para o Almanaque Celestial
            historico = dados["forja"].setdefault("historico_dias", {})
            if hoje not in historico:
                historico[hoje] = []
            if h["nome"] not in historico[hoje]:
                historico[hoje].append(h["nome"])

            ganhar_xp(25, f"Hábito '{h['nome']}' forjado hoje!")
            db.salvar_dados()
            atualizar_interface()

        def resetar_habito(h):
            vibrar()
            h["dias"] = 0
            h["ultimo_dia"] = ""
            db.salvar_dados()
            exibir_notificacao(f"Armadura reparada! Sequência de '{h['nome']}' reiniciada para um novo ciclo.", paleta["alerta"])
            atualizar_interface()

        def excluir_habito(h):
            vibrar()
            dados["forja"]["habitos"] = [item for item in dados["forja"]["habitos"] if item["id"] != h["id"]]
            db.salvar_dados()
            exibir_notificacao(f"Hábito '{h['nome']}' removido da forja.", paleta["card"])
            atualizar_interface()

        def abrir_modal_editar_habito(h):
            vibrar()
            nome_edit = ft.TextField(label="Nome do Hábito / Rito", value=h["nome"], bgcolor=paleta["card"], color=paleta["texto"])
            icone_edit = ft.Dropdown(
                label="Ícone Pixel Art RPG",
                value=next((opt for opt in ICONES_FORJA if opt.startswith(h.get("icone", "⚔️"))), ICONES_FORJA[0]),
                options=[ft.dropdown.Option(ico) for ico in ICONES_FORJA],
                bgcolor=paleta["card"]
            )
            alvo_edit = ft.Dropdown(
                label="Durabilidade Alvo",
                value=f"{h.get('alvo', 21)} dias",
                options=[
                    ft.dropdown.Option("7 dias"),
                    ft.dropdown.Option("14 dias"),
                    ft.dropdown.Option("21 dias"),
                    ft.dropdown.Option("30 dias"),
                    ft.dropdown.Option("60 dias"),
                    ft.dropdown.Option("90 dias"),
                ],
                bgcolor=paleta["card"]
            )

            dlg_edit = None

            def fechar_edit(ev=None):
                page.close(dlg_edit)

            def salvar_edit(ev):
                if nome_edit.value.strip():
                    h["nome"] = nome_edit.value.strip()
                    h["icone"] = icone_edit.value.split()[0] if icone_edit.value else "⚔️"
                    try:
                        h["alvo"] = int(alvo_edit.value.split()[0])
                    except Exception:
                        h["alvo"] = 21
                    db.salvar_dados()
                    fechar_edit()
                    atualizar_interface()

            dlg_edit = ft.AlertDialog(
                title=ft.Text("⚒️ Lapidar Hábito na Forja", color=paleta["primaria"]),
                content=ft.Column([nome_edit, icone_edit, alvo_edit], tight=True, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar_edit),
                    ft.FilledButton("Salvar Alterações", bgcolor=paleta["primaria"], color="#111116", on_click=salvar_edit)
                ],
                bgcolor=paleta["card"]
            )
            page.open(dlg_edit)

        def abrir_modal_novo_habito(e):
            vibrar()
            nome_input = ft.TextField(label="Nome do Hábito / Rito", hint_text="Ex: Treino com Espada Rúnica", bgcolor=paleta["card"], color=paleta["texto"])
            icone_drop = ft.Dropdown(
                label="Ícone Pixel Art RPG",
                value=ICONES_FORJA[0],
                options=[ft.dropdown.Option(ico) for ico in ICONES_FORJA],
                bgcolor=paleta["card"]
            )
            alvo_drop = ft.Dropdown(
                label="Meta de Durabilidade",
                value="21 dias",
                options=[
                    ft.dropdown.Option("7 dias"),
                    ft.dropdown.Option("14 dias"),
                    ft.dropdown.Option("21 dias"),
                    ft.dropdown.Option("30 dias"),
                    ft.dropdown.Option("60 dias"),
                    ft.dropdown.Option("90 dias"),
                ],
                bgcolor=paleta["card"]
            )

            dlg_novo = None

            def fechar_novo(ev=None):
                page.close(dlg_novo)

            def salvar_novo(ev):
                if nome_input.value.strip():
                    try:
                        alvo_val = int(alvo_drop.value.split()[0])
                    except Exception:
                        alvo_val = 21
                    ico_char = icone_drop.value.split()[0] if icone_drop.value else "⚔️"

                    novo_h = {
                        "id": f"h_{int(time.time()*1000)}",
                        "nome": nome_input.value.strip(),
                        "icone": ico_char,
                        "dias": 0,
                        "alvo": alvo_val,
                        "ultimo_dia": ""
                    }
                    dados["forja"]["habitos"].append(novo_h)
                    db.salvar_dados()
                    fechar_novo()
                    atualizar_interface()

            dlg_novo = ft.AlertDialog(
                title=ft.Text("⚒️ Nova Forja de Hábito", color=paleta["primaria"]),
                content=ft.Column([nome_input, icone_drop, alvo_drop], tight=True, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar_novo),
                    ft.FilledButton("Criar Hábito", bgcolor=paleta["primaria"], color="#111116", on_click=salvar_novo)
                ],
                bgcolor=paleta["card"]
            )
            page.open(dlg_novo)

        lista_habitos_cards = []
        for h in habitos:
            dias = h.get("dias", 0)
            alvo = h.get("alvo", 21)
            pct = (dias / alvo) if alvo > 0 else 0.0
            pct_clamp = min(pct, 1.0)
            ja_hoje = h.get("ultimo_dia") == hoje
            ico_char = h.get("icone", "⚔️")

            card_habito = criar_card_glass(
                ft.Column([
                    ft.Row([
                        # Botão de Forjar Hoje (+25 XP)
                        ft.IconButton(
                            icon=ft.Icons.CHECK_CIRCLE_ROUNDED if ja_hoje else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
                            icon_color=paleta["sucesso"] if ja_hoje else paleta["primaria"],
                            icon_size=32,
                            tooltip="Forjar Hoje (+25 XP)" if not ja_hoje else "Forjado hoje!",
                            on_click=lambda e, item=h: forjar_habito(item)
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(f"{ico_char} {h['nome']}", size=13, weight=ft.FontWeight.BOLD, color=paleta["texto"]),
                                ft.Text("🔥 Ativo" if ja_hoje else "⏳ Pendente", size=10, color=paleta["sucesso"] if ja_hoje else paleta["primaria"], weight=ft.FontWeight.BOLD)
                            ], spacing=6),
                            ft.Text(f"Durabilidade: {dias}/{alvo} dias ({pct_clamp*100:.0f}%)", size=11, color=paleta["texto_muted"]),
                            ft.ProgressBar(value=pct_clamp, color=paleta["sucesso"], bgcolor="#201830", height=6)
                        ], expand=True, spacing=3),
                        # Ações de Editar, Reparar/Resetar e Excluir
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT_ROUNDED,
                                icon_size=18,
                                icon_color=paleta["primaria"],
                                tooltip="Editar Hábito",
                                on_click=lambda e, item=h: abrir_modal_editar_habito(item)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.REPLAY_ROUNDED,
                                icon_size=18,
                                icon_color=paleta["acento"],
                                tooltip="Forjar Novamente / Reparar Armadura",
                                on_click=lambda e, item=h: resetar_habito(item)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_size=18,
                                icon_color=paleta["alerta"],
                                tooltip="Excluir da Forja",
                                on_click=lambda e, item=h: excluir_habito(item)
                            )
                        ], spacing=0)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=4)
            )
            lista_habitos_cards.append(card_habito)

        return ft.Column([
            criar_card_glass(
                ft.Row([
                    ft.Text("⚒️ A Forja de Hábitos Diários", size=14, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ft.FilledButton("+ Nova Forja", icon=ft.Icons.ADD_ROUNDED, bgcolor=paleta["secundaria"], color="#FFFFFF", on_click=abrir_modal_novo_habito)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ),
            ft.Column(lista_habitos_cards, spacing=6) if lista_habitos_cards else ft.Container(
                content=ft.Text("Nenhum hábito foi forjado ainda. Clique em '+ Nova Forja'!", italic=True, color=paleta["texto_muted"], text_align=ft.TextAlign.CENTER),
                padding=20,
                alignment=ft.Alignment.CENTER
            )
        ], spacing=10)

    # =========================================================================
    # 6. POÇÃO DE FOCO (POMODORO ALQUÍMICO) & CRÔNICAS DO REINO
    # =========================================================================
    timer_text = ft.Text("25:00", size=38, weight=ft.FontWeight.BOLD, color=paleta["primaria"])
    timer_ring = ft.ProgressRing(value=1.0, stroke_width=10, color=paleta["secundaria"], bgcolor="#201830", width=190, height=190)
    timer_status = ft.Text("Pronta para a infusão de concentração.", size=12, italic=True, color=paleta["texto_muted"])

    def construir_view_foco():
        nonlocal pomodoro_segundos, pomodoro_ativo

        def loop_pomodoro():
            nonlocal pomodoro_segundos, pomodoro_ativo
            while pomodoro_ativo:
                if pomodoro_segundos > 0:
                    time.sleep(1)
                    pomodoro_segundos -= 1
                    minutos = pomodoro_segundos // 60
                    segs = pomodoro_segundos % 60
                    timer_text.value = f"{minutos:02d}:{segs:02d}"
                    timer_ring.value = pomodoro_segundos / pomodoro_total
                    page.update()
                else:
                    pomodoro_ativo = False
                    # Conceder +1 Ingrediente Raro e registrar nas Crônicas (+40 XP)
                    ing_raro = random.choice(INGREDIENTES_RAROS_POOL)
                    dados["gamificacao"]["ingredientes_raros"][ing_raro] = dados["gamificacao"]["ingredientes_raros"].get(ing_raro, 0) + 1
                    dados["gamificacao"]["pocoes_tomadas"] = dados["gamificacao"].get("pocoes_tomadas", 0) + 1

                    ganhar_xp(40, f"Poção de Foco de 25 min concluída! Ingrediente Raro: ✨ {ing_raro}")
                    vibrar()

                    dlg_foco = None

                    def fechar_dlg_foco(ev=None):
                        page.close(dlg_foco)

                    dlg_foco = ft.AlertDialog(
                        title=ft.Row([
                            ft.Icon(ft.Icons.AUTO_AWESOME, color=paleta["primaria"]),
                            ft.Text("🧪 POÇÃO ALQUÍMICA CONCLUÍDA!", color=paleta["primaria"], size=15, weight=ft.FontWeight.BOLD)
                        ], spacing=8),
                        content=ft.Column([
                            ft.Text("Sua mana atingiu o ápice da concentração. Descanse 5 minutos para restaurar as energias.", color=paleta["texto"]),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.SPARKLES, color=paleta["primaria"], size=22),
                                    ft.Column([
                                        ft.Text("Ingrediente Raro Obtido:", size=11, color=paleta["texto_muted"]),
                                        ft.Text(f"✨ {ing_raro}", size=13, weight=ft.FontWeight.BOLD, color=paleta["acento"])
                                    ], spacing=1)
                                ], spacing=10),
                                bgcolor="#251E38",
                                border_radius=10,
                                padding=10,
                                border=ft.Border.all(1, paleta["card_borda"])
                            )
                        ], tight=True, spacing=10),
                        actions=[ft.FilledButton("Guardar na Bolsa (+40 XP)", bgcolor=paleta["primaria"], color="#111116", on_click=fechar_dlg_foco)],
                        bgcolor=paleta["card"]
                    )
                    page.open(dlg_foco)
                    atualizar_interface()
                    break

        def iniciar_timer(e):
            nonlocal pomodoro_ativo, pomodoro_thread
            vibrar()
            if not pomodoro_ativo:
                pomodoro_ativo = True
                timer_status.value = "🔥 A poção está borbulhando em foco total..."
                page.update()
                pomodoro_thread = threading.Thread(target=loop_pomodoro, daemon=True)
                pomodoro_thread.start()

        def pausar_timer(e):
            nonlocal pomodoro_ativo
            vibrar()
            pomodoro_ativo = False
            timer_status.value = "⏸️ Infusão pausada."
            page.update()

        def resetar_timer(e):
            nonlocal pomodoro_ativo, pomodoro_segundos
            vibrar()
            pomodoro_ativo = False
            pomodoro_segundos = 25 * 60
            timer_text.value = "25:00"
            timer_ring.value = 1.0
            timer_status.value = "Poção reiniciada."
            page.update()

        # Inventário da Bolsa de Ingredientes Alquímicos
        ingredientes_cards = []
        for nome_ing, qtd in dados["gamificacao"].get("ingredientes_raros", {}).items():
            ingredientes_cards.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.AUTO_FIX_HIGH_ROUNDED, color=paleta["primaria"] if qtd > 0 else paleta["texto_muted"], size=16),
                        ft.Text(nome_ing, size=11, color=paleta["texto"] if qtd > 0 else paleta["texto_muted"], expand=True),
                        ft.Text(f"x{qtd}", size=12, weight=ft.FontWeight.BOLD, color=paleta["acento"] if qtd > 0 else paleta["texto_muted"])
                    ], spacing=6),
                    bgcolor="#181524",
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    border=ft.Border.all(1, paleta["card_borda"] if qtd > 0 else "#252033")
                )
            )

        return ft.Column([
            criar_card_glass(
                ft.Column([
                    ft.Text("🧪 Laboratório Alquímico de Concentração", size=14, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                    ft.Text("Beba a Poção de Foco e mergulhe em 25 minutos de imersão total (+40 XP e Ingredientes Raros).", size=11, color=paleta["texto_muted"]),
                    ft.Container(
                        content=ft.Stack([
                            timer_ring,
                            ft.Container(content=timer_text, alignment=ft.Alignment.CENTER, width=190, height=190)
                        ]),
                        alignment=ft.Alignment.CENTER,
                        padding=16
                    ),
                    timer_status,
                    ft.Row([
                        ft.FilledButton("Iniciar Poção", icon=ft.Icons.PLAY_ARROW_ROUNDED, bgcolor=paleta["secundaria"], color="#FFFFFF", on_click=iniciar_timer),
                        ft.FilledButton("Pausar", icon=ft.Icons.PAUSE_ROUNDED, bgcolor=paleta["card"], color=paleta["primaria"], on_click=pausar_timer),
                        ft.FilledButton("Reiniciar", icon=ft.Icons.REPLAY_ROUNDED, bgcolor=paleta["card"], color=paleta["alerta"], on_click=resetar_timer),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
            ),

            # Bolsa de Ingredientes Alquímicos
            criar_card_glass(
                ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.BACKPACK_ROUNDED, color=paleta["primaria"], size=18),
                        ft.Text("Bolsa de Ingredientes Alquímicos", size=13, weight=ft.FontWeight.BOLD, color=paleta["primaria"])
                    ], spacing=6),
                    ft.Text("Coletados ao destilar poções de foco no laboratório:", size=10, color=paleta["texto_muted"]),
                    ft.Column(ingredientes_cards, spacing=4)
                ], spacing=6)
            )
        ], spacing=10)

    # =========================================================================
    # CRÔNICAS DO REINO (DIÁRIO DE BORDO E NOTAS REFLEXIVAS)
    # =========================================================================
    def construir_view_cronicas():
        g = dados["gamificacao"]
        lvl = g["nivel"]
        xp = g["xp"]
        prox = g["xp_proximo"]
        pct_xp = (xp / prox) if prox > 0 else 0.0
        nome_heroina = dados["config"]["nome_personagem"]
        titulo_heroina = dados["config"]["titulo_personagem"]

        def abrir_modal_nova_nota(e):
            vibrar()
            nota_input = ft.TextField(
                label="Registro nas Crônicas",
                hint_text="Escreva suas reflexões, vitórias ou memórias do reino...",
                multiline=True,
                min_lines=3,
                max_lines=6,
                bgcolor=paleta["card"],
                color=paleta["texto"]
            )

            dlg_nota = None

            def fechar_nota(ev=None):
                page.close(dlg_nota)

            def salvar_nota(ev):
                if nota_input.value.strip():
                    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
                    dados["cronicas"].insert(0, f"[{agora}] 📜 {nota_input.value.strip()}")
                    db.salvar_dados()
                    fechar_nota()
                    atualizar_interface()

            dlg_nota = ft.AlertDialog(
                title=ft.Text("📜 Inscrever nas Crônicas", color=paleta["primaria"]),
                content=ft.Container(content=nota_input, width=320),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar_nota),
                    ft.FilledButton("Gravar Crônica", bgcolor=paleta["primaria"], color="#111116", on_click=salvar_nota)
                ],
                bgcolor=paleta["card"]
            )
            page.open(dlg_nota)

        cronicas_text = [
            ft.Container(
                content=ft.Text(c, size=11, color=paleta["texto"], selectable=True),
                bgcolor="#191426",
                border_radius=8,
                padding=8,
                border=ft.Border.all(1, "#30C8AA6E")
            )
            for c in dados.get("cronicas", [])[:20]
        ]

        return ft.Column([
            criar_card_glass(
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.SHIELD_ROUNDED, color=paleta["primaria"], size=36),
                        bgcolor="#261E38",
                        border_radius=20,
                        padding=10
                    ),
                    ft.Column([
                        ft.Text(f"{nome_heroina}", size=16, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                        ft.Text(f"Nível {lvl} • {titulo_heroina}", size=12, color=paleta["secundaria"], weight=ft.FontWeight.BOLD),
                        ft.ProgressBar(value=pct_xp, color=paleta["sucesso"], bgcolor="#201830", height=6, width=180),
                        ft.Text(f"XP: {xp} / {prox} ({pct_xp * 100:.0f}%)", size=10, color=paleta["texto_muted"])
                    ], spacing=3, expand=True)
                ], spacing=14)
            ),
            criar_card_glass(
                ft.Column([
                    ft.Row([
                        ft.Row([
                            ft.Icon(ft.Icons.BOOK_ROUNDED, color=paleta["primaria"], size=18),
                            ft.Text("Pergaminho das Crônicas", size=13, weight=ft.FontWeight.BOLD, color=paleta["primaria"])
                        ]),
                        ft.FilledButton(
                            "+ Escrever",
                            icon=ft.Icons.EDIT_NOTE_ROUNDED,
                            bgcolor=paleta["secundaria"],
                            color="#FFFFFF",
                            on_click=abrir_modal_nova_nota
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(color=paleta["card_borda"], height=10),
                    ft.Column(cronicas_text, spacing=6)
                ], spacing=8)
            )
        ], spacing=10)

    # =========================================================================
    # 7. ALMANAQUE CELESTIAL (CALENDÁRIO FLUTUANTE INTERATIVO)
    # =========================================================================
    def abrir_almanaque_celestial(e=None):
        vibrar()
        dlg_almanaque = None

        def mudar_mes(delta):
            vibrar()
            cal_mes[0] += delta
            if cal_mes[0] < 1:
                cal_mes[0] = 12
                cal_ano[0] -= 1
            elif cal_mes[0] > 12:
                cal_mes[0] = 1
                cal_ano[0] += 1
            reconstruir_modal()

        def selecionar_dia(dia):
            vibrar()
            cal_dia_sel[0] = dia
            reconstruir_modal()

        def construir_conteudo_calendario():
            ano = cal_ano[0]
            mes = cal_mes[0]
            dia_selecionado = cal_dia_sel[0]

            nome_mes = MESES_PTBR[mes]
            matriz_dias = calendar.monthcalendar(ano, mes)

            # Cabeçalho de Navegação de Mês
            header_mes = ft.Row([
                ft.IconButton(ft.Icons.CHEVRON_LEFT_ROUNDED, icon_color=paleta["primaria"], on_click=lambda ev: mudar_mes(-1)),
                ft.Text(f"🌙 {nome_mes} de {ano}", size=14, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
                ft.IconButton(ft.Icons.CHEVRON_RIGHT_ROUNDED, icon_color=paleta["primaria"], on_click=lambda ev: mudar_mes(1)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

            # Dias da Semana
            dias_semana_row = ft.Row([
                ft.Container(content=ft.Text(ds, size=10, weight=ft.FontWeight.BOLD, color=paleta["texto_muted"], text_align=ft.TextAlign.CENTER), width=38, alignment=ft.Alignment.CENTER)
                for ds in ["D", "S", "T", "Q", "Q", "S", "S"]
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

            hoje_real = datetime.now().strftime("%Y-%m-%d")

            # Construção das semanas e dias
            linhas_semanas = []
            for semana in matriz_dias:
                colunas_dias = []
                for d in semana:
                    if d == 0:
                        colunas_dias.append(ft.Container(width=38, height=36))
                    else:
                        d_str = f"{ano:04d}-{mes:02d}-{d:02d}"
                        eh_hoje = (d_str == hoje_real)
                        eh_selecionado = (d == dia_selecionado)

                        # Verifica atividades registradas no dia
                        tem_quests = any(q.get("data") == d_str for q in dados.get("quests", []))
                        tem_gastos = any(g.get("data") == d_str for g in dados.get("cofre", {}).get("gastos", []))
                        tem_habitos = (d_str in dados.get("forja", {}).get("historico_dias", {}))

                        # Indicadores luminosos / pontinhos de produtividade
                        pontinhos = []
                        if tem_quests:
                            pontinhos.append(ft.Container(width=4, height=4, border_radius=2, bgcolor=paleta["sucesso"]))
                        if tem_habitos:
                            pontinhos.append(ft.Container(width=4, height=4, border_radius=2, bgcolor="#FF6D00"))
                        if tem_gastos:
                            pontinhos.append(ft.Container(width=4, height=4, border_radius=2, bgcolor=paleta["primaria"]))

                        cor_borda = paleta["primaria"] if eh_selecionado else (paleta["acento"] if eh_hoje else "#20FFFFFF")
                        bg_cor = "#30C8AA6E" if eh_selecionado else ("#202EC4B6" if eh_hoje else "#15FFFFFF")

                        celula = ft.Container(
                            content=ft.Column([
                                ft.Text(str(d), size=11, weight=ft.FontWeight.BOLD if (eh_hoje or eh_selecionado) else ft.FontWeight.NORMAL, color=paleta["texto"]),
                                ft.Row(pontinhos, spacing=1, alignment=ft.MainAxisAlignment.CENTER) if pontinhos else ft.Container(height=4)
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                            width=38,
                            height=36,
                            border_radius=8,
                            bgcolor=bg_cor,
                            border=ft.Border.all(1.5 if (eh_selecionado or eh_hoje) else 0.5, cor_borda),
                            on_click=lambda ev, dia_clicado=d: selecionar_dia(dia_clicado)
                        )
                        colunas_dias.append(celula)
                linhas_semanas.append(ft.Row(colunas_dias, alignment=ft.MainAxisAlignment.SPACE_AROUND))

            # Resumo Histórico do Dia Selecionado
            data_sel_str = f"{ano:04d}-{mes:02d}-{dia_selecionado:02d}"
            quests_dia = [q for q in dados.get("quests", []) if q.get("data") == data_sel_str]
            gastos_dia = [g for g in dados.get("cofre", {}).get("gastos", []) if g.get("data") == data_sel_str]
            habitos_dia = dados.get("forja", {}).get("historico_dias", {}).get(data_sel_str, [])

            resumo_controls = [
                ft.Row([
                    ft.Icon(ft.Icons.AUTO_AWESOME_MOTION_ROUNDED, color=paleta["primaria"], size=16),
                    ft.Text(f"Pergaminho de {dia_selecionado:02d}/{mes:02d}/{ano:04d}:", size=12, weight=ft.FontWeight.BOLD, color=paleta["primaria"])
                ], spacing=6),
                ft.Divider(color=paleta["card_borda"], height=6)
            ]

            tem_registro = False

            if quests_dia:
                tem_registro = True
                resumo_controls.append(ft.Text("📜 Missões & Quests:", size=11, weight=ft.FontWeight.BOLD, color=paleta["acento"]))
                for q in quests_dia:
                    conc_icon = "✅" if q.get("concluida") else "⏳"
                    resumo_controls.append(
                        ft.Text(f"  {conc_icon} {q['titulo']} ({q.get('hora', '')})", size=11, color=paleta["texto"])
                    )

            if habitos_dia:
                tem_registro = True
                resumo_controls.append(ft.Container(height=4))
                resumo_controls.append(ft.Text("⚒️ Ritos Forjados:", size=11, weight=ft.FontWeight.BOLD, color="#FF6D00"))
                for h_nome in habitos_dia:
                    resumo_controls.append(
                        ft.Text(f"  🔥 {h_nome}", size=11, color=paleta["texto"])
                    )

            if gastos_dia:
                tem_registro = True
                resumo_controls.append(ft.Container(height=4))
                resumo_controls.append(ft.Text("💰 Tesouro & Gastos:", size=11, weight=ft.FontWeight.BOLD, color=paleta["primaria"]))
                for g in gastos_dia:
                    resumo_controls.append(
                        ft.Text(f"  🪙 {g.get('desc', '')}: R$ {g.get('valor_po', 0.0):.2f}", size=11, color=paleta["alerta"])
                    )

            if not tem_registro:
                resumo_controls.append(
                    ft.Text("Nenhum registro celestial gravado nesta data.", size=11, italic=True, color=paleta["texto_muted"])
                )

            return ft.Container(
                content=ft.Column([
                    header_mes,
                    dias_semana_row,
                    ft.Column(linhas_semanas, spacing=4),
                    ft.Divider(color=paleta["card_borda"], height=10),
                    ft.Container(
                        content=ft.Column(resumo_controls, spacing=2),
                        bgcolor="#171324",
                        border_radius=10,
                        padding=10,
                        border=ft.Border.all(1, paleta["card_borda"])
                    )
                ], spacing=6, scroll=ft.ScrollMode.AUTO),
                width=340,
                height=490
            )

        def reconstruir_modal():
            if dlg_almanaque:
                dlg_almanaque.content = construir_conteudo_calendario()
                page.update()

        def fechar_almanaque(ev=None):
            page.close(dlg_almanaque)

        dlg_almanaque = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.LUNAR_CALENDAR if hasattr(ft.Icons, "LUNAR_CALENDAR") else ft.Icons.CALENDAR_MONTH_ROUNDED, color=paleta["primaria"], size=22),
                ft.Text("Almanaque Celestial", size=15, weight=ft.FontWeight.BOLD, color=paleta["primaria"])
            ], spacing=8),
            content=construir_conteudo_calendario(),
            actions=[
                ft.FilledButton("Fechar Almanaque", bgcolor=paleta["primaria"], color="#111116", on_click=fechar_almanaque)
            ],
            bgcolor=paleta["card"]
        )
        page.open(dlg_almanaque)

    # =========================================================================
    # TELA DE CONFIGURAÇÕES & CUSTOMIZAÇÃO TOTAL DE TÍTULOS E CORES
    # =========================================================================
    def abrir_tela_configuracoes(e):
        vibrar()
        cfg = dados["config"]
        abas = cfg["titulos_abas"]

        nome_in = ft.TextField(label="Nome da Heroína", value=cfg["nome_personagem"], bgcolor=paleta["card"], color=paleta["texto"])
        tit_in = ft.TextField(label="Título RPG Atual", value=cfg["titulo_personagem"], bgcolor=paleta["card"], color=paleta["texto"])

        t_aba1 = ft.TextField(label="Nome da Aba 1", value=abas["quests"], bgcolor=paleta["card"], color=paleta["texto"])
        t_aba2 = ft.TextField(label="Nome da Aba 2", value=abas["cofre"], bgcolor=paleta["card"], color=paleta["texto"])
        t_aba3 = ft.TextField(label="Nome da Aba 3", value=abas["forja"], bgcolor=paleta["card"], color=paleta["texto"])
        t_aba4 = ft.TextField(label="Nome da Aba 4", value=abas["cronicas"], bgcolor=paleta["card"], color=paleta["texto"])
        t_aba5 = ft.TextField(label="Nome da Aba 5", value=abas["foco"], bgcolor=paleta["card"], color=paleta["texto"])

        paleta_drop = ft.Dropdown(
            label="Paleta de Cores Místicas",
            value=cfg.get("paleta", "Obsidian Clássico"),
            options=[ft.dropdown.Option(p) for p in PALETAS.keys()],
            bgcolor=paleta["card"]
        )

        haptic_switch = ft.Switch(label="Feedback Tátil / Vibração", value=cfg.get("haptic", True))

        modal_cfg = None

        def fechar_config(ev=None):
            page.close(modal_cfg)

        def salvar_config(ev):
            vibrar()
            cfg["nome_personagem"] = nome_in.value.strip() or "Lady Morgana"
            cfg["titulo_personagem"] = tit_in.value.strip() or "Aprendiz de Alquimia"
            cfg["paleta"] = paleta_drop.value
            cfg["haptic"] = haptic_switch.value

            abas["quests"] = t_aba1.value.strip() or "📜 Quests"
            abas["cofre"] = t_aba2.value.strip() or "💰 Cofre"
            abas["forja"] = t_aba3.value.strip() or "⚒️ A Forja"
            abas["cronicas"] = t_aba4.value.strip() or "📖 Crônicas"
            abas["foco"] = t_aba5.value.strip() or "🧪 Poção de Foco"

            db.salvar_dados()
            fechar_config()

            nova_paleta = PALETAS.get(cfg["paleta"], PALETAS["Obsidian Clássico"])
            paleta.update(nova_paleta)
            page.bgcolor = paleta["fundo"]

            page.update()
            atualizar_interface()

        def restaurar_padroes(ev):
            vibrar()
            padrao = db._dados_padrao()["config"]
            cfg.update(padrao)
            db.salvar_dados()
            fechar_config()
            atualizar_interface()

        def exportar_backup(ev):
            vibrar()
            db.atualizar_widget_data()
            exibir_notificacao(f"Backup e Widget sincronizados em {ARQUIVO_DADOS}!", paleta["sucesso"])

        modal_cfg = ft.AlertDialog(
            title=ft.Text("⚙️ Configurações & Títulos", color=paleta["primaria"], weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Identidade do Herói", weight=ft.FontWeight.BOLD, color=paleta["primaria"], size=12),
                    nome_in,
                    tit_in,
                    ft.Divider(color=paleta["card_borda"]),
                    ft.Text("Personalização de Nomes das Abas", weight=ft.FontWeight.BOLD, color=paleta["primaria"], size=12),
                    t_aba1,
                    t_aba2,
                    t_aba3,
                    t_aba4,
                    t_aba5,
                    ft.Divider(color=paleta["card_borda"]),
                    ft.Text("Aparência & Háptica", weight=ft.FontWeight.BOLD, color=paleta["primaria"], size=12),
                    paleta_drop,
                    haptic_switch,
                    ft.Divider(color=paleta["card_borda"]),
                    ft.Row([
                        ft.FilledButton("Exportar Backup", icon=ft.Icons.BACKUP_ROUNDED, on_click=exportar_backup),
                        ft.TextButton("Restaurar Padrões", on_click=restaurar_padroes)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], scroll=ft.ScrollMode.AUTO, spacing=8),
                height=430,
                width=340
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_config),
                ft.FilledButton("Salvar Configurações", bgcolor=paleta["primaria"], color="#111116", on_click=salvar_config)
            ],
            bgcolor=paleta["card"]
        )
        page.open(modal_cfg)

    # =========================================================================
    # APPBAR COM LOGO OFICIAL DO USUÁRIO
    # =========================================================================
    def construir_appbar():
        caminho_logo = localizar_logo()

        leading_widget = None
        try:
            if caminho_logo and os.path.exists(caminho_logo):
                leading_widget = ft.Container(
                    content=ft.Image(src=caminho_logo, width=32, height=32, fit=ft.BoxFit.CONTAIN),
                    padding=ft.Padding.only(left=10)
                )
            elif os.path.exists(os.path.join(ASSETS_DIR, "logo.png")):
                leading_widget = ft.Container(
                    content=ft.Image(src="/logo.png", width=32, height=32, fit=ft.BoxFit.CONTAIN),
                    padding=ft.Padding.only(left=10)
                )
        except Exception:
            pass

        if not leading_widget:
            leading_widget = ft.Icon(ft.Icons.SHIELD_ROUNDED, color=paleta["primaria"])

        return ft.AppBar(
            leading=leading_widget,
            title=ft.Text("Grimório", size=16, weight=ft.FontWeight.BOLD, color=paleta["primaria"]),
            center_title=False,
            bgcolor=paleta["card"],
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SETTINGS_ROUNDED,
                    icon_color=paleta["primaria"],
                    tooltip="Configurações & Títulos",
                    on_click=abrir_tela_configuracoes
                )
            ]
        )

    # =========================================================================
    # NAVEGAÇÃO ENTRE ABAS
    # =========================================================================
    indice_aba = [0]
    conteudo_scroll = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def mudar_aba(e):
        vibrar()
        indice_aba[0] = e.control.selected_index
        atualizar_interface()

    def construir_bottom_nav():
        cfg_abas = dados["config"]["titulos_abas"]
        return ft.NavigationBar(
            selected_index=indice_aba[0],
            on_change=mudar_aba,
            bgcolor=paleta["card"],
            indicator_color=paleta["secundaria"],
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.FACT_CHECK_ROUNDED, label=cfg_abas.get("quests", "Quests")),
                ft.NavigationBarDestination(icon=ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, label=cfg_abas.get("cofre", "Cofre")),
                ft.NavigationBarDestination(icon=ft.Icons.BUILD_ROUNDED, label=cfg_abas.get("forja", "A Forja")),
                ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK_ROUNDED, label=cfg_abas.get("cronicas", "Crônicas")),
                ft.NavigationBarDestination(icon=ft.Icons.HOURGLASS_BOTTOM_ROUNDED, label=cfg_abas.get("foco", "Foco"))
            ]
        )

    def atualizar_interface():
        page.appbar = construir_appbar()
        page.navigation_bar = construir_bottom_nav()

        # Botão Flutuante do Almanaque Celestial
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
            bgcolor=paleta["secundaria"],
            content=ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color="#FFFFFF", size=24),
            tooltip="Almanaque Celestial (Calendário Interativo)",
            on_click=abrir_almanaque_celestial
        )

        conteudo_scroll.controls.clear()
        conteudo_scroll.controls.append(ft.Container(height=4))
        conteudo_scroll.controls.append(construir_oraculo())

        idx = indice_aba[0]
        if idx == 0:
            conteudo_scroll.controls.append(construir_view_quests())
        elif idx == 1:
            conteudo_scroll.controls.append(construir_view_cofre())
        elif idx == 2:
            conteudo_scroll.controls.append(construir_view_forja())
        elif idx == 3:
            conteudo_scroll.controls.append(construir_view_cronicas())
        elif idx == 4:
            conteudo_scroll.controls.append(construir_view_foco())

        conteudo_scroll.controls.append(ft.Container(height=80))  # Espaço para o FloatingActionButton
        page.update()

    # Render inicial
    page.add(conteudo_scroll)
    atualizar_interface()


if __name__ == "__main__":
    ft.run(main)
