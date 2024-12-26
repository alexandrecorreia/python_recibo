from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from time import sleep
import datetime

# Impressao Recibos
from dotenv import load_dotenv
from weasyprint import HTML
import base64
import os

db = create_engine("sqlite:///db_recibos.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Recibo(Base):
    __tablename__ = "recibos"
    id_recibo = Column(Integer, unique=True, primary_key=True, autoincrement=False)
    numero_recibo = Column(String)
    nome_recibo = Column(String)
    nome_pagador = Column(String)
    servico = Column(String)
    quantia = Column(String)
    valor = Column(String)
    valor_ir = Column(String)
    valor_total = Column(String)

    def __init__( self, nome_recibo, nome_pagador, servico, quantia, valor, valor_ir, valor_total ):
        self.set_id_recibo()
        self.set_numero_recibo()
        self.set_nome_recibo(nome_recibo)
        self.set_nome_pagador(nome_pagador)
        self.set_servico(servico)
        self.set_quantia(quantia)
        self.set_valor(valor)
        self.set_valor_ir(valor_ir)
        self.set_valor_total(valor_total)

    def get_id_recibo(self, auto_increment = True ):
        
        if auto_increment : 
            indice = 1

            try:
                with open("id_recibo", "r") as f:  
                    indice = int(f.read())  
                    indice += 1 
            except FileNotFoundError:
                pass

            with open("id_recibo", "w") as f:
                f.write(str(indice))

            return indice
        
        else:
            with open("id_recibo", "r") as f:
                indice = int(f.read()) 

            return indice

    def set_id_recibo(self):
        self.id_recibo = self.get_id_recibo()
    
    def set_numero_recibo(self):
        dt = datetime.datetime.now()
        self.numero_recibo = f"{self.get_id_recibo(auto_increment=False):06d}/{dt.year}"

    def set_nome_recibo( self, nome_recibo ):
        self.nome_recibo = nome_recibo
    
    def set_nome_pagador( self, nome_pagador):
        self.nome_pagador = nome_pagador

    def set_servico(self, servico):
        self.servico = servico
    
    def set_quantia(self, quantia):
        self.quantia =  quantia

    def set_valor(self, valor):
        self.valor = valor

    def set_valor_ir(self, valor_ir):
        self.valor_ir = valor_ir
    
    def set_valor_total(self, valor_total):
        self.valor_total = valor_total
     
Base.metadata.create_all(bind=db)

class ImprimirRecibo():

    def abrir_pdf(self, caminho_pdf):
        # Verifica o sistema operacional e abre o PDF de acordo
        if os.name == 'posix':  # Linux e MacOS
            os.system(f'open "{caminho_pdf}"')
        elif os.name == 'nt':  # Windows
            os.startfile(caminho_pdf)
        else:
            print("Sistema operacional não suportado para abrir o PDF automaticamente.")

    def carrega_imagem(self, img):

        imagem_base64 = ''

        if os.path.exists(img):
            with open(img, "rb") as imagem:
                # Lê a imagem como binário e a converte para Base64
                imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        
        return imagem_base64
    
    def gerar_pdf_recibo(self, data ):

        nome_pdf = "recibo_gerado.pdf"
        
        load_dotenv()

        # Renderize o HTML com os dados do recibo
        with open("recibo_template.html") as template_file:
            recibo = template_file.read()
            recibo = recibo.replace("$logo_empresa", self.carrega_imagem(os.getenv('LOGO_EMPRESA')))
            recibo = recibo.replace("$assinatura", self.carrega_imagem(os.getenv('ASSINATURA')))
            recibo = recibo.replace("$cnpj", os.getenv("CNPJ"))
            recibo = recibo.replace("$nome_empresa", os.getenv("EMPRESA"))
            recibo = recibo.replace("$endereco_empresa", os.getenv("ENDERECO"))
            recibo = recibo.replace("$telefone_empresa", os.getenv("TELEFONE"))
            recibo = recibo.replace("$email_empresa", os.getenv("EMAIL"))
            recibo = recibo.replace("$numero_recibo", data.numero_recibo )
            recibo = recibo.replace("$nome_cliente", data.nome_pagador )
            recibo = recibo.replace("$quantia_extenso", data.quantia)
            recibo = recibo.replace("$descricao", data.servico )
            recibo = recibo.replace("$valor", data.valor )
            recibo = recibo.replace("$vir", data.valor_ir )
            recibo = recibo.replace("$vtotal", data.valor_total )
            recibo = recibo.replace("$dia", str(datetime.datetime.now().day) )
            recibo = recibo.replace("$mes", str(datetime.datetime.now().month) )
            recibo = recibo.replace("$ano", str(datetime.datetime.now().year) )

        # Converte o HTML para PDF usando WeasyPrint
        HTML(string=recibo).write_pdf(nome_pdf)

        self.abrir_pdf(nome_pdf)

    def gerar_pdf_recibos(self, data):

        nome_pdf = "recibos.pdf"

        with open("recibos_template.html") as template_file:
            recibo = template_file.read()
            colunas = ""            

            for dt in data:
                colunas += f"<tr><td>{dt.numero_recibo}</td><td>{dt.nome_pagador}</td><td>{dt.valor}</td></tr>"
            
            recibo = recibo.replace("$colunas", colunas)
            recibo = recibo.replace("$total_emitidos", str(len(data)))

        # Converte o HTML para PDF usando WeasyPrint
        HTML(string=recibo).write_pdf(nome_pdf)

        self.abrir_pdf(nome_pdf)

class Gerador():

    campos = [
        ['nome_recibo','Informe o Nome do Recibo','title'],
        ['nome_pagador','Informe o Nome do Pagador','title'],
        ['servico','Informe a Descricao do Servico','title'],
        ['quantia','Informe a Quantia','title'],
        ['valor','Informe o Valor'],
        ['valor_ir','Informe o Valor I.R'],
        ['valor_total','Informe o Valor Total']
    ]

    valores = {}

    def __init__( self, recibo: Recibo ):
        self.recibo = recibo

    def set_valores(self):
        for i in self.campos:
            self.valores[ i[0] ] = input( i[1]+ " : ").title() if len(i) > 1 != None else input( i[1]+ " : ")
    
    def get_valores(self):
        for i in self.campos:
            print(f"{ i[1]} : {self.valores[i[0]]}" )

    def cadastrar_recibo(self):

        print('\n--- CADASTRAR NOVO RECIBO ---\n')

        self.set_valores()

        print('\n--- OS DADOS ESTAO CORRETOS ? ---\n' )

        self.get_valores()

        if input('\nOs Dados estão corretos ( S / N ) : ').upper() == "S":
            recibo = Recibo( self.valores['nome_recibo'], 
                            self.valores['nome_pagador'], 
                            self.valores['servico'],
                            self.valores['quantia'], 
                            self.valores['valor'], 
                            self.valores['valor_ir'], 
                            self.valores['valor_total'] )
            session.add(recibo)
            session.commit()
            print("\n--- Recibo cadastrado com sucesso ---\n")
            
            self.imprimir_recibo( recibo.id_recibo )
    
    def imprimir_numero_recibo(self, numero_recibo):
        recibo = session.query(Recibo).filter_by(numero_recibo=numero_recibo).first()
        if recibo:
            self.imprimir_recibo( recibo.id_recibo )
        else:
            print('\n--- Numero de Recibo NÃO ENCONTRADO!---')

    def imprimir_recibo(self, id_recibo):

        recibo = session.query(Recibo).filter_by(id_recibo=id_recibo).first()
        msg  = f"\n--- Deseja imprimir o Recibo " 
        msg += f"{recibo.numero_recibo} - {recibo.nome_recibo} ( S / N ) --- : "

        if input( msg ).upper() == "S":
            imprimir = ImprimirRecibo()
            imprimir.gerar_pdf_recibo( recibo )
    
    def listar(self):
        
        recibos = session.query(Recibo).order_by(Recibo.id_recibo.desc()).all()
        imprimir = ImprimirRecibo()
        imprimir.gerar_pdf_recibos( recibos )



if __name__ == "__main__":
    
    gerador = Gerador(Recibo)
    gerador.cadastrar_recibo()