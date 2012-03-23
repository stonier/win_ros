
# My Key
KEY_ID=9903B1CC 
KEY_NAME="WinRos Fuerte"
EMAIL=d.stonier@gmail.com
PUB_KEY_NAME=winros.fuerte.pub.asc

# Nabber's key
#KEY_ID=2DF1479E

all:
	@echo "Usage:"
	@echo "  help"
	@echo "  key : generate a gpg key for the group (interactive)."
	@echo "  list_keys : list local gpg keys."
	@echo "  send_key : send the key to the public gpg servers."
	@echo "  recv_keys: receive the key from the public gpg server."
	@echo "  ascii_key : generate an ascii keyfile."
	@echo "  signatures : assuming you have your key, make sigs for each file."
	@echo "  verify_signatures : check signatures against downloaded/imported key."
	@echo ""
	@echo "Current key name : $(KEY_NAME)"
	@echo "Current key id   : $(KEY_ID)"
	@echo "Current key email: $(EMAIL)"
	@echo ""

key:
	gpg --gen-key

list_keys:
	gpg --list-keys

send_key:
	gpg --send-keys --keyserver keyserver.ubuntu.com $(KEY_ID) 

import_key:
	gpg --recv-keys --keyserver keyserver.ubuntu.com $(KEY_ID) 

receive_key:
	gpgp --recv-keys $(KEY_ID)
	
ascii_key:
	gpg --armor --output database/$(PUB_KEY_NAME) --export $(KEY_ID) 

signatures:
	@rm -f database/fuerte*.asc
	@for i in database/fuerte*; do \
	  echo "gpg -u $(KEY_ID) --armor --detach-sign $$i"; \
	  gpg -u $(KEY_ID) --armor --detach-sign $$i; \
	done
	@if [ $$? -ne 0 ]; then \
	  echo "You need to generate/import a key first - 'make key'"; \
	fi
	@rm -f database/utilities*.asc
	@for i in database/utilities*; do \
	  echo "gpg -u $(KEY_ID) --armor --detach-sign $$i"; \
	  gpg -u $(KEY_ID) --armor --detach-sign $$i; \
	done
	@if [ $$? -ne 0 ]; then \
	  echo "You need to generate/import a key first - 'make key'"; \
	fi

verify_signatures:
	@for i in database/*.xml; do \
          echo "  $$i"; \
	  gpg --verify $$i.asc $$i; \
	done
	@if [ $$? -ne 0 ]; then \
	  echo "You need to generate/import a key first - 'make key'"; \
	fi

