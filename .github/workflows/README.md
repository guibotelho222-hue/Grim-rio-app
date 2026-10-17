# Grimório Mobile - Versão 2.0.0 (Android) 📱👑

Projeto mobile oficial do **Grimório: Dark Fantasy & Gestão do Reino**, preparado e otimizado exclusivamente para geração de **Build APK** no Android via **Flet**.

---

## 🏰 Estrutura do Projeto

```text
GrimorioMobile/
├── assets/                       # Ícones, imagens e efeitos sonoros
│   ├── logo.png                  # Ícone oficial do app Android
│   ├── logo.ico                  # Ícone fallback
│   ├── mascote.png               # Imagem oficial de Sir Fagulha
│   ├── rei_joaquim_trono.png     # Ilustração oficial do Rei Joaquim
│   ├── som_foco.mp3              # Som do Pomodoro
│   └── som_alerta.mp3            # Som de notificação
├── components/                   # Componentes visuais reutilizáveis
│   ├── __init__.py
│   ├── common_ui.py              # Header fixo mobile, modais e botões táteis
│   └── mascote_vector.py         # Card e renderização vetorial do mascote
├── tabs/                         # Abas adaptadas para Mobile Portrait
│   ├── __init__.py
│   ├── tab_trono.py              # Sala do Trono (Rei Joaquim & Pet)
│   ├── tab_quests.py             # Calendário & Missões
│   ├── tab_cofre.py              # Finanças, Teto de Gastos & Projeção
│   ├── tab_forja.py              # Hábitos (HP/Mana/Ouro) & Níveis
│   ├── tab_foco.py               # Poção Pomodoro Alquímica
│   └── oraculo_tab.py            # Suporte ao módulo de Oráculo
├── grimorio_mobile_dados.json    # Base de dados seed inicial em UTF-8
├── main.py                       # Ponto de entrada do aplicativo Flet Mobile
├── oracle.py                     # Falas acolhedoras do Rei e Runas
├── pyproject.toml                # Configuração oficial Flet Build v2.0.0
├── splash_screen.py              # Splash screen responsiva com toque para entrar
├── storage.py                    # Persistência síncrona segura para Android
├── theme.py                      # Paletas dinâmicas, fase da lua e áudio mobile
└── README.md
```

---

## 🚀 Como Testar Localmente no Computador

No terminal, dentro da pasta `GrimorioMobile`:

```bash
# Instalar dependências se necessário:
pip install flet pillow

# Executar a aplicação (abrirá em formato vertical de celular):
python main.py
```

---

## 📦 Como Gerar o Build APK com o Flet

### 1. Requisitos para Build Local (ou via CI/GitHub Actions):
- Python 3.9+
- Flet instalado (`pip install flet`)
- Flutter SDK & Android SDK instalados e configurados no PATH

### 2. Comando de Build APK:
Na raiz da pasta `GrimorioMobile`, execute:

```bash
flet build apk --project "grimorio"
```

Ou para gerar o pacote otimizado para a Google Play Store (AAB):
```bash
flet build aab --project "grimorio"
```

O arquivo gerado ficará em:
`build/apk/app-release.apk`

---

## 🔒 Configurações Específicas do Android (pyproject.toml)

- **App Name**: `grimorio`
- **Versão**: `2.0.0` (Evita conflito com cache da v1 no dispositivo)
- **Package ID**: `com.grimorio.app`
- **Ícone**: `assets/logo.png`
- **Cor da Splash**: `#121214` (Dark Fantasy)
- **Armazenamento Seguro**: Implementado em `storage.py` com detecção de diretório gravável interno do Android (`FLET_APP_STORAGE_DATA`).
