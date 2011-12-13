.PHONY: all setup clean_dist distro clean install dsc source_deb upload

VERSION='0.5.16'



all:
	echo "noop for debbuild"

setup:
	mkdir -p src/rosinstall/vcs
	svn export --force $(shell rospack find vcstools)/src/vcstools src/rosinstall/vcs
	echo "confirming version numbers are all consistent"
	grep ${VERSION} scripts/rosinstall
	grep ${VERSION} setup.py
	echo "building version ${VERSION}"

clean_dist:
	-rm -f MANIFEST
	-rm -rf dist
	-rm -rf deb_dist

distro: setup clean_dist
	python setup.py sdist

push: distro
	python setup.py sdist register upload
	scp dist/rosinstall-${VERSION}.tar.gz ipr:/var/www/pr.willowgarage.com/html/downloads/rosinstall


clean: clean_dist
	rm -rf src/rosinstall/vcs

install: distro
	sudo checkinstall python setup.py install


dsc: distro
	python setup.py --command-packages=stdeb.command sdist_dsc

source_deb: dsc
	# need to convert unstable to each distro and repeat
	cd deb_dist/rosinstall-${VERSION} && dpkg-buildpackage -sa -k84C5CECD

binary_deb: dsc
	# need to convert unstable to each distro and repeat
	cd deb_dist/rosinstall-${VERSION} && dpkg-buildpackage -sa -k84C5CECD

upload: source_deb
	cd deb_dist && dput ppa:tully.foote/tully-test-ppa ../rosinstall_${VERSION}-1_source.changes 
