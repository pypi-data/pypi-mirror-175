import webbrowser
from IPython.display import Javascript
def YouHaveAGooddayinDSITU(answer=''):
    while True:
        if answer in ['yes','y','Yes','Y','YES']:
            feedback = 'สู้ต่อไปนะครับ เป็นกำลังใจให้ :)'
            break
        elif answer in ['no','n','No','N','NO']:
            url = 'https://cis.tu.ac.th/uploads/ci/dsi/form05.pdf'
            display(Javascript('window.open("{url}");'.format(url=url)))
            break
        else:
            feedback = 'ไม่ชัดเจนเลยนะครับ ขออีกรอบนึงนะ'
            break
    print(feedback)