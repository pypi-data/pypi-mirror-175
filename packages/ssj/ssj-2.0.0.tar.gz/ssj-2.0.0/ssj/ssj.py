# imports are in defs bellow! 
#dropbox, threading, socket, pathlib, tinydb, nested_dict, cryptography, json, ast

class PathListEmpty(Exception):
    pass

class DataError(Exception):
    pass

class ServerError(Exception):
    pass

class DatabaseEncrypted(Exception):
    pass

class SaveData(Exception):
    pass

class PathError(Exception):
    pass

def send_msg_sock(msg, sock, key_f=None):
    if key_f == None:
        global key_tinydb
    else:
        key_tinydb = key_f
    fernet = Fernet(key_tinydb)
    sock.send(fernet.encrypt(msg.encode('utf-8')))
    sock.recv(512) # recive confirmation

def recvall(sock, key_f=None):
    if key_f == None:
        global key_tinydb
    else:
        key_tinydb = key_f
    fernet = Fernet(key_tinydb)
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    sock.send(b'Confirmation message')
    return fernet.decrypt(data)

def messagesTreatment(client):
    global server_is_running
    global editando
    global maintenance_use
    global path_dir_client
    path_dir_client = []
    while True:
        try:
            try:
                msg = recvall(client, key_tinydb)
            except:
                break
            if msg != None:
                msg = msg.decode('utf-8')
            else:
                continue
            if msg == 'close_client':
                break
            elif msg == 'active_threads_at_moment':
                send_msg_sock(f'Threads at moment: {threading.active_count()}', client)
            elif msg == 'close_server':
                if maintenance_use:
                    close(True)
                    server_is_running = False
                    #('mandou fechar')
                    break
            elif msg == 'unlock':
                editando = False
            elif msg == 'lock':
                editando = True
            elif msg == 'backup':
                if maintenance_use:
                    send_msg_sock(str(backup()), client)
            elif msg == 'recover_backup':
                if maintenance_use:
                    send_msg_sock(str(recover_backup()), client)
            elif 'verify_key;' in msg:
                key_recived = msg.replace('verify_key;', '').encode('utf-8')
                if key_recived == key_tinydb:
                    maintenance_use = True
                    send_msg_sock('Autorizado', client)
                    break
                else:
                    send_msg_sock('Não autorizado', client)
                    break
            else:
                comando(msg, client)
        except:
            break

def comando(msg, client):
    global path_dir_client
    cmm = msg
    if cmm == 'dirfdb':
        resp = str(dirfdb(path_dir_=path_dir_client))
        if resp == None:
            send_msg_sock('Empty', client)
        else:
            send_msg_sock(resp, client)
            
    elif cmm[:13] == 'update_infodb':
        if cmm.count(';') == 1:
            cmm = cmm.split(';')[1]
            if cmm[0] == '[':
                cmm = str_to_list(cmm)
                update_infodb(cmm, path_dir_=path_dir_client)
            elif cmm[0] == '{':
                cmm = str_to_dict(cmm)
                update_infodb(cmm, path_dir_=path_dir_client)
            elif cmm[0] == '"' or cmm[0] == "'":
                update_infodb(cmm.replace('"', '').replace("'", ''), path_dir_=path_dir_client)
            elif '.' in cmm:
                update_infodb(float(cmm), path_dir_=path_dir_client)
            else:
                update_infodb(int(cmm), path_dir_=path_dir_client)
        else:
            cmm = cmm.split(';')[1]
            if cmm[0] == '[':
                cmm = str_to_list(cmm)
                update_infodb(cmm, True, path_dir_=path_dir_client)
            elif cmm[0] == '{':
                cmm = str_to_dict(cmm)
                update_infodb(cmm, True, path_dir_=path_dir_client)
            elif cmm[0] == '"' or cmm[0] == "'":
                update_infodb(cmm.replace('"', '').replace("'", ''), True, path_dir_=path_dir_client)
            elif '.' in cmm:
                update_infodb(float(cmm), True, path_dir_=path_dir_client)
            else:
                update_infodb(int(cmm), True, path_dir_=path_dir_client)
                
    elif cmm[:12] == 'salva_infodb':
        cmm = cmm.split(';')[1]
        if cmm[0] == '{':
            salva_infodb(str_to_dict(cmm))
        else:
            salva_infodb(cmm)
    
    elif cmm[:5] == 'cdadd':
        cmm = cmm.split(';')[1]
        arg = False
        if ', True' in cmm or ',True' in cmm:
            arg = True
            cmm = cmm.replace(', True', '').replace(',True', '')
            path_dir_client = cdadd(cmm, arg, path_dir_=path_dir_client)
        if cmm[0] == '[':
            cmm = str_to_list(cmm)
            path_dir_client = cdadd(cmm, arg, path_dir_=path_dir_client)
        elif cmm[0] == '"' or cmm[0] == "'":
            cmm = cmm.replace('"', '').replace("'", '')
            path_dir_client = cdadd(cmm, arg, path_dir_=path_dir_client)
        elif '.' in cmm:
            path_dir_client = cdadd(float(cmm), arg, path_dir_=path_dir_client)
        else:
            path_dir_client = cdadd(int(cmm), arg, path_dir_=path_dir_client)
    
    elif 'close' in cmm:
        close()
    
    elif cmm[:13] == 'remove_infodb':
        if ';' in cmm:
            remove_infodb(str_to_list(cmm.split(';')[1]), path_dir_=path_dir_client)
        else:
            remove_infodb(path_dir_=path_dir_client)
    
    elif cmm == 'formata_db':
        formata_db()
    
    elif cmm == 'pwdb':
        send_msg_sock(str(pwdb(path_dir_=path_dir_client)), client)
    
    elif cmm[:5] == 'cdmin':
        if ';' in cmm:
            path_dir_client = cdmin(int(cmm.split(';')[1]), path_dir_=path_dir_client)
        else:
            path_dir_client = cdmin(path_dir_=path_dir_client)
            
    else:
        pass

