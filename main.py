#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Madhav (https://github.com/madhav-mknc)


from os import system as cmd

# run app.py
def main():
    from app import start_server
    print("[GOING ONLINE...]")
    start_server()

# install dependencies
def install():
    print("[*] Installing the Requirements")
    cmd("pip install -r requirements.txt")
    
# mains
if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError:
        install()
    except ImportError:
        install()
    except KeyboardInterrupt:
        print("\n[exitted]")



        

