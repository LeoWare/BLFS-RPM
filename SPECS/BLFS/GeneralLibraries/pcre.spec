#	 https://downloads.sourceforge.net/pcre/pcre-8.41.tar.bz2
Summary:	The cpio package contains tools for archiving
Name:		pcre
Version:	8.41
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
		--docdir=/usr/share/doc/pcre-8.41 \
		--enable-unicode-properties \
		--enable-pcre16 \
		--enable-pcre32 \
		--enable-pcregrep-libz \
		--enable-pcregrep-libbz2 \
		--enable-pcretest-libreadline \
		--disable-static
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -vdm 755 %{buildroot}/lib
	mv -v %{buildroot}/usr/lib/libpcre.so.* %{buildroot}/lib
	ln -sfv ../../lib/$(readlink %{buildroot}/usr/lib/libpcre.so) %{buildroot}/usr/lib/libpcre.so
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
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> pcre-8.41-1
-	Initial build.	First version