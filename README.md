# Convite de casamento — Ihanny Gabrielly & Marcos Ryan

Site mobile-first, single-file (`index.html` com CSS/JS embutidos), para o convite de casamento do dia 26/06/2027.

## Rodar localmente

Dentro da pasta do projeto, execute:

```powershell
npx serve . -l 5500
```

Abra no computador:

```text
http://localhost:5500
```

No celular conectado à mesma rede Wi-Fi, abra o endereço de rede mostrado pelo `serve`.

## Estrutura

```text
index.html                    site completo (envelope, hero, cerimônia, recepção,
                               presentes, RSVP, manual do convidado, rodapé)
assets/turning-page-instrumental.mp3   música de fundo
assets/qr/                    QR codes gerados (Pix e WhatsApp) + payloads
assets/paper-texture.png      textura de papel de fundo (embutida em base64 no index.html
                               via a variável CSS --paper; este PNG é só a fonte/preview)
assets/corner-flowers.jpg     foto da folhagem de eucalipto usada nos cantos (embutida em
                               base64 via a variável CSS --corner-flowers; a borda é suavizada
                               com um CSS mask-image, sem precisar de recorte/transparência)
print/gen_qrcodes.py          script que gera os QR codes (payload Pix EMV válido)
print/                        entregáveis de impressão (PDF A4, cartão, instruções)
```

## Configurações

Chave Pix, nomes, endereço, links do WhatsApp e do Maps estão diretamente em `index.html`
(constante `PIX_KEY` no script e nos elementos de texto/atributos `href`).

Para regenerar os QR codes (por exemplo se a chave Pix mudar), edite os parâmetros no
topo de `print/gen_qrcodes.py` e rode:

```powershell
python print/gen_qrcodes.py
```

Isso atualiza `assets/qr/qr-pix.png` e `assets/qr/qr-whatsapp.png` — depois é só
copiar os novos arquivos para o mesmo caminho referenciado no `index.html`.
