from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from time import sleep
import datetime

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
        self.set_nome_recibo(nome_recibo)
        self.set_nome_pagador(nome_pagador)
        self.set_servico(servico)
        self.set_quantia(quantia)
        self.set_valor(valor)
        self.set_valor_ir(valor_ir)
        self.set_valor_total(valor_total)

    def get_id_recibo(self):
        
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

    def set_id_recibo(self):
        self.id_recibo = self.get_id_recibo()

    def set_nome_recibo( self, nome_recibo ):
        while not nome_recibo:
            nome_recibo = input("Informe o Nome do Recibo : ").title()
        self.nome_recibo = nome_recibo
    
    def set_nome_pagador( self, nome_pagador):
        while not nome_pagador:
            nome_pagador = input("Informe o Nome do Pagador : " ).title()  
        self.nome_pagador = nome_pagador

    def set_servico(self, servico):
        while not servico:
            servico = input("Informe a Descrição do Serviço : ").title()
        self.servico = servico
    
    def set_quantia(self, quantia):
        while not quantia:
            quantia = input("Informe a Quantia : ").title()
        self.quantia =  quantia

    def set_valor(self, valor):
        while not valor:
            valor = input("Informe o Valor : ").title()
        self.valor = valor

    def set_valor_ir(self, valor_ir):
        while not valor_ir:
            valor_ir = input("Informe o Valor I.R : ").title()
        self.valor_ir = valor_ir
    
    def set_valor_total(self, valor_total):
        while not valor_total:
            valor_total = input("Informe o Valor Total : ").title()
        self.valor_total = valor_total
     
Base.metadata.create_all(bind=db)

class Gerador():

    def __init__( self, recibo: Recibo ):
        self.recibo = recibo

    def cadastrar_recibo(self):

        print('\n--- CADASTRAR NOVO RECIBO ---\n')
        nome_recibo = input("Informe o Nome do Recibo : ").title()
        nome_pagador = input("Informe o Nome do Pagador : " ).title()
        servico = input("Informe a Descrição do Serviço : ").title()
        quantia = input("Informe a Quantia : ").title()
        valor = input("Informe o Valor : ").title()
        valor_ir = input("Informe o Valor I.R : ").title()
        valor_total = input("Informe o Valor Total : ").title()

        print('\n --- OS DADOS ESTAO CORRETOS ? ---\n' )
        print(f"Informe o Nome do Recibo : {nome_recibo}")
        print(f"Informe o Nome do Pagador : {nome_pagador}")
        print(f"Informe a Descrição do Serviço : {servico}")
        print(f"Informe a Quantia : {quantia}")
        print(f"Informe o Valor : {valor}")
        print(f"Informe o Valor I.R : {valor_ir}")
        print(f"Informe o Valor Total : {valor_total}")

        if input('Os Dados estão corretos ( S / N ) : ').upper() == "S":
            recibo = Recibo( nome_recibo, nome_pagador, servico, quantia, valor, valor_ir, valor_total )
            session.add(recibo)
            session.commit()
            print("\n--- Recibo cadastrado com sucesso ---\n")

if __name__ == "__main__":
    
    gerador = Gerador(Recibo)
    gerador.cadastrar_recibo()