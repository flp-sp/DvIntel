# Agente de IA - DvIntel
Esse projeto tem como finalidade aprimorar conhecimentos no funcionamento de agentes de IA.

Embora tenham sido feitas alterações durante o desenvolvimento, o funcionamento do agente está explicado [aqui](docs/arquitetura.md).

> [!WARNING]  
> Esse agente de IA foi desenvolvido com finalidade academica, não é recomendável usá-lo para projetos reais ou utilizar sem um certo nível de virtualização ou jaula.

## Modelo
O projeto utilizará a API do `groq` como motor principal usando o modelo `openai/gpt-oss-20b`, podendo ser alterado futuramente a depender do desempenho do modelo.

## Stack
- Python
- pytermGUI
- groq

## NoAI
Foi decidido que esse projeto não utilizará código gerado por IA, ferramentas de IA como LLMs e agentes poderão ser usados para revisão e testes.