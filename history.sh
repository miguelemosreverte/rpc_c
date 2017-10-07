
rpcgen -C add.x
rpcgen -a -C add.x
make -f Makefile.add
systemctl add-wants multi-user.target rpcbind
#sudo apt-get install rpcbind
