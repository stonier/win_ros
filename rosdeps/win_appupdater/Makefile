
all: signatures

key:
	gpg --gen-key

signatures:
	@rm -f database/*.asc
	@for i in database/*; do \
	  echo $$i; \
	  echo "gpg --output $$i.asc --sign $$i"; \
	  gpg --output $$i.asc --sign $$i; \
	done
	@if [ $? -ne 0 ]; then \
	  echo "You need to generate a secrete key first - 'make key'"
	fi


