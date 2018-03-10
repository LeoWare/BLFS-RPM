#	Python-2.7.13.tar.xz
Summary:	The Python 2 package contains the Python development environment.
Name:		Python2
Version:	2.7.13
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	libffi >= 3.2.1
Source0:	Python-%{version}.tar.xz
%description
	The Python 2 package contains the Python development environment. 
	It is useful for object-oriented programming, writing scripts,
	prototyping large programs or developing entire applications.
	This version is for backward compatibility with other dependent packages. 
%prep
%setup -q -n Python-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--with-ensurepip=yes \
		--enable-unicode=ucs4
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	chmod -v 755 %{buildroot}/usr/lib/libpython2.7.so.1.0
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm "%{buildroot}/usr/lib/python2.7/site-packages/setuptools/command/launcher manifest.xml"
	rm "%{buildroot}/usr/lib/python2.7/site-packages/setuptools/script (dev).tmpl"
	rm "%{buildroot}/usr/bin/2to3"
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> Python-2.7.13-1
-	Initial build.	First version