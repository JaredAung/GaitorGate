import csv 
import mysql.connector
import bcrypt

## READ CSV DATASET INTO MYSQL DATABASE

def read_csv(file_path):
    
    mydb = mysql.connector.connect(**database_config)
    cursor = mydb.cursor()
    # Read the CSV file
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            thumbnail_url = row.get('logo_url').strip()
            company_name = row.get('company_name').strip()
            task = row.get('primary_task').strip()  #category
            task1 = row.get('applicable_tasks').strip() #keywords
            description = row.get('full_description').strip()
            price = row.get('pricing').strip()
            url = row.get('visit_website_url').strip()
            password = '12345'
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            print(f"Thumbnail URL: {thumbnail_url}")
            print(f"Company Name: {company_name}")
            print(f"Task1: {task1}")
     

                # INSERT COMPANY

            cursor.execute("SELECT idAccount FROM Company WHERE company_name = %s", (company_name,))
            idCompany = cursor.fetchone()
            if idCompany:
                idCompany = idCompany[0]
            else:
                cursor.execute("INSERT INTO User(name) VALUES (%s)", (company_name,))
                mydb.commit()
                idUser = cursor.lastrowid

                cursor.execute("INSERT INTO Account (idUser, email, hashed_password, username, Account_Type) VALUES (%s,%s,%s,%s,%s)", (idUser,company_name,hashed_password,company_name,"Company"))
                mydb.commit()
                idAccount = cursor.lastrowid
                cursor.execute("INSERT INTO Company (idAccount, company_name, website) VALUES (%s,%s,%s)", (idAccount,company_name,url))
                mydb.commit()
                cursor.execute("SELECT idAccount FROM Company WHERE company_name = %s", (company_name,))
                idCompany = cursor.fetchone()[0]
            
            # INSERT TOOL
            cursor.execute("SELECT idTool FROM Tools WHERE name = %s", (company_name,))
            idTool = cursor.fetchone()
            if idTool:
                idTool = idTool[0]
            else:
                cursor.execute("INSERT INTO Tools (name, description, url, thumbnail_url, company, pricing) VALUES (%s,%s,%s,%s,%s,%s)", (company_name,description,url,thumbnail_url,idCompany,price))
                mydb.commit()
                idTool = cursor.lastrowid

                # INSERT CATEGORY
                cursor.execute("SELECT idCategory FROM Category WHERE name = %s", (task,))
                idCategory = cursor.fetchone()[0]

                # INSERT INDEX
                cursor.execute("SELECT idIndex FROM SearchIndex WHERE idTool = %s", (idTool,))
                idIndex = cursor.fetchone()
                if idIndex:
                    idIndex = idIndex[0]
                else:
                    cursor.execute("INSERT INTO SearchIndex (idTool, idCategory) VALUES (%s,%s)", (idTool,idCategory))
                    mydb.commit()
                    idIndex = cursor.lastrowid
                
                # INSERT PLATFORM
                platform = 4

                cursor.execute("INSERT IGNORE INTO IndexPlatform (idIndex, idPlatform) VALUES (%s,%s)", (idIndex,platform))
                mydb.commit()
            

                #INSERT keywords
                keywords = task1.split(",")

                for keyword in keywords:
                    keyword = keyword.strip()
                    cursor.execute("SELECT idKeywords FROM Keywords WHERE name = %s", (keyword,))
                    idKeyword = cursor.fetchone()
                    if idKeyword:
                        idKeyword = idKeyword[0]
                    else:
                        cursor.execute("INSERT INTO Keywords (name) VALUES (%s)", (keyword,))
                        mydb.commit()
                        idKeyword = cursor.lastrowid
                    print(f"Keyword: {keyword}, ID: {idIndex}")

                    cursor.execute("INSERT IGNORE INTO Keywords_Indexes (IndexID, keywordID) VALUES (%s,%s)", (idIndex,idKeyword))
                    mydb.commit()

                
            




    return data

if __name__ == "__main__":
    # Example usage
    file_path = 'application/static/dataset/tools.csv'

    database_config = {
        'host': '18.222.76.244',
        'user': 'team3admin',
        'password': '12345',
        'database': 'TestDb'
    }
    data = read_csv(file_path)
   



