# Instruções de impressão e montagem

Convite de casamento — Ihanny Gabrielly & Marcos Ryan — 26/06/2027

Este pacote tem dois materiais para impressão, pensados para usos diferentes:

- `convite-cartao-105x148mm.png` — **um cartão único**, no formato de convite físico
  tradicional (105×148mm, como um A6), pronto para impressão em gráfica ou impressora
  doméstica com bandeja de cartolina.
- `convite-impressao-A4.pdf` — **versão do site em 4 páginas A4**, com todo o conteúdo
  do convite (capa, cerimônia/recepção, presentes, RSVP e manual do convidado),
  pensada para impressão caseira em folha comum ou para montar um pequeno caderno/
  booklet a ser entregue junto com o cartão.

Ambos foram renderizados a 300 DPI (resolução de gráfica profissional), com as fontes
já embutidas na imagem — não é necessário instalar nenhuma fonte para imprimir.

## 1. Cartão único (105×148mm)

**Papel recomendado:** cartolina ou papel couché/fotográfico 250–300g, acabamento
fosco ou levemente texturizado (realça os tons verde/dourado). Evite papel muito
brilhante, que pode refletir luz sobre o QR code e dificultar a leitura.

**Configuração de impressão:**
1. Abra `convite-cartao-105x148mm.png` no visualizador de imagens ou diretamente no
   driver de impressão.
2. Selecione tamanho de papel personalizado 105×148mm (ou imprima em A6 e corte, já
   que A6 é 105×148mm).
3. Escala: **100% / "tamanho real"** — nunca use "ajustar à página", pois isso
   distorce a proporção e desfoca o texto.
4. Qualidade: máxima ("fotográfica" ou "melhor qualidade").
5. Se for enviar para uma gráfica, entregue o PNG diretamente — ele já está em
   300 DPI, sem necessidade de conversão.

## 2. Caderno A4 (4 páginas)

**Papel recomendado:** sulfite 120–180g (mais espesso que o padrão de escritório,
para não transparecer o verso) ou papel couché fosco 150g se for uma gráfica.

**Configuração de impressão:**
1. Abra `convite-impressao-A4.pdf`.
2. Papel: A4, orientação retrato.
3. Escala: **100%** (não usar "encolher para caber" — o PDF já nasceu no tamanho A4
   exato).
4. Se sua impressora imprime frente e verso automaticamente, ative a opção de
   "borda longa" (long-edge binding), já que todas as páginas estão no mesmo sentido.

**Ordem das páginas:**
1. Capa (nomes, versículo, data)
2. Cerimônia religiosa + Recepção
3. Lista de presentes (fundo verde-escuro — capricho extra de tinta se for impressora
   jato de tinta, prefira modo "alta qualidade" para a cor ficar uniforme)
4. Confirmação de presença (RSVP) + Manual do convidado

**Sugestão de encadernação:** como são só 4 páginas, o acabamento mais simples e
elegante é dobrar ao meio (como um mini-livreto) e fechar com um grampo central ou um
laço de fita na cor dourada/verde — combinando com a paleta do convite. Alternativas:
- Espiral fina (encadernação em espiral) para um acabamento mais durável.
- Furar 2 furos na lateral esquerda e amarrar com fita, no estilo "caderno artesanal".

## 3. Regenerando os arquivos

Se qualquer informação mudar (endereço, chave Pix, data), os três scripts em
`print/` recriam os artefatos a partir do zero, sem depender de internet no momento
da geração (as fontes já estão salvas localmente em `print/fonts/`):

```powershell
python print/gen_qrcodes.py     # QR codes (Pix + WhatsApp)
python print/make_card.py       # cartão 105x148mm
python print/make_pdf.py        # PDF A4 de 4 páginas
```
