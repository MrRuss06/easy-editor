import os
from PyQt5.QtWidgets import(QApplication, QWidget,
QLabel,QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget)

from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
from PIL import Image 

app = QApplication([])
window = QWidget()
window.resize(1000, 700)
window.setWindowTitle('Простой фоторедактор')

lb_image = QLabel("Картинка")
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw =  QPushButton('Ч\Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)

row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
window.setLayout(row)

workdir = ''

def filter(files,exctensions):
    result = []
    for filename in files:
        for ext in exctensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    exctensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), exctensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)


btn_dir.clicked.connect(showFilenamesList) 

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
    
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(),lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(workdir, filename)
       image_path = os.path.join(workimage.dir, workimage.filename)
       workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
window.show()
app.exec()
