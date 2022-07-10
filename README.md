# encrypted-chat

## Como rodar?
Executar "main.py"

## Como utilizar?
Temos o seguinte layout:

![image](https://user-images.githubusercontent.com/80294295/178164293-5f084398-948f-4588-84cf-95e2daa3f098.png)

- Caso o campo status esteja offline, clique em "Hostear"
- Informe ao seu parceiro o IP que aparece em "Meu IP:"
- Selecione o método de criptografia e a chave.
- Informe a mensagem e clique em "Enviar".

### Diffie-Hellman
- Para utilizar a troca de chaves por Diffie-Hellman, faça todos os passos acima, porém deixe o campo "Chave:" em branco, ele será completado automaticamente.
- Informe um número primo P, uma raiz primitiva G de P, e a chave privada de sua escolha, desde que seja um inteiro menor que P.
- Feito o passo acima, o campo "Sua chave pública" será gerado automaticamente. Passe esse valor para o computador que deseja se conectar.
- Informe a chave pública de seu parceiro em "Chave pública de seu parceiro".
- Feito isso o campo "Chave" será gerado automaticamente, basta digitar a mensagem e enviar.
