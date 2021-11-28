import PySimpleGUI as sg
import ImageProcessing as ip
from PIL import Image, ImageTk


class Main():
    def __init__(self):
        minSettingValue = 0.0  # 彩度，コントラスト変更のパラメータ下限
        maxSettingValue = 2.0  # 彩度，コントラスト変更のパラメータ上限
        defaultSettingValue = 1.0  # 彩度，コントラスト変更のパラメータ初期値
        resolutionValue = 0.1  # 彩度，コントラスト変更のスライダー刻み幅

        # ファイルブラウザを使用したファイル入力(拡張子png, bmp)
        # テキストボックスにパスを入力しようとするとエラーが出る
        # "参照"ボタンを押して画像ファイルを選択すること
        file_input_col = [sg.Text('ファイル'),
                          sg.InputText(key='INPUT_FILE', enable_events=True, size=(45, 1)),
                          sg.FileBrowse('参照', file_types=(('png', '*.png'), ('bmp', '*.bmp')))]

        # 画像処理の名前リスト
        image_process_list = [[sg.Text('彩度')],
                              [sg.Text('コントラスト')],
                              [sg.Text('透明度')]]
        # 画像の彩度を設定するスライダー
        vivid_slider_col = [sg.Slider(range=(minSettingValue, maxSettingValue),
                                      default_value=defaultSettingValue, resolution=resolutionValue,
                                      orientation='h', size=(35, None), key='sld_vivid', enable_events=True),
                            sg.InputText(default_text=str(defaultSettingValue), size=(10, 1), key='itx_vivid'),
                            sg.Button('Set', key='btn_vivid')]
        # 画像のコントラストを設定するスライダー
        contrast_slider_col = [sg.Slider(range=(minSettingValue, maxSettingValue),
                                         default_value=defaultSettingValue, resolution=resolutionValue,
                                         orientation='h', size=(35, None), key='sld_contrast',
                                         enable_events=True),
                               sg.InputText(default_text='1.0', size=(10, 1), key='itx_contrast'),
                               sg.Button('Set', key='btn_contrast')]
        # 画像の透明度を設定するスライダー
        alpha_slider_col = [sg.Slider(range=(0, 255), default_value=255, resolution=1,
                            orientation='h', size=(35, None), key='sld_alpha',
                            enable_events=True),
                            sg.InputText(default_text='0', size=(10, 1), key='itx_alpha'),
                            sg.Button('Set', key='btn_alpha')]
        # 画像を400x400の大きさにする．画像の横にヒストグラムも表示させる
        self.image_element = [sg.Image(filename='', size=(400, 400)), sg.Image(filename='', size=(400, 400))]
        # アプリを終了するためのボタン
        finish_button = [sg.Button('Finish')]
        # ウィンドウのレイアウト
        self.layout = [file_input_col,
                       image_process_list[0],
                       contrast_slider_col,
                       image_process_list[1],
                       vivid_slider_col,
                       image_process_list[2],
                       alpha_slider_col,
                       self.image_element,
                       finish_button]

    def main(self):
        # ウィンドウオブジェクトの作成
        window = sg.Window('Show Picture', self.layout)
        image_original = None

        # イベントのループ
        while True:
            event, values = window.read()

            if event == None:
                break
            elif event == 'Finish':
                break
            elif event == 'sld_alpha':
                window['itx_alpha'].update(int(values['sld_alpha']))
            elif event == 'sld_vivid':
                window['itx_vivid'].update(float(values['sld_vivid']))
            elif event == 'sld_contrast':
                window['itx_contrast'].update(float(values['sld_contrast']))
                
            elif event == 'btn_alpha': 
                val = int(values['itx_alpha'])
                if val < 255 or val > 0:
                    window['sld_alpha'].update(val)
            elif event == 'btn_vivid': 
                val = float(values['itx_vivid'])
                if val < 2.0 or val > 0.0:
                    window['sld_vivid'].update(val)
            elif event == 'btn_contrast': 
                val = float(values['itx_contrast'])
                if val < 2.0 or val > 0.0:
                    window['sld_contrast'].update(val)
            elif event == 'INPUT_FILE' and values['INPUT_FILE'] != '':
                # image = ip.set_image_data(values['INPUT_FILE'])
                image_original = ip.set_image_data(values['INPUT_FILE'])
                
            # if values['INPUT_FILE'] != '':
            if image_original is not None:
                image_after = ip.get_image(image_original,
                                           values['sld_alpha'],
                                           values['sld_vivid'],
                                           values['sld_contrast'])
                self.image_element[0].update(data=ImageTk.PhotoImage(image_after))
                fig = ip.make_histgram(image_after)
                fig_bytes = ip.plot_image(fig)
                self.image_element[1].update(data=fig_bytes)

        # ウィンドウクローズ処理
        window.close()


if __name__ == '__main__':
    gui = Main()
    gui.main()
