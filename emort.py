from cryptography.fernet import Fernet

import argparse
import getpass
import json
import os
import random
import smtplib, ssl
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
  parser.add_argument('-c', '--config', action='store_true', help='Give config file as argument or type values at the cli')
  args = parser.parse_args()

  if args.config:
    usr = input("Username: ")
    pss = getpass.getpass("Password: ")
    srv = input("Outgoing Server: ")
    prt = input("SMTP Port: ")
    write_config(usr, pss, srv, prt)

  exists = check_config()
  if exists:
    config = decrypt_config()
    email_signin(config)
  else:
    creds_prompt()
  
def check_config():
  if os.path.exists('dist/config/config.json'):
    return True
  else:
    return False

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
      config = write_config(usr, pswrd, smtp, port)
      email_signin(config)

def make_group(name, members):
  config = decrypt_config()
  print("Config:\n", config)
    

def email_signin(config):
  usr = config["username"]
  pswrd = config["password"]
  SMTP = config["SMTP"]
  port = config["port"]

  print(f"Info >> \n\t{usr}\n\t{pswrd}\n\t{SMTP}\n\t{port}")

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL(SMTP, port, context=context) as server:
    server.login(usr, pswrd)
    print("Logged in to mail server", SMTP)
    return True
  
  return False
    # server.sendmail(usr, None, )


def write_config(usr, pswrd, smtp, port):
  try:
    file_name = os.getcwd()+"/dist/config/config.json"
    if os.path.exists(file_name): f = open(file_name, "w")
    else: f = open(file_name, "x")
    if port == "":
      port = 465
    data = json.dumps({"username": usr, "password": pswrd, "SMTP": smtp, "port": port})
    f.write(data)
    print("Wrote Config >>>\n\n", data)
    f.close()
    encrypt_config(file_name)
    return json.loads(data)
  except Exception as e:
    print("Unable to write to config.json >>> \n\n", e)
    sys.exit(1)

def make_key():
  f = open('dist/config/.kemort', 'x')
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
    f = open('dist/config/.kemort', 'r')
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
  if (not os.path.exists('dist/config/.kemort')):
    make_key()
  key = get_key()
  fernet = Fernet(key)
  with open(file, 'rb') as f:
    og = f.read()
  encrypted = fernet.encrypt(og)
  with open(file, 'wb') as f:
    f.write(encrypted)

  print("Finished Encrypting")

def decrypt_config():
  try:
    key = get_key()
    print("Key:", key)
    with open('dist/config/config.json', 'rb') as f:
      encrypted = f.read()
    fernet = Fernet(key)
    data = fernet.decrypt(encrypted).decode()
    print("Data:", data)
    config = json.loads(data)
    print("File Data >>> \n\n", data)
    return config
  except Exception as e:
    print("Unable to decrypt. Please Try Again later", e)
    sys.exit(1)

def send_email():
  pass

if __name__ == "__main__":
  main()