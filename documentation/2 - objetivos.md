# Geral

Desenvolver um modelo de IA generativa baseado em Vision Transformer (ViT) que, treinado com pares de imagens HiRISE e seus DEMs correspondentes (gerados pelo ASP), possa inferir DEMs de alta resolução com qualidade comparável, mas com inferência muito mais rápida.

# Específicos

- Obter DEMs com erro altimétrico comparável ao método ASP em regiões de teste.
- Reduzir tempo de processamento para inferência direta (segundos a poucos minutos), contra horas/dias dos métodos clássicos.
- Tornar possível gerar ou preencher relevo mesmo em áreas sem pares estéreo ideais.
- Facilitar produção em larga escala de mosaicos de alta resolução com menor custo computacional.