# This file is part of mingw-cross-env.
# See doc/index.html for further information.

# Type sizes
#
# Sometimes wine has an emulation environment which runs conf tests,
# unfortunately these return like a 4^M, not 4 which breaks all the 
# configure script logic.
#    ac_cv_sizeof_off_t=4
#    ac_cv_sizeof_pid_t=4 
#    ac_cv_sizeof_size_t=4
#    ac_cv_sizeof_ssize_t=4

PKG             := apr
$(PKG)_IGNORE   :=
$(PKG)_VERSION  := 1.4.2
$(PKG)_CHECKSUM := d48324efb0280749a5d7ccbb053d68545c568b4b
# apr 1.4.5 has a bug yet - it defines __MSVCRT__ which sets __stdcall
# (1.4.2 doesn't). This ends up causing a conflict with LOG4CXX which does 
# not set __stdcall and a macro clash arises in log4cxx's filewatchdog.cpp.
#$(PKG)_VERSION  := 1.4.5
#$(PKG)_CHECKSUM := acdde5a7fdda11e7815fe3035de5fc4c10c1d428
$(PKG)_SUBDIR   := apr-$($(PKG)_VERSION)
$(PKG)_FILE     := apr-$($(PKG)_VERSION).tar.gz
$(PKG)_WEBSITE  := http://apr.apache.org/
$(PKG)_URL      := http://archive.apache.org/dist/apr/$($(PKG)_FILE)
# Mirrors aren't keeping links to the tarballs, only the apache site itself
#$(PKG)_URL      := http://mirror.apache-kr.org/apr/$($(PKG)_FILE)
$(PKG)_URL_2    := http://win-ros-pkg.googlecode.com/files/$($(PKG)_FILE)
$(PKG)_DEPS     := gcc

#define $(PKG)_UPDATE
#    wget -q -O- 'http://www.ijg.org/' | \
#    $(SED) -n 's,.*jpegsrc\.v\([0-9][^>]*\)\.tar.*,\1,p' | \
#    head -1
#endef

define $(PKG)_BUILD
    cd '$(1)' && ./configure \
        --prefix='$(PREFIX)/$(TARGET)' \
        --host='$(TARGET)' \
        --disable-shared \
        --enable-static \
        ac_cv_sizeof_off_t=4 \
        ac_cv_sizeof_pid_t=4 \
        ac_cv_sizeof_size_t=4 \
        ac_cv_sizeof_ssize_t=4 \
        CFLAGS=-D_WIN32_WINNT=0x0500 
    $(MAKE) -C '$(1)' -j '$(JOBS)' install bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS= man_MANS=
endef
