import sys
import os
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from sympy import randprime
from sympy import *
from random import randint

class mainWindow:

    def __init__(self, client, command):



        self.client = client
        self.command = command

        app = QApplication(sys.argv)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, "mainwindow2.ui")

        if not os.path.exists(ui_path):
            print(f"ERREUR: Fichier introuvable -> {ui_path}")
            sys.exit(1)

        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
            print(f"ERREUR: Impossible d'ouvrir {ui_path}")
            sys.exit(1)

        loader = QUiLoader()
        top = loader.load(ui_file)
        ui_file.close()
        
        if top is None:
            print(f"ERREUR: QUiLoader a échoué -> {loader.errorString()}")
            sys.exit(1)

        window = top

        window.setMinimumSize(0, 0)
        window.resize(1261, 672)

        def w(name):
            return window.findChild(QWidget, name)

        # DEBUG
        print(f"UI chargé: {ui_path}")
        print(w("BCS"))

#FUNC FOR THE BUTTON DOING THE APPEARANCE


        def showTextMode():
            w("BImage").move(560, 80)
            w("TextSend").show()
            w("BImage").show()
            w("BText").hide()

        def showImageMode():
            w("TextSend").hide()
            w("BImage").hide()
            w("BText").show()

        def showDiffieHellman():
            w("TextGenerator").show()
            w("TextMRM").show()
            w("TextMW").show()
            w("TextMS").show()
            w("TextPrivateA").show()
            w("TextPublicgA").show()
            w("TextPublicgB").show()
            w("label_Generator").show()
            w("label_MRM").show()
            w("label_MW").show()
            w("label_MS").show()
            w("label_PrivateA").show()
            w("label_PublicgA").show()
            w("label_PublicgB").show()
            w("BCS").show()
            w("BClear").show()
            w("BGM").show()
            w("BHK").show()

        def hideDiffieHellman():
            w("TextGenerator").hide()
            w("TextMRM").hide()
            w("TextMW").hide()
            w("TextMS").hide()
            w("TextPrivateA").hide()
            w("TextPublicgA").hide()
            w("TextPublicgB").hide()
            w("label_Generator").hide()
            w("label_MRM").hide()
            w("label_MW").hide()
            w("label_MS").hide()
            w("label_PrivateA").hide()
            w("label_PublicgA").hide()
            w("label_PublicgB").hide()
            w("BCS").hide()
            w("BClear").hide()
            w("BGM").hide()
            w("BHK").hide()

        def showHashing():
            w("BSHA256").show()

        def hideHashing():
            w("BSHA256").hide()

        def showRSA():
            w("TextPrivateKey").show()
            w("TextPublicKey").show()
            w("TextModular").show()
            w("label_PrivateKey").show()
            w("label_Modular").show()
            w("label_PublicKey").show()

        def hideRSA():
            w("TextPrivateKey").hide()
            w("TextPublicKey").hide()
            w("TextModular").hide()
            w("label_PrivateKey").hide()
            w("label_Modular").hide()
            w("label_PublicKey").hide()

        def hideDecode():
            w("BDecode").hide()

        def showDecode():
            w("BDecode").show()

        def hideBFindKey():
            w("BFindKey").hide()

        def showBFindKey():
            w("BFindKey").show()

        def hideSingleShift():
            w("BEncodeSS").hide()
            w("TextSSKey").hide()
            w("label_SSKey").hide()

        def showSingleShift():
            w("BEncodeSS").show()
            w("TextSSKey").show()
            w("label_SSKey").show()

        def hideVigenere():
            w("BEncodeVigenere").hide()
            w("label_Vigenere").hide()
            w("TextVigenere").hide()

        def showVigenere():
            w("BEncodeVigenere").show()
            w("label_Vigenere").show()
            w("TextVigenere").show()

#FUNC FOR THE CONNECTION FOR THE BUTTON DOING THE APPEARANCE

        def text_b():
            showTextMode()

        def image_b():
            showImageMode()

        def diffieHellman_b():
            showDiffieHellman()
            hideRSA()
            hideSingleShift()
            hideHashing()
            hideVigenere()

        def rsa_b():
            showRSA()
            hideSingleShift()
            hideHashing()
            hideDiffieHellman()
            hideVigenere()

        def vigenere_b():
            hideSingleShift()
            hideRSA()
            hideHashing()
            hideDiffieHellman()
            showVigenere()

        def singleShift_b():
            showSingleShift()
            hideRSA()
            hideHashing()
            hideDiffieHellman()
            hideVigenere()

        def hashing_b():
            showHashing()
            hideRSA()
            hideSingleShift()
            hideDiffieHellman()
            hideVigenere()

