import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QComboBox
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5.QtCore import Qt
import json

with open('service-account-credentials.json') as json_file:
    data = json.load(json_file)
    firebase_credentials = data['firebase']

cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

empresa = [
    "LOGGI", "JADLOG", "SHOPEE", "ANJUN", "SEQUOIA"
]
base = [
    "ROTAS","FEIRA DE SANTANA", "BAIRROS DE FEIRA DE SANTANA", "ALAGOINHAS",
    "JACOBINA", "SANTO ANTONIO DE JESUS", "TRANSFERENCIA", "DEVOLUÇÃO" 
]

tranferencia = [
    "TRANSFERENCIA PARA FEIRA", "TRANSFERENCIA PARA ALAGOINHAS", "TRANSFERENCIA PARA JACOBINA", "TRANSFERENCIA PARA SANTO ANTONIO DE JESUS"
]
cidades_feira = [
    "IPIRA", "BAIXA GRANDE", "MAIRI", "VARZEA DA ROÇA", "MORRO DO CHAPEU", "IRECE",
    "ITABERABA", "IAÇU", "ITATIM", "CASTRO ALVES", "SANTA TEREZINHA", "SANTO ESTEVÃO",
    "ANTONIO CARDOSO", "IPECAETA", "SÃO GONÇALO DOS CAMPOS", "CACHOEIRA", "SÃO FELIX",
    "CONCEIÇÃO DA FEIRA", "AMELIA RODRIGUES", "CONCEIÇÃO DO JACUIPE", "CORAÇÃO DE MARIA",
    "TEODORO SAMPAIO", "IRARA", "SANTANOPOLIS", "MURITIBA", "SAPEAÇU", "CRUZ DAS ALMAS",
    "GOVERNADOR MANGABEIRA", "CABACEIRA DO PARAGUAÇU", "SÃO FELIPE",
    "MARAGOGIPE", "TANQUINHO", "CANDEAL", "ICHU", "SERRINHA", "BIRITINGA", "BARROCAS",
    "ARACI", "TEOFILANDIA", "SANTA BARBARA", "LAMARÃO", "AGUA FRIA", "CONCEIÇÃO DO COITÉ",
    "VALENTE", "RETIROLANDIA", "SANTA LUZ", "CANSANÇÃO", "QUEIMADAS", "SÃO DOMINGOS",
    "RIACHÃO DO JACUIPE", "NOVA FATIMA", "PE DE SERRA", "CIPÓ", "BANZAÊ", "FATIMA",
    "CICERO DANTAS", "NOVA SOURE", "TUCANO", "RIBEIRA DO AMPARO", "SITIO DO QUINTO",
    "CORONEL JOÃO SÁ", "HELIOPOLIS", "RIBEIRA DO POMBAL", "ANGUERA", "SERRA PRETA",
    "RAFAEL JAMBEIRO", "FEIRA DE SANTANA", "BAIXA GRANDE"
]
cidades_algoinhas = [
    "ALAGOINHAS","ACAJUTIBA","CONDE","CRISÓPOLIS","ENTRE RIOS","ESPLANADA","INHAMBUPE",
    "ITANAGRA","JANDAÍRA","MATA DE SÃO JOÃO","OURIÇANGAS","RIO REAL","SÁTIRO DIAS",
    "ARATUÍPE","APORÁ","ARAMARI","ARAÇÁS","CARDEAL DA SILVA","CATU","ITAPICURU",
    "OLINDINA"
]
cidades_saj = [
    "CONCEIÇÃO DO ALMEIDA","ELÍSIO MEDRADO","ITAPARICA","ITUBERÁ","JIQUIRIÇÁ","LAJE",
    "MUNIZ FERREIRA","MUTUÍPE","NILO PEÇANHA","SANTO ANTÔNIO DE JESUS",
    "SÃO MIGUEL DAS MATAS","UBAÍRA","VALENÇA","VARZEDO","DOM MACEDO COSTA","ITAQUARA",
    "NAZARÉ","TAPEROÁ","TEOLÂNDIA","IGRAPIÚNA","JAGUARIPE","AMARGOSA","CRAVOLÂNDIA",
    "GANDU","NOVA IBIÁ","PRESIDENTE TANCREDO NEVES","SALINAS DA MARGARIDA","SANTA INÊS",
    "VERA CRUZ","WENCESLAU GUIMARÃES"
]
cidades_jacobina = [
    "CAÉM","MAIRI","MIGUEL CALMON","SERROLÂNDIA","VÁRZEA DO POÇO",
    "VÁRZEA NOVA","JACOBINA"
]
devolucaos = [
    "DEVOLUÇÃO PARA LOGGI", "DEVOLUÇÃO PARA FEIRA", "DEVOLUÇÃO PARA JADLOG", 
    "DEVOLUÇÃO PARA SHOPEE", "DEVOLUÇÃO PARA ANJUN", "DEVOLUÇÃO PARA SEQUOIA"
]
barrios_feria = [
    "35º BI","ALTO DO CRUZEIRO","ALTO DO PAPAGAIO","ASA BRANCA","AVIÁRIO",
    "BARAÚNAS","BRASÍLIA","CALUMBI","CAMPO DO GADO NOVO","CAMPO LIMPO",
    "CASEB","CASEB","CENTRO","CIDADE NOVA","FEIRA IX","FEIRA IX","FEIRA VI",
    "FEIRA VII","FEIRA VIII","FEIRA X","FEIRA X","GABRIELA","GEORGE AMÉRICO",
    "JARDIM ACÁCIA","JARDIM CRUZEIRO","LAGOA SALGADA","LIMOEIRO","MANGABEIRA",
    "MUCHILA","NOVA BRASÍLIA","NOVA ESPERANÇA","NOVA ESPERANÇA","NOVO HORIZONTE",
    "PAPAGAIO","PARQUE GETÚLIO VARGAS","PARQUE IPÊ","PARQUE IPÊ","PARQUE LAGOA SUBAÉ",
    "PARQUE VIVER","PONTO CENTRAL","QUEIMADINHA","RUA NOVA","SANTA MÔNICA",
    "SANTO ANTÔNIO DOS PRAZERES","SÃO JOÃO","SIM","SÍTIO MATIAS","SOBRADINHO",
    "SUBAÉ","TOMBA"
]
rotas = [
    "aguardando", "ROTA 01", "ROTA 02", "ROTA 03", "ROTA 04", "ROTA 05", "ROTA 06", "ROTA 07"
]
tipo = "Rota"
class FirebaseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RTA controler")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        
        self.layout_base = QHBoxLayout()
        self.base_label = QLabel("Região de destino:")
        self.layout_base.addWidget(self.base_label)
        self.base_combo_box = QComboBox()
        self.base_combo_box.addItems(base)
        self.layout_base.addWidget(self.base_combo_box)
        layout.addLayout(self.layout_base)
        self.base_combo_box.currentIndexChanged.connect(self.on_base_selected)
        
        self.layout_cidade = QHBoxLayout()
        self.cidade_label = QLabel("Cidade:")
        self.layout_cidade.addWidget(self.cidade_label)
        self.combo_box = QComboBox()
        self.combo_box.addItems(rotas)
        self.layout_cidade.addWidget(self.combo_box)
        layout.addLayout(self.layout_cidade)
        self.combo_box.currentIndexChanged.connect(self.on_cidade_selected)

        self.label = QLabel("Documentos na coleção:")
        layout.addWidget(self.label)

        self.search_layout = QHBoxLayout()
        layout.addLayout(self.search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite o ID do documento ou uma chave de pesquisa...")
        self.search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Pesquisar")
        self.search_button.clicked.connect(self.search_documents)
        self.search_layout.addWidget(self.search_button)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)

        self.delete_button = QPushButton("Deletar Documentos Selecionados")
        self.delete_button.clicked.connect(self.delete_documents)
        layout.addWidget(self.delete_button)
        
        self.ceos_label_layout = QHBoxLayout()
        self.Ceos = QLabel("Github.com/dudurtg2 - Versão Alpha 0.1.1")
        self.Ceos.setStyleSheet("color: gray;")
        self.ceos_label_layout.addWidget(self.Ceos)
        self.ceos_label_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(self.ceos_label_layout)

        self.load_documents()

    def on_cidade_selected(self, index):
        self.load_documents()

    def on_base_selected(self, index):
        global tipo  
        base_selecionada = self.base_combo_box.currentText()
        if base_selecionada == "ALAGOINHAS":
            self.atualizar_cidades(sorted(cidades_algoinhas))
            self.cidade_label.setText("Cidade:")
            tipo = "Local"
        elif base_selecionada == "JACOBINA":
            self.atualizar_cidades(sorted(cidades_jacobina)) 
            self.cidade_label.setText("Cidade:")
            tipo = "Local"
        elif base_selecionada == "SANTO ANTONIO DE JESUS":
            self.atualizar_cidades(sorted(cidades_saj))
            self.cidade_label.setText("Cidade:")
            tipo = "Local"
        elif base_selecionada == "FEIRA DE SANTANA":
            self.atualizar_cidades(sorted(cidades_feira))
            self.cidade_label.setText("Cidade:")
            tipo = "Local" 
        elif base_selecionada == "DEVOLUÇÃO":
            self.atualizar_cidades(sorted(devolucaos))
            self.cidade_label.setText("Local:") 
            tipo = "Local"
        elif base_selecionada == "TRANSFERENCIA":
            self.atualizar_cidades(sorted(tranferencia))
            self.cidade_label.setText("Local:")
            tipo = "Local"
        elif base_selecionada == "BAIRROS DE FEIRA DE SANTANA":
            self.atualizar_cidades(sorted(barrios_feria))
            self.cidade_label.setText("Bairros:")
            tipo = "Local"
        elif base_selecionada == "ROTAS":
            self.atualizar_cidades(rotas)
            self.cidade_label.setText("Rota:")
            tipo = "Rota"
        self.on_cidade_selected(self)

    def atualizar_cidades(self, lista_cidades):
        global tipo  
        self.combo_box.clear()
        self.combo_box.addItems(lista_cidades)

    def load_documents(self):
        global tipo  
        self.list_widget.clear()
        query_text = self.combo_box.currentText()
        
        if query_text:
            collection_ref = db.collection('bipagem')
            query_ref = collection_ref.where(tipo, '==', query_text).where('Status', '==', 'aguardando')
            docs = query_ref.stream()
        else:
            collection_ref = db.collection('bipagem')
            docs = collection_ref.where('Status', '==', 'aguardando').stream()
        
        for doc in docs:
            data = doc.to_dict()
            rota = data.get('Rota', 'Campo não encontrado')
            cidade = data.get('Local', 'Campo não encontrado')
            hora_dia = data.get('Hora e Dia', 'Campo não encontrado')
            campo_valor = f"Rota: {rota}, Local: {cidade}, Data e Hora: {hora_dia}"
            self.list_widget.addItem(f"ID: {doc.id}, {campo_valor}")

    def documents(self):
        global tipo  
        self.list_widget.clear()
        collection_ref = db.collection('bipagem')
        docs = collection_ref.where('Status', '==', 'aguardando').stream()
        
        for doc in docs:
            data = doc.to_dict()
            rota = data.get('Rota', 'Campo não encontrado')
            cidade = data.get('Local', 'Campo não encontrado')
            hora_dia = data.get('Hora e Dia', 'Campo não encontrado')
            campo_valor = f"Rota: {rota}, Local: {cidade}, Data e Hora: {hora_dia}"
            self.list_widget.addItem(f"ID: {doc.id}, {campo_valor}")

    def search_documents(self):
        global tipo  
        query_text = self.search_input.text()
        self.list_widget.clear()

        if query_text:
            try:
                doc_ref = db.collection('bipagem').document(query_text)
                doc = doc_ref.get()

                if doc.exists:
                    data = doc.to_dict()
                    rota = data.get('Rota', 'Campo não encontrado')
                    cidade = data.get('Local', 'Campo não encontrado')
                    hora_dia = data.get('Hora e Dia', 'Campo não encontrado')
                    campo_valor = f"Rota: {rota}, Local: {cidade}, Data e Hora: {hora_dia}"
                    self.list_widget.addItem(f"ID: {doc.id}, {campo_valor}")
                else:
                    print(f"Documento com ID {query_text} não encontrado.")
            except Exception as e:
                print(f"Erro ao buscar documento: {e}")
        else:
            self.documents()

    def delete_documents(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            doc_ids = [item.text().split(',')[0].split(':')[1].strip() for item in selected_items]
            try:
                for doc_id in doc_ids:
                    db.collection('bipagem').document(doc_id).delete()
                QMessageBox.information(self, "Sucesso", f"Documentos deletados com sucesso.")
                self.load_documents()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao deletar os documentos: {e}")
        else:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione pelo menos um documento para deletar.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirebaseApp()
    window.show()
    sys.exit(app.exec_())