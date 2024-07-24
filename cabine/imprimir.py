"""
import pyautogui
from PIL import Image, ImageWin
import win32print
import win32ui
import win32con

def imprimir_foto():
    # Capturar a tela
    screenshot = pyautogui.screenshot()

    # Salvar a captura de tela em um arquivo temporário
    screenshot.save("screenshot.png")

    # Abrir a imagem
    image = Image.open("screenshot.png")
    # Cortar a imagem
    image = image.crop(crop_box)

    # Configurar a impressora
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        # Começar um documento de impressão
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc("Screenshot Print")
        hdc.StartPage()
        
        # Obter o tamanho da imagem
        width, height = image.size

        # Definir o tamanho de impressão em pixels
        printable_area = hdc.GetDeviceCaps(win32con.HORZRES), hdc.GetDeviceCaps(win32con.VERTRES)
        print_size = (int(printable_area[0] * 0.9), int((height / width) * printable_area[0] * 0.9))
        
        # Redimensionar a imagem para caber na página
        image = image.resize(print_size, Image.LANCZOS)
        
        # Converter a imagem para um formato compatível com o Windows
        dib = ImageWin.Dib(image)
        
        # Imprimir a imagem
        dib.draw(hdc.GetHandleOutput(), (0, 0, print_size[0], print_size[1]))
        
        # Finalizar a página e o documento de impressão
        hdc.EndPage()
        hdc.EndDoc()
    finally:
        # Fechar a impressora
        win32print.ClosePrinter(hprinter)
"""
import pyautogui
from PIL import Image, ImageWin
import win32print
import win32ui
import win32con

def imprimir_foto():
    # Capturar a tela
    screenshot = pyautogui.screenshot()

    # Salvar a captura de tela em um arquivo temporário
    screenshot.save("screenshot.png")

    # Abrir a imagem
    image = Image.open("screenshot.png")
    # Girar a imagem 90 graus no sentido horário
    image = image.rotate(-90, expand=True)

    # Configurar a impressora
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        # Começar um documento de impressão
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc("Screenshot Print")
        hdc.StartPage()
        
        # Obter o tamanho da imagem
        width, height = image.size

        # Definir o tamanho de impressão em pixels
        printable_area = hdc.GetDeviceCaps(win32con.HORZRES), hdc.GetDeviceCaps(win32con.VERTRES)
        print_size = (int(printable_area[0] * 0.9), int((height / width) * printable_area[0] * 0.9))
        
        # Redimensionar a imagem para caber na página
        image = image.resize(print_size, Image.LANCZOS)
        
        # Converter a imagem para um formato compatível com o Windows
        dib = ImageWin.Dib(image)
        
        # Imprimir a imagem
        dib.draw(hdc.GetHandleOutput(), (0, 0, print_size[0], print_size[1]))
        
        # Finalizar a página e o documento de impressão
        hdc.EndPage()
        hdc.EndDoc()
    except:
        return "Erro"
    finally:
        # Fechar a impressora
        win32print.ClosePrinter(hprinter)

    return "Imprimindo"