def str_to_dict(string):
    return literal_eval(string)

def str_to_list(string):
    return literal_eval(string)

def lock():
    if client_use:
        send_msg_sock('lock', client)

def conta_users():
    if client_use:
        send_msg_sock('active_threads_at_moment', client)
        return recvall(client).decode('utf-8')

def unlock():
    #
    if client_use:
        send_msg_sock('unlock', client)
        
def recover_backup():
    #
    if client_use:
        send_msg_sock('recover_backup', client)
    else:
        try:
            if maintenance_use:
                global editando
                while editando:
                    pass
                editando = True
                global is_closed
                try:
                    dbx = dropbox.Dropbox(tokent)
                    with open(name_of_tinydb_path, 'wb') as f:
                        metadata, result = dbx.files_download(path=f'/backup/{name_of_tinydb_path}')
                        f.write(result.content)
                except Exception as e:
                    raise e
                try:
                    with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                        storage_before_decrypt = tiny_db_storage.read()
                    try:
                        storage_after_decrypt = Fernet(key_tinydb).decrypt(storage_before_decrypt)
                    except:
                        try:
                            close(True)
                            with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                                storage_before_decrypt = tiny_db_storage.read()
                            storage_after_decrypt = Fernet(key_tinydb).decrypt(storage_before_decrypt)
                        except:
                            raise DatabaseEncrypted('Database is encryptaded! Probably caused by an not closed use or an incorrect key!')
                    
                    with open(name_of_tinydb_path, 'wb') as tiny_db_storage:
                        tiny_db_storage.write(storage_after_decrypt)
                    tiny_db = TinyDB(name_of_tinydb_path)
                    is_closed = False
                except:
                    pass
            else:
                raise ServerError('This command is just for maintenance only!')
        except Exception as error_temp:
            editando = False
            return str(error_temp)
        else:
            editando = False
            return 'Restauração realizada com sucesso!'


