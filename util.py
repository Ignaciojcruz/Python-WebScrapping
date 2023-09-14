import pandas as pd
import requests
from bs4 import BeautifulSoup
from parametros import MULTIFONDOS, URL
from datetime import date 

def strip_number(number):   
    number = number.strip()

    if number == '-':
        return 0   

    number = number.replace('.', '')
    number = number.replace(',', '.')
    return float(number) 

def scrap_aum(row, df, multifondos=MULTIFONDOS):  

    td = row.find_all('td')
    identificador = td[0].text.strip() 

    if identificador == '':
        identificador = 'Entidades Extranjeras' 

    for index, data in enumerate(td[2:len(td) - 2]):
        aum = strip_number(data.text)

        if aum != 0:
            df['Identificador'].append(identificador)
            df['Multifondo'].append(MULTIFONDOS[index])
            df['AUM'].append(aum)                    

def scrap_SP(url):   

    df = {'Identificador': [],
          'Multifondo': [],
          'AUM': []}   

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')  

    # 1. EMPRESAS EXTRANJERAS
    eex = soup.find(text='EMPRESAS EXTRANJERAS').parent.find_next('tr')
    while 'TOTAL EMPRESAS EXTRANJERAS' not in eex.text:  
        scrap_aum(eex, df)
        eex = eex.find_next('tr') 

    # 2. ESTADOS EXTRANJEROS    
    ee = soup.find(text='ESTADOS EXTRANJEROS').parent.find_next('tr')
    while 'TOTAL ESTADOS EXTRANJEROS' not in ee.text:  
        scrap_aum(ee, df)
        ee = ee.find_next('tr') 

    # 3. ENTIDADES BANCARIAS INTERNACIONALES
    ebi = soup.find(text='ENTIDADES BANCARIAS INTERNACIONALES').parent.find_next('tr')
    while 'TOTAL ENTIDADES BANCARIAS INTERNACIONALES' not in ebi.text:  
        scrap_aum(ebi, df)
        ebi = ebi.find_next('tr')
 
    # 4. ENTIDADES BANCARIAS EXTRANJERAS
    ebe = soup.find(text='ENTIDADES BANCARIAS EXTRANJERAS').parent.find_next('tr')
    while 'TOTAL ENTIDADES BANCARIAS EXTRANJERAS' not in ebe.text:  
        scrap_aum(ebe, df)
        ebe = ebe.find_next('tr') 

    # 5. TITULOS REPRESENTATIVOS DE INDICES
    etf = soup.find(text='TITULOS REPRESENTATIVOS DE INDICES').parent.find_next('tr')
    while 'TOTAL TITULOS REPRESENTATIVOS DE INDICES' not in etf.text:  
        scrap_aum(etf, df)
        etf = etf.find_next('tr') 

    # 6. FONDOS MUTUOS Y DE INVERSION EXTRANJEROS
    fme = soup.find(text='FONDOS MUTUOS Y DE INVERSION EXTRANJEROS').parent.find_next('tr')
    while 'TOTAL FONDOS MUTUOS Y DE INVERSION EXTRANJEROS' not in fme.text:  
        scrap_aum(fme, df)
        fme = fme.find_next('tr') 

    # 7. FONDOS DE INVERSION Y FONDOS MUTUOS NACIONALES (1)    
    fmn = soup.find(text='FONDOS DE INVERSION Y FONDOS MUTUOS NACIONALES (1)').parent.find_next('tr')
    while 'TOTAL FONDOS DE INVERSION Y FONDOS MUTUOS NACIONALES (2)' not in fmn.text:  
        scrap_aum(fmn, df)
        fmn = fmn.find_next('tr') 

    # 8. ACTIVOS ALTERNATIVOS
    aa = soup.find(text='TOTAL FONDOS DE INVERSION Y FONDOS MUTUOS NACIONALES (2)').parent.find_next('tr')  #Se deja ese texto ya que la información en la página no contiene titulo
    while 'TOTAL ACTIVOS ALTERNATIVOS' not in aa.text:  
        if aa.text == '':
            aa = aa.find_next('tr')            
        
        scrap_aum(aa, df)
        aa = aa.find_next('tr')                       

    return pd.DataFrame(df)
 
def get_date(months_ago=1):   
    today = date.today()   
    month = (int(today.month) - months_ago) if (int(today.month) - months_ago) > 1 else 12
    month = '0' + str(month) if (len(str(month)) == 1) else str(month)
    year = str(today.year)   

    return year + month # YYYYMM
      
def match_missing(last_db, new_db):   
    new_db['Isin'] = new_db['Identificador']   
    new = last_db.merge(new_db, on=['Isin', 'Multifondo'], how='outer')
    new['AUM'] = new['AUM'].fillna(0)   
    new = new[['Isin', 'Multifondo', 'AUM']]
    new.columns = ['Identificador', 'Multifondo', 'AUM']  

if __name__ == "__main__":
    input("EL ARCHIVO A CORRER ES main.py. Por favor, cierre este archivo.")

 

 

 

 

 

 

 

 

 

 

 

 

 

 