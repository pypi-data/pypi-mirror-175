import webbrowser

def YouHaveAGooddayinDSITU(answer=''):
    while True:
        if answer in ['yes','y','Yes','Y','YES']:
            feedback = 'สู้ต่อไปนะครับ เป็นกำลังใจให้ :)'
            break
        elif answer in ['no','n','No','N','NO']:
            feedback =  webbrowser.open_new_tab(r'https://cis.tu.ac.th/uploads/ci/dsi/form05.pdf')
            break
        else:
            feedback = 'ไม่ชัดเจนเลยนะครับ ขออีกรอบนึงนะ'
            break
    print(feedback)
