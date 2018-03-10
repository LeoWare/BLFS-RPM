#	curl-7.55.1.tar.xz
Summary:	The cURL package contains an utility and a library used for transferring files
Name:		curl
Version:	7.55.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	 Certificate-Authority-Certificates >= 8.1, OpenSSL >= 1.1.0f 
Source0:	%{name}-%{version}.tar.xz
%description
	The cURL package contains an utility and a library used for transferring files with
	URL syntax to any of the following protocols: FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP,
	TELNET, DICT, LDAP, LDAPS and FILE. Its ability to both download and upload files can
	be incorporated into other programs to support functions like streaming media. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static \
		--enable-threaded-resolver \
		--with-ca-path=/etc/ssl/certs
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	rm -rf docs/examples/.deps
	find docs \( -name Makefile\* -o -name \*.1 -o -name \*.3 \) -exec rm {} \;
	install -v -d -m755 %{buildroot}/usr/share/doc/curl-7.55.1
	cp -v -R docs/* %{buildroot}/usr/share/doc/curl-7.55.1
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
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> curl-7.55.1-1
-	Initial build.	First version