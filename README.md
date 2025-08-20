# Owlficina SSI 2025: Criando Bots no Telegram💬

Esta oficina foi desenvolvida para apresentar, de forma prática e acessível, como criar e programar bots no Telegram usando Python.  
Ao final, os participantes terão experimentado a criação de seus próprios bots e entenderão os fundamentos para expandir e personalizar suas ideias.

---

## Por que bots no Telegram?
Bots no Telegram são programas que interagem automaticamente em conversas.  
Com eles, é possível:
- Criar assistentes pessoais.  
- Automatizar tarefas.  
- Fazer integração com APIs externas.  
- Criar jogos ou quizzes dentro do chat.  

Durante a oficina, vamos montar alguns bots simples e colocá-los diretamente no grupo da oficina para que todos possam experimentar!

---

## Roteiro da Oficina

⏰ **Duração total: 1h**

### **15 min — Introdução**
- Por que aprender a criar bots?  
- Exemplos de coisas que podem ser feitas.  
- Teste de alguns bots dentro do grupo da oficina.  

### **30 min — Mão na massa**
- Criação do bot no **BotFather** (nome, descrição, foto e token).  
- Explicação da biblioteca [`python-telegram-bot`](https://docs.python-telegram-bot.org/).  
- Como a biblioteca interage com a API do Telegram e por que é o caminho mais simples.  
- Imports básicos e primeiras funções em Python.  
- Construindo juntos o primeiro bot funcional.  

### **15 min — Prática guiada**
- Participantes personalizam seus bots.  
- Espaço aberto para dúvidas e experimentação.  

---

## Estrutura básica do projeto

- **base_bot.py** → Arquivo principal do bot em Python.   

---

## Funções básicas ensinadas

- **/start** → Mensagem de boas-vindas.  
- **/help** → Lista de comandos disponíveis.  
- **Comandos customizados** → Criados durante a oficina.  

Exemplo de função inicial em Python:

```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou seu primeiro bot no Telegram"
    )
