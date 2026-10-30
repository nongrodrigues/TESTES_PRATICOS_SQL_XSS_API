# Respostas — Quiz e Exercícios

## Quiz

1. Porque permite que o usuário envie caracteres especiais (como aspas simples e comentários) que alteram a sintaxe e a lógica do interpretador SQL, executando instruções arbitrárias.
2. Utilizar Consultas Parametrizadas (Prepared Statements), nas quais os dados do usuário são enviados separadamente e tratados exclusivamente como valores literais pelo banco de dados.
3. No XSS Armazenado, o script malicioso é persistido no banco de dados e afeta qualquer usuário que visualize aquele registro posteriormente; no XSS Refletido, o payload viaja na requisição atual e é devolvido imediatamente na resposta do servidor.
4. Status HTTP 401 Unauthorized rejeitando categoricamente o login.

## Exercício 1 — SQL Injection via UNION SELECT

**Payload ofensivo:**

```sql
%' UNION SELECT id, email, senha FROM usuarios --