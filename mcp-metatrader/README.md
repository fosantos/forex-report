# MCP MetaTrader 5 (global)

Servidor MCP que entrega o terminal **MetaTrader 5** ao Muse: cotações ao vivo,
histórico OHLC, posições abertas, histórico de negócios e — opcionalmente —
envio de ordens. Instalado como **global** (`muse mcp add --user`), vale para
todos os projetos.

## Arquitetura

```
Muse (aqui, WSL/Linux) --stdio--> server.py --HTTP+token--> mt5_bridge.py --MetaTrader5--> terminal64.exe (Windows)
```

- [`server.py`](server.py) — servidor MCP stdio. Roda no mesmo ambiente do Muse.
- [`mt5_bridge.py`](mt5_bridge.py) — bridge HTTP que roda **no Windows**, ao lado do
  terminal (o pacote `MetaTrader5` só funciona no Windows com o terminal aberto).
  Só usa stdlib + `MetaTrader5`.

## Pré-requisitos (Windows)

1. Terminal MT5 instalado e logado pelo menos uma vez (ideal: conta demo).
   Não precisa estar aberto: a bridge lança o `terminal64.exe` sozinha
   quando ele não está rodando.
2. Python 3.10+ **do Windows** (python.org — o atalho da Microsoft Store não serve):
   `py -3 --version`
3. `py -3 -m pip install MetaTrader5`
4. Copie `mt5_bridge.py` para o Windows (ou rode direto de `C:\Projetos\forex-report\mcp-metatrader\`).

## Subindo a bridge (Windows)

```bat
set MT5_BRIDGE_TOKEN=<o segredo gerado na instalação — ver .bridge_token>
set MT5_ENABLE_TRADING=1   :: só se quiser ordens; omita para somente-leitura
py -3 mt5_bridge.py --host 0.0.0.0 --port 8765
```

- `--host 0.0.0.0` é necessário para o WSL alcançar a bridge. O token é obrigatório.
- Sem `MT5_ENABLE_TRADING=1` nos **dois lados**, as ferramentas de trading recusam.

### Abertura automática do terminal

Quando `initialize()` falha e não há `terminal64.exe` rodando (checado via
`tasklist`), a bridge abre o terminal sozinha e aguarda até
`MT5_TERMINAL_TIMEOUT` segundos (padrão: 60) pela conexão. O terminal
continua rodando mesmo se a bridge for encerrada.

| Variável | Padrão | Efeito |
|---|---|---|
| `MT5_TERMINAL_PATH` | `C:\Program Files\MetaTrader 5\terminal64.exe` | Caminho do executável (use se o MT5 está em outra pasta; instalações `MetaTrader*` vizinhas também são procuradas) |
| `MT5_TERMINAL_TIMEOUT` | `60` | Segundos de espera após abrir o terminal |
| `MT5_NO_AUTOLAUNCH=1` | desligado | Desativa a abertura automática (falha rápido como antes) |

Descubra o IP do Windows a partir do WSL:

```bash
grep nameserver /etc/resolv.conf   # use esse IP no MT5_BRIDGE_URL abaixo
```

## Registro no Muse (global)

Instalação padrão (somente leitura; troque o IP pelo do passo acima):

```bash
muse mcp add metatrader --user \
  -e MT5_BRIDGE_URL=http://10.255.255.254:8765 \
  -e MT5_BRIDGE_TOKEN=<segredo> \
  -e MT5_ENABLE_TRADING=0 \
  -- /mnt/c/Projetos/forex-report/mcp-metatrader/.venv/bin/python \
     /mnt/c/Projetos/forex-report/mcp-metatrader/server.py
```

> Registrado exatamente assim (global, somente leitura). Se o IP do host mudar
> (ex.: reinício do WSL), refaça com `muse mcp remove metatrader --user` + `add`
> com o novo IP do `grep nameserver /etc/resolv.conf`.

Para mover a pasta depois: `muse mcp remove metatrader --user` e repita o `add`
com os novos caminhos. Para ativar trading: troque `MT5_ENABLE_TRADING` para `1`
(servidor **e** bridge) e reinicie a sessão.

Verificação:

```bash
muse mcp get metatrader
```

## Ferramentas

| Ferramenta | Trading? | O que faz |
|---|---|---|
| `mt5_status` | não | Conexão, conta, saldo, equity, margem |
| `mt5_quote` | não | Tick ao vivo (bid/ask/hora/spread) |
| `mt5_rates` | não | Histórico OHLC (M1–MN1, até 5000 barras) |
| `mt5_symbols` | não | Lista/filtra símbolos negociáveis |
| `mt5_positions` | não | Posições abertas (ticket, volume, SL/TP, lucro) |
| `mt5_deals` | não | Negócios fechados por período |
| `mt5_order` | **sim** | Ordem a mercado/limit/stop, com SL/TP |
| `mt5_close_position` | **sim** | Fecha posição a mercado |
| `mt5_modify_position` | **sim** | Move SL/TP de posição aberta |

## Segurança

- A bridge **não sobe sem token** e compara com `hmac.compare_digest`.
- Trading exige `MT5_ENABLE_TRADING=1` no servidor MCP **e** na bridge.
- Nunca commite `.bridge_token` (já está no `.gitignore`).
- Comece numa **conta demo**. Ordens enviadas pelo agente são reais.

## Testes

Bateria com terminal simulado (stub `MetaTrader5` em `/tmp`, nada de rede real):

```bash
python3 /tmp/mcp_run_tests.py   # bridge direta + cliente MCP stdio, trading off/on
```

Esperado: todos `PASS`, `FAILURES: none`, `TESTS-DONE`.
