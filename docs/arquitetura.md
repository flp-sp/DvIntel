# Agente
## Loop
1. User input
2. Message = Input + Memory(compactada)
3. Call tool
4. Executa tool
> Volta para o 2 a menos que haja `erro da api` ou `excedeu 5 loops` ou `response tool_calls vazio`

## Tools
- Read Project
- Read File
- Change File
- Run Wishlisted commands (run project, ls, read, create file | Apenas no diretório em que o projeto for executado)

## Memory
A memória vai ser armazenada em um `jsonl` e vai armazenar:
- prompt do usuário
- decisão do agente + tool e argumentos
- resultado de todas as tools
- resposta final
- uso de tokens

Ao ser chamada ao loop, será compactada aparecendo apenas o que for mais importante