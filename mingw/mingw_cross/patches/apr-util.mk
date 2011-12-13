# This file is part of mingw-cross-env.
# See doc/index.html for further information.

PKG             := apr-util
$(PKG)_IGNORE   :=
#$(PKG)_VERSION  := 1.3.10
#$(PKG)_CHECKSUM := f5aaf15542209fee479679299dc4cb1ac0924a59
$(PKG)_VERSION  := 1.3.12
$(PKG)_CHECKSUM := bb8c03cfff08423a240b2bc139067bab8a7af8f1
$(PKG)_SUBDIR   := apr-util-$($(PKG)_VERSION)
$(PKG)_FILE     := apr-util-$($(PKG)_VERSION).tar.gz
$(PKG)_WEBSITE  := http://apr.apache.org/
$(PKG)_URL      := http://archive.apache.org/dist/apr/$($(PKG)_FILE)
# Mirror links break when the latest is updated, do not use
#$(PKG)_URL      := http://mirror.apache-kr.org/apr/$($(PKG)_FILE)
$(PKG)_URL_2    := http://win-ros-pkg.googlecode.com/files/$($(PKG)_FILE)
$(PKG)_DEPS     := gcc libiconv apr expat

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
        --without-pgsql \
        --without-sqlite2 \
        --without-sqlite3 \
        --with-apr='$(PREFIX)/$(TARGET)' \
        CFLAGS=-D_WIN32_WINNT=0x0500 
    $(MAKE) -C '$(1)' -j '$(JOBS)' install bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS= man_MANS=
endef
