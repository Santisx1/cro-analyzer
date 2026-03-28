# 🤖 Automação do CRO Scheduler

Guia completo para configurar análises automáticas de CRO sem intervenção manual.

## ⚡ Início Rápido (Recomendado)

Se quiser deixar rodando agora e não se preocupar mais:

```bash
cd "/Users/kaiofernandes/Desktop/Análise de CRO"
chmod +x setup_launchd.sh
./setup_launchd.sh
```

Escolha opção **1** e pronto! Seu Mac rodará análises automaticamente às 2 AM todo dia.

---

## 📋 Opções de Automação

### Opção 1: LaunchD (RECOMENDADO - Melhor para Mac)

**Vantagens:**
- ✅ Integrado ao macOS (nativo)
- ✅ Continua rodando mesmo se fechar o terminal
- ✅ Roda mesmo que o Mac acorde da suspensão
- ✅ Sem necessidade de manter terminal aberto

**Como instalar:**

```bash
chmod +x setup_launchd.sh
./setup_launchd.sh
```

Escolha opção `1` no menu.

**Ver status:**
```bash
launchctl list | grep cro
```

**Forçar execução agora (testes):**
```bash
launchctl start com.cro.analyzer.scheduler
```

**Ver logs:**
```bash
tail -f launchd.log           # Output
tail -f launchd_error.log     # Erros
```

**Desinstalar:**
```bash
./setup_launchd.sh
```

Escolha opção `2`.

---

### Opção 2: Script de Background (Alternativa Rápida)

**Vantagens:**
- ✅ Simples de usar
- ✅ Sem configuração extra
- ⚠️ Precisa rodar script manualmente

**Como usar:**

```bash
chmod +x run_scheduler.sh
./run_scheduler.sh
```

Menu interativo para escolher:
1. **Diário às 2 AM** (recomendado)
2. **A cada hora** (para testes)
3. **Semanalmente**
4. **Rodar uma vez**

**Monitorar em tempo real:**
```bash
tail -f scheduler.log
```

**Parar quando quiser:**
```bash
./run_scheduler.sh stop
```

---

### Opção 3: Cron Job (Avançado)

Se preferir usar `crontab` tradicional:

```bash
crontab -e
```

E adicione:

```bash
# Rodar análise de CRO diariamente às 2 AM
0 2 * * * cd "/Users/kaiofernandes/Desktop/Análise de CRO" && ./venv/bin/python3 scheduler.py --run >> scheduler.log 2>&1
```

**Salvar:** `Ctrl+X`, depois `Y`, depois Enter

---

## 🔧 Configuração Avançada

### Alterar horário de execução

**LaunchD:**

Editar `com.cro.analyzer.scheduler.plist`:

```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Hour</key>
        <integer>3</integer>        <!-- Alterar para hora desejada (0-23) -->
        <key>Minute</key>
        <integer>30</integer>       <!-- Alterar para minuto desejado (0-59) -->
    </dict>
</array>
```

Depois recarregar:
```bash
launchctl unload ~/Library/LaunchAgents/com.cro.analyzer.scheduler.plist
launchctl load ~/Library/LaunchAgents/com.cro.analyzer.scheduler.plist
```

**Script de Background:**

```bash
./run_scheduler.sh   # Escolher novo horário
```

---

### Variáveis de Ambiente

Se precisar usar credenciais (Supabase, GA4), criar arquivo `.env`:

```bash
# Supabase
SUPABASE_URL=sua_url_aqui
SUPABASE_ANON_KEY=sua_chave_aqui

# Google Analytics 4
GA4_PROPERTY_ID=seu_property_id
GA4_CREDENTIALS_PATH=/caminho/para/credentials.json

# Análise
MIN_ABANDONMENT_THRESHOLD=20
MIN_RECOMMENDATION_SCORE=0.5

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
NOTIFICATIONS_EMAIL=seu_email@gmail.com
```

---

## 📊 Saída Gerada

Cada execução automática gera:

```
reports_automated/
├── analysis_2024-01-15_02-00-00.html     # Relatório visual
├── analysis_2024-01-15_02-00-00.json     # Dados estruturados
├── analysis_2024-01-14_02-00-00.html
├── analysis_2024-01-14_02-00-00.json
└── ...
```

---

## 🐛 Troubleshooting

### LaunchD não executa

```bash
# Verificar se está carregado
launchctl list | grep cro

# Ver erros detalhados
log stream --predicate 'process == "launchd"' | grep cro

# Ver arquivo de erros
cat launchd_error.log
```

### Verificar Python está funcionando

```bash
/Users/kaiofernandes/Desktop/Análise\ de\ CRO/venv/bin/python3 -c "print('OK')"
```

### Script não encontra módulos

```bash
# Adicionar ao script (dentro do .sh antes de rodar python):
cd "/Users/kaiofernandes/Desktop/Análise de CRO"
source venv/bin/activate
```

### Permissões incorretas

```bash
chmod +x scheduler.py run_scheduler.sh setup_launchd.sh
chmod 644 com.cro.analyzer.scheduler.plist
```

---

## 📈 Monitoramento

### Ver todas as execuções

```bash
ls -lart reports_automated/ | tail -20
```

### Último relatório gerado

```bash
open reports_automated/$(ls -t reports_automated/ | grep .html | head -1)
```

### Verificar se rodou hoje

```bash
ls -1 reports_automated/ | grep $(date +%Y-%m-%d)
```

---

## 🛑 Como Pararal/ Reiniciar

### Parar LaunchD

```bash
launchctl unload ~/Library/LaunchAgents/com.cro.analyzer.scheduler.plist
```

### Parar script de background

```bash
./run_scheduler.sh stop
```

ou

```bash
pkill -f scheduler.py
```

### Reiniciar LaunchD

```bash
launchctl load ~/Library/LaunchAgents/com.cro.analyzer.scheduler.plist
```

---

## ✅ Checklist Pré-Automação

- [ ] Python venv configurado e ativado
- [ ] `pip install -r requirements.txt` executado
- [ ] `examples/sample_data.csv` existe ou GA4 está configurado
- [ ] `.env` configurado (se usar Supabase/GA4)
- [ ] Diretório `reports_automated/` criado (autom criado na primeira execução)
- [ ] Scripts `.sh` têm permissão de execução (`chmod +x`)

---

## 🎯 Próximos Passos

1. **Escolher método:** LaunchD (recomendado) ou script background
2. **Instalar:** `./setup_launchd.sh` ou `./run_scheduler.sh`
3. **Testar:** Forçar execução manual para confirmar
4. **Monitorar:** Verificar logs após primeira execução automática
5. **Dormir tranquilo:** Sistema roda sozinho todos os dias 🌙

---

## 📝 Notas

- **Tempo típico de execução:** 2-5 segundos
- **Consumo de recursos:** Mínimo (< 10% CPU)
- **Armazenamento:** ~50KB por relatório
- **Sem necessidade de intervenção:** Sistema totalmente autonomizado

---

**Perguntas?** Revisar logs ou executar manualmente:
```bash
./venv/bin/python3 scheduler.py --run
```
