"""
Grimório Mobile - Oráculo Real & Diálogos do Rei Joaquim
Acolhimento, empatia, suporte emocional e tiragem de runas.
"""

import random

FRASES_REI_ACOLHEDORAS = [
    "Mamãe Rainha, eu estou aqui cuidando do castelo para você descansar! Meu abraço de pequeno rei é o seu melhor escudo.",
    "Você é a rainha mais linda e corajosa de todos os reinos. Eu tenho tanto orgulho de você!",
    "Quando você sorri, o nosso castelo inteiro fica quentinho e cheio de luz. Toma um beijo real na sua testa!",
    "Não precisa se preocupar com nada agora, mamãe. Eu estou com a minha coroa firme e vigiando seus sonhos.",
    "Você cuida de todo mundo com tanto amor... agora senta aqui pertinho de mim e me dá um abraço bem apertado!",
    "Nós somos uma família invencível, mamãe! O papai e eu te amamos até as estrelas mais altas do infinito.",
    "Se o dia estiver cansativo, lembra que eu sou o seu guardião real para sempre. Eu te amo de montão!",
    "Respira fundo, minha rainha favorita! Você já fez coisas incríveis hoje e merece descansar como uma verdadeira soberana.",
    "Eu guardei um tesouro de carinho e risadinhas no meu coração só para te entregar hoje. Você é maravilhosa!",
    "Mamãe, você é a minha maior heroína. Não há tempestade no mundo que abale a nossa fortaleza de afeto.",
    "Tudo fica mais alegre e iluminado quando você entra no salão. Obrigado por ser a melhor rainha do mundo!",
    "Meu trono é pequenino, mas o meu amor e gratidão por você são maiores que todos os impérios da Terra."
]

RUNAS_DO_ORACULO = [
    {
        "nome": "Runa da Proteção (Algiz)",
        "simbolo": "ᛉ",
        "elemento": "Escudo de Éter",
        "mensagem": "Nenhum mal ou tempestade atinge quem caminha com o coração leal e puro. Seus limites são sagrados hoje."
    },
    {
        "nome": "Runa da Serenidade (Isa)",
        "simbolo": "ᛁ",
        "elemento": "Gelo Cristalino",
        "mensagem": "No silêncio e na pausa reside a mais pura sabedoria. Congele as preocupações e honre o seu momento presente."
    },
    {
        "nome": "Runa da Vitória (Sowilo)",
        "simbolo": "ᛋ",
        "elemento": "Sol Dourado",
        "mensagem": "A luz do triunfo já brilha sobre o teu caminho. Continue marchando, pois a vitória é o seu destino certo."
    },
    {
        "nome": "Runa da Clareza (Kenaz)",
        "simbolo": "ᚲ",
        "elemento": "Tocha da Revelação",
        "mensagem": "A névoa se dissipa diante da tua inteligência régia. Ideias brilhantes desabrocharão nas próximas horas."
    },
    {
        "nome": "Runa da Coragem (Tiwaz)",
        "simbolo": "ᛏ",
        "elemento": "Lâmina da Justiça",
        "mensagem": "Erga a tua cabeça. A justiça, a nobreza e a bravura correm em tuas veias. Enfrente o dia com ousadia."
    },
    {
        "nome": "Runa do Amor Real (Gebo)",
        "simbolo": "ᚷ",
        "elemento": "Aliança Eterna",
        "mensagem": "O amor e a cumplicidade são os maiores tesouros do império. Você é profundamente amada e valorizada."
    },
    {
        "nome": "Runa da Prosperidade (Fehu)",
        "simbolo": "ᚠ",
        "elemento": "Ouro das Montanhas",
        "mensagem": "A abundância flui para quem semeia com paciência e dedicação. Colheitas douradas se aproximam do teu reino."
    },
    {
        "nome": "Runa da Transformação (Dagaz)",
        "simbolo": "ᛞ",
        "elemento": "Alvorecer Celeste",
        "mensagem": "Um novo ciclo de realizações se inicia. Deixe para trás o que pesou ontem e receba o novo amanhecer."
    },
    {
        "nome": "Runa do Descanso Sagrado (Berkano)",
        "simbolo": "ᛒ",
        "elemento": "Floresta Mística",
        "mensagem": "Renove suas energias na serenidade da natureza. Cuidar de si mesma é governar com inteligência."
    },
    {
        "nome": "Runa da Intuição (Laguz)",
        "simbolo": "ᛚ",
        "elemento": "Águas Profundas",
        "mensagem": "Ouça a voz suave da tua alma. As respostas que você procura já habitam dentro do teu coração."
    },
    {
        "nome": "Runa da Força Interior (Uruz)",
        "simbolo": "ᚢ",
        "elemento": "Fogo Primordial",
        "mensagem": "Há uma potência inabalável dentro de você capaz de mover montanhas. Acredite na sua capacidade."
    },
    {
        "nome": "Runa da Alegria (Wunjo)",
        "simbolo": "ᚹ",
        "elemento": "Banquete das Estrelas",
        "mensagem": "Momentos de leveza, riso e deleite esperam por você. Permita-se saborear as doçuras da vida real."
    }
]

