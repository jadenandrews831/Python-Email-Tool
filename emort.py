import argparse
import json
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
  

def check_config():
  pass

def creds_prompt():
  pass

def email_signin():
  pass

def write_config():
  pass

def encrypt_pass():
  pass

def encrypt_config():
  pass

def decrypt_pass():
  pass

def decrypt_config():
  pass

def send_email():
  pass

if __name__ == "__main__":
  main()