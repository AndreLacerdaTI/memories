from flask import Flask, render_template, Response, request, jsonify, url_for, flash
import cv2
import os

from dados import *
from imprimir import *

app = Flask(__name__)
app.secret_key = 'cabine'
camera = cv2.VideoCapture(0)  # Inicia a captura da webcam

global cliente_codigo
global codigo_foto
cliente_codigo = 0
codigo_foto = 0

global tema
tema = ['default','branco']

def gen_frames():
    while True:
        success, frame = camera.read()  # Lê o frame da câmera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Converte o frame em bytes e envia para o navegador

@app.route('/')
def index():
    DIRETORIO = './static/fotos/'
    global tema
    fotos = [os.path.basename(arquivo) for arquivo in os.listdir(DIRETORIO)]
    return render_template('index.html', fotos=fotos[-3:], tema=tema)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tirar_foto', methods=['POST'])
def tirar_foto():
    global cliente_codigo
    global codigo_foto
    cliente_codigo = cliente_codigo + 1
    return render_template('capturar.html', tema=tema)

@app.route('/tirar')
def tirar():
    return render_template('capturar.html', tema=tema)

@app.route('/capture', methods=['POST','GET'])
def capture():
    global cliente_codigo
    cliente = cliente_codigo
    global codigo_foto
    codigo_foto = codigo_foto + 1
    DIRETORIO = './static/fotos/'
    #num_arquivos = sum(len(arquivos) for _, _, arquivos in os.walk(DIRETORIO))
    success, frame = camera.read()    
    if success:
        cv2.imwrite(f'./static/fotos/{cliente}-{codigo_foto}.jpg', frame)
    else:
        return jsonify(success=False, message="Falha ao capturar a imagem.")
    
    if codigo_foto==3:
        redirect_url = url_for('fotografia', cliente=cliente, tema=tema)
        codigo_foto = 0
        return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
    else:
        #redirect_url = url_for('fotografia', cliente=cliente)
        #return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
        redirect_url = url_for('tirar')
        return jsonify(success=True, message="Imagem capturada com sucesso!", redirect_url=redirect_url)
    
@app.route('/fotografia')
def fotografia():
    cliente = request.args.get('cliente', '')
    return render_template('fotografia.html', cliente = cliente, tema=tema)

@app.route('/admin', methods=['POST','GET'])
def admin():
    return render_template('admin.html')

@app.route('/trocar_tema', methods=['POST'])
def trocar_tema():
    global tema
    return render_template('admin.html', trocar_tema=True, tema=tema)

@app.route('/salvar_tema', methods=['POST'])
def salvar_tema():
    novo_tema = request.form['tema']
    global tema
    tema = ['default',novo_tema]
    print(tema)
    return render_template('admin.html')

@app.route('/personalizar_tema', methods=['POST'])
def personalizar_tema():
    global tema
    return render_template('admin.html', personalizar_tema=True, tema=tema)

@app.route('/salvar_tema_personalizado', methods=['POST'])
def salvar_tema_personalizado():
    #novo_tema = request.form['tema']
    cor_primaria = request.form['cor-primaria']
    cor_secundaria = request.form['cor-secundaria']
    cor_texto_botao = request.form['cor-texto-botao']
    cor_botao = request.form['cor-botao']
    cor_de_texto = request.form['cor-de-texto']
    tipo_fundo = request.form['tipo-fundo']
    novo_tema = ['custom',cor_primaria,cor_secundaria,cor_texto_botao,cor_botao,cor_de_texto,tipo_fundo]
    print(novo_tema)
    global tema
    tema = novo_tema
    return render_template('admin.html')

@app.route('/trocar_logo', methods=['POST'])
def trocar_logo():
    return render_template('admin.html', trocar_logo=True)
@app.route('/salvar_logo', methods=['POST'])
def salvar_logo():
    if request.method == 'POST':
        if 'logo' not in request.files:
            flash('Erro ao enviar Logo, por favor tente novamente.')
            return render_template('admin.html', trocar_logo=True)
        file = request.files['logo']
        if file.filename == '':
            flash('Erro ao enviar Logo, por favor tente novamente.')
            return render_template('admin.html', trocar_logo=True)
        if file:
            filename = 'logo.png' #file.filename
            DIRETORIO = './static/images/'
            file.save(os.path.join(DIRETORIO, filename))
            flash('Logo salva com sucesso!')
            return render_template('admin.html')
    return render_template('admin.html')

@app.route('/sair', methods=['POST'])
def sair():
    global tema
    return render_template('index.html', tema=tema) 

@app.route('/imprimir', methods=['POST','GET'])
def imprimir():
    cliente = request.form['cliente']
    
    retorno = imprimir_foto()
    if retorno=='Imprimindo':
        return render_template('fotografia.html', cliente=cliente)
    if retorno=='Erro':
        flash('Erro ao imprimir')
        return render_template('fotografia.html', cliente=cliente)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.20.125', debug=True)
