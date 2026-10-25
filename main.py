import csv

class Imovel:
    def __init__(self, tipo, valor_base):
        self.tipo = tipo
        self.valor_base = valor_base
        self.taxa_contratual = 2000.00
        
    def calcular_aluguel(self):
        return self.valor_base
        
    def gerar_projecao_csv(self, valor_mensal_aluguel, parcelas_taxa, arquivo_nome="projecao_locacao.csv"):
        valor_parcela_taxa = self.taxa_contratual / parcelas_taxa
        
        with open(arquivo_nome, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Mes', 'Aluguel_Mensal', 'Parcela_Taxa', 'Total_Mes'])
            
            for mes in range(1, 13):
                taxa = valor_parcela_taxa if mes <= parcelas_taxa else 0.00
                total = valor_mensal_aluguel + taxa
                writer.writerow([mes, f"R$ {valor_mensal_aluguel:.2f}", f"R$ {taxa:.2f}", f"R$ {total:.2f}"])
        print(f"\n[+] Arquivo CSV '{arquivo_nome}' gerado com sucesso!")


class Apartamento(Imovel):
    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas
        
    def calcular_aluguel(self):
        valor = self.valor_base
        if self.quartos == 2:
            valor += 200.00
        if self.tem_garagem:
            valor += 300.00
            
        if not self.tem_criancas:
            valor -= (valor * 0.05) # 5% de desconto
            
        return valor


class Casa(Imovel):
    def __init__(self, quartos, tem_garagem):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        
    def calcular_aluguel(self):
        valor = self.valor_base
        if self.quartos == 2:
            valor += 250.00
        if self.tem_garagem:
            valor += 300.00
        return valor


class Estudio(Imovel):
    def __init__(self, vagas_garagem):
        super().__init__("Estúdio", 1200.00)
        self.vagas_garagem = vagas_garagem
        
    def calcular_aluguel(self):
        valor = self.valor_base
        if self.vagas_garagem >= 2:
            valor += 250.00
            vagas_extras = self.vagas_garagem - 2
            if vagas_extras > 0:
                valor += (vagas_extras * 60.00)
        elif self.vagas_garagem == 1:
            pass # A regra diz pacote inicial de DUAS vagas por 250. Assume-se que 1 vaga não tem esse custo ou nao aplica. (Ajustável)
            
        return valor


class RentSmartApp:
    def obter_inteiro(self, mensagem, min_val, max_val):
        while True:
            try:
                valor = int(input(mensagem))
                if min_val <= valor <= max_val:
                    return valor
                print(f"Por favor, digite um valor entre {min_val} e {max_val}.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def obter_sim_nao(self, mensagem):
        while True:
            resp = input(mensagem).strip().lower()
            if resp in ['s', 'n']:
                return resp == 's'
            print("Entrada inválida. Digite 's' para sim ou 'n' para não.")

    def iniciar(self):
        print("="*40)
        print(" Bem-vindo ao RentSmart - R.M Imóveis ")
        print("="*40)
        
        print("\nTipos de Imóveis:")
        print("1 - Apartamento")
        print("2 - Casa")
        print("3 - Estúdio")
        
        tipo_imovel = self.obter_inteiro("Escolha o tipo de imóvel (1-3): ", 1, 3)
        
        imovel = None
        
        if tipo_imovel == 1:
            quartos = self.obter_inteiro("Número de quartos (1 ou 2): ", 1, 2)
            garagem = self.obter_sim_nao("Deseja vaga de garagem? (s/n): ")
            criancas = self.obter_sim_nao("Possui crianças? (s/n): ")
            imovel = Apartamento(quartos, garagem, criancas)
            
        elif tipo_imovel == 2:
            quartos = self.obter_inteiro("Número de quartos (1 ou 2): ", 1, 2)
            garagem = self.obter_sim_nao("Deseja vaga de garagem? (s/n): ")
            imovel = Casa(quartos, garagem)
            
        elif tipo_imovel == 3:
            vagas = self.obter_inteiro("Quantas vagas de garagem deseja? (0 a 10): ", 0, 10)
            imovel = Estudio(vagas)
            
        parcelas = self.obter_inteiro("\nEm quantas vezes deseja parcelar a taxa contratual de R$ 2.000,00? (1 a 5): ", 1, 5)
        
        # Processamento
        aluguel = imovel.calcular_aluguel()
        valor_parcela = 2000.00 / parcelas
        
        # Saída
        print("\n" + "="*40)
        print(" ORÇAMENTO DETALHADO ")
        print("="*40)
        print(f"Tipo de Imóvel: {imovel.tipo}")
        print(f"Aluguel Mensal Calculado: R$ {aluguel:.2f}")
        print(f"Taxa Contratual: R$ 2000.00 (em {parcelas}x de R$ {valor_parcela:.2f})")
        print("-" * 40)
        print(f"Total a pagar nos {parcelas} primeiros meses: R$ {(aluguel + valor_parcela):.2f}")
        print(f"Total a pagar nos meses restantes: R$ {aluguel:.2f}")
        print("="*40)
        
        imovel.gerar_projecao_csv(aluguel, parcelas)

if __name__ == "__main__":
    app = RentSmartApp()
    app.iniciar()
