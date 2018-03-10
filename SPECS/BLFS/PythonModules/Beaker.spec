#	Beaker-1.9.0.tar.gz
Summary:	Beaker is a Python module that implements caching and sessions WSGI middleware
Name:		Beaker
Version:	1.9.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	Python2 >= 2.7.13, Python >= 3.6.2
Source0:	%{NAME}-%{version}.tar.gz
%description
	Beaker is a Python module that implements caching and sessions WSGI middleware
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
%install
	python setup.py install --root="%{buildroot}" --optimize=1
	python3 setup.py install --root="%{buildroot}" --optimize=1
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
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
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> Beaker-1.9.0-1
-	Initial build.	First version