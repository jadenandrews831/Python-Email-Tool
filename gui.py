import emort
import tkinter as tk

root = tk.Tk()

root.title("Email Marketing Tool")
root.geometry("1500x1000")

name_var = tk.StringVar()
pass_var = tk.StringVar()
smtp_var = tk.StringVar()
port_var = tk.StringVar()
text_var = tk.StringVar()
foi_var = tk.StringVar()

def reset_display():
  for child in root.winfo_children():
    child.destroy()

def emort_signin():
  reset_display()

  usr = name_var.get()
  pss = pass_var.get()
  smtp = smtp_var.get()
  port = port_var.get()

  print(f"INFO >>>\n\n{usr}\n{pss}\n{smtp}\n{port}")
  data = emort.write_config(usr, pss, smtp, port)
  print(f"Data >>>\n{data}")
  gui_main()

def emort_sendemail(email):
  reset_display()

  print("Email:\n\n ", email)

def gui_main(config):
  name_label = tk.Label(root, text=config['username'], font=('calibre', 10, 'bold'))
  server_label = tk.Label(root, text=config['SMTP'], font=('calibre', 10, 'bold'))
  groups_label = tk.Label(root, text="Groups:", font=('calibre', 20, 'bold'))
  ag_btn = tk.Button(root, text="+ Group", command=lambda: gui_makegroup(config))

  name_label.grid(column=0, row=0)
  server_label.grid(column=0, row=1)
  groups_label.grid(column=0, row=3)
  ag_btn.grid(column=1, row=3)

  print("Config:", config)
  if hasattr(config, 'groups'):
    names = config['groups'].keys()
    for name in names:
      print("Name")
  else:
    ng_label = tk.Label(root, text="No Groups Available", font=('calibre', 18))
    ng_label.grid(column=0, rows=4)

 

  root.mainloop()

def gui_grpoptions(config):
  reset_display()

  name_label = tk.Label(root, text=config['username'], font=('calibre', 10, 'bold'))
  server_label = tk.Label(root, text=config['SMTP'], font=('calibre', 10, 'bold'))
  ag_label = tk.Label(root, text="Add Group:", font=('calibre', 20, 'bold'))

  name_label.grid(column=0, row=0)
  server_label.grid(column=0, row=1)
  ag_label.grid(column=0, row=3)

  vals = {"File": 1, "Input": 2}
  

def gui_makegroup(config):
  reset_display()

  name_label = tk.Label(root, text=config['username'], font=('calibre', 10, 'bold'))
  server_label = tk.Label(root, text=config['SMTP'], font=('calibre', 10, 'bold'))
  ag_label = tk.Label(root, text="Add Group:", font=('calibre', 20, 'bold'))

  name_label.grid(column=0, row=0)
  server_label.grid(column=0, row=1)
  ag_label.grid(column=0, row=3)

  vals = {"File": 1, "Input": 2}
  for (name, val) in vals.items():
    tk.Radiobutton(root, text = name, variable = foi_var, value = val, command=lambda: gui_grpoptions(config)).grid(column=val, row=3) 

  

  root.mainloop()


def gui_choose_recp():
  pass

def gui_signin():
  name_label = tk.Label(root, text="Username", font=('calibre', 10, 'bold'))
  name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'bold'))
  passw_label = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
  passw_entry = tk.Entry(root, textvariable=pass_var, font=('calibre', 10, 'bold'), show="*")
  smtp_label = tk.Label(root, text="SMTP Server", font=('calibre', 10, 'bold'))
  smtp_entry = tk.Entry(root, textvariable=smtp_var, font=('calibre', 10, 'bold'))
  port_label = tk.Label(root, text="Port Number (Default 456)", font=('calibre', 10, 'bold'))
  port_entry = tk.Entry(root, textvariable=port_var, font=('calibre', 10, 'bold'))
  sub_btn = tk.Button(root, text="Submit", command=emort_sendemail)

  name_label.grid(row=0,column=1)
  name_entry.grid(row=0,column=2)
  passw_label.grid(row=1,column=1)
  passw_entry.grid(row=1,column=2)
  smtp_label.grid(row=2, column=1)
  smtp_entry.grid(row=2, column=2)
  port_label.grid(row=3, column=1)
  port_entry.grid(row=3, column=2)
  sub_btn.grid(row=4,column=2)

  root.mainloop()

def gui_sendemail(config):
  print("Config:", config)
  name_label = tk.Label(root, text=config['username'], font=('calibre', 10, 'bold'))
  server_label = tk.Label(root, text=config['SMTP'], font=('calibre', 10, 'bold'))
  email_label = tk.Label(root, text="Email Section:", font=('calibre', 20, 'bold'))
  text_area = tk.Text(root, wrap=tk.WORD, width=100, height=30, font=('Times New Roman', 20))
  sub_btn = tk.Button(root, text="Submit", command=lambda: emort_sendemail(text_area.get("1.0", "end-1c")))

  name_label.grid(column=0, row=0)
  server_label.grid(column=0, row=1)
  email_label.grid(column=0, row=3)
  text_area.grid(column=0, row=4, pady=10, padx=10)
  sub_btn.grid(column=0, row=5)

  text_area.focus()
  root.mainloop()

def main():
  exists = emort.check_config()

  if exists:
    config = emort.decrypt_config()
    signedin = emort.email_signin(config)
    if signedin:
      gui_main(config)
    else:
      gui_signin()
  else:
    gui_signin()

if __name__ == '__main__':
  main()