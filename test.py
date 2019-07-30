# -*- coding: utf-8 -*-
import cv2
import dlib
from datetime import datetime

IMAGE_PATH = "./nc73730.png" # 画像パス
CAPTURE_SCALE = 0.5 # カメラの画像サイズ

def main():
    # 顔認証の準備
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(0) # カメラの準備

    while True:
        _, frame = cap.read() # カメラ画像を取得
        
        # 画像サイズを変更
        frame = img_resize(frame, CAPTURE_SCALE)
        h, w, _  = frame.shape

        img = frame # img = frame * 0とすると黒画面になる
        dets = detector(frame[:, :, ::-1])

        if len(dets) > 0:
            parts = predictor(frame, dets[0]).parts() # 顔の点を取得
            distance, pos = calc_distance_and_pos(img, parts) # 顔の横幅と顔の中心を取得
            icon, icon_w, icon_h = load_icon(IMAGE_PATH, distance) # アイコン読み込み

            if (pos != None) and (distance > 0.0):
                x = pos.x - int(icon_w/2)
                y = pos.y - int(icon_h/2)
                if (0 <= y) and (y <= (h-int(icon_h))) and (0 <= x) and (x <= (w-int(icon_w))):
                    # 画面の範囲内だったら画像を合成
                    img = merge_images(img, icon, x, y)

        cv2.imshow("camera", img) # 画像を表示

        k = cv2.waitKey(1)&0xff # キー入力を待つ
        if k == ord('q'):
            # 「q」キーが押されたら終了する
            break
        elif k == ord('p'):
            # 「p」キーで画像を保存
            save_image(img)
            cv2.imshow("saved", img) # キャプチャした画像を表示

    # キャプチャをリリースして、ウィンドウをすべて閉じる
    cap.release()
    cv2.destroyAllWindows()

# アイコンを読み込む関数
def load_icon(path, distance):
    icon = cv2.imread(path, -1)
    icon_height, _  = icon.shape[:2]
    icon = img_resize(icon, float(distance * 1.5/icon_height))
    icon_h, icon_w  = icon.shape[:2]

    return icon, icon_w, icon_h

# 画像をリサイズする関数
def img_resize(img, scale):
    h, w  = img.shape[:2]
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    return img

# 距離と顔の中心座標を計算
def calc_distance_and_pos(img, parts):
    # 確認(33が顔の中心位置)
    cnt = 0
    pos = None
    p1 = None
    distance = 0.0

    for i in parts:
        if (cnt == 0):
            # 顔の幅を測る時の始点
            p1 = i
        if (cnt == 16):
            # 顔の幅を計算
            distance = ((p1.x-i.x)**2 + (p1.y-i.y)**2)**0.5
        if (cnt == 33):
            pos = i # 顔の中心位置
        # 画像に点とテキストをプロット
        cv2.putText(img, str(cnt), (i.x, i.y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), thickness=1, lineType=cv2.LINE_8)
        cv2.circle(img, (i.x, i.y), 1, (255, 0, 0), -1)
        cnt = cnt + 1

    return distance, pos

# 画像を保存する関数
def save_image(img):
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = "./" + date + ".png"
    cv2.imwrite(path, img) # ファイル保存

# 画像を合成する関数
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

if __name__ == '__main__':
    main()