def backup():
    #
    global client
    if client_use:
        send_msg_sock('backup', client)
        retorno_server = recvall(client, key_tinydb).decode('utf-8')
        if retorno_server == 'Error!':
            sleep(1)
            client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client1.connect((ip_server_local, port_server_local))
            send_msg_sock('change_editing_state', client1)
            sleep(1)
            client1.close()
            client.close()
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip_server_local, port_server_local))
        return retorno_server
    else:
        global editando
        try:
            if maintenance_use:
                while editando:
                    pass
                editando = True
                global is_closed
                close(True)
                try:
                    try:
                        dbx = dropbox.Dropbox(tokent)
                    except:
                        editando = False
                        raise ServerError('Error to make backup, check the token!')
                    local_file_path = Path('.') / name_of_tinydb_path
                    try:
                        with local_file_path.open("rb") as f:
                            meta = dbx.files_upload(f.read(), f'/backup/{name_of_tinydb_path}', mode=dropbox.files.WriteMode("overwrite"))
                    except:
                        editando = False
                        raise ServerError('Error to make backup, check the token!')
                except:
                    editando = False
                    raise ServerError('An error ocurred to make backup, check the token')
                try:
                    with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                        storage_before_decrypt = tiny_db_storage.read()
                    try:
                        storage_after_decrypt = Fernet(key_tinydb).decrypt(storage_before_decrypt)
                    except:
                        try:
                            close(True)
                            with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                                storage_before_decrypt = tiny_db_storage.read()
                            storage_after_decrypt = Fernet(key_tinydb).decrypt(storage_before_decrypt)
                        except:
                            editando = False
                            raise DatabaseEncrypted('Database is encryptaded! Probably caused by an not closed use or an incorrect key!')
                    
                    with open(name_of_tinydb_path, 'wb') as tiny_db_storage:
                        tiny_db_storage.write(storage_after_decrypt)
                    tiny_db = TinyDB(name_of_tinydb_path)
                    is_closed = False
                except:
                    pass
                editando = False
            else:
                editando = False
                raise ServerError('This command is just for maintenance only!')
        except Exception as error_temp:
            editando = False
            return 'Error!'
        else:
            editando = False
            return 'Backup realizado com sucesso!'
            


def update_infodb(valor_atualizar, just_append=True, path_dir_=None, antiblock=False):
    global editando
    if client_use:
        if type(valor_atualizar) == str:
            send_msg_sock(f'update_infodb;"{valor_atualizar}"', client)
        else:
            if just_append:
                send_msg_sock(f'update_infodb;{str(valor_atualizar)};True', client)
            else:
                send_msg_sock(f'update_infodb;{str(valor_atualizar)}', client)
    else:
        if antiblock == False:
            while editando:
                pass
            editando = True
        if path_dir_ == None:
            global path_dir
        else:
            path_dir = path_dir_[:]
        testa_existe_info = dirfdb(antiblock=True, return_pathed=False)
        if just_append == False:
            qntd_infos_path = len(path_dir)
            if qntd_infos_path == 0:
                if testa_existe_info == None and type(valor_atualizar) != dict:
                    raise DataError('Path list is empty and value to save isnt a dict!')
                elif testa_existe_info != None:
                    raise PathListEmpty('List that contains path to update db must not be empty!')
                else:
                    salva_infodb(valor_atualizar, antiblock=True)
                    editando = False
                    return
                
            contador_exect = 1
            dict_pushed = dirfdb(antiblock=True, return_pathed=False)
            if dict_pushed == None:
                dict_saved_in_db = nested_dict()
            else:
                dict_saved_in_db = nested_dict(dict_pushed)
            if qntd_infos_path > 0:
                for path_in_list in path_dir:
                    if contador_exect == 1:
                        current = dict_saved_in_db[path_in_list]
                    elif qntd_infos_path - contador_exect == 0:
                        current[path_in_list] = valor_atualizar
                        
                    else:
                        current = current[path_in_list]
                    contador_exect += 1
            else:
                dict_saved_in_db[path_dir[0]] = valor_atualizar
            dict_saved_in_db = dict(dict_saved_in_db)
            salva_infodb(dict_saved_in_db, antiblock=True)
            if antiblock == False:
                editando = False
        elif just_append == True:
            resultado_volta_db = dirfdb(antiblock=True)
            if type(valor_atualizar) == dict and type(resultado_volta_db) != str:
                temp_list = list()
                temp_list = path_dir[:]
                path_dir_backup = path_dir[:]
                for k, v in valor_atualizar.items():
                    temp_list.append(k)
                    update_infodb(v, antiblock=True, path_dir_=temp_list, just_append=False)
                    temp_list.pop(-1)
                path_dir = path_dir_backup[:]
            else:
                update_infodb(valor_atualizar, antiblock=True, just_append=False)
            editando = False
        editando = False

def generate_key():
    return Fernet.generate_key()

def inicia_localdb(path_db_local_local, key_local_db_db=b'', token_drop_local=''):
    global Query, where, delete, nested_dict, Fernet, dumps, loads, literal_eval, dropbox, Path, AuthError, TinyDB, sleep
    import dropbox
    from dropbox.exceptions import AuthError
    from pathlib import Path
    from tinydb import TinyDB, Query, where
    from tinydb.operations import delete
    from nested_dict import nested_dict
    from cryptography.fernet import Fernet
    from time import sleep
    from json import dumps, loads
    from ast import literal_eval
    inicia_db(path_to_jsontiny=path_db_local_local, key_decript=key_local_db_db, token_drop=token_drop_local)

