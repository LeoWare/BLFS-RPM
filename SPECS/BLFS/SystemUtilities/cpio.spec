#	cpio-2.12.tar.bz2
Summary:	The cpio package contains tools for archiving
Name:		cpio
Version:	2.12
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.bz2
%description
	The cpio package contains tools for archiving
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--bindir=/bin \
		--enable-mt \
		--with-rmt=/usr/libexec/rmt
	make %{?_smp_mflags}
	makeinfo --html            -o doc/html      doc/cpio.texi
	makeinfo --html --no-split -o doc/cpio.html doc/cpio.texi
	makeinfo --plaintext       -o doc/cpio.txt  doc/cpio.texi
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> cpio-2.12-1
-	Initial build.	First version