# Proposta de Projeto: Paint Multiplayer

Este projeto propõe o desenvolvimento de um jogo multiplayer simplificado no estilo "Gartic", focado na implementação de uma comunicação de rede robusta e de baixa latência entre dois jogadores. Nosso objetivo é criar uma experiência por turnos onde um jogador desenha e o outro tenta adivinhar o desenho, com a comunicação de estado e as ações do canvas sendo sincronizadas através de um servidor central.

## Fluxo do Jogo

O jogador utiliza o canvas para desenha
- Ferramentad: desenho, borracha, espessura do lápis, escolha da cor, apagar tudo, e salvar png
- Ao finalizar, o jogador salva o desenho

![Logo da empresa](img.png)

**Palpite:** o adversário recebe o desenho e insere o que acha em um campo de texto, confirmando

**Valida:** aquele que desenhou recebe o palpite e confirma se está certo ou errado

**Pontuação:** quem atingir 3 pontos ganha

## Infos

- salvar imagem
- lógica para envio de imagens em formato de bytes
- lógica do jogo, em geral

- [Reading and Writing Imgaes and Videos](https://www.opencv.org.cn/opencvdoc/2.3.2/html/modules/highgui/doc/reading_and_writing_images_and_video.html)
- [Image send via TCP](https://stackoverflow.com/questions/20820602/image-send-via-tcp)