#include $(shell rospack find eros_build)/mk/custom_installer.mk

# You can modify where it gets installed by setting MINGW_INSTALL_PREFIX
# as an environment variable (using for the jenkins build).
ifdef MINGW_INSTALL_PREFIX
  PREFIX=${MINGW_INSTALL_PREFIX}
else
  PREFIX=$(HOME)/mingw
endif
TUPLE=i686-pc-mingw32
URL=http://hg.savannah.nongnu.org/hgweb/mingw-cross-env

##############################################################################
# Primary targets
##############################################################################

.PHONY: clean

usage: help

help:
	@echo ""
	@echo "Usage:"
	@echo "  make install : install mingw_cross (by default to ~/mingw)"
	@echo "  make uninstall : remove mingw_cross from your system"
	@echo ""
	@echo "You can modify the install prefix by setting the environment"
	@echo "variable MINGW_INSTALL_PREFIX before executing make install."
	@echo ""

install: compile
	@if grep "$(PREFIX)/usr/bin" $(HOME)/.bashrc -q; then \
	  echo "Mingw path already added to .bashrc"; \
	else \
	  echo "Adding MINGW_ROOT and PATH to .bashrc"; \
	  echo "export MINGW_ROOT=$(PREFIX); export PATH=\$${PATH}:$(PREFIX)/usr/bin" >> $(HOME)/.bashrc; \
	fi
	@echo "You may need to resource your .bashrc if you want to use mingw directly."
	
uninstall:
	@if grep "$(PREFIX)/usr/bin" $(HOME)/.bashrc -q; then \
	  echo "Removing mingw path from .bashrc"; \
	  grep -v "$(PREFIX)/usr/bin" $(HOME)/.bashrc > /tmp/.bashrc; \
	  cp /tmp/.bashrc $(HOME)/.bashrc; \
	fi
	rm -rf $(PREFIX)

compile: clone
	@echo "Compiling mingw gcc, log4cxx, boost and qt."
	$(MAKE) -C $(PREFIX) $(ROS_PARALLEL_JOBS) gcc log4cxx boost qt
	@if [ ! -f ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt.a ]; then \
	  echo "Making links to fix boost_thread."; \
	  ln -sf ${PREFIX}/usr/${TUPLE}/lib/libboost_thread_win32-mt.a ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt.a; \
	  ln -sf ${PREFIX}/usr/${TUPLE}/lib/libboost_thread_win32-mt-d.a ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt-d.a; \
	fi

clone: 
	@if [ ! -f $(PREFIX)/Makefile ]; then \
	    mkdir -p $(PREFIX); \
	    chown -R $(USER) $(PREFIX); \
		echo "Cloning stable branch to $(PREFIX)"; \
		hg clone -r stable $(URL) $(PREFIX); \
	    for i in patches/*.mk; do cp $$i ${PREFIX}/src; done; \
	    for i in patches/*.patch; do cp $$i ${PREFIX}/src; done; \
	else \
		echo "Mingw cross has already been cloned at $(PREFIX)."; \
	fi

#@for i in patches/*.c; do cp $$i ${PREFIX}/src; done
