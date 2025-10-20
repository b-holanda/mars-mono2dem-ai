# Metodologia

1. Iniciar com o donload dos 100 primeiros pares isponibilizados diretamente do repositório oficial da HiRISE
2. Realizar as normalizações nescessárias dos 10 primeiros pares para utilizar a ferramenta ASP
3. Gerar DEMs utilizando a ferramenta ASP a partir dos 10 primeiros pares e medir: (RMSE, Tempo de Execução, Uso médio de cpu, uso médio de memória) por par processado
4. Realizar as normalizações nescessáras dos 10 primeiros pares para o treinamento do Vision Transformer (ViT)
5. Realizar o treinamento do ViT com 80% do dataset utilizando validação cruzada
6. Testar modelo ViT gerado com os 20% restante do dataset e medir (RMSE, Tempo de Execução, Uso médio de cpu, uso médio de memória) e analizar curvas de regressão
7. Realizar novamente os procedimentos para 20, 30, 40, 50, 60, 70, 80, 90 e 100 pares e analizar a curva de regressão


Conversores .JP2/.IMG → GeoTIFF, alinhamento, máscaras.

 Gerador de patches + splits geográficos + augmentations.

 Implementar ViT-DPT (PyTorch) + losses (SILog, BerHu, Grad, opcional SSIM-Hillshade).

 Treinador com AMP, cosine, warmup, early stopping, W&B.

 Métricas de val/test (altura + morfometria + espectro).

 Baselines (MOLA upscale, ResNet-FPN).

 Incerteza (ensembles/MC-Dropout) e relatório de calibração.

 Pós-processo + export GeoTIFF (scripts infer_scene.py, stitch_tiles.py).

 Tabelas e mapas de erro (hillshade overlay) para o paper/relatório.