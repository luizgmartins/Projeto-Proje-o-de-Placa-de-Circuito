# Projeto - Projeção de Placa de Circuito Impresso

**Descrição**: Projeto da disciplina de Processamento Digital de Imagem da UFPE, ministrada pelo professor João Marcelo. Consiste na utilização da biblioteca opencv em Python para projetar o lado oposto de uma placa de circuito impresso sobre a imagem em tempo real da placa.


----------------------------

## Recursos Utilizados
* Câmera do celular -> Utilizada como webcam para exibir as imagens da placa em tempo real e tirar as fotos para a criação das máscaras.
* Placas de circuito -> Utilizadas para detecção e projeção das imagens.
* Biblioteca opencv -> Utilizada para manipular imagens e frames de vídeo.
* Biblioteca numpy -> Utilizada para converter alguns tipos de variáveis.
* Adobe CS6 -> Utilizado para editar as máscaras das imagens das placas.
* Spyder -> Utilizado para criação e edição do programa em Python.

----------------------------
## Feature Matching

O feature matching consiste na busca de correspondências de imagens. Isto é, a busca de pontos em comum entre imagens e a busca de uma correlação entre elas. A ideia é conseguir identificar algum objeto pré definido que se encontra em uma imagem, podendo ter diferenças entre a imagem inicial do objeto e a imagem de destino. No caso do projeto realizado a imagem de um dos lados da placa foi salva em um banco de imagens e posteriormente usada para procurar a correspondência dessa placa na imagem da webcam. Na webcam era exibida a placa em diferentes ângulos e iluminações para o programa identificar alguma correspondência entre as imagens.

Foi utilizado o método Brute-Force Matcher para obter a combinação entre os descritores do conjunto de pontos da imagem do banco de dados com o conjunto de pontos do frame de vídeo a ser analisado utilizando um cálculo de distância. Os mais próximos eram selecionados para obter uma relação. Foi utilizado os descritores SIFT para obter as melhores correspodências.

O projeto além do uso do método Brute-Force, também foi utilizado o matcher baseado em FLANN que consiste em uma biblioteca com uma série de algoritmos para busca rápida de correspondências mais próximas. Esse método funciona mais rápido que o BF para um grande conjunto de dados.

Durante o projeto foi realizado o teste com o BF Matcher e o FLANN, tendo o método FLANN levado uma certa vantagem para as buscas de imagens analisadas. Os diferentes algoritmos do FLANN também foram testados, porém a mudança dos algoritmos fez com que o processamento das imagens ficasse mais lento e a imagem em tempo real foi ficando cada vez mais difícil de ver pela velocidade muito lenta que ia sendo exibida.

----------------------------
## Homography

Após obter os descritores e pontos chaves utilizando feature matching e seleção das melhores correspondências, foi obtida a homografia das imagens. Isto é, a obtenção de uma matriz 3x3 que mapeia os pontos da imagem do banco de imagens na imagem correspondente do frame de vídeo. Para obter a homografia entre as imagens é necessário pelo menos 4 pontos correspondentes. Com isso conseguimos encontrar uma matriz que pode levar os pontos da imagem da placa que queremos encontrar que leva até os pontos da imagem que vemos na webcam, assim podemos relacionar exatamente onde se encontra a placa na webcam. Esse mapeamento de pontos independe do formato em que a imagem de destino se encontra, contanto que os melhores pontos obtidos incialmente sejam mais próximos entre as imagens.

----------------------------
## Perspective

Já com a matriz obtida com a homografia foi necessário utilizar a transformação em perspectiva para levar a imagem do banco de imagens na imagens para sua correspondência no frame de vídeo. Inicialmente foi utilizada a função cv2.perspectiveTransform() que utiliza a matriz da homografia e os pontos extremos da imagem do frame de vídeo para gerar a transformação em perspectiva que será utilizada para criar uma borda branca ao redor da imagem da placa que foi identificada no frame de vídeo.

Como a ideia seria pegar a imagem do lado oposto da placa que vemos na webcam e projetar essa imagem sobre a placa que vemos na webcam, então para isso foi utilizada a função cv2.warpPerspective() que utiliza a imagem do lado oposto da placa (imagem espelhada) e a matriz de homografia para levar a imagem do lado oposto da placa exatamente sobre a placa.

Assim conseguimos identificar a placa de circuito nos frames de vídeo utilizando a imagem salva no banco de imagens e utilizamos a homografia encontrada para gerar uma transformação em perspectiva do lado oposto da placa para ser projetado sobre a visualização da placa em tempo real. Ao rodar o programa ainda é possível variar o brilho de exibição da imagem da webcam em relação ao brilho de exibição da imagem projetada sobre a placa. Também é possível desativar a detecção da placa utilizando os botões do teclado.

----------------------------
## Resultado

A ideia do projeto é observar a trilhas da placa sobre os componentes da mesma ou vice-versa, observando ambos os lados da placa em uma mesma imagem de vídeo. O resultado do projeto pode ser visto no vídeo clicando na imagem abaixo:

[![](https://github.com/luizgmartins/Projeto-Projecao-Placa-de-Circuito/blob/main/Imagens/video.png)](https://drive.google.com/file/d/1wOQVBMZd7nhXUHOH6VM-d1r9bMO1hgBL/view?usp=sharing)

----------------------------
## Observações

* Alguns momentos o programa apresentou dificuldades para encontrar a homografia e gerar uma imagem em perspectiva fazendo com que a placa não fosse projetada sobre o frame de vídeo de forma correta. A distorção poderia ser evitada se o programa conseguisse sempre identificar os melhores pontos correspondentes.
* Foi observado que as correspondências entre os pontos dependem bastante da qualidade da imagem que se encontra salva no banco de imagens, pois a iluminação mais baixa ou uma mudança grande no programa de edição poderia levar a falhas na obtenção da matriz de homografia.
* A resolução e foco da câmera utilizada como webcam também atrapalham na obtenção dos pontos correspondentes, mas apesar das dificuldades o programa apresentou resultados muito bons.
* Algumas placas apresentaram resultados bem melhores do que outras. Isso nos levar a concluir que o formato das placas e quantidade e disposição dos componentes sobre elas também influenciam na obtenção da homografia.
* Uma das dificuldades do projeto ficou por conta da criação do banco de imagens, pois era preciso tirar fotos da placa da mesma distância e ângulo em relação a câmera e a edição deveria recortar as imagens de frente e verso da placa e aplicar transformações para que as imagens ficassem do mesmo tamanho e com componentes nos mesmo locais. Caso não fosse feito de forma correta a imagem projetada seria deslocada em relação aos componentes da placa vista na webcam.
* Uma ideia de projeto futuro é utilização de outros tipos de descritores além do SIFT. No caso fazer uma comparação entre o que foi utilizado no projeto e outros tipos de descritores como ORB, SURF, etc.

----------------------------
## Referências

- https://blog.cedrotech.com/opencv-uma-breve-introducao-visao-computacional-com-python
- https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
- https://www.youtube.com/watch?v=I8tHLZDDHr4&list=PLfUs-MEc_zl92oNhomHK1M9yYAIeWz1C9&index=3&ab_channel=Pysource
- https://www.youtube.com/watch?v=UquTAf_9dVA&ab_channel=sentdex
- https://www.pyimagesearch.com/2016/03/07/transparent-overlays-with-opencv/
- https://www.geeksforgeeks.org/perspective-transformation-python-opencv/
- https://docs.opencv.org/4.x/d9/dc8/tutorial_py_trackbar.html
