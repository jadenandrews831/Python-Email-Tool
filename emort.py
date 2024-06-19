from cryptography.fernet import Fernet

import argparse
import getpass
import json
import os
import random
import string
import subprocess
import sys
import textwrap
import threading

def main():
  parser = argparse.ArgumentParser(
    description="Email Marketing Tool",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''Example:
                           emort send_mail.txt emails.csv             # Give email list(.csv, .json, .txt) and email(.txt) (default)
                           emort -e user@email.com emails.csv         # Give email at the cli
                           emort -e user@email.com,fry@email.com      # Give list of emails at the cli
                           emort -w send_mail.txt                     # Write email at the cli
                           emort -c new_config.json                    # Give new config file 
                           emort -c                                   # Write new config at the cli     
                           ''')
  )
  parser.add_argument('-w', '--write', type=str, help="write email at the cli")
  parser.add_argument('-e', '--email', type=str, help="give recipient addresses at the cli")
  parser.add_argument('-c', '--config', help='Give config file as argument or type values at the cli')
  check_config()
  
def check_config():
  if os.path.exists('config/config.json'):
    decrypt_config()
    decrypt_pass()
    email_signin()
  else:
    creds_prompt()

def creds_prompt(usr=None, pswrd=None):
  if usr and pswrd:
    pass
  else:
    try:
      usr = input("Username: ")
      pswrd = getpass.getpass("Password: ")
      smtp  = input("Outgoing Server: ")
      port = input("SMTP Port: ")
    except Exception as e:
      print('Error: ', e)
      sys.exit(1)
    else:
      print("Creds Received")
      write_config(usr, pswrd, smtp, port)
      email_signin()

def email_signin():
  print("Email Signin")

def write_config(usr, pswrd, smtp, port=465):
  try:
    file_name = os.getcwd()+"/config/config.json"
    f = open(file_name, "x")
    data = json.dumps({"username": usr, "password": pswrd, "SMTP": smtp, "port": port})
    f.write(data)
    print("Wrote Config >>>\n\n", data)
    f.close()
    encrypt_config(file_name)
  except Exception as e:
    print("Unable to write to config.json >>> \n\n", e)
    sys.exit(1)

def encrypt_pass():
  pass

def make_key():
  f = open('config/.kemort', 'x')
  seed_len = random.randint(10,90)
  garb_len = random.randint(10,90)
  seed = ''.join(random.choices(string.ascii_letters + string.digits + '='+'-'+'_', k=seed_len))
  key = Fernet.generate_key().decode()
  garbage = ''.join(random.choices(string.ascii_letters + string.digits + '='+'-'+'_', k=garb_len))
  print(f"seed_len:\t{seed_len}\nseed:\t{seed}\nkey:\t{key}\ngarb_len:\t{garb_len}")
  val = str(seed_len+1)+seed+key+garbage
  print(f"Val: {val}")
  f.write(val)
  print("Made Encryption Key")
  f.close()

def get_key():
  try:
    f = open('config/.kemort', 'r')
    file = f.read()
    idx = int(file[:2])+1
    print("idx:", idx)
    key = file[idx:].split("=")[0]+"="
    print("Key:", key)
    f.close()
    return key
  except Exception as e:
    print("Unable to get key >>> ", e)
    sys.exit(1)


def encrypt_config(file):
  if (not os.path.exists('config/.kemort')):
    make_key()
  key = get_key()
  fernet = Fernet(key)
  with open(file, 'rb') as f:
    og = f.read()
  encrypted = fernet.encrypt(og)
  with open(file, 'wb') as f:
    f.write(encrypted)

  print("Finished Encrypting")
  # key = os.getenv('emort_key')
  # if key == None:
  #   key = Fernet.generate_key()
  #   print("Key:", key)
  #   os.environ['emort_key'] = key.decode()
  #   print("Key: ",os.getenv('emort_key'))

def decrypt_pass():
  pass

def decrypt_config():
  try:
    key = get_key()
    print("Key:", key)
    with open('config/config.json', 'rb') as f:
      encrypted = f.read()
    fernet = Fernet(key)
    data = fernet.decrypt(encrypted)
    print("Data:", data)
    config = json.loads(data)
    print("File Data >>> \n\n", data)
  except Exception as e:
    print("Unable to decrypt. Please Try Again later", e)
    sys.exit(1)

def send_email():
  pass

if __name__ == "__main__":
  main()