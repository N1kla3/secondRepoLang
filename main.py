import os

import nltk
import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog)
from nltk.draw.tree import TreeView
from fpdf import FPDF


def run(sample_text):
    # optional
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    from nltk import pos_tag, word_tokenize, RegexpParser

    tagged = pos_tag(word_tokenize(sample_text))

    chunker = RegexpParser("""
                        NP: {<CD>?<DT>?<JJ>*<NN|NNS>}    #To extract Noun Phrases
                       P: {<IN>}               #To extract Prepositions
                       V: {<MD>?<V.*>}              #To extract Verbs
                       PP: {<P> <NP>}          #To extract Prepostional Phrases
                       VP: {<V> <NP|PP>*} 
                       """)

    output = chunker.parse(tagged, 2)
    # verbose level
    output.draw()
    return
    TreeView(output)._cframe.print_to_file('output.ps')
    os.system('magick output.ps outputs.png')
    pdf = FPDF()
    pdf.add_page()
    pdf.image('output.png', 0, 0, 100, 100)
    pdf.output("output.pdf", "F")


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.edit = QLineEdit("Write text here")
        self.button = QPushButton("Analyse text")
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.analyse)

    def analyse(self):
        run(self.edit.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
