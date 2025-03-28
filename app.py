import pdfplumber
import pandas as pd
import zipfile
import os


def compactar(arquivo, nome):
    zip_path = os.path.join(pasta_saida, f'Teste_{nome}.zip')
    
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w') as ziparquivo:
        ziparquivo.write(arquivo, os.path.basename(arquivo))

    
print("Deseja colar o caminho do arquivo PDF ou usar o caminho padrão dessa pasta?")
print("1 - Para usar caminho padrão da pasta")
print("2 - Para colar novo caminho")
print('\n')

pasta_saida = 'arquivos_saida'
if not os.path.exists('arquivos_saida'):
    os.makedirs('arquivos_saida')

while True:
    try:
        opcao = int(input('1 ou 2:'))
        if opcao == 1:
            caminho_arquivo = ("AnexoPdf\\Anexo_1.pdf")
            print('Prosseguindo com processo...')
            print('\n')
            break
        
        elif opcao == 2:
            caminho = input('Cole o caminho do arquivo PDF desejado:')
            caminho_arquivo = caminho.replace("\\", '\\\\')
            print('Prosseguindo com processo...')
            print('\n')
            break
        
        else:
            print("Digite apenas 1 ou 2")
    
    except ValueError:
        print("Digite um valor NUMÉRICO entre 1 e 2")

with pdfplumber.open(caminho_arquivo) as pdf:
    # Bloco de extração das tabelas do PDF(por páginas)
    todas_tabelas = []

    for page in pdf.pages:
        tabela = page.extract_table()
        if tabela is not None:
            todas_tabelas.append(tabela)
    print('Tabelas extraídas')

    # Bloco de extração dos data frames com o conteúdo de cada tabela
    if todas_tabelas:
        todos_dfs = []

        df_primeira_tabela = pd.DataFrame(todas_tabelas[0])
        todos_dfs.append(df_primeira_tabela)

        for tabela in (todas_tabelas[1:]):
            df = pd.DataFrame(tabela[1:]).fillna("")
            todos_dfs.append(df)

        # Concatenando todos os data frames e gerando o arquivo csv
        df_final = pd.concat(todos_dfs)
        arquivo_csv = os.path.join(pasta_saida,"TabelaAnexo1.csv")
        df_final.to_csv(arquivo_csv, index=False, header=False)

        if df_final is not None:
            print('Tabela estruturada em formato csv.')
            compactar(arquivo_csv, "Gabriel_Rodrigues")

        # Bloco de edição das abreviações das colunas OD e AMB
        novo_df = pd.read_csv(arquivo_csv)
        novo_df.rename(columns={'OD': 'Seg.Odontológica',
                       'AMB': 'Seg.Ambulatorial'}, inplace=True)
        arquivo_modificado = os.path.join(pasta_saida,'Modificado.csv')
        novo_df.to_csv(arquivo_modificado, index=False)

        print("Títulos das colunas OD e AMB alterados no arquivo 'Modificado.csv'")
