#include $(shell rospack find eros_build)/mk/custom_installer.mk

# Check if an environment variable has been set (using for the jenkins
# build).
ifdef MINGW_INSTALL_PREFIX
  PREFIX=${MINGW_INSTALL_PREFIX}
  SUDO=
else
  PREFIX=/opt/mingw
  SUDO=sudo
endif
TUPLE=i686-pc-mingw32
NAME=mingw-cross-env-2.21
URL=http://hg.savannah.nongnu.org/hgweb/mingw-cross-env

##############################################################################
# Primary targets
##############################################################################

.PHONY: clean

# Using sudo to make the directories anyway, may as well as get it to do
# the lot - should perhaps move mingw_cross to user's home directory.
all: links

# all: compile

install: links
	
uninstall:
	$(SUDO) rm -rf ${PREFIX}
	$(SUDO) rm -f /usr/local/bin/$(TUPLE)-*

clean:
	rm -rf build

##############################################################################
# Helper targets
##############################################################################

help:
	@echo "all       : clones to ${PREFIX} and compiles gcc, qt, boost and apache libs."
	@echo "links     : installs links to binaries in ${PREFIX}/usr/bin."
	@echo "install   : same as above."
	@echo "uninstall : uninstalls links and deletes ${PREFIX}."
	@echo "clone     : just clone the stable mingw cross repo."

links: compile
	@if [ -d $(PREFIX)/usr/bin ]; then \
		for i in $(PREFIX)/usr/bin/*; do \
			$(SUDO) ln -sf $$i /usr/local/bin/`basename $$i`; \
		done; \
	else \
		echo "Not installed yet, run make first."; \
	fi
	$(SUDO) ln -sf ${PREFIX}/usr/${TUPLE}/lib/libboost_thread_win32-mt.a ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt.a
	$(SUDO) ln -sf ${PREFIX}/usr/${TUPLE}/lib/libboost_thread_win32-mt-d.a ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt-d.a



compile: clone
	@echo "Compiling mingw gcc, log4cxx, boost and qt."
	@if [ ! -f $(PREFIX)/usr/installed/gcc ]; then \
	    cd $(PREFIX); make gcc log4cxx boost qt; \
	    echo; \
	    echo "Mingw cross environment successfully installed in ${PREFIX}."; \
	    echo " - run 'make links' or 'make install' to install symbolic links in"; \
	    echo "   /usr/local/bin from binaries in ${PREFIX}/usr/bin"; \
	    echo " - run 'make uninstall' to delete links and ${PREFIX}."; \
	    echo; \
	    echo "The cross environment has many build scripts that can be used to"; \
	    echo "install packages into your toolchain. Refer to"; \
	    echo; \
	    echo "  http://mingw-cross-env.nongnu.org/ for a full list."; \
	    echo; \
	    echo "Example (installation of gdb and wxwidgets):"; \
	    echo; \
	    echo "  cd ${PREFIX}"; \
	    echo "  make gdb wxwidgets"; \
	    echo; \
	    echo "If the download links should ever happen to be broken, try"; \
	    echo; \
	    echo "  cd ${PREFIX}/src"; \
	    echo "  hg pull -u"; \
	    echo; \
	    echo "that will sometimes work. If it fails, then contact help as something is";  \
	    echo "probably really broken."; \
	    echo; \
	else \
		echo "There is already an installed gcc in $(PREFIX)."; \
	fi


clone: 
	@echo "Cloning stable branch to $(PREFIX)"
	$(SUDO) mkdir -p $(PREFIX)
	$(SUDO) chown -R $(USER) $(PREFIX)
	@if [ ! -f $(PREFIX)/Makefile ]; then \
		hg clone -r stable $(URL) $(PREFIX); \
	else \
		echo "Mingw cross has already been cloned at $(PREFIX)."; \
	fi
	@for i in patches/*.mk; do cp $$i ${PREFIX}/src; done
	@for i in patches/*.patch; do cp $$i ${PREFIX}/src; done
	#@for i in patches/*.c; do cp $$i ${PREFIX}/src; done