#FUNC FOR BUTTONS HAVING SOME FUNCTIONNALITIES

        def findPrimaryFactors(p):
            psub = p - 1
            divider = 2
            primeFactors = []
            while (isprime(psub)==False):
                while (psub % divider != 0):
                    divider += 1
                primeFactors.append(divider)
                psub = psub // divider
                divider = 2
            if psub not in primeFactors:
                primeFactors.append(psub)
            return primeFactors


        def findGenerator(p):
            primeFactors = findPrimaryFactors(p)
            is_generator = True
            for g in range(2, p):
                is_generator = True
                for q in primeFactors:
                    x = pow(g, (p-1)//q, p)
                    if (x == 1):
                        is_generator = False
                if (is_generator == True):
                    return g
                
                
        def computeHalfKey():
            p = int(w("TextMW").toPlainText())
            privateA = randint(2, p-2)
            w("TextPrivateA").setPlainText(str(privateA))
            a = privateA
            g = int(w("TextGenerator").toPlainText())
            public_gA = pow(g, a, p)
            w("TextPublicgA").setPlainText(str(public_gA))

        def generateModulo():
            maxRandomModulo = w("TextMRM").toPlainText()
            maxRandomModulo = int(maxRandomModulo)
            p = randprime(2,maxRandomModulo)
            w("TextMW").setPlainText(str(p))
            g = findGenerator(p)
            w("TextGenerator").setPlainText(str(g))

        def ComputeSecret():
            gB = int(w("TextPublicgB").toPlainText())
            a = int(w("TextPrivateA").toPlainText())
            p = int(w("TextMW").toPlainText())

            MutualSecret = pow(gB, a, p)
            w("TextMS").setPlainText(str(MutualSecret))


        def vigenereEncode():
            text = w("TextSend").toPlainText()
            key = w("TextVigenere").toPlainText()
            encoded = command.cmd_vigenere(text, key)
            w("TextEncoded").setPlainText(encoded)

        def shiftEncode():
            text = w("TextSend").toPlainText()
            key = w("TextSSKey").toPlainText()
            encoded = command.cmd_shift_message(text, key)
            w("TextEncoded").setPlainText(encoded)


        def getResponseFromServer(text):
            w("TextLog").append(text)

        def send_encoded():
            text = w("TextEncoded").toPlainText()
            self.client.send(text, 't')


        def send_clear():
            text = w("TextSend").toPlainText()
            if (text == ""):
                getResponseFromServer("Your message can't be nothing")
            else:
                if w("SendToServerOnly").isChecked():
                    self.client.send(text, 's')
                else:
                    self.client.send(text, 't')

        def clearText():
            w("TextSend").clear()

        def clearDiffieHellman():
            w("TextGenerator").clear()
            w("TextMRM").clear()
            w("TextMW").clear()
            w("TextMS").clear()
            w("TextPrivateA").clear()
            w("TextPublicgA").clear()
            w("TextPublicgB").clear()

#START
        
        w("TextSend").hide()
        hideBFindKey()
        hideDecode()
        hideVigenere()
        hideDiffieHellman()
        hideSingleShift()
        hideRSA()
        hideHashing()
        window.show()

        threading.Thread(
            target=self.client.receive,
            args=(getResponseFromServer,),
            daemon=True
        ).start()

#BUTTON CONNECTION

        w("BCS").clicked.connect(ComputeSecret)
        w("BHK").clicked.connect(computeHalfKey)
        w("BGM").clicked.connect(generateModulo)
        w("BSendEncoded").clicked.connect(send_encoded)
        w("BEncodeVigenere").clicked.connect(vigenereEncode)
        w("BEncodeSS").clicked.connect(shiftEncode)
        w("BText").clicked.connect(text_b)
        w("BImage").clicked.connect(image_b)
        w("BClear").clicked.connect(clearDiffieHellman)
        w("BDiffieHellman").clicked.connect(diffieHellman_b)
        w("BHashing").clicked.connect(hashing_b)
        w("BVigenere").clicked.connect(vigenere_b)
        w("BSingleShift").clicked.connect(singleShift_b)
        w("BRSA").clicked.connect(rsa_b)
        w("BSendClear").clicked.connect(send_clear)
        w("BDelTextImage").clicked.connect(clearText)

        sys.exit(app.exec())