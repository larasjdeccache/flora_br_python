import pandas as pd
import difflib
import zipfile


with zipfile.ZipFile('dwca-lista_especies_flora_brasil-v393.222.zip') as zip:
            with zip.open('taxon.txt') as myZip:
                flora_df = pd.read_csv(myZip, sep='\t', low_memory=False)
                
my_species=pd.read_csv("my_species.csv")

flora_df.head()

flora_df.tail()

flora_df.shape


# Primeiramente, criando um nova coluna scientificName1, a partir da remoção dos autores de scientificName
flora_df['scientificName1'] = flora_df.apply(lambda row : row['scientificName'].replace(str(row['scientificNameAuthorship']), ''), axis=1)

# Depois, removendo um "espaço" que ficou residual, no final de 'scientificName1
flora_df['scientificName1'] = flora_df['scientificName1'].str.rstrip()
flora_df

possibilities = flora_df['scientificName1']
species_typo_corrected = my_species['species'].apply(lambda row: difflib.get_close_matches(row, possibilities, n=1) [0] if difflib.get_close_matches(row, possibilities) else row)

species_typo_corrected.df = pd.DataFrame(species_typo_corrected)
species_typo_corrected.columns=['species']
species_typo_corrected.df

species_syno_corrected=[]

for species in species_typo_corrected:
    
    line = flora_df[flora_df['scientificName1'] == species]
    accepted_name = line["acceptedNameUsage"]
    species_syno_corrected.append(list(accepted_name))
    species_syno_corrected_df=pd.DataFrame(species_syno_corrected) 
    final_table=pd.concat([species_typo_corrected, species_syno_corrected_df],  axis = 1) 
    final_table.columns =['Species', 'Correction']
    final_table['Correction'] = final_table.apply(lambda x: x['Species'] if pd.isnull(x['Correction']) else x['Correction'], axis=1)
    final_table['Correction'] = final_table['Correction'].str.extract(r'(^\w*\s*\w*)')
    
    
    

final_table


def flora_clean (flora_df):
    ''' flora_df = arquivo importado a partir do banco de dados da Flora do Brasil'''
    
    flora_df['scientificName1'] = flora_df.apply(lambda row : row['scientificName'].replace(str(row['scientificNameAuthorship']), ''), axis=1)
    flora_df['scientificName1'] = flora_df['scientificName1'].str.rstrip()
    return flora_df

# Função flora_typo_correct, para correcao de erros tipográficos

def flora_typo_correct (my_species,flora_clean):
   
    ''' 
    my_species = arquivo importado a partir da listagem florística a ser corrigida
    flora_clean = Arquivo da Flora do Brasil limpo, após a aplicação da função flora_clean
    
    '''
    
    possibilities = flora_clean['scientificName1']
    species_typo_corrected = my_species['species'].apply(lambda row: difflib.get_close_matches(row, possibilities, n=1) [0] if difflib.get_close_matches(row, possibilities) else row)
    species_typo_corrected.df = pd.DataFrame(species_typo_corrected)
    species_typo_corrected.columns=['species']
    species_typo_corrected.df
    return species_typo_corrected.df


def flora_accepted_names(my_species_clean, data_clean):
    
    ''' 
    my_clean_species = lista florística corrigida, a partir da aplicação de flora_typo_correct
    flora_clean = Arquivo da Flora do Brasil limpo, após a aplicação da função flora_clean
    
    '''
    
    species_syno_corrected=[]
    
    for species in my_species_clean['species']:
        
        line = data_clean[data_clean['scientificName1'] == species]
        accepted_name = line["acceptedNameUsage"]
        species_syno_corrected.append(list(accepted_name))
        species_syno_corrected_df=pd.DataFrame(species_syno_corrected) 
        final_table=pd.concat([my_species_clean, species_syno_corrected_df],  axis = 1) 
        final_table.columns =['Species', 'Correction']
        final_table['Correction'] = final_table.apply(lambda x: x['Species'] if pd.isnull(x['Correction']) else x['Correction'], axis=1)
        final_table['Correction'] = final_table['Correction'].str.extract(r'(^\w*\s*\w*)')
    return final_table

    with zipfile.ZipFile('dwca-lista_especies_flora_brasil-v393.222.zip') as zip:
            with zip.open('taxon.txt') as myZip:
                data_df = pd.read_csv(myZip, sep='\t', low_memory=False)
                
minha_lista=pd.read_csv("my_species.csv")

data_clean=flora_clean(data_df)

data_clean

my_species_clean=flora_typo_correct(minha_lista, data_clean)

flora_accepted_names(my_species_clean, data_clean)