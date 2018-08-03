#	MarkupSafe-1.0.tar.gz
Summary:	MarkupSafe is a Python module that implements a XML/HTML/XHTML Markup safe string
Name:		MarkupSafe	
Version:	1.0
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
	MarkupSafe is a Python module that implements a XML/HTML/XHTML Markup safe string
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
%install
	python setup.py build
	python setup.py install --root="%{buildroot}" --optimize=1
	python3 setup.py build
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
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> MarkupSafe-1.0-1
-	Initial build.	First version