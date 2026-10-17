"""
Grimório Mobile - Persistência Segura Síncrona para Android & Mobile
Gerenciamento de dados locais em JSON com suporte a diretório gravável do aplicativo.
"""

import os
import json
import uuid
import shutil
from datetime import datetime, date, timedelta

DATA_FILE_NAME = "grimorio_mobile_dados.json"

def get_data_filepath() -> str:
    """
    Retorna o caminho seguro e gravável do arquivo de dados no Android/Mobile.
    Prioriza o diretório de dados persistente do Flet Mobile ou documentos.
    """
    # 1. Verifica variável de ambiente oficial do Flet Mobile no Android/iOS
    flet_storage = os.environ.get("FLET_APP_STORAGE_DATA")
    if flet_storage and os.path.exists(flet_storage):
        caminho_flet = os.path.join(flet_storage, DATA_FILE_NAME)
        # Se ainda não existe no storage gravável, copia o arquivo seed padrão
        if not os.path.exists(caminho_flet):
            seed = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FILE_NAME)
            if os.path.exists(seed):
                try:
                    shutil.copy2(seed, caminho_flet)
                except Exception:
                    pass
        return caminho_flet

    # 2. Testa se o diretório local do script é gravável (modo desenvolvimento)
    local_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(local_dir, DATA_FILE_NAME)
    try:
        teste = os.path.join(local_dir, ".write_test")
        with open(teste, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(teste)
        return local_path
    except Exception:
        # 3. Fallback seguro para diretório home do usuário
        home_dir = os.path.expanduser("~")
        caminho_home = os.path.join(home_dir, DATA_FILE_NAME)
        if not os.path.exists(caminho_home) and os.path.exists(local_path):
            try:
                shutil.copy2(local_path, caminho_home)
            except Exception:
                pass
        return caminho_home

def get_default_data() -> dict:
    """Estrutura padrão inicial do Grimório."""
    hoje_str = date.today().isoformat()
    mes_atual = datetime.now().strftime("%Y-%m")
    
    return {
        "versao": "2.0.0",
        "ultimo_mes_processado": mes_atual,
        "configuracoes": {
            "nome_rainha": "Minha Rainha",
            "tema_atual": "Dark Fantasy Dourado",
            "nomes_abas": {
                "trono": "Trono",
                "quests": "Quests",
                "cofre": "Cofre",
                "forja": "Forja",
                "foco": "Foco"
            }
        },
        "reino": {
            "nome_rainha": "Minha Rainha",
            "nome_reino": "Reino de Eldoria",
            "nivel": 2,
            "titulo_nivel": "Forte de Pedra",
            "exp_atual": 45,
            "exp_proximo": 435,
            "ouro_tesouro": 425.0
        },
        "pet": {
            "nome": "Sir Fagulha",
            "titulo": "Gato Alado Guardião",
            "humor": "Valente e Atento",
            "nivel_afeto": 100,
            "energia": 80,
            "fome": 90,
            "ultimo_cuidado": hoje_str
        },
        "emocional": {
            "historico": [
                {
                    "data": hoje_str,
                    "humor": "Tranquila",
                    "desabafo": "Hoje iniciei a nova jornada no reino com o coração sereno.",
                    "resposta_rei": "Que a paz do teu coração seja a muralha que protege nossos dias mais felizes, minha Rainha."
                }
            ],
            "ultima_runa": {
                "nome": "Runa da Coragem (Tiwaz)",
                "simbolo": "ᛏ",
                "elemento": "Lâmina da Justiça",
                "mensagem": "Erga a tua cabeça. A justiça, a nobreza e a bravura correm em tuas veias. Enfrente o dia com ousadia.",
                "data": hoje_str
            }
        },
        "quests": [
            {
                "id": str(uuid.uuid4()),
                "titulo": "Consagrar o Alvorecer do Reino",
                "categoria": "Principal",
                "dificuldade": "Média",
                "recompensa_ouro": 30.0,
                "recompensa_exp": 40,
                "data_limite": hoje_str,
                "concluida": True,
                "data_conclusao": hoje_str
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Organizar os pergaminhos da semana",
                "categoria": "Diária",
                "dificuldade": "Fácil",
                "recompensa_ouro": 15.0,
                "recompensa_exp": 20,
                "data_limite": hoje_str,
                "concluida": False,
                "data_conclusao": None
            },
            {
                "id": str(uuid.uuid4()),
                "titulo": "Revisar as finanças do trono real",
                "categoria": "Coroa",
                "dificuldade": "Lendária",
                "recompensa_ouro": 60.0,
                "recompensa_exp": 80,
                "data_limite": hoje_str,
                "concluida": False,
                "data_conclusao": None
            }
        ],
        "cofre": {
            "reserva_do_reino": 1200.0,
            "divida_da_coroa": 0.0,
            "teto_gastos_mes": 3000.0,
            "transacoes": [
                {
                    "id": str(uuid.uuid4()),
                    "tipo": "entrada",
                    "titulo": "Tributos do Comércio Nobre",
                    "valor": 1500.0,
                    "categoria": "Tributos",
                    "data": hoje_str,
                    "mes_ano": mes_atual
                },
                {
                    "id": str(uuid.uuid4()),
                    "tipo": "saida",
                    "titulo": "Provisões e Banquete da Corte",
                    "valor": 320.0,
                    "categoria": "Essenciais",
                    "data": hoje_str,
                    "mes_ano": mes_atual
                }
            ],
            "historico_fechamentos": {}
        },
        "forja": {
            "habitos": [
                {
                    "id": str(uuid.uuid4()),
                    "nome": "Beber Elixir Vital (2L de Água)",
                    "tipo": "HP",
                    "streak_atual": 4,
                    "melhor_streak": 12,
                    "concluido_hoje": False,
                    "datas_concluidas": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "nome": "Leitura Arcana (20 minutos)",
                    "tipo": "Mana",
                    "streak_atual": 7,
                    "melhor_streak": 15,
                    "concluido_hoje": True,
                    "datas_concluidas": [hoje_str]
                },
                {
                    "id": str(uuid.uuid4()),
                    "nome": "Caminhada pelos Jardins Reais",
                    "tipo": "HP",
                    "streak_atual": 2,
                    "melhor_streak": 5,
                    "concluido_hoje": False,
                    "datas_concluidas": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "nome": "Meditação & Gratidão",
                    "tipo": "Ouro",
                    "streak_atual": 5,
                    "melhor_streak": 20,
                    "concluido_hoje": True,
                    "datas_concluidas": [hoje_str]
                }
            ]
        },
        "foco": {
            "minutos_foco": 25,
            "minutos_descanso": 5,
            "total_pomodoros": 8,
            "tempo_total_minutos": 200
        }
    }

class GrimorioStorage:
    TITULOS_NIVEL = [
        "Vilarejo Inicial",
        "Forte de Pedra",
        "Cidadela de Prata",
        "Baluarte Arcano",
        "Reino Radiante",
        "Império Celestial",
        "Trono Eterno de Eldoria"
    ]

    def __init__(self):
        self.filepath = get_data_filepath()
        self.data = self.carregar()
        self.verificar_fechamento_mensal()

    def carregar(self) -> dict:
        """Carrega os dados sincronamente do arquivo JSON com tratamento de erros."""
        if not os.path.exists(self.filepath):
            dados = get_default_data()
            self.salvar_dados(dados)
            return dados
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            # Mescla campos faltantes se houver atualizações estruturais
            padrao = get_default_data()
            for chave, valor in padrao.items():
                if chave not in dados:
                    dados[chave] = valor
                elif isinstance(valor, dict) and isinstance(dados.get(chave), dict):
                    for subchave, subvalor in valor.items():
                        if subchave not in dados[chave]:
                            dados[chave][subchave] = subvalor
            return dados
        except Exception as e:
            print(f"[Grimorio Storage] Erro ao carregar JSON: {e}")
            return get_default_data()

    def salvar(self):
        """Salva o estado atual no disco de forma síncrona e atômica."""
        self.salvar_dados(self.data)

    def salvar_dados(self, dados: dict):
        try:
            temp_path = self.filepath + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            os.rename(temp_path, self.filepath)
        except Exception as e:
            # Fallback direto caso rename falhe em alguns SOs
            try:
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)
            except Exception as e2:
                print(f"[Grimorio Storage] Falha ao salvar: {e2}")

    # ==================== CONFIGURAÇÕES & TEMA ====================
    def obter_configuracoes(self) -> dict:
        if "configuracoes" not in self.data:
            self.data["configuracoes"] = get_default_data()["configuracoes"]
            self.salvar()
        return self.data["configuracoes"]

    def atualizar_configuracoes(self, nome_rainha: str, tema_atual: str, nomes_abas: dict = None):
        cfg = self.obter_configuracoes()
        if nome_rainha is not None:
            cfg["nome_rainha"] = nome_rainha.strip()
            self.data["reino"]["nome_rainha"] = nome_rainha.strip()
        if tema_atual is not None:
            cfg["tema_atual"] = tema_atual
        if nomes_abas:
            cfg["nomes_abas"].update(nomes_abas)
        self.salvar()

    def salvar_configuracoes(self, nome_rainha: str = None, tema_atual: str = None, nomes_abas: dict = None):
        cfg = self.obter_configuracoes()
        if nome_rainha is not None:
            cfg["nome_rainha"] = str(nome_rainha).strip()
            self.data["reino"]["nome_rainha"] = str(nome_rainha).strip()
        if tema_atual is not None:
            cfg["tema_atual"] = tema_atual
        if nomes_abas:
            cfg["nomes_abas"].update(nomes_abas)
        self.salvar()

    # ==================== FECHAMENTO MENSAL DO COFRE ====================
    def verificar_fechamento_mensal(self):
        """
        Executa a lenda do Fechamento Mensal no primeiro dia útil do novo mês:
        - Saldo positivo vira Reserva do Reino (poupança mágica)
        - Saldo negativo vira Dívida da Coroa
        - Saldo do mês corrente é zerado para o novo ciclo
        """
        mes_atual = datetime.now().strftime("%Y-%m")
        ultimo_mes = self.data.get("ultimo_mes_processado", mes_atual)
        
        if ultimo_mes != mes_atual:
            self.executar_fechamento_mensal(ultimo_mes, mes_atual)

    def executar_fechamento_mensal(self, mes_antigo: str, mes_novo: str):
        cofre = self.data.get("cofre", {})
        txs = cofre.get("transacoes", [])
        
        txs_antigas = [t for t in txs if t.get("mes_ano") == mes_antigo or t.get("data", "").startswith(mes_antigo)]
        
        entradas = sum(t["valor"] for t in txs_antigas if t.get("tipo") == "entrada")
        saidas = sum(t["valor"] for t in txs_antigas if t.get("tipo") == "saida")
        saldo_antigo = entradas - saidas
        
        reserva_atual = cofre.get("reserva_do_reino", 0.0)
        divida_atual = cofre.get("divida_da_coroa", 0.0)
        
        if saldo_antigo > 0:
            cofre["reserva_do_reino"] = round(reserva_atual + saldo_antigo, 2)
            self.adicionar_ouro(saldo_antigo * 0.1)
        elif saldo_antigo < 0:
            cofre["divida_da_coroa"] = round(divida_atual + abs(saldo_antigo), 2)
            
        if "historico_fechamentos" not in cofre:
            cofre["historico_fechamentos"] = {}
            
        cofre["historico_fechamentos"][mes_antigo] = {
            "entradas": entradas,
            "saidas": saidas,
            "saldo_final": saldo_antigo,
            "data_fechamento": datetime.now().isoformat()
        }
        
        self.data["ultimo_mes_processado"] = mes_novo
        self.salvar()

    # ==================== REINO & LEVEL-UP ====================
    def adicionar_exp(self, qtd: int) -> bool:
        reino = self.data["reino"]
        reino["exp_atual"] += qtd
        subiu = False
        while reino["exp_atual"] >= reino["exp_proximo"]:
            reino["exp_atual"] -= reino["exp_proximo"]
            reino["nivel"] += 1
            reino["exp_proximo"] = int(reino["exp_proximo"] * 1.45)
            idx = min(reino["nivel"] - 1, len(self.TITULOS_NIVEL) - 1)
            reino["titulo_nivel"] = self.TITULOS_NIVEL[idx]
            subiu = True
        self.salvar()
        return subiu

    def adicionar_ouro(self, qtd: float):
        self.data["reino"]["ouro_tesouro"] = round(self.data["reino"]["ouro_tesouro"] + qtd, 2)
        self.salvar()

    # ==================== PET & MASCOTE ====================
    def alimentar_pet(self) -> dict:
        pet = self.data["pet"]
        pet["fome"] = min(100, pet.get("fome", 50) + 20)
        pet["nivel_afeto"] = min(100, pet.get("nivel_afeto", 50) + 10)
        pet["ultimo_cuidado"] = date.today().isoformat()
        self.adicionar_exp(10)
        self.salvar()
        return pet

    def brincar_pet(self) -> dict:
        pet = self.data["pet"]
        pet["energia"] = max(0, pet.get("energia", 50) - 15)
        pet["nivel_afeto"] = min(100, pet.get("nivel_afeto", 50) + 15)
        pet["humor"] = "Valente e Feliz"
        pet["ultimo_cuidado"] = date.today().isoformat()
        self.adicionar_exp(15)
        self.salvar()
        return pet

    def curar_pet(self) -> dict:
        pet = self.data["pet"]
        pet["energia"] = 100
        pet["fome"] = 100
        pet["ultimo_cuidado"] = date.today().isoformat()
        self.salvar()
        return pet

    # ==================== QUESTS ====================
    def obter_quests_por_data(self, data_iso: str) -> list:
        return [q for q in self.data["quests"] if q.get("data_limite") == data_iso]

    def alternar_conclusao_quest(self, quest_id: str) -> dict:
        for q in self.data["quests"]:
            if q["id"] == quest_id:
                q["concluida"] = not q.get("concluida", False)
                if q["concluida"]:
                    q["data_conclusao"] = date.today().isoformat()
                    self.adicionar_ouro(q.get("recompensa_ouro", 10.0))
                    self.adicionar_exp(q.get("recompensa_exp", 25))
                else:
                    q["data_conclusao"] = None
                self.salvar()
                return q
        return None

    def toggle_quest_concluida(self, quest_id: str) -> dict:
        return self.alternar_conclusao_quest(quest_id)

    def adicionar_quest(self, titulo: str, categoria: str, dificuldade: str, data_limite: str, horario: str = None):
        valores = {
            "Fácil": (15.0, 20),
            "Média": (30.0, 40),
            "Difícil": (50.0, 70),
            "Lendária": (100.0, 150)
        }
        ouro, exp = valores.get(dificuldade, (20.0, 30))
        
        nova = {
            "id": str(uuid.uuid4()),
            "titulo": titulo.strip(),
            "categoria": categoria,
            "dificuldade": dificuldade,
            "recompensa_ouro": ouro,
            "recompensa_exp": exp,
            "data_limite": data_limite,
            "horario": horario.strip() if horario else None,
            "concluida": False,
            "data_conclusao": None
        }
        self.data["quests"].append(nova)
        self.salvar()
        return nova

    def remover_quest(self, quest_id: str):
        self.data["quests"] = [q for q in self.data["quests"] if q["id"] != quest_id]
        self.salvar()

    # ==================== COFRE & TRANSAÇÕES ====================
    def obter_teto_gastos(self) -> float:
        return self.data["cofre"].get("teto_gastos_mes", 3000.0)

    def definir_teto_gastos(self, novo_teto: float):
        self.data["cofre"]["teto_gastos_mes"] = max(0.0, float(novo_teto))
        self.salvar()

    def atualizar_teto_gastos(self, novo_teto: float):
        self.definir_teto_gastos(novo_teto)

    def obter_reserva_reino(self) -> float:
        return self.data["cofre"].get("reserva_do_reino", 1200.0)

    def definir_reserva_reino(self, nova_reserva: float):
        self.data["cofre"]["reserva_do_reino"] = max(0.0, float(nova_reserva))
        self.salvar()

    def atualizar_reserva_guardada(self, nova_reserva: float):
        self.definir_reserva_reino(nova_reserva)

    def obter_transacoes_mes(self, mes_ano: str = None) -> list:
        if not mes_ano:
            mes_ano = datetime.now().strftime("%Y-%m")
        return [t for t in self.data["cofre"]["transacoes"] if t.get("mes_ano") == mes_ano or t.get("data", "").startswith(mes_ano)]

    def adicionar_transacao(self, tipo: str, titulo: str, valor: float, categoria: str, data_str: str = None) -> dict:
        if not data_str:
            data_str = date.today().isoformat()
        mes_ano = data_str[:7]
        
        nova = {
            "id": str(uuid.uuid4()),
            "tipo": tipo,
            "titulo": titulo.strip(),
            "valor": round(float(valor), 2),
            "categoria": categoria,
            "data": data_str,
            "mes_ano": mes_ano
        }
        self.data["cofre"]["transacoes"].insert(0, nova)
        
        if tipo == "entrada":
            self.adicionar_ouro(float(valor))
        elif tipo == "saida":
            self.adicionar_ouro(-float(valor))
            
        self.salvar()
        return nova

    def remover_transacao(self, transacao_id: str):
        self.data["cofre"]["transacoes"] = [t for t in self.data["cofre"]["transacoes"] if t["id"] != transacao_id]
        self.salvar()

    def calcular_resumo_mes(self, mes_ano: str = None) -> dict:
        if not mes_ano:
            mes_ano = datetime.now().strftime("%Y-%m")
            
        txs = self.data["cofre"]["transacoes"]
        txs_mes = [t for t in txs if t.get("mes_ano") == mes_ano or t.get("data", "").startswith(mes_ano)]
        
        entradas = sum(t["valor"] for t in txs_mes if t["tipo"] == "entrada")
        saidas = sum(t["valor"] for t in txs_mes if t["tipo"] == "saida")
        saldo = entradas - saidas
        
        teto = self.obter_teto_gastos()
        porcentagem_teto = (saidas / teto * 100) if teto > 0 else 0.0
        
        return {
            "mes_ano": mes_ano,
            "entradas": round(entradas, 2),
            "saidas": round(saidas, 2),
            "saldo": round(saldo, 2),
            "teto": round(teto, 2),
            "porcentagem_teto": round(porcentagem_teto, 1),
            "divida": round(self.data["cofre"].get("divida_da_coroa", 0.0), 2),
            "reserva": round(self.data["cofre"].get("reserva_do_reino", 0.0), 2),
            "transacoes": txs_mes
        }

    def calcular_gastos_por_categoria(self, mes_ano: str = None) -> dict:
        if not mes_ano:
            mes_ano = datetime.now().strftime("%Y-%m")
            
        txs = self.data["cofre"]["transacoes"]
        saidas_mes = [t for t in txs if t["tipo"] == "saida" and (t.get("mes_ano") == mes_ano or t.get("data", "").startswith(mes_ano))]
        
        total_saidas = sum(t["valor"] for t in saidas_mes)
        categorias_map = {}
        for t in saidas_mes:
            cat = t.get("categoria", "Outros")
            categorias_map[cat] = categorias_map.get(cat, 0.0) + t["valor"]
            
        categorias_ordenadas = []
        for cat, val in sorted(categorias_map.items(), key=lambda x: x[1], reverse=True):
            pct = (val / total_saidas * 100) if total_saidas > 0 else 0.0
            categorias_ordenadas.append({
                "categoria": cat,
                "valor": round(val, 2),
                "porcentagem": round(pct, 1)
            })
            
        return {
            "total_saidas": round(total_saidas, 2),
            "categorias": categorias_ordenadas
        }

    def calcular_saude_financeira(self, mes_ano: str = None) -> dict:
        resumo = self.calcular_resumo_mes(mes_ano)
        entradas = resumo["entradas"]
        saidas = resumo["saidas"]
        
        if saidas == 0:
            status = "Sustentável"
            cor = "#10B981"
            descricao = "O tesouro está intacto e protegido. Nenhuma despesa comprometeu as arcas reais este mês."
        elif entradas == 0 and saidas > 0:
            status = "Crítico / Déficit"
            cor = "#EF4444"
            descricao = "Alerta máximo: há despesas registradas sem nenhuma entrada de tributos neste ciclo!"
        else:
            taxa = saidas / entradas
            if taxa <= 0.75:
                status = "Sustentável"
                cor = "#10B981"
                descricao = f"Finanças exemplares! O reino preserva {((1 - taxa) * 100):.0f}% das riquezas arrecadadas."
            elif taxa <= 1.0:
                status = "Alerta da Coroa"
                cor = "#F59E0B"
                descricao = f"Atenção necessária: {taxa * 100:.0f}% dos tributos estão comprometidos com custos da corte."
            else:
                status = "Crítico / Déficit"
                cor = "#EF4444"
                descricao = f"Déficit ativo: os gastos excedem as receitas em {(saidas - entradas):.2f} Ouros!"
                
        return {
            "status": status,
            "cor": cor,
            "descricao": descricao,
            "saldo_atual": resumo["saldo"]
        }

    def calcular_projecao(self) -> dict:
        txs = self.data["cofre"]["transacoes"]
        hoje = date.today()
        limite_passado = hoje - timedelta(days=60)
        recentes = []
        for t in txs:
            try:
                t_date = datetime.strptime(t["data"], "%Y-%m-%d").date()
                if t_date >= limite_passado:
                    recentes.append(t)
            except Exception:
                continue
                
        entradas_rec = sum(t["valor"] for t in recentes if t["tipo"] == "entrada")
        saidas_rec = sum(t["valor"] for t in recentes if t["tipo"] == "saida")
        dias_base = max(1, (hoje - limite_passado).days)
        
        media_diaria_entradas = entradas_rec / dias_base
        media_diaria_saidas = saidas_rec / dias_base
        saldo_diario = media_diaria_entradas - media_diaria_saidas
        
        saldo_atual_mes = self.calcular_resumo_mes()["saldo"]
        reserva_reino = self.data["cofre"].get("reserva_do_reino", 0.0)
        base_acumulada = saldo_atual_mes + reserva_reino
        
        saldo_30d = base_acumulada + (saldo_diario * 30)
        saldo_60d = base_acumulada + (saldo_diario * 60)
        saldo_90d = base_acumulada + (saldo_diario * 90)
        
        if saldo_90d >= base_acumulada * 1.25 and saldo_diario > 0:
            status = "prospero"
            msg_rei = (
                f"Minha Rainha, as estrelas favorecem nosso reinado! Se o ritmo de tributos se mantiver firme, "
                f"nossa reserva alcançará {saldo_90d:,.0f} Ouros em 90 dias. Teu governo é sinônimo de prosperidade."
            )
        elif saldo_90d >= 0 and saldo_diario >= 0:
            status = "sustentavel"
            msg_rei = (
                f"Se o ritmo de gastos se mantiver equilibrado, a reserva alcançará {saldo_60d:,.0f} Ouros em 60 dias "
                f"e {saldo_90d:,.0f} Ouros em 90 dias. Tua prudência resguarda o castelo com serenidade."
            )
        elif saldo_90d >= 0 and saldo_diario < 0:
            status = "alerta"
            msg_rei = (
                f"Atenção da Coroa, Rainha: embora ainda haja reserva, o ritmo diário consome mais do que arrecadamos. "
                f"Em 90 dias nosso tesouro diminuirá para {saldo_90d:,.0f} Ouros. Recomendo conter despesas secundárias."
            )
        else:
            status = "risco_deficit"
            deficit_previsto = abs(saldo_90d)
            msg_rei = (
                f"Alerta Real Urgente: Se mantivermos este padrão de despesas, o reino enfrentará um déficit projetado "
                f"de {deficit_previsto:,.0f} Ouros em 90 dias. É tempo de convocar austeridade orçamentária."
            )
            
        return {
            "media_diaria_entradas": round(media_diaria_entradas, 2),
            "media_diaria_saidas": round(media_diaria_saidas, 2),
            "saldo_diario": round(saldo_diario, 2),
            "projecao_30d": round(saldo_30d, 2),
            "projecao_60d": round(saldo_60d, 2),
            "projecao_90d": round(saldo_90d, 2),
            "status": status,
            "mensagem_rei": msg_rei
        }

    # ==================== FORJA & HÁBITOS ====================
    def alternar_habito_hoje(self, habito_id: str) -> dict:
        hoje_str = date.today().isoformat()
        for h in self.data["forja"]["habitos"]:
            if h["id"] == habito_id:
                datas = set(h.get("datas_concluidas", []))
                if hoje_str in datas:
                    datas.remove(hoje_str)
                    h["concluido_hoje"] = False
                    h["streak_atual"] = max(0, h.get("streak_atual", 1) - 1)
                else:
                    datas.add(hoje_str)
                    h["concluido_hoje"] = True
                    h["streak_atual"] = h.get("streak_atual", 0) + 1
                    if h["streak_atual"] > h.get("melhor_streak", 0):
                        h["melhor_streak"] = h["streak_atual"]
                    self.adicionar_exp(12)
                    self.adicionar_ouro(5.0)
                    
                h["datas_concluidas"] = sorted(list(datas))
                self.salvar()
                return h
        return None

    def adicionar_habito(self, nome: str, tipo: str):
        novo = {
            "id": str(uuid.uuid4()),
            "nome": nome.strip(),
            "tipo": tipo,
            "streak_atual": 0,
            "melhor_streak": 0,
            "concluido_hoje": False,
            "datas_concluidas": []
        }
        self.data["forja"]["habitos"].append(novo)
        self.salvar()
        return novo

    def remover_habito(self, habito_id: str):
        self.data["forja"]["habitos"] = [h for h in self.data["forja"]["habitos"] if h["id"] != habito_id]
        self.salvar()

    # ==================== FOCO & POMODORO ====================
    def registrar_foco_concluido(self, minutos: int):
        foco = self.data.setdefault("foco", {
            "minutos_foco": 25,
            "minutos_descanso": 5,
            "total_pomodoros": 0,
            "tempo_total_minutos": 0
        })
        foco["total_pomodoros"] = foco.get("total_pomodoros", 0) + 1
        foco["tempo_total_minutos"] = foco.get("tempo_total_minutos", 0) + int(minutos)
        self.adicionar_exp(25)
        self.adicionar_ouro(10.0)
        self.salvar()

    # ==================== TRONO & EMOCIONAL ====================
    def registrar_emocional(self, humor: str, desabafo: str, resposta_rei: str):
        hoje_str = date.today().isoformat()
        reg = {
            "data": hoje_str,
            "humor": humor,
            "desabafo": desabafo.strip(),
            "resposta_rei": resposta_rei
        }
        self.data["emocional"]["historico"].insert(0, reg)
        self.adicionar_exp(15)
        self.salvar()
        return reg

    def salvar_runa(self, runa: dict):
        runa["data"] = date.today().isoformat()
        self.data["emocional"]["ultima_runa"] = runa
        self.salvar()


# Instância Global de Armazenamento
storage = GrimorioStorage()
