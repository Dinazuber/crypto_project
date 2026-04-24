import sys
import os
import threading
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject, Signal
from sympy import randprime
from sympy import *
from random import randint

# Bridge object needed to emit Qt signals from a non-Qt background thread
class MessageReceiver(QObject):
    message_received = Signal(str)


class mainWindow:

    def __init__(self, client, command):

        self.client = client
        self.command = command

        app = QApplication(sys.argv)
        
        # Resolve UI file relative to this script, not the working directory
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
            # Reposition BImage before showing it so it doesn't overlap TextSend
            w("BImage").move(560, 80)
            w("TextSend").show()
            w("BImage").show()
            w("BText").hide()

        def showImageMode():
            # Hide the text input and image-confirm button; reveal the switch-back button
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
            w("BVerify").show()
            w("BSHA256").show()

        def hideHashing():
            w("BVerify").hide()
            w("BSHA256").hide()

        def showRSA():
            w("BGenerateRSA").show()
            w("BDecodeRSA").show()
            w("BEncodeRSA").show()
            w("TextPrivateKey").show()
            w("TextPublicKey").show()
            w("TextModular").show()
            w("label_PrivateKey").show()
            w("label_Modular").show()
            w("label_PublicKey").show()

        def hideRSA():
            w("BDecodeRSA").hide()
            w("BGenerateRSA").hide()
            w("BEncodeRSA").hide()
            w("TextPrivateKey").hide()
            w("TextPublicKey").hide()
            w("TextModular").hide()
            w("label_PrivateKey").hide()
            w("label_Modular").hide()
            w("label_PublicKey").hide()

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

# Panel-switching callbacks: each one shows exactly one crypto panel and hides all others,
# ensuring only the relevant controls are visible at any time.

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

        def verifyHash():
            # Compares TextEncoded (expected hash) against TextSend (hash to verify); result replaces TextEncoded
            OurMessage = w("TextEncoded").toPlainText()
            MessageToVerify = w("TextSend").toPlainText()
            if (OurMessage == MessageToVerify):
                w("TextEncoded").setPlainText("true")
            else :
                w("TextEncoded").setPlainText("false")

        def encodeHash():
            message = w("TextSend").toPlainText()
            encoded = self.command.cmd_hash(message)
            w("TextEncoded").setPlainText(encoded)

        def encodeRSA():
            # Encrypts using public key (n=modulus, e=public exponent): c = m^e mod n
            n = int(w("TextModular").toPlainText())
            e = int(w("TextPublicKey").toPlainText())
            message = w("TextSend").toPlainText()
            encoded = self.command.cmd_rsa_encrypt(message,n,e)
            w("TextEncoded").setPlainText(encoded)

        def generateRSA():
            # Generates a fresh RSA key pair: N=modulus, e=public exponent, d=private exponent
            N, e, d = self.command.cmd_prepareKeys()
            w("TextModular").setPlainText(str(N))
            w("TextPublicKey").setPlainText(str(e))
            w("TextPrivateKey").setPlainText(str(d))

        def decodeRSA():
            # Decrypts using private key (N=modulus, d=private exponent): m = c^d mod N
            message = w("TextSend").toPlainText()
            N = int(w("TextModular").toPlainText())
            d = int(w("TextPrivateKey").toPlainText())
            decoded = self.command.cmd_rsa_decrypt(message ,N , d)
            w("TextEncoded").setPlainText(decoded)


        def findPrimaryFactors(p):
            # Returns the distinct prime factors of (p-1), needed to test primitive roots
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
            # A primitive root g of p satisfies: g^((p-1)/q) != 1 (mod p) for every prime factor q of (p-1)
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
            # DH step 1: pick a random private key a in [2, p-2], then compute public half-key g^a mod p
            p = int(w("TextMW").toPlainText())
            privateA = randint(2, p-2)
            w("TextPrivateA").setPlainText(str(privateA))
            a = privateA
            g = int(w("TextGenerator").toPlainText())
            public_gA = pow(g, a, p)
            w("TextPublicgA").setPlainText(str(public_gA))

        def generateModulo():
            # Picks a random prime p below the user-supplied max, then finds its primitive root g
            maxRandomModulo = w("TextMRM").toPlainText()
            maxRandomModulo = int(maxRandomModulo)
            p = randprime(2,maxRandomModulo)
            w("TextMW").setPlainText(str(p))
            g = findGenerator(p)
            w("TextGenerator").setPlainText(str(g))

        def ComputeSecret():
            # DH step 2: shared secret = gB^a mod p  (same result as gA^b mod p on the other side)
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
            # Encrypted messages are always sent to the server only (never broadcast raw)
            text = w("TextEncoded").toPlainText()
            self.client.send(text, 's')


        def send_clear():
            text = w("TextSend").toPlainText()
            if (text == ""):
                getResponseFromServer("Your message can't be nothing")
            else:
                # 's' = server only, 't' = broadcast to all peers
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

# --- Initial UI state: hide all crypto panels and optional widgets so the window
#     starts clean; the user picks a mode via the sidebar buttons.
        w("TextSend").hide()
        hideBFindKey()
        hideVigenere()
        hideDiffieHellman()
        hideSingleShift()
        hideRSA()
        hideHashing()
        window.show()

        receiver = MessageReceiver()
        receiver.message_received.connect(getResponseFromServer)

        # daemon=True so the thread exits automatically when the main window closes
        threading.Thread(
            target=self.client.receive,
            args=(receiver.message_received.emit,),
            daemon=True
        ).start()

#BUTTON CONNECTION

        w("BVerify").clicked.connect(verifyHash)
        w("BDecodeRSA").clicked.connect(decodeRSA)
        w("BGenerateRSA").clicked.connect(generateRSA)
        w("BSHA256").clicked.connect(encodeHash)
        w("BEncodeRSA").clicked.connect(encodeRSA)
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