def inicia_client(ip_to_connect, port_to_connect, key_to_verify):
    global sleep, dumps, loads, socket, literal_eval, Fernet
    from time import sleep
    from json import dumps, loads
    from cryptography.fernet import Fernet
    from ast import literal_eval
    import socket
    key_decoded = key_to_verify.decode('utf-8')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip_to_connect, port_to_connect))
    except:
        raise ServerError('Server probably is offline!')
    send_msg_sock(f'verify_key;{key_decoded}', client, key_to_verify)
    try:
        resp = recvall(client, key_to_verify).decode('utf-8')
    except:
        raise ServerError('Key is incorrect!')
    if resp != 'Autorizado':
        client.close()
        client = ''
        raise ServerError('Key is incorrect!')
    else:
        client.close()
        client = ''
        maintenance_use = True
    inicia_db(ip_host_server=ip_to_connect, port_host_server=port_to_connect, client_server=True)

def inicia_host(path_db_local_local, ip_to_connect, port_to_connect, key_local_db_db=b'', token_drop_local=''):
    global Query, where, delete, sleep, nested_dict, Fernet, dumps, loads, literal_eval, threading, dropbox, socket, Path, AuthError, TinyDB
    import dropbox
    import threading
    import socket
    from dropbox.exceptions import AuthError
    from pathlib import Path
    from tinydb import TinyDB, Query, where
    from tinydb.operations import delete
    from nested_dict import nested_dict
    from cryptography.fernet import Fernet
    from json import dumps, loads
    from ast import literal_eval
    from time import sleep
    inicia_db(path_to_jsontiny=path_db_local_local, key_decript=key_local_db_db, token_drop=token_drop_local, ip_host_server=ip_to_connect, port_host_server=port_to_connect, host_server=True)

def inicia_manutencao(ip_to_connect, port_to_connect, key_local_db_db=b''):
    global sleep, dumps, loads, socket, Fernet, literal_eval
    import socket
    from time import sleep
    from ast import literal_eval
    from json import dumps, loads
    from cryptography.fernet import Fernet
    
    key_decoded = key_local_db_db.decode('utf-8')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip_to_connect, port_to_connect))
    except:
        raise ServerError('Server probably is offline!')
    send_msg_sock(f'verify_key;{key_decoded}', client, key_local_db_db)
    resp = recvall(client, key_local_db_db).decode('utf-8')
    if resp != 'Autorizado':
        client.close()
        client = ''
        raise ServerError('Key is incorrect!')
    
    else:
        client.close()
        client = ''
        inicia_db(ip_host_server=ip_to_connect, port_host_server=port_to_connect, client_server=True, maintenance_antiblock=True)

    
def inicia_db(path_to_jsontiny='', key_decript=b'', client_server=False, host_server=False, ip_host_server='', port_host_server='', token_drop='', maintenance_antiblock=False):
    global maintenance_use
    global buscador_db
    global tiny_db
    global thread
    global path_dir
    global is_closed
    global contador_exec
    global server_is_running
    global key_tinydb
    global name_of_tinydb_path
    global tokent
    global client_use
    global client
    global host_use
    global editando
    global ip_server_local
    global port_server_local
    if maintenance_antiblock == True:
        maintenance_use = True
    else:
        maintenance_use = False
    ip_server_local = ip_host_server
    port_server_local = port_host_server
    is_closed = False
    editando = False
    server_is_running = True
    tokent = token_drop
    host_use = host_server
    client_use = client_server
    key_not_exist = False
    name_of_tinydb_path = path_to_jsontiny
    if client_use and host_use:
        raise ServerError('Client use and host use must not is True at same time!')
    
    if client_server == False:
        if key_decript == b'':
            key_not_exist = True
            print('Key of your db is:')
            key_tinydb = Fernet.generate_key()
            print(key_tinydb)
        else:
            key_tinydb = key_decript
        if key_not_exist:
            tiny_db = TinyDB(name_of_tinydb_path)
            is_closed = False
        else:
            try:
                with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                    storage_before_decrypt = tiny_db_storage.read()
                try:
                    storage_after_decrypt = Fernet(key_tinydb).decrypt(storage_before_decrypt)
                except:
                    try:
                        close()
                        with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                            storage_before_decrypt = tiny_db_storage.read()
                        storage_after_decrypt = Fernet(key_tinydb).decrypt(storage_before_decrypt)
                    except:
                        raise DatabaseEncrypted('Database is encryptaded! Probably caused by an not closed use or an incorrect key!')
                
                with open(name_of_tinydb_path, 'wb') as tiny_db_storage:
                    tiny_db_storage.write(storage_after_decrypt)
                tiny_db = TinyDB(name_of_tinydb_path)
                is_closed = False
            except(FileNotFoundError):
                tiny_db = TinyDB(name_of_tinydb_path)
                is_closed = False
        
        try:
            dirfdb(return_pathed=False)
        except:
            raise DatabaseEncrypted('Database is encrypted!')
        buscador_db = Query()
        path_dir = []
        contador_exec = 0
        if host_use:
            editando = False
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                server.bind((ip_host_server, port_host_server))
                server.listen()
            except:
                return ServerError('Server cant be initialized!')
            while True:
                if server_is_running:
                    print('Threads at moment: ', threading.active_count())
                    client, addr = server.accept()
                    thread = threading.Thread(target=messagesTreatment, args=[client])
                    thread.start()
                else:
                    break
            #('server fechado')
            #(is_closed)
            
        
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((ip_host_server, port_host_server))
        except:
            raise ServerError('Server probably is offline!')

