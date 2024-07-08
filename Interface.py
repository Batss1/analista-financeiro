import sys, os
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QMessageBox,
                             QPushButton, QVBoxLayout, QLabel, QFileDialog)
from PyQt6.QtGui import QIcon


class Aplicativo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Analista Financeiro')
        self.setWindowIcon(QIcon('maps.ico'))
        self.resize(500, 350)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # widgets
        cd_importar = QPushButton('Importar', clicked=self.importar)
        texto_entrada = QLabel()
        texto_entrada.setText('Digite o nome desejado para o gráfico:')
        self.entrada = QLineEdit()
        cd_exportar = QPushButton('Criar Gráfico', clicked=self.exportar)
        self.caixaMsg = QMessageBox()

        layout.addWidget(cd_importar)
        layout.addWidget(texto_entrada)
        layout.addWidget(self.entrada)
        layout.addWidget(cd_exportar)

        self.titulo = ''
        self.eixo_y = ''
        self.eixo_x = []
        self.dados = []

    def importar(self):
        nomeArquivo = QFileDialog.getOpenFileName(self, 'Importar Arquivo',
                                  os.path.dirname(os.path.realpath(sys.argv[0])),
                                  'Arquivos de texto *.txt')
        if nomeArquivo[0]:
            arq = open(nomeArquivo[0], 'r')
            self.titulo = arq.readline().rstrip()
            self.eixo_y = arq.readline().rstrip()
            self.eixo_x = arq.readline().rstrip().split(sep=',')
            self.dados = arq.readline().rstrip().split(sep=',')
            for i in range(len(self.dados)):
                self.dados[i] = int(self.dados[i])
            arq.close()
            self.caixaMsg.setText('Dados importados do arquivo.')
            self.caixaMsg.setIcon(QMessageBox.Icon.Information)
            self.caixaMsg.setWindowTitle('Importação concluída')
            self.caixaMsg.exec()

    def exportar(self):
        if len(self.dados) > 0:
            if len(self.entrada.text()) > 0:
                fig, ax = plt.subplots(figsize=(16, 10), facecolor='white', dpi=80, num=self.entrada.text())
                ax.vlines(x=[i for i in range(len(self.dados))], ymin=0, ymax=self.dados,
                          color='firebrick', alpha=0.7, linewidth=20)
                for dado in self.dados:
                    ax.text(self.dados.index(dado), dado+0.5, f'{dado}%', horizontalalignment='center')
                ax.set_title(self.titulo, fontdict={'size': 22})
                ax.set(ylabel=self.eixo_y, ylim=(0, round(max(self.dados)+max(self.dados)/10)))
                plt.xticks([i for i in range(len(self.eixo_x))], self.eixo_x,
                           horizontalalignment='center', fontsize=12)
                plt.show()
            else:
                self.caixaMsg.setText('Você precisa escolher um nome para o gráfico.')
                self.caixaMsg.setIcon(QMessageBox.Icon.Warning)
                self.caixaMsg.setWindowTitle('Atenção')
                self.caixaMsg.exec()
        else:
            self.caixaMsg.setText('Nenhum dado foi importado.')
            self.caixaMsg.setIcon(QMessageBox.Icon.Warning)
            self.caixaMsg.setWindowTitle('Atenção')
            self.caixaMsg.exec()


app = QApplication(sys.argv)
app.setStyleSheet('''
    QWidget{
        font-size: 25px;
    }
    QPushButton{
        font-size: 20px;
    }
''')

janela = Aplicativo()
janela.show()

app.exec()