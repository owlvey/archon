import requests
from requests.auth import HTTPBasicAuth


class GrafanaGateway:

    def __init__(self, host, username, password) -> None:
        self.host = host
        self.username = username
        self.password = password
        

    def create_datasource(self, dbuser, dbpassword, dbhost, dbport, database, name):        
        datasource = {    
            "name": name,
            "type": "mysql",    
            "access": "proxy",
            "url": f"{dbhost}:{dbport}",
            "password": dbpassword,
            "user": dbuser,
            "database": database,  
            "isDefault": True
        }
        url = f"{self.host}/api/datasources"
        response = requests.post(url, json=datasource, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code > 299:
            if response.status_code == 409:
                pass
            else:
                raise ValueError(response.text + str(response.status_code))
    
    def create_folder(self, name):        
        datasource = {    
            "title": name,            
        }
        url = f"{self.host}/api/folders"
        response = requests.post(url, json=datasource, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code > 299:
            if response.status_code == 400:
                pass
            else:
                raise ValueError(response.text + str(response.status_code))
        
    def get_folders(self):
        url = f"{self.host}/api/folders"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code > 299:            
            raise ValueError(response.text + str(response.status_code))
        return response.json()

    
    def create_dashboard(self, folder, definition: dict ):        
        dashboard = {    
            "dashboard": definition,            
            "folderId": folder,
            "overwrite": True
        }
        url = f"{self.host}/api/dashboards/db"
        response = requests.post(url, json=dashboard, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code > 299:            
            raise ValueError(response.text + str(response.status_code))
        




