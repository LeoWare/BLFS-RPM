#		https://dbus.freedesktop.org/releases/dbus/dbus-1.10.22.tar.gz
Summary:	D-Bus is a message bus system, a simple way for applications to talk to one another
Name:		dbus
Version:	1.10.22
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}.tar.gz
%description
	D-Bus is a message bus system, a simple way for applications to talk to one another.
	D-Bus supplies both a system daemon (for events such as "new hardware device added"
	or "printer queue changed") and a per-user-login-session daemon (for general IPC
	needs among user applications). Also, the message bus is built on top of a general
	one-to-one message passing framework, which can be used by any two applications to
	communicate directly (without going through the message bus daemon). D-Bus is a
	message bus system, a simple way for applications to talk to one another. D-Bus
	supplies both a system daemon (for events such as "new hardware device added" or
	"printer queue changed") and a per-user-login-session daemon (for general IPC needs
	among user applications). Also, the message bus is built on top of a general
	one-to-one message passing framework, which can be used by any two applications to
	communicate directly (without going through the message bus daemon). 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--sysconfdir=%{_sysconfdir} \
		--localstatedir=%{_localstatedir} \
		--disable-doxygen-docs \
		--disable-xml-docs \
		--disable-static \
		--docdir=%{_datarootdir}/doc/%{name}-%{version} \
		--with-console-auth-dir=/run/console \
		--with-system-pid-file=/run/dbus/pid \
		--with-system-socket=/run/dbus/system_bus_socket
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	#	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	#	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%pre
	/usr/bin/getent group  messagebus || /usr/sbin/groupadd -g 18 messagebus
	/usr/bin/getent passwd messagebus || /usr/sbin/useradd  -c "D-Bus Message Daemon User" -d /var/run/dbus -u 18 -g messagebus -s /bin/false messagebus
%post	-p /sbin/ldconfig
%postun	
	/sbin/ldconfig
	/usr/sbin/userdel messagebus
%files
	%defattr(-,root,root)
	%{_sysconfdir}/dbus-1
	%{_bindir}/dbus-cleanup-sockets
	%{_bindir}/dbus-daemon
	%{_bindir}/dbus-launch
	%{_bindir}/dbus-monitor
	%{_bindir}/dbus-run-session
	%{_bindir}/dbus-send
	%{_bindir}/dbus-test-tool
	%{_bindir}/dbus-update-activation-environment
	%{_bindir}/dbus-uuidgen
	%{_includedir}/dbus-1.0
	/usr/lib/dbus-1.0/include/dbus/dbus-arch-deps.h
	%{_libdir}/libdbus-1.so
	%{_libdir}/libdbus-1.so.3
	%{_libdir}/libdbus-1.so.3.14.13
	%{_libdir}/pkgconfig/dbus-1.pc
	%{_libexecdir}/dbus-daemon-launch-helper
	%{_datarootdir}/dbus-1
	%{_datarootdir}/doc/%{name}-%{version}
%changelog
*	Thu Mar 01 2018 baho-utot <baho-utot@columbus.rr.com> 1.10.22-1
-	Initial build.	First version