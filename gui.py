from PyQt5.QtWidgets import QApplication, QSlider, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QRadioButton, QGroupBox, QGridLayout, QTextEdit
from PyQt5.QtGui import QColor
from cache_simulator_for_gui import cache_sim
from cache import CacheConfig

import threading
import queue

resultado_queue = queue.Queue()

class DataGrid(QMainWindow):
    def __init__(self, num_colunas):
        super().__init__()
        # Configurar janela
        self.setWindowTitle("Cache Sim")
        # get user screen resolution
        screen_resolution = QApplication.desktop().screenGeometry()
        p1 = screen_resolution.height()/2
        p2 = screen_resolution.width()/2
        self.setGeometry(int(p2-475), int(p1-450), 960, 900)
        self.setFixedSize(960, 900)
        #self.setFixedSize(int(p2*2-100), int(p1*2-100))

        # Criar widget principal
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Criar widget para os campos à esquerda
        left_widget = QWidget()
        left_layout = QFormLayout()
        left_widget.setLayout(left_layout)
        #-------------------------------------------------------------
        rbtn_instructions = QGroupBox("Instructions")
        hbox_instructions = QGridLayout()
        rbtn_instructions.setLayout(hbox_instructions)

        #Criar labels de entrada de texto
        lbl_nset_label = QLabel("NSet = Cache Lines")
        lbl_block_size_label = QLabel("Block Size = 1 byte")
        lbl_assoc_label = QLabel("Associativity = 2*")
        lbl_input_file_label = QLabel("Input File = FileName")
        lbl_text_redBlock_label = QLabel("Red block's = Dirty")
        lbl_text_greenBlock_label = QLabel("Green block's = Block is not dirty")
        lbl_text_greenBlock_label.setStyleSheet("QLabel { color : green; }")
        lbl_text_redBlock_label.setStyleSheet("QLabel { color : red; }")

        # Criar layout horizontal
        hbox_instructions.addWidget(lbl_nset_label, 0, 0)
        hbox_instructions.addWidget(lbl_block_size_label, 0, 1)
        hbox_instructions.addWidget(lbl_assoc_label, 0, 2)
        hbox_instructions.addWidget(lbl_input_file_label, 0, 3)
        hbox_instructions.addWidget(lbl_text_redBlock_label, 1, 0)
        hbox_instructions.addWidget(lbl_text_greenBlock_label, 1, 1)
        left_layout.addRow(rbtn_instructions)
        #-------------------------------------------------------------
        rbtn_settings = QGroupBox("Cache Settings")
        hbox_settings = QGridLayout()
        rbtn_settings.setLayout(hbox_settings)

        lbl_nset = QLabel("NSet:\t\t")
        self.txt_nset = QLineEdit()
        self.txt_nset.setText("256")

        lbl_block_size = QLabel("Block Size:\t")
        self.txt_block_size = QLineEdit()
        self.txt_block_size.setText("4")

        self.txt_nset.setMaximumWidth(100)
        self.txt_block_size.setMaximumWidth(100)

        lbl_assoc = QLabel("Associativity:\t")
        self.txt_assoc = QLineEdit()
        self.txt_assoc.setText("2")

        lbl_assoc.setMaximumWidth(100)
        self.txt_assoc.setMaximumWidth(100)

        lbl_input_file = QLabel("Input File:")
        self.txt_input_file = QLineEdit()
        self.txt_input_file.setMaximumWidth(100)
        self.txt_input_file.setText("vortex")

        # Criar layout horizontal
        hbox_settings.addWidget(lbl_nset, 0, 0)
        hbox_settings.addWidget(self.txt_nset, 0, 1)
        hbox_settings.addWidget(lbl_block_size, 0, 2)
        hbox_settings.addWidget(self.txt_block_size, 0, 3)
        hbox_settings.addWidget(lbl_assoc, 2, 0)
        hbox_settings.addWidget(self.txt_assoc, 2, 1)
        hbox_settings.addWidget(lbl_input_file, 2, 2)
        hbox_settings.addWidget(self.txt_input_file, 2, 3)
        left_layout.addRow(rbtn_settings)
        #-------------------------------------------------------------
        #create 3 radio buttons
        self.rbtn_lru = QRadioButton("LRU")
        self.rbtn_fifo = QRadioButton("FIFO")
        self.rbtn_random = QRadioButton("Random")
        self.rbtn_random.setChecked(True)
        
        #create a group box
        rbtn_group = QGroupBox("Replacement Policy")
        #create a layout for the radio buttons
        rbtn_layout = QHBoxLayout()
        #add the radio buttons to the layout
        rbtn_layout.addWidget(self.rbtn_lru)
        rbtn_layout.addWidget(self.rbtn_fifo)
        rbtn_layout.addWidget(self.rbtn_random)
        #set the layout to the group box
        rbtn_group.setLayout(rbtn_layout)
        #add the group box to the layout
        left_layout.addRow(rbtn_group)
        #-------------------------------------------------------------

        #-------------------------------------------------------------
        rbtn_buttons = QGroupBox("Operations")
        hbox_buttons = QGridLayout()
        rbtn_buttons.setLayout(hbox_buttons)
        # Criar botões
        btn_run = QPushButton("Run")
        btn_save = QPushButton("Save")
        btn_stop = QPushButton("Stop")

        # Criar layout horizontal
        hbox_buttons.addWidget(btn_run, 0, 0)
        hbox_buttons.addWidget(btn_save, 0, 1)
        hbox_buttons.addWidget(btn_stop, 0, 2)
        left_layout.addRow(rbtn_buttons)
        #-------------------------------------------------------------
        rbtn_result = QGroupBox("Results")
        hbox_result = QGridLayout()
        rbtn_result.setLayout(hbox_result)

        #Total de acessos, Taxa de hit, Taxa de miss, Taxa de miss compulsório, Taxa de miss de capacidade, Taxa de miss de conflito

        lbl_total_access = QLabel("Total Accesses:")
        self.txt_total_access = QLineEdit()
        self.txt_total_access.setReadOnly(True)
        self.txt_total_access.setMaximumWidth(100)

        lbl_hit_rate = QLabel("Hit Rate:")
        self.txt_hit_rate = QLineEdit()
        self.txt_hit_rate.setReadOnly(True)
        self.txt_hit_rate.setMaximumWidth(100)

        lbl_miss_rate = QLabel("Miss Rate:")
        self.txt_miss_rate = QLineEdit()
        self.txt_miss_rate.setReadOnly(True)
        self.txt_miss_rate.setMaximumWidth(100)

        lbl_compulsory_miss_rate = QLabel("Compulsory Miss Rate:")
        self.txt_compulsory_miss_rate = QLineEdit()
        self.txt_compulsory_miss_rate.setReadOnly(True)
        self.txt_compulsory_miss_rate.setMaximumWidth(100)

        lbl_capacity_miss_rate = QLabel("Capacity Miss Rate:")
        self.txt_capacity_miss_rate = QLineEdit()
        self.txt_capacity_miss_rate.setReadOnly(True)
        self.txt_capacity_miss_rate.setMaximumWidth(100)

        lbl_conflict_miss_rate = QLabel("Conflict Miss Rate:")
        self.txt_conflict_miss_rate = QLineEdit()
        self.txt_conflict_miss_rate.setReadOnly(True)
        self.txt_conflict_miss_rate.setMaximumWidth(100)

        hbox_result.addWidget(lbl_total_access, 0, 0)
        hbox_result.addWidget(self.txt_total_access, 0, 1)
        hbox_result.addWidget(lbl_hit_rate, 1, 0)
        hbox_result.addWidget(self.txt_hit_rate, 1, 1)
        hbox_result.addWidget(lbl_miss_rate, 2, 0)
        hbox_result.addWidget(self.txt_miss_rate, 2, 1)
        hbox_result.addWidget(lbl_compulsory_miss_rate, 3, 0)
        hbox_result.addWidget(self.txt_compulsory_miss_rate, 3, 1)
        hbox_result.addWidget(lbl_capacity_miss_rate, 4, 0)
        hbox_result.addWidget(self.txt_capacity_miss_rate, 4, 1)
        hbox_result.addWidget(lbl_conflict_miss_rate, 5, 0)
        hbox_result.addWidget(self.txt_conflict_miss_rate, 5, 1)


        left_layout.addRow(rbtn_result)
        #-------------------------------------------------------------
        rbtn_output = QGroupBox("Output")
        hbox_output = QVBoxLayout()
        rbtn_output.setLayout(hbox_output)

        self.otp = QTextEdit()
        self.otp.setReadOnly(True)
        self.otp.setMaximumHeight(280)
        self.otp.setMaximumWidth(460)
        hbox_output.addWidget(self.otp)
        left_layout.addRow(rbtn_output)
        #-------------------------------------------------------------
        # Conectar eventos de clique dos botões
        btn_run.clicked.connect(self.on_btn_run_clicked)
        btn_save.clicked.connect(self.on_btn_save_clicked)
        btn_stop.clicked.connect(self.on_btn_stop_clicked)
        #slider.valueChanged.connect(self.on_slider_value_changed)

        # Adicionar widget à esquerda do layout central
        central_layout.addWidget(left_widget)

        # Criar widget para a tabela à direita
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        # Criar tabela
        self.table = QTableWidget()
        right_layout.addWidget(self.table)
        # Definir a escala da tabela para uma fonte de tamanho 10
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.verticalHeader().setDefaultSectionSize(1)

        # Definir número de colunas
        self.table.setColumnCount(num_colunas)

        # Definir número de linhas
        num_linhas = 256
        self.table.setRowCount(num_linhas)

        # Configurar campos da tabela
        for i in range(num_linhas):
            for j in range(num_colunas):
                item = QTableWidgetItem()
                item.setBackground(QColor("red"))  # Definir cor de fundo como vermelha
                self.table.setItem(i, j, item)

        # Conectar evento de clique
        self.table.cellClicked.connect(self.on_cell_clicked)

        # Adicionar widget à direita do layout central
        central_layout.addWidget(right_widget)

    def reset_table(self, num_linhas, num_colunas):
        for i in range(num_linhas):
            for j in range(num_colunas):
                item = QTableWidgetItem()
                item.setBackground(QColor("red"))  # Definir cor de fundo como vermelha
                self.table.setItem(i, j, item) 

    def checkReplacement(self):
        if self.rbtn_lru.isChecked():
            return "L"
        elif self.rbtn_fifo.isChecked():
            return "F"
        else:
            return "R"

    def on_cell_clicked(self, row, col):
        item = self.table.item(row, col)
        item.setBackground(QColor("yellow"))

    def cache_sim_thread(self):
        # Função que será executada na thread
        resultado = cache_sim(int(self.txt_nset.text()), int(self.txt_block_size.text()), int(self.txt_assoc.text()), self.checkReplacement(), 1, self.txt_input_file.text(), self.table)
        resultado_queue.put(resultado)

    def on_btn_run_clicked(self):
        if int(self.txt_nset.text()) >= 1 or int(self.txt_nset.text())%2 == 0:
            pass
        else :
            self.otp.append("Invalid Nset ")
            return
        if int(self.txt_assoc.text()) >= 1 or int(self.txt_assoc.text())%2 == 0:
            pass
        else :
            self.otp.append("Invalid Nway")
            return
        if int(self.txt_block_size.text()) >= 1:
            pass
        else :
            self.otp.append("Invalid Block Size")
            return
        
        self.table.setColumnCount(int(self.txt_assoc.text()))
        self.table.setRowCount(int(self.txt_nset.text()))
        self.reset_table(int(self.txt_nset.text()), int(self.txt_assoc.text()))
        
        #teste = CacheConfig(int(self.txt_nset.text()), int(self.txt_block_size.text()), int(self.txt_assoc.text()), 8)
        
        self.otp.append("Starting Benchmark")
        
        thread = threading.Thread(target=self.cache_sim_thread)
        thread.start()
        resultado = resultado_queue.get()
       
        if(resultado == None):
            self.otp.append("Invalid Input File")
            return
        
        val = resultado.split()
        self.txt_total_access.setText(val[0])
        self.txt_hit_rate.setText(val[1])
        self.txt_miss_rate.setText(val[2])
        self.txt_compulsory_miss_rate.setText(val[3])
        self.txt_capacity_miss_rate.setText(val[4])
        self.txt_conflict_miss_rate.setText(val[5])
        self.otp.append("Benchmark ended!")

    def on_btn_save_clicked(self):
        print("Botão 'Save' clicado")
        # Adicione aqui a lógica que você deseja executar quando o botão 'Save' for clicado

    def on_btn_stop_clicked(self):
        print("Botão 'Stop' clicado")
        # Adicione aqui a lógica que você deseja executar quando o botão 'Stop' for clicado
    
    def on_slider_value_changed(self, value):
        self.lbl_speed.setText("" + str(value))

if __name__ == '__main__':
    app = QApplication([])
    window = DataGrid(4)  # Número de colunas da tabela
    window.show()
    app.exec_()
