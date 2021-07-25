import os
import shutil
import hashlib
import json
import chardet
import regex as re
from frameworks.utils.crypto import Crypto
from frameworks.utils.log import Log
from frameworks.utils.excel2json import ExcelParser

import configparser


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None, allow_no_value=True):
        configparser.ConfigParser.__init__(self, defaults=defaults,
                                           allow_no_value=allow_no_value)

    def optionxform(self, optionstr):
        return optionstr


class FileUtils:
    """docstring for FileUtils"""

    def __init__(self):
        super(FileUtils, self).__init__()

    @staticmethod
    def check_path_in_rule(path, rule):
        pattern = re.compile(rule)
        groups = pattern.findall(path)
        return len(groups) > 0

    @staticmethod
    def check_path_in_rules(path, rules):
        if rules is None:
            return True
        if len(rules) is None:
            return True
        for rule in rules:
            if FileUtils.check_path_in_rule(path, rule):
                return True
        return False

    @staticmethod
    def copy_files_in_dir(src, dst, rules=None):
        if not os.path.isdir(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isfile(path) and FileUtils.check_path_in_rules(path, rules):
                shutil.copy(path, dst)

            if os.path.isdir(path):
                new_dst = os.path.join(dst, item)
                if not os.path.isdir(new_dst):
                    os.makedirs(new_dst)
                FileUtils.copy_files_in_dir(path, new_dst, rules)

    @staticmethod
    def copy_files_in_dir_with_replacement(src, old, new):
        dst = src.replace(old, new)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isfile(path):
                shutil.copy(path, dst)

            if os.path.isdir(path):
                FileUtils.copy_files_in_dir_with_replacement(path, old, new)

    @staticmethod
    def copy_files_in_dir_if_newer(src, dst, cpstat=False):
        if not os.path.isdir(src):
            return

        if not os.path.isdir(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isfile(path):
                copy_dst = dst
                copy_dst_path = copy_dst + '\\' + os.path.split(path)[1]
                if os.path.isfile(copy_dst_path) and os.stat(copy_dst_path).st_mtime >= os.stat(path).st_mtime:
                    pass
                else:
                    # Log.i path
                    if cpstat:
                        shutil.copy2(path, copy_dst)
                    else:
                        shutil.copy(path, copy_dst)
            if os.path.isdir(path):
                new_dst = os.path.join(dst, item)
                FileUtils.copy_files_in_dir_if_newer(path, new_dst, cpstat)

    @staticmethod
    def copy_files_in_dir_if_changed(src, dst):
        if not os.path.isdir(src):
            return

        if not os.path.isdir(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isfile(path):
                copy_dst = dst
                dstpath = os.path.join(dst, item)
                md5 = FileUtils.get_file_md5(path)
                dstmd5 = 0
                if os.path.exists(dstpath):
                    dstmd5 = FileUtils.get_file_md5(dstpath)

                if md5 != dstmd5:
                    shutil.copy(path, copy_dst)
                    Log.i("{0} done".format(path))
                else:
                    Log.i("{0} don't need copy".format(path))

            if os.path.isdir(path):
                new_dst = os.path.join(dst, item)
                FileUtils.copy_files_in_dir_if_changed(path, new_dst)




    @staticmethod
    def remove_files_in_dir(src, ext):
        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isfile(path):
                if os.path.splitext(path)[1] == ext:
                    os.remove(path)
                    if os.path.isfile(path.replace(".json", ".skel")) is False:
                        Log.i(path)

            if os.path.isdir(path):
                new_dst = os.path.join(src, item)
                FileUtils.remove_files_in_dir(new_dst, ext)

    @staticmethod
    def remove_empty_dirs(dir_path):
        for item in os.listdir(dir_path):
            path = os.path.join(dir_path, item)
            if os.path.isdir(path):
                FileUtils.remove_empty_dirs(path)

        if not os.listdir(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def get_text_md5(text):
        hl = hashlib.md5()
        hl.update(text.encode(encoding='utf-8'))
        return hl.hexdigest()
        pass

    @staticmethod
    def get_file_md5(path):
        with open(path, 'rb') as fp:
            hl = hashlib.md5()
            hl.update(fp.read())
            return hl.hexdigest()


    @staticmethod
    def save_json_file(path, data):
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    @staticmethod
    def load_json_file(path):
        with open(path) as json_file:
            data = json.load(json_file)
            return data

    @staticmethod
    def load_file(path, encoding = 'utf8'):
        file = open(path, "r", encoding = encoding, newline='')
        buff = file.read()
        file.close()
        return buff

    @staticmethod
    def encrypt_file(path, key, sign):
        file = open(path, "rb+")

        buff = file.read()
        pre_sign = str(buff[0:len(sign)])

        if pre_sign == sign:
            Log.i('have entrypt :' + path)
        else:
            Log.i('entrypt file :' + path)
            bytes = Crypto.encrypt_by_xxtea(buff, key)
            bytes = sign + bytes
            file.seek(0)
            file.write(bytes)
        file.close()

    @staticmethod
    def excel_to_json(path, export_path):
        ep = ExcelParser()
        data_map = ep.parse(path)
        file = open(export_path, "w")
        json.dump(data_map, file)
        file.close()

    @staticmethod
    def decode_to_utf8(buff):
        encoding_type = chardet.detect(buff)
        try:
            buff = buff.decode(encoding_type['encoding'])
        except Exception as e:
            try:
                buff = buff.decode('GB18030')
            except Exception as e:
                raise e

        buff = buff.encode('utf-8')
        return buff

    @staticmethod
    def change_file_to_utf8(path):
        file = open(path, "rb")
        buff = file.read()
        encoding_type = chardet.detect(buff)
        print(encoding_type)
        try:
            buff = buff.decode(encoding_type['encoding'])
        except Exception as e:
            try:
                buff = buff.decode('GB18030')
            except Exception as e:
                try:
                    buff = buff.decode('utf-8')
                except Exception as e:
                    raise e

        buff = buff.encode('utf-8')
        file.close()
        file2 = open(path, "wb")
        file2.write(buff)
        file2.close()
        return buff

    @staticmethod
    def load_ini_file(path):
        cp = MyConfigParser()
        cp.read(path)
        return cp

    @staticmethod
    def remove_local_class(path):
        FileUtils.change_file_to_utf8(path)
        buff = FileUtils.load_file(path)
        pattern = re.compile("local (C[A-Z]\w+)[ ]*=[ ]*([\w.]+)")
        groups = pattern.findall(buff)
        for group in groups:
            if group[1] != "class" and group[1] != "require" and group[1] != "reloadFile":
                print(group)
                buff = re.sub(r"local {0} = {1}[\r\n]*".format(group[0], group[1]), "", buff)
                buff = re.sub(r"\b{0}\b".format(group[0]), group[1], buff)

        name, ext = os.path.splitext(path)
        file = open(path, "w", encoding='utf8', newline='')
        file.write(buff)
        file.close()

    @staticmethod
    def remove_local_class_in_dir(src, rules=None):
        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isfile(path) and FileUtils.check_path_in_rules(path, rules):
                print(path)
                FileUtils.remove_local_class(path)

            if os.path.isdir(path):
                FileUtils.remove_local_class_in_dir(path, rules)

    @staticmethod
    def gen_list_file(path, root):
        list_file_path = os.path.join(path, "list.lua")
        file = open(list_file_path, "w")
        file.write("return {\n")
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                file.write("\t\"{0}\"\n".format(name))
        file.write("}")

    @staticmethod
    def gen_list_if_exist(path, root=""):
        if root is "":
            root = path

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                list_path = os.path.join(item_path, "list.lua")
                if os.path.exists(list_path):   
                    FileUtils.gen_list_file(item_path, root);
                else:
                    FileUtils.gen_list_if_exist(item_path, root)
