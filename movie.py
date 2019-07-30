import sys
import cv2 

# OpenCV のインポート
# VideoCaptureのインスタンスを作成する。
# 引数でカメラを選べれる。
cap = cv2.VideoCapture(0)

if cap.isOpened() is False:
    print("can not open camera")
    sys.exit()

# 評価器を読み込み
cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

def img_resize(img, h, w):
    img = cv2.resize(img, (int(w), int(h)))
    return img

def merge_images(bg, fg_alpha, s_x, s_y):
    alpha = fg_alpha[:,:,3]  # アルファチャンネルだけ抜き出す(要は2値のマスク画像)
    alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGR) # grayをBGRに
    alpha = alpha / 255.0    # 0.0〜1.0の値に変換

    fg = fg_alpha[:,:,:3]

    f_h, f_w, _ = fg.shape # アルファ画像の高さと幅を取得
    b_h, b_w, _ = bg.shape # 背景画像の高さを幅を取得

    # 画像の大きさと開始座標を表示
    print("f_w:{} f_h:{} b_w:{} b_h:{} s({}, {})".format(f_w, f_h, b_w, b_h, s_x, s_y))

    bg[s_y:f_h+s_y, s_x:f_w+s_x] = (bg[s_y:f_h+s_y, s_x:f_w+s_x] * (1.0 - alpha)).astype('uint8') # アルファ以外の部分を黒で合成
    bg[s_y:f_h+s_y, s_x:f_w+s_x] = (bg[s_y:f_h+s_y, s_x:f_w+s_x] + (fg * alpha)).astype('uint8')  # 合成

    return bg

while True:
    # VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()

    # そのままの大きさだと処理速度がきついのでリサイズ
    frame = cv2.resize(frame, (int(frame.shape[1]*0.7), int(frame.shape[0]*0.7)))

    # 処理速度を高めるために画像をグレースケールに変換したものを用意
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔検出
    facerect = cascade.detectMultiScale(
        gray,
        scaleFactor=1.11,
        minNeighbors=3,
        minSize=(100, 100)
    )

    if len(facerect) != 0:
        for x, y, w, h in facerect:
            # 顔の部分(この顔の部分に対して目の検出をかける)
            face_gray = gray[y: y + h, x: x + w]

            # くり抜いた顔の部分を表示(処理には必要ない。ただ見たいだけ。)
            show_face_gray = cv2.resize(face_gray, (int(gray.shape[1]), int(gray.shape[0])))
            cv2.imshow('face', show_face_gray)

            # 顔検出した部分に枠を描画
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 255, 255),
                thickness=2
            )

            print((x, y),(x + w, y + h))
            icon = cv2.imread("./nc73730.png", -1)
            icon = img_resize(icon, h, w)
            print(h,w)
            frame = merge_images(frame, icon, x, y)
    
    cv2.imshow('frame', frame)
    
    k = cv2.waitKey(1)
    if k == 27:
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()