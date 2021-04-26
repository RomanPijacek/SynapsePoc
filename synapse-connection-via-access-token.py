from msrestazure.azure_active_directory import AADTokenCredentials
from datetime import datetime
import pyodbc
import struct
import adal

def authenticate_device_code():

    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = '45597f60-6e37-4be7-acfb-4c9e23b261ea' #SwissReTenantID
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://database.windows.net/'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46' # Global Client ID

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials

credentials = authenticate_device_code()
token = credentials.token['access_token']
dateTimeObj = datetime.now()

print('test_time_stamp = ', dateTimeObj)
print('token_details = ', credentials.token)

token_bytes = token.encode('utf-16-le')
token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
connection_string = 'driver=ODBC Driver 17 for SQL Server;server=synapsewsatelierdev-ondemand.sql.azuresynapse.net;database=master'

SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h

cnxn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

cursor = cnxn.cursor()
#Sample select query
cursor.execute("SELECT @@version;") 

row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()

"""

from msrestazure.azure_active_directory import AADTokenCredentials
from datetime import datetime
import adal
import pyodbc
import struct

connection_string = 'driver=ODBC Driver 17 for SQL Server;server=synapsewsatelierdev-ondemand.sql.azuresynapse.net;database=master'
SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
dateTimeObj = datetime.now()

def authenticate_device_code():

    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = '45597f60-6e37-4be7-acfb-4c9e23b261ea'
    authority_uri = authority_host_uri + '/' + tenant
    resource_uri = 'https://management.core.windows.net/'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    credentials = AADTokenCredentials(mgmt_token, client_id)

    return credentials

credentials = authenticate_device_code()
token = credentials.token['access_token'].encode('utf-16-le')
exptoken = b"";

print('test_time_stamp = ', dateTimeObj)
print('token_details = ', credentials.token)

for i in token:
    exptoken += bytes({i});
    exptoken += bytes(1);
tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;
conn = pyodbc.connect(connection_string, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct });

"""
