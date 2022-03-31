import cv2
import mediapipe as mp

#inicializar opencv e mediapipe
webcam = cv2.VideoCapture(0) #ativar webcam
identificador_rostos = mp.solutions.face_detection

reconhecedor_rostos = identificador_rostos.FaceDetection(model_selection=0, min_detection_confidence=0.5)
box_mark = mp.solutions.drawing_utils

while True:
    #ler info webcam
    verificador, frame = webcam.read()
    if not verificador:
        break
    
    #reconhecer rostos
    lista_rostos = reconhecedor_rostos.process(frame)
    
    #desenhar os rostos
    if lista_rostos.detections:
        for rosto in lista_rostos.detections:
            box_mark.draw_detection(frame, rosto)
    
    # abrir janela da webcam
    cv2.imshow("Face Detection", frame) #(nome_da_janela, local_desenho(na img))
    
    #apertar ESC para fechar
    if cv2.waitKey(10) == 27: #waitKey(ms) = "cod_tecla" (esc = 27 )
        break

webcam.release() #para a webcam
cv2.destroyAllWindows() #fecha a janela