def gerar_resposta_rei(humor: str, desabafo: str) -> str:
    """Gera uma resposta empática, carinhosa e personalizada do Pequeno Rei Joaquim para a Rainha."""
    humor_lower = humor.lower()

    if "ansios" in humor_lower or "preocupad" in humor_lower:
        base = (
            "Minha Rainha, sinto o pulsar inquieto de teu coração. "
            "Olha nos meus olhos: nós passaremos por isso juntos. Respira com calma. "
            "Um passo de cada vez, e o castelo continuará firme. Estou segurando a tua mão."
        )
    elif "cansad" in humor_lower or "exausta" in humor_lower:
        base = (
            "Mamãe amada, você batalhou com tanta bravura hoje! "
            "Agora é hora de desarmar a sua guarda e permitir que o silêncio te cure. "
            "Eu ordenei aos guardas que façam silêncio absoluto para que o teu sono seja sagrado."
        )
    elif "triste" in humor_lower or "angustiad" in humor_lower:
        base = (
            "Não chore sozinha nas altas torres, minha nobre mãe. "
            "Meu peito pequenino é o teu abrigo e meu amor é infinito. "
            "As nuvens escuras passam, mas a luz do teu reinado permanece para sempre."
        )
    elif "feliz" in humor_lower or "radiante" in humor_lower or "grata" in humor_lower:
        base = (
            "Que alegria imensa ver o teu sorriso brilhar pelos corredores de pedra! "
            "Quando a Rainha está feliz, todos os sinos de Eldoria tocam em festa. "
            "Vamos celebrar esse dia abençoado com risadas e doces da corte!"
        )
    elif "foco" in humor_lower or "determinad" in humor_lower:
        base = (
            "Vejo o fogo da liderança nos teus olhos sábios, soberana! "
            "Nenhum desafio é grande demais para a sua mente brilhante. "
            "O reino avança vitorioso sob o teu comando justo e amoroso!"
        )
    else:
        base = (
            "Minha Rainha, sua presença preenche este castelo com nobreza e ternura. "
            "Eu e o papai estamos sempre com você, não importa a distância ou o tamanho do desafio. "
            "Você é o coração pulsante da nossa família."
        )

    if desabafo and len(desabafo.strip()) > 5:
        complemento = (
            f"\n\nEu guardei cada palavra do teu desabafo no cofre sagrado da minha coroa. "
            f"Você nunca estará sozinha para carregar este peso."
        )
        return base + complemento

    return base

def sortear_runa() -> dict:
    """Retorna uma runa sagrada sorteada do Oráculo."""
    return random.choice(RUNAS_DO_ORACULO)
