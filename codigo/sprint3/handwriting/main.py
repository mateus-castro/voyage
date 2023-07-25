import cv2
import numpy as np
import cv2
import easyocr

reader = easyocr.Reader(['en'])

# Carregar a imagem
image = cv2.imread("images/argent06.jpg")

# Obter as dimensões da imagem
height, width, _ = image.shape

# Definir as coordenadas do canto inferior esquerdo do quadrante
x = 0  # Coordenada x do canto inferior esquerdo
y = height // 2  # Coordenada y do canto inferior esquerdo
width = width // 2  # Largura do quadrante (metade da largura da imagem)
height = height // 2  # Altura do quadrante (metade da altura da imagem)

# Recortar o quadrante da imagem
quadrant = image[y:y+height, x:x+width]

# Converter o quadrante para o espaço de cores HSV
hsv_quadrant = cv2.cvtColor(quadrant, cv2.COLOR_BGR2HSV)

# Definir os limites do intervalo de cor da assinatura (em HSV)
lower_color = np.array([0, 0, 0])  # Limite inferior (preto)
upper_color = np.array([180, 255, 100])  # Limite superior (branco)

# Aplicar uma máscara para obter a região da assinatura no quadrante
mask = cv2.inRange(hsv_quadrant, lower_color, upper_color)

# Aplicar a máscara invertida no quadrante original para preservar o restante do quadrante
result = cv2.bitwise_and(quadrant, quadrant, mask=mask)

# Substituir o quadrante original pelo quadrante com a assinatura destacada
image[y:y+height, x:x+width] = result

# Exibir a imagem completa com a assinatura destacada no quadrante
cv2.imshow("Signature", image)
cv2.waitKey(0)
cv2.destroyAllWindows()