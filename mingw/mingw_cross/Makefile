
# You can modify where it gets installed by setting MINGW_INSTALL_PREFIX
# as an environment variable (using for the jenkins build).
ifdef MINGW_INSTALL_PREFIX
  PREFIX=${MINGW_INSTALL_PREFIX}
else
  PREFIX=$(HOME)/mingw
endif
TUPLE=i686-pc-mingw32
#URL=http://hg.savannah.nongnu.org/hgweb/mingw-cross-env
URL=https://github.com/mxe/mxe.git
URL_DEV=https://github.com/yujinrobot/mxe.git
CMAKE_CACHE_FILE=$(PREFIX)/usr/${TUPLE}/share/cmake/mingw-cross-env-ros.cmake
CMAKE_TOOLCHAIN_FILE=$(PREFIX)/usr/${TUPLE}/share/cmake/mxe-conf.cmake

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
	@if grep "MINGW_ROOT" $(HOME)/.bashrc -q; then \
          echo "There are MINGW_XXX variables already added to .bashrc"; \
          echo "Not disturbing these values, please update by hand if necessary."; \
	else \
	  echo "Adding MINGW_ROOT and updating PATH in .bashrc"; \
	  echo "export MINGW_ROOT=$(PREFIX); export PATH=\$${PATH}:$(PREFIX)/usr/bin" >> $(HOME)/.bashrc; \
	  echo "Adding MINGW_CMAKE_TOOLCHAIN_FILE to .bashrc"; \
	  echo "export MINGW_CMAKE_TOOLCHAIN_FILE=${CMAKE_TOOLCHAIN_FILE}" >> $(HOME)/.bashrc; \
	  echo "Adding MINGW_CMAKE_ROS_CONFIG_FILE to .bashrc"; \
	  echo "export MINGW_CMAKE_ROS_CONFIG_FILE=${CMAKE_CACHE_FILE}" >> $(HOME)/.bashrc; \
	fi
	@echo "Copying ros configuration variable file -> $(CMAKE_CACHE_FILE)"
	@cp cmake/mingw-cross-env-ros.cmake $(CMAKE_CACHE_FILE)
	@echo "You may need to resource your .bashrc if you want to use mingw directly."
	@echo ""

uninstall:
	@if grep "$(PREFIX)/usr/bin" $(HOME)/.bashrc -q; then \
          echo "Removing mingw path and variables from .bashrc"; \
          grep -v "MINGW" $(HOME)/.bashrc > /tmp/.bashrc; \
          cp /tmp/.bashrc $(HOME)/.bashrc; \
        fi
	rm -rf $(PREFIX)

compile: clone
	@echo "Compiling mingw gcc, log4cxx, boost and qt."
	$(MAKE) -C $(PREFIX) gcc log4cxx boost qt
	@if [ ! -f ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt.a ]; then \
	  echo "Making links to fix boost_thread."; \
	  ln -sf ${PREFIX}/usr/${TUPLE}/lib/libboost_thread_win32-mt.a ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt.a; \
	  ln -sf ${PREFIX}/usr/${TUPLE}/lib/libboost_thread_win32-mt-d.a ${PREFIX}/usr/${TUPLE}/lib/libboost_thread-mt-d.a; \
	fi

clone: 
	@if [ ! -f $(PREFIX)/Makefile ]; then \
	    mkdir -p $(PREFIX); \
	    chown -R $(USER) $(PREFIX); \
		echo "Cloning mxe dev fork to $(PREFIX)"; \
		git clone $(URL_DEV) $(PREFIX); \
	else \
		echo "Mingw cross has already been cloned at $(PREFIX)."; \
	fi

clone_stable: 
	@if [ ! -f $(PREFIX)/Makefile ]; then \
	    mkdir -p $(PREFIX); \
	    chown -R $(USER) $(PREFIX); \
		echo "Cloning stable branch to $(PREFIX)"; \
		git clone -b stable $(URL) $(PREFIX); \
		echo "Patching mingw_cross makefiles."; \
	    for i in patches/*.mk; do cp $$i ${PREFIX}/src; done; \
	    for i in patches/*.patch; do cp $$i ${PREFIX}/src; done; \
	    patch -d ${PREFIX} -p0 < index.patch; \
	else \
		echo "Mingw cross has already been cloned at $(PREFIX)."; \
	fi

