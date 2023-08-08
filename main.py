import warnings
warnings.simplefilter("ignore")

import PySimpleGUI as sg
import threading
import speedtest

# Theme
sg.theme('DarkGrey5')

# Schriftart und -größe
title_font = ("Any", 24)
text_font = ("Any", 16)
button_font = ("Any", 18)

# Layout
layout = [
    [sg.Text("Speedtest", font=title_font, size=(25, 1), justification='center', pad=(0, 20))],
    [sg.Text("Klicke Start um den speedtest zu Starten.", font=text_font, size=(30, 2), justification='center', pad=(0, 20))],
    [sg.Text("", key='-DOWNLOAD-', size=(25, 1), font=text_font, justification='center')],
    [sg.Text("", key='-UPLOAD-', size=(25, 1), font=text_font, justification='center')],
    [sg.Button('Start', size=(10, 1), key='-START-', font=button_font, button_color=("white", "green"), pad=(0, 20)),
     sg.Button('Stop', size=(10, 1), key='-STOP-', font=button_font, button_color=("white", "red"), visible=False, pad=(0, 20))]
]



# Fenster erstellen
window = sg.Window('SPEEDTEST', layout, size=(400, 300), element_justification='center', finalize=True)



def run_test():
    test = speedtest.Speedtest()
    window['-DOWNLOAD-'].update("Downloadspeed: loading...")
    download = test.download()
    download_mbits = download / 1000000
    window['-DOWNLOAD-'].update(f"Downloadspeed: {download_mbits:.2f} Mbps")
    
    window['-UPLOAD-'].update("Uploadspeed: loading...")
    upload = test.upload()
    upload_mbits = upload / 1000000
    window['-UPLOAD-'].update(f"Uploadspeed: {upload_mbits} Mbps")

# Event Loop
while True:
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == '-START-':
        threading.Thread(target=run_test, daemon=True).start()  # Speedtest in einem separaten Thread starten
        window['-START-'].update(visible=False)
        window['-STOP-'].update(visible=True)

    if event == '-STOP-':
        window['-START-'].update(visible=True)
        window['-STOP-'].update(visible=False)

window.close()
