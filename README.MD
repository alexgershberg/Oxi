# Oxi / simple client - server chat application
## Build instructions:

1. Navigate to Oxi/bin
3. Run `zsh dependencies_add.zsh`
2. Run `zsh deploy.zsh`

This will build required images locally 
and deploy both logger and the app in
a stack. 

### Optional:
Modify docker-compose.yml for desired scale.

## Commands:
    zsh deploy.zsh           # - build local images, run in stack from docker-compose.yml
    zsh undeploy.zsh         # - remove stack, remove local images
    zsh build_images.zsh     # - build local images
    zsh remove_images.zsh    # - remove local images
    zsh app_attach.zsh       # - attach terminal to app output
    zsh logger_attach.zsh    # - attach terminal to logger output

## Connecting with client:
### Oxi has two client scripts:
### 
    client.py serves as stdout 
    view.py serves as stdin

### You need to configure Client virtual environment in order to run client.py and view.py.

### Setting Up client-venv:
1. Navigate to Oxi/Client
2. Run `python3 -m venv client-venv`
3. Run `source client-venv/bin/activate`
4. Run `pip install -r requirements.txt`

### Connecting to the server: (after setting up client-venv)
1. Navigate to Oxi/Client
2. Run `source client-venv/bin/activate`
3. Run `python3 client.py`
4. Run `python3 view.py` (in a separate window)
