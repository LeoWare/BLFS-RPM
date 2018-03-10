#	funcsigs-1.0.2.tar.gz
Summary:	funcsigs is a is a backport of the PEP 362 function signature features from Python 3.3's inspect module for Python 2.x. 
Name:		python2-funcsigs
Version:	1.0.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	Python2 >= 2.7.13
Source0:	funcsigs-%{version}.tar.gz
%description
	funcsigs is a is a backport of the PEP 362 function signature features from Python 3.3's inspect module for Python 2.x.
%prep
%setup -q -n funcsigs-%{VERSION}
%build
%install
	python setup.py install --root="%{buildroot}" --optimize=1
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
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> funcsigs-1.0.2-1
-	Initial build.	First version