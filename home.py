from flask import Flask, render_template, request
import main
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      formulario = request.form
      perguntaResposta = {}
      print(formulario['input'])
      perguntaResposta['pergunta'] = formulario['input']
      perguntaResposta['resposta'] = main.getResposta( perguntaResposta['pergunta'])
      
      return render_template("home.html", result = perguntaResposta)

