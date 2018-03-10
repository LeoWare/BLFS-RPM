#		https://downloads.xiph.org/releases/cdparanoia/cdparanoia-III-10.2.src.tgz
Summary:	The CDParanoia package contains a CD audio extraction tool
Name:		cdparanoia-III
Version:	10.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}.src.tgz
Patch0:		cdparanoia-III-10.2-gcc_fixes-1.patch
%description
	The CDParanoia package contains a CD audio extraction tool. This is useful for
	extracting .wav files from audio CDs. A CDDA capable CDROM drive is needed.
	Practically all drives supported by Linux can be used. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%patch0 -p1
%build
	./configure \
		--prefix=%{_prefix} \
		--mandir=%{_mandir}
	make -j1
%install
	make prefix="%{buildroot}/usr" MANDIR="%{buildroot}%{_mandir}" install
	chmod -v 755 %{buildroot}%{_libdir}/libcdda_*.so.0.10.2
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_bindir}/cdparanoia
	%{_includedir}/*.h
	%{_libdir}/*.a
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.2
	%{_mandir}/man1/cdparanoia.1.gz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 10.2-1
-	Initial build.	First version