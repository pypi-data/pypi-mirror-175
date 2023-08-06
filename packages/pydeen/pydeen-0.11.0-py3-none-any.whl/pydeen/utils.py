"""
    some utils for PyDEEN
"""

from multiprocessing.spawn import import_main_path
import pathlib
import hashlib
import base64
import sys
import os
import uuid

from cryptography.fernet import Fernet
from pydeen.menu import UserInput
from datetime import datetime

class CryptEngine():
    
    PROP_SALT = "salt"
    PROP_ENGINE  = "engine"
    PROP_ENCODED = "encoded"
    
    def __init__(self, context:bytes=None, salt:bytes=None) -> None:
        self.context:bytes = context
        self.salt:bytes = salt
        self.engine:str = "unknown"  
    
    def encode(self, content:str):
        return content

    def decode(self, content:any):
        return content    

    def set_salt(self, salt:bytes):
        self.salt = salt        

    def set_context(self, context:bytes):
        self.context = context        

class CryptEngineDefault(CryptEngine):
    def __init__(self, context: bytes = None, salt: bytes = None) -> None:
        super().__init__(context, salt)
        self.engine = "default"
    
    def get_key(self) -> bytes:
        if self.context == None:
            self.context = CryptUtil.get_context_key()

        if self.salt == None:
            self.salt = CryptUtil.create_salt_key()  

        lenc = len(self.context)
        if lenc < 16:
            key = self.context + self.salt
        else:
            key = self.context[:16] + self.salt[:16]   

        return base64.urlsafe_b64encode(key) 

    def encode(self, content:str):        
        f = Fernet(self.get_key())
        e = f.encrypt(content.encode())
        result = {}
        result[CryptEngine.PROP_ENGINE] = self.engine
        result[CryptEngine.PROP_SALT] = CryptUtil.byte_to_base64(self.salt)
        result[CryptEngine.PROP_ENCODED] = CryptUtil.byte_to_base64(e)
        return result

    def decode(self, content:dict):
        try:
            engine = content[CryptEngine.PROP_ENGINE]
            if engine != self.engine:
                return content # wrong engine
            else:
                salt_b64 = content[CryptEngine.PROP_SALT]
                encoded_b64 = content[CryptEngine.PROP_ENCODED]
                self.salt = CryptUtil.base64_to_bytes(salt_b64)
                encoded = CryptUtil.base64_to_bytes(encoded_b64)    
                return Fernet(self.get_key()).decrypt(encoded).decode()
        except:
            print("Error", sys.exc_info()[0], "occurred.")
            return content  

class CryptUtil():
    
    @classmethod
    def __init__(cls) -> None:
        cls.engines = {}

    @staticmethod
    def get_context_key() -> bytes:
        context = str(pathlib.Path().resolve())
        context = context.replace("\\","")
        context = context.replace(":","")
        return hashlib.md5(context.encode()).digest()

    @staticmethod
    def create_salt_key() -> bytes:
        return base64.urlsafe_b64decode(Fernet.generate_key())

    @classmethod
    def register_engine(cls, name:str, engine:CryptEngine):
        cls.engines[name] = engine

    @classmethod
    def get_engine(cls, name:str=None, context:bytes=None, salt:bytes=None) -> CryptEngine:
        if name == None or name == "default" or len(name) == 0:
            return CryptEngineDefault(context, salt)
        
        if name in cls.engines.keys():
            return cls.engines[name]         

    @staticmethod
    def byte_to_base64(content:bytes) -> str:
        if content == None:
            return ""
        else:
            return base64.b64encode(content).decode()        

    @staticmethod
    def base64_to_bytes(base64_str:str) -> bytes:
        if base64_str == None or base64_str == "":
            return b""
        else:    
            return base64.b64decode(base64_str)    

class FileTransferUtil():
    
    def get_datetime_prefix(self, with_time:bool=True, format:str=None) -> str:
        now = datetime.now() # current date and time
        if format != None:
            myformat = format
        else:
            myformat = "%Y%m%d"
            if with_time == True:
                myformat = myformat + "_%H%M%S"

        return now.strftime(myformat)        

    def enter_filename_to_save(self, title:str, name:str, extension:str="txt", use_datetime_prefix:bool=True, show_current_path:bool=True) -> str:
        # current path
        if show_current_path:
            cur_path = pathlib.Path().resolve()
            print(f"Current working directory is {cur_path}")        
        
        # prepare filename
        filename = f"{name}"
        if use_datetime_prefix == True:
            filename = self.get_datetime_prefix() + "_" + filename

        if filename.find(".") < 0:
            filename = f"{filename}.{extension}"

        filename = UserInput(title,filename).get_input(empty_allowed=True)
        if filename == None or len(filename) == 0:
            return None

        return filename      

    def enter_filename_to_load(self, title:str, name:str=None, extension:str="txt", show_current_path:bool=True, show_files_with_ext:bool=True) -> str:
        # current path
        if show_current_path:
            cur_path = pathlib.Path().resolve()
            print(f"Current working directory is {cur_path}")

            if show_files_with_ext and extension != None:
                relevant_path = str(cur_path)
                included_extensions = []
                included_extensions.append(extension.lower())
                included_extensions.append(extension.upper())
                file_names = [fn for fn in os.listdir(relevant_path)
                    if any(fn.endswith(ext) for ext in included_extensions)]
                
                if file_names != None and len(file_names) > 0:
                    print(f"Files found in {cur_path}:\n")
                    for file_name in file_names:
                        print(file_name)
                else:
                    print(f"No files with extension {extension} found in {cur_path}.")

        # prepare filename    
        filename = f"{name}"
        if filename.find(".") < 0:
            filename = f"{filename}.{extension}"

        filename = UserInput(title,filename).get_input(empty_allowed=True)
        if filename == None or len(filename) == 0:
            return None

        return filename      


    def save_file(self, filename:str, content:str, print_msg:bool=True) -> bool:
        try:
            with open(filename, "w") as text_file:
                text_file.write(content)
            if print_msg == True:
                print(f"File saved as {filename}")
            return True
        except Exception as exc:
            print(f"Errors occured while writing file {filename}: {type(exc)} - {exc}")
            return False

    def enter_filename_and_save_text(self, title:str, name:str, content:str, with_datetime_prefix:bool=True, extension:str="txt") -> bool:
            if name == None or len(name) == 0:
                filename = "unknown"
            else:
                filename = name.replace("/", "x")

            filename = self.enter_filename_to_save(title, f"{filename}", extension=extension, use_datetime_prefix=with_datetime_prefix)
            if filename != None and filename.find(".") > 0:
                return self.save_file(filename, content)  
            else:
                print("Save file skipped.")
                return False              


class UUIDUtil():
    @staticmethod
    def new_uuid32_separated_string() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def new_uuid32_string() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def build_unique_key(key_str, namespace_str32:str=None) -> str:
        if namespace_str32 == None:
            use_ns_str = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        else:
            use_ns_str = namespace_str32

        ns = uuid.UUID(hex=use_ns_str)
        generated = str(uuid.uuid3(ns, key_str))
        return generated


if __name__ == "__main__":
    print(UUIDUtil.build_unique_key("test"))
    print(UUIDUtil.build_unique_key("test"))
    print(UUIDUtil.build_unique_key("test"))

    print("test_utils finished")            