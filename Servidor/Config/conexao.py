import pyodbc

create_connection = pyodbc.connect(
    'DRIVER = {MySQL ODBC 8.0 Driver};'
    'SERVER = localhost;'
    'DATABASE = ORBITRA;'
    'UID = seu_usuario;'
    'PWD = Administrador123;'
);
