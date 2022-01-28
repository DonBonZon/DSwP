import json
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir= r"C:\Users\DonBo\Desktop\Dev\dswpProject\instantclient_21_3")

def read_json(path):
    file = open("credentials.json", "r")
    content = json.load(file)
    file.close()
    return content


def get_credentials(path):
    content = read_json(path)
    user = content["USER"]
    password = content["PASSWORD"]
    url = content["URL"]
    port = content["PORT"]
    return (user, password, url, port)


def connect_to_db():
    credentials = get_credentials("credential.json")
    full_url = f"{credentials[2]}:{credentials[3]}"

    dsn_tns = cx_Oracle.makedsn(credentials[2], credentials[3], service_name="orcl")
    cnn = cx_Oracle.connect(user=credentials[0], password=credentials[1], dsn=dsn_tns)

    print(f"Successfully connected to {credentials[2]}")

    return cnn
