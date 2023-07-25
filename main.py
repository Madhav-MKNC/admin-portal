#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Madhav (https://github.com/madhav-mknc)


from os import system as cmd

# run app.py
def main():
    print("[booting...]")
    from app import start_server
    print("[GOING ONLINE...]")
    start_server()

# install dependencies
def install(err):
    print("[error]",err)
    print("[*] Installing the Requirements")
    cmd("pip install -r requirements.txt")
    
# mains
if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        install(e)
    except KeyboardInterrupt:
        print("\n[exitted]")



        