def close_server():
    #
    global editando
    if maintenance_use:
        while editando:
            pass
        editando = True
        send_msg_sock('close_server', client)
        sleep(1)
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect((ip_server_local, port_server_local))
        client1.close()
        
    else:
        raise ServerError('This command can be use only for maintenance, not allowed to host, local db or clients!')

def close_client():
    #
    if client_use:
        send_msg_sock('close_client', client)
        client.close()

def close(travar=False):
    #
    global editando
    if maintenance_use:
        send_msg_sock('close', client)
    elif client_use:
        send_msg_sock('close_client', client)
        client.close()
    else:
        global is_closed
        if is_closed:
            pass
        else:
            if travar:
                pass
            else:
                while editando:
                    pass
            editando = True
            is_closed = True
            global key_tinydb
            fernet_key_processed = Fernet(key_tinydb)
            with open(name_of_tinydb_path, 'rb') as tiny_db_storage:
                storage_before_crypt = tiny_db_storage.read()
                storage_after_crypt = Fernet.encrypt(fernet_key_processed, storage_before_crypt)
                
            with open(name_of_tinydb_path, 'wb') as tiny_db_storage_encrypted:
                tiny_db_storage_encrypted.write(storage_after_crypt)
            
            editando = False

def dirfdb(searchdb=None, antiblock=False, path_dir_=None, return_pathed=True):
    #
    global editando
    if client_use:
        send_msg_sock('dirfdb', client)
        resp = str(recvall(client, key_tinydb).decode('utf-8'))
        if resp[0] == '{':
            return str_to_dict(resp)
        elif resp[0] == '[':
            return str_to_list(resp)
        elif resp == 'Empty' or resp == 'None':
            return None
        else:
            return resp
    else:
        if antiblock == False:
            while editando:
                pass
            editando = True
        if path_dir_ == None:
            global path_dir
        else:
            path_dir = path_dir_
        if searchdb != None:
            path_dir.append(searchdb)
            db = dirfdb(antiblock=True, return_pathed=False)
            for path_use in path_dir:
                db = db[path_use]
            editando = False
            return db
        else:
            data_tinydb_storade = tiny_db.all()
            if len(data_tinydb_storade) > 0:
                if antiblock == False:
                    editando = False
                if return_pathed:
                    data_pushed_tiny = data_tinydb_storade[0]
                    try:
                        for item in path_dir:
                            data_pushed_tiny = data_pushed_tiny[item]
                        return data_pushed_tiny
                    except:
                        return None
                else:
                    return data_tinydb_storade[0]
            else:
                if antiblock == False:
                    editando = False
                return None
        

def salva_infodb(data_db_tiny, antiblock=False):
    #
    global editando
    if client_use:
        send_msg_sock(f'salva_infodb;{str(data_db_tiny)}', client)
    else:
        if antiblock == False:
            while editando:
                pass
            editando = True
        if type(data_db_tiny) != dict:
            raise SaveData('Data to save in database must be a dict!')
        formata_db(antiblock=True)
        tiny_db.insert(data_db_tiny)
        if antiblock == False:
            editando = False

