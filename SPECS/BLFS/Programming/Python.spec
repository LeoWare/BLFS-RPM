#	Python-3.6.2.tar.xz
Summary:	The Python 3 package contains the Python development environment.
Name:		Python
Version:	3.6.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Programming
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{NAME}-%{VERSION}.tar.xz
Source1:	python-3.6.2-docs-html.tar.bz2
%description
	The Python 3 package contains the Python development environment.
	This is useful for object-oriented programming, writing scripts,
	prototyping large programs or developing entire applications.

%prep
#	install -vdm 755  %{_builddir}/Python-%{version}
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1  -n %{NAME}-%{VERSION}
%build
	CXX="/usr/bin/g++" \
	./configure \
		--prefix=%{_prefix} \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--with-ensurepip=yes
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	chmod -v 755 %{buildroot}/usr/lib/libpython3.6m.so
	chmod -v 755 %{buildroot}/usr/lib/libpython3.so
	install -v -dm755 %{buildroot}/usr/share/doc/python-3.6.2/html
	cp -var python-3.6.2-docs-html/* %{buildroot}/usr/share/doc/python-3.6.2/html
	ln -svfn python-3.6.2 %{buildroot}/usr/share/doc/python-3
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm "%{buildroot}/usr/lib/python3.6/site-packages/setuptools/command/launcher manifest.xml"
	rm "%{buildroot}/usr/lib/python3.6/site-packages/setuptools/script (dev).tmpl"
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find %{buildroot} -not -type d -print > filelist.rpm
	sed -i "s|^%{buildroot}||" filelist.rpm
%post
	pushd /usr/share/info
		rm -v dir
		for f in *;do install-info $f dir 2>/dev/null;done;
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> Python-3.2.1-1
-	Initial build.	First version