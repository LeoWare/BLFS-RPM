#	screen-4.5.1.tar.gz
Summary:	Screen is a terminal multiplexor that runs several separate processes
Name:		screen
Version:	4.5.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.gz
%description
	Screen is a terminal multiplexor that runs several separate processes,
	typically interactive shells, on a single physical character-based terminal.
	Each virtual terminal emulates a DEC VT100 plus several ANSI X3.64 and
	ISO 2022 functions and also provides configurable input and output translation,
	serial port support, configurable logging, multi-user support, and many
	character encodings, including UTF-8. Screen sessions can be detached and
	resumed later on a different terminal. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure --prefix=%{_prefix} \
		--infodir=/usr/share/info \
		--mandir=/usr/share/man \
		--with-socket-dir=/run/screen \
		--with-pty-group=5 \
		--with-sys-screenrc=/etc/screenrc
	sed -i -e "s%/usr/local/etc/screenrc%/etc/screenrc%" {etc,doc}/*
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -vDm 644 etc/etcscreenrc %{buildroot}/etc/screenrc
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
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> screen-4.5.1-1
-	Initial build.	First version