def cdadd(path_to_update, replace_all_path=False, path_dir_=None):
    #
    if client_use:
        if replace_all_path:
            if type(path_to_update) == str:
                send_msg_sock(f'cdadd;"{str(path_to_update)}", True', client)
            else:
                send_msg_sock(f'cdadd;{str(path_to_update)}, True', client)
        else:
            if type(path_to_update) == str:
                send_msg_sock(f'cdadd;"{str(path_to_update)}"', client)
            else:
                send_msg_sock(f'cdadd;{str(path_to_update)}', client)
    else:
        if path_dir_ == None:
            global path_dir
        else:
            path_dir = path_dir_
        if type(path_to_update) == list:
            if replace_all_path:
                path_dir = path_to_update
            else:
                for item_path_new in path_to_update:
                    path_dir.append(item_path_new)
        else:
            if len(str(path_to_update)) > 2 and '/' in path_to_update:
                return cdadd(path_to_update.split('/'), True)
                
            if replace_all_path:
                path_dir = []
                if path_to_update != '-' or path_to_update != '/':
                    path_dir.append(path_to_update)
            else:
                if path_to_update == '-' or path_to_update == '/':
                    path_dir = []
                else:
                    path_dir.append(path_to_update)
        return path_dir

def remove_infodb(path_delete=None, path_dir_=None, antiblock=False):
    global editando
    if client_use:
        if path_delete != None:
            send_msg_sock(f'remove_infodb;{str(path_delete)}', client)
        else:
            send_msg_sock('remove_infodb', client)
    else:
        if antiblock == False:
            while editando:
                pass
            editando = True
        if path_dir_ == None:
            global path_dir
        else:
            path_dir = path_dir_
        if path_delete == None:
            path_delete = path_dir
            if len(path_delete) == 0:
                raise PathListEmpty('List that contains path to update db must not be empty!')
        if type(path_delete) != list:
            raise TypeError('Path to delete must be a list!')
        db_returned = dirfdb(antiblock=True, return_pathed=False)
        for item_path_temp in path_dir:
            try:
                db_returned = db_returned[item_path_temp]
            except:
                raise PathError('Path to delete doesnt exists! Verify them!')
        global contador_exec
        db_delete = dirfdb(antiblock=True, return_pathed=False)
        if db_delete == None:
            pass
        else:
            db_delete = nested_dict(db_delete)
            contador_exec += 1
            qntd_path_delete = len(path_delete)
            contador_delete = 1
            if qntd_path_delete == 1:
                del db_delete[path_delete[0]]
            else:
                for item in path_delete:
                    if contador_delete == 1:
                        current = db_delete[item]
                    elif qntd_path_delete - contador_delete == 0:
                        del current[item]
                        if current == {}:
                            db_delete = remove_infodb(path_delete[:-1], antiblock=True)
                    else:
                        current = current[item]
                    contador_delete += 1
            if contador_exec == 1:
                salva_infodb(dict(db_delete), antiblock=True)
                contador_exec -= 1
            else:
                contador_exec -= 1
                return db_delete
        if antiblock == False:
            editando = False
    
def formata_db(antiblock=False):
    #
    global editando
    if client_use:
        send_msg_sock('formata_db', client)
    else:
        if antiblock == False:
            while editando:
                pass
            editando = True
            tiny_db.truncate()
            editando = False
        else:
            tiny_db.truncate()
def pwdb(path_dir_=None):
    #
    if client_use:
        send_msg_sock('pwdb', client)
        return str(recvall(client, key_tinydb).decode('utf-8'))
    else:
        if path_dir_ == None:
            global path_dir
        else:
            path_dir = path_dir_
        if len(path_dir) == 0:
            return '/'
        else:
            path_inteiro = ''
            for item_item in path_dir:
                path_inteiro = f'{path_inteiro}/{item_item}'
            return path_inteiro

def cdmin(qntd_min=1, path_dir_=None):
    #
    if type(qntd_min) != int:
        raise ValueError('Quantity of cdmin must be an integer!')
    if qntd_min < 0:
        raise ValueError('Quantity of cdmin must be bigger tan 0!')
    if client_use:
        send_msg_sock(f'cdmin;{qntd_min}', client)
    else:
        if path_dir_ == None:
            global path_dir
        else:
            path_dir = path_dir_
        if qntd_min == 0:
            path_dir = []
        elif len(path_dir) > 0:
            for c in range(0, qntd_min):
                path_dir.pop(-1)
        return path_dir

def dirfdbp():
    #
    tempor = dirfdb(return_pathed=False)
    if tempor != None:
        print(dumps(dirfdb(return_pathed=False), indent=4, ensure_ascii=False).encode('utf-8').decode())
    else:
        print(None)
