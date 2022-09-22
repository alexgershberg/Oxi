# Oxi / simple client - server chat application
## Build instructions:

1. Navigate to Oxi/bin
2. Run zsh deploy.zsh 

This will build required images locally 
and deploy both logger and the app in
a stack. 

#### Optional:
Modify docker-compose.yml for desired scale.

## Commands:
    zsh deploy.zsh           # - build local images, run in stack from docker-compose.yml
    zsh undeploy.zsh         # - remove stack, remove local images
    zsh build_images.zsh     # - build local images
    zsh remove_images.zsh    # - remove local images
    zsh app_attach.zsh       # - attach terminal to app output
    zsh logger_attach.zsh    # - attach terminal to logger output

## Connecting with client:
Oxi has two client scripts:
    client.py serves as stdout 
    view.py serves as stdin

1. Navigate to Oxi/Client
2. Run python3 client.py
3. Run python3 view.py (in a separate window)
