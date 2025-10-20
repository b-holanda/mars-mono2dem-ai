# Contextualização

Os modelos digitais de elevação (DEMs) de Marte com alta resolução são fundamentais para o estudo da morfologia e geologia local em escalas menores (< 10 km) (Hepburn et al., 2019). Os DEMs de HiRISE (post spacing de 1-2 metros) são gerados via métodos estereofotogramétricos robustos, alinhados a altimetria laser (MOLA) para controle absoluto (USGS HiRISE DTM dataset).

A ferramenta NASA Ames Stereo Pipeline (ASP) é amplamente usada para esse tipo de processamento, empregando correlação estéreo, bundle adjustment e triangulação geométrica (Hepburn et al., 2019; Hepburn et al., 2019b). Apesar de gerar DEMs de qualidade elevada, o processo é computacionalmente intensivo e demanda etapas complexas de calibragem e ajustes finos.

# Problema / Lacuna

- O tempo de processamento de pares de alta resolução (HiRISE) por meio de ASP pode ser elevado, especialmente em escala de mosaicos grandes.
- A necessidade de múltiplos passos (pré-processamento, correlação, ajuste de feixes, registro) exige recursos computacionais expressivos e expertise técnica.
- Em regiões sem cobertura estéreo ideal, ou onde pares estejam escassos, os métodos tradicionais têm limitações de aplicabilidade.

Essas restrições podem dificultar a geração rápida de DEMs em larga escala ou em contextos operacionais restritos (por ex. missões futuras com hardware limitado).

# Proposta

Desenvolver um modelo de IA generativa baseado em Vision Transformer (ViT) que, treinado com pares de imagens HiRISE e seus DEMs correspondentes (gerados pelo ASP), possa inferir DEMs de alta resolução com qualidade comparável, mas com inferência muito mais rápida.

A ideia é que o modelo aprenda a mapear diretamente de textura/área de imagem para relevo, internalizando padrões de paralaxe, iluminação e variações geométricas complexas.

A escolha de ViT se justifica porque transformadores visuais demonstraram bom desempenho em tarefas de previsão densa (dense prediction) e estimativa de profundidade, aproveitando atenção global para capturar relações espaciais de longo alcance (Ranftl et al., 2021).

Modelos ViT foram adaptados para estimativa monocular de profundidade, combinando atenção global e decodificadores densos (por exemplo, “Vision Transformers for Dense Prediction”) obtendo ganhos de precisão frente a redes puramente convolucionais (Ranftl et al., 2021).

Além disso, arquiteturas modernas com atenção eficiente já vêm sendo propostas para reduzir o custo computacional de redes ViT em estimativa de profundidade (por exemplo, Schiavella et al., 2025) — o que indica viabilidade técnica para alcançar tempos de inferência baixos.

# Justificativa

A reconstrução de relevo de Marte de alta resolução com o método clássico baseado em estereofotogrametria (via ASP) gera DEMs de excelente qualidade, com espaçamento de 1-2 m e alinhamento confiável a altimetria laser (MOLA) (Hepburn et al., 2019). No entanto, esse processo demanda tempo computacional significativo e várias etapas de calibração e ajuste. Propõe-se, portanto, o desenvolvimento de um modelo de IA generativa baseado em ViT (Vision Transformer), treinado a partir de pares HiRISE e seus DEMs gerados pelo ASP. Esse modelo visa inferir DEMs de alta resolução com qualidade similar, porém com processamento muito mais rápido, permitindo a produção eficiente de relevo em larga escala ou em contextos com restrição de recursos. Os transformadores visuais demonstraram vantagem em tarefas densas de previsão de profundidade graças à atenção global (Ranftl et al., 2021), e técnicas recentes de atenção eficiente permitem mitigar o custo computacional (Schiavella et al., 2025). Assim, essa proposta combina o rigor altimétrico já existente com a eficiência de modelos de aprendizado profundo, abrindo caminho para mapeamentos de relevo marciano em tempo prático.
