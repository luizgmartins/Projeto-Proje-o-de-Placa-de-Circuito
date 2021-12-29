import cv2
import numpy as np

#Função utilizada na trackbar
def nothing(x):
    pass

#Função para inverter o lado da placa a ser projetada
def inverterImagem(img, img2):
    img3 = img
    img2 = cv2.flip(img2, 1)
    img = img2
    img2 = img3
    img2 = cv2.flip(img2, 1)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp_image, desc_image = sift.detectAndCompute(gray_img, None)
    return img, img2, kp_image, desc_image

#variáveis para uso dos botões do teclado
normal = 1
face = 0

#Carrega imagem da parte de cima da placa e converte em escala de cinza
img = cv2.imread("1-sup.png", 1)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#Carrega imagem da parte de baixo da placa, espelha a imagem e converte em escala de cinza
img2 = cv2.imread("1-inf.png", 1)
img2 = cv2.flip(img2, 1)
gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#Inicia a captura de vídeo da webcam do celular
cap = cv2.VideoCapture(1)

#Cria uma janela com uma trackbar para alteração do brilho da imagem projetada e da webcam
cv2.namedWindow('Webcam')
cv2.createTrackbar('Brilho Sup','Webcam',0,100,nothing)
brilho_sup = 0

#Inicia o detector SIFT
sift = cv2.xfeatures2d.SIFT_create()
#Encontra os pontos chave e descritores da imagem que será buscada na webcam
kp_image, desc_image = sift.detectAndCompute(gray_img, None)

#Define os parâmetro para uso nos métodos BF ou flann
index_params = dict(algorithm=1, trees=5)
search_params = dict(checks=70)
bf = cv2.BFMatcher()
flann = cv2.FlannBasedMatcher(index_params, search_params)

while True:
    _, frame = cap.read()
    if normal == 0:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp2, des2 = sift.detectAndCompute(gray_frame, None)
        #Condição necessária para evitar que o matches feche a função por falta de correspondência de pontos
        if(len(kp2)>5):
            #matches recebe a aplicação de um dos métodos para encontrar os pontos entre a imagem carregada e o frame do video
            #matches = bf.knnMatch(desc_image,des2,k=2)
            matches = flann.knnMatch(desc_image,des2, k=2)
            
            #Teste de proporção para encontrar boas correspondências
            good_points = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_points.append(m)
            
            #Condicição para evitar que o programa dê erro por não achar a transfromação
            if len(good_points) >20:
                #Obtenção dos pontos de origem e destino para encontrar a homografia
                query_pts = np.float32([kp_image[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
                train_pts = np.float32([kp2[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
                
                #Identifica os pontos extremos da imagem analisada e utiliza a matriz encontrada na homografia
                #e cria um contorno na perspectiva sobre os pontos correspondentes no frame de video
                h, w, l = img.shape
                pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                homography = cv2.polylines(frame, [np.int32(dst)], True, (255, 255, 255), 2)
                
                #Utiliza o warpPespective para levar a imagem do outro lado da placa em perspectiva
                a = frame.shape
                perspective = cv2.warpPerspective(img2, matrix, (a[1],a[0]))
                #Utiliza addWeighted para mudar o brilho da imagem da webcam inversamente proporcional ao da imagem projetada em perspectiva
                imagem = cv2.addWeighted(homography,abs(1 - brilho_sup),perspective,brilho_sup, 1)
                cv2.imshow("Webcam", imagem)
            else:
                cv2.imshow("Webcam", frame)
        else:
            cv2.imshow("Webcam", frame)
    else:
        cv2.imshow("Webcam", frame)
    #Recebe o valor alterado no trackbar do brilho e divide por 100
    brilho_sup = (cv2.getTrackbarPos('Brilho Sup','Webcam'))/100
    
    #Condições dos botões do teclado. n = muda a imagem normal da webcam para a projeção da placa. 
    #m= muda o lado da placa que será visualizado. Esc= encerra o código
    key = cv2.waitKey(1)
    if key == ord('n'):
        if normal == 0:
            normal = 1
        else:
            normal = 0
    if key == ord('m'):
        if face == 0:
            face = 1
            img, img2, kp_image, desc_image = inverterImagem(img, img2)
        else:
            face = 0
            img, img2, kp_image, desc_image = inverterImagem(img, img2)
    elif key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
