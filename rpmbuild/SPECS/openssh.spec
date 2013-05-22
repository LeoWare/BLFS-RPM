Summary:	'Free version of the SSH connectivity tools
Name:		openssh
Version:	6.2p1
Release:	2
License:	BSD
URL:		http://openssh.org
Group:		BLFS/Security
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.gz
Source1:	blfs-bootscripts-20130512.tar.bz2

%description
The OpenSSH package contains ssh clients and the sshd daemon. This is
useful for encrypting authentication and subsequent traffic over a 
network. The ssh and scp commands are secure implementions of telnet 
and rcp respectively.
%prep
%setup -q
tar xf %{SOURCE1}
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc/ssh     \
	--datadir=/usr/share/sshd \
	--with-md5-passwords      \
	--with-privsep-path=/var/lib/sshd
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
mkdir -vp %{buildroot}/var/lib/sshd
echo "PermitRootLogin no" >> %{buildroot}/etc/ssh/sshd_config
#	Install daemon script
pushd blfs-bootscripts-20130512
make DESTDIR=%{buildroot} install-sshd
popd
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post
/sbin/ldconfig
chown -v root:sys /var/lib/sshd
if ! getent group sshd >/dev/null; then
	groupadd -g 50 sshd
fi
if ! getent passwd sshd >/dev/null; then
	useradd -c 'sshd PrivSep' -d /var/lib/sshd -g sshd -s /bin/false -u 50 sshd
fi
ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa
%postun
/sbin/ldconfig
if getent passwd sshd >/dev/null; then
	userdel sshd
fi
if getent group sshd >/dev/null; then
	groupdel sshd
fi
%clean
rm -rf %{buildroot}/*
#%files -f %{name}.lang
%files
%defattr(-,root,root)
%{_sysconfdir}/ssh/*
%{_sysconfdir}/rc.d/init.d/sshd
%{_sysconfdir}/rc.d/rc0.d/K30sshd
%{_sysconfdir}/rc.d/rc1.d/K30sshd
%{_sysconfdir}/rc.d/rc2.d/K30sshd
%{_sysconfdir}/rc.d/rc3.d/S30sshd
%{_sysconfdir}/rc.d/rc4.d/S30sshd
%{_sysconfdir}/rc.d/rc5.d/S30sshd
%{_sysconfdir}/rc.d/rc6.d/K30sshd
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(700,root,sys)/var/lib/sshd
%changelog
*	Wed May 22 2013 baho-utot <baho-utot@columbus.rr.com> 6.2p1-1
-	Initial build.	First version
