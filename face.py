import cv2

def main():
    # 画像読込み
    origin_img = cv2.imread("A.jpg")
    # 画像コピー
    img = origin_img.copy()

    # カスケードファイルのパス
    cascade_path = "haarcascade_frontalface_default.xml"
    # カスケード分類器の特徴量取得
    cascade = cv2.CascadeClassifier(cascade_path)

    # 画像グレースケール化
    image_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 顔検出
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

    #print(facerect)
    color = (255, 255, 255) #白

    # 検出した場合
    if len(facerect) > 0:

    #検出した顔を囲む矩形の作成
        for rect in facerect:
            cv2.rectangle(origin_img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

    #認識結果の保存
    cv2.imwrite("./out.jpg", origin_img)

if __name__ == "__main__":
    main()