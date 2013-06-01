Summary:	The ISC BIND nameserver
Name:		bind
Version:	9.9.2
Release:	1
License:	ISC
URL:		http://www.isc.org/software/bind/
Group:		BLFS/MajorServers
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://ftp.isc.org/isc/bind9/%{version}/%{name}-%{version}-P2.tar.gz
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20130512.tar.bz2
Provides:	libbind9.so.90 = 9.9.2
Provides:	libdns.so.95 = 9.9.2
Provides:	libisc.so.92 = 9.9.2
Provides:	libisccc.so.90 = 9.9.2
Provides:	libisccfg.so.90 = 9.9.2
Provides:	liblwres.so.90 = 9.9.2
%description
The BIND package provides a DNS server and client utilities.
%prep
%setup -q -n %{name}-%{version}-P2
tar xf %{SOURCE1}
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--localstatedir=/var \
	--mandir=%{_mandir} \
	--sysconfdir=/etc \
	--disable-static \
	--enable-threads \
	--with-libtool
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/etc/namedb
install -v -m755 -d %{buildroot}%{_datadir}/doc/%{name}-%{version}/{arm,misc}
install -v -m644 doc/arm/*.html %{buildroot}%{_datadir}/doc/%{name}-%{version}/arm
install -v -m644 doc/misc/{dnssec,ipv6,migrat*,options,rfc-compliance,roadmap,sdb} \
	%{buildroot}%{_datadir}/doc/%{name}-%{version}/misc
install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
#
#	Bind configuration caching server
#
cat >> %{buildroot}/etc/named.conf << "EOF"
options {
	directory "/etc/namedb";
	pid-file "/var/run/named.pid";
	statistics-file "/var/run/named.stats";
	recursion yes;
	allow-recursion {192.168.1.0/24;};
};
zone "." {
    type hint;
    file "named.root";
};
zone "localhost" in {
	type master;
	file "localhost.fwd";
	allow-update {none;};
};
zone "0.0.127.in-addr.arpa" {
	type master;
	file "localhost.rev";
	allow-update {none;};
};
logging {
	category default { default_syslog; default_debug; };
	category unmatched { null; };
	channel default_syslog {
		syslog daemon;		// send to syslog's daemon facility
		severity info;		// only send priority >= info
	};
	channel default_debug {
		file "named.run";
		severity dynamic;
	};
	channel default_stderr {
		stderr;			// writes to stderr
		severity info;		// only send priority >= info
	};
	channel null {
		null;			// toss anything sent to
	};
};
EOF

cat > %{buildroot}/etc/namedb/named.root << "EOF"
;       This file holds the information on root name servers needed to
;       initialize cache of Internet domain name servers
;       (e.g. reference this file in the "cache  .  <file>"
;       configuration file of BIND domain name servers).
;
;       This file is made available by InterNIC 
;       under anonymous FTP as
;           file                /domain/named.cache
;           on server           FTP.INTERNIC.NET
;       -OR-                    RS.INTERNIC.NET
;
;       last update:    Jan 3, 2013
;       related version of root zone:   2013010300
;
; formerly NS.INTERNIC.NET
;
.                        3600000  IN  NS    A.ROOT-SERVERS.NET.
A.ROOT-SERVERS.NET.      3600000      A     198.41.0.4
A.ROOT-SERVERS.NET.      3600000      AAAA  2001:503:BA3E::2:30
;
; FORMERLY NS1.ISI.EDU
;
.                        3600000      NS    B.ROOT-SERVERS.NET.
B.ROOT-SERVERS.NET.      3600000      A     192.228.79.201
;
; FORMERLY C.PSI.NET
;
.                        3600000      NS    C.ROOT-SERVERS.NET.
C.ROOT-SERVERS.NET.      3600000      A     192.33.4.12
;
; FORMERLY TERP.UMD.EDU
;
.                        3600000      NS    D.ROOT-SERVERS.NET.
D.ROOT-SERVERS.NET.      3600000      A     199.7.91.13
D.ROOT-SERVERS.NET.	 3600000      AAAA  2001:500:2D::D
;
; FORMERLY NS.NASA.GOV
;
.                        3600000      NS    E.ROOT-SERVERS.NET.
E.ROOT-SERVERS.NET.      3600000      A     192.203.230.10
;
; FORMERLY NS.ISC.ORG
;
.                        3600000      NS    F.ROOT-SERVERS.NET.
F.ROOT-SERVERS.NET.      3600000      A     192.5.5.241
F.ROOT-SERVERS.NET.      3600000      AAAA  2001:500:2F::F
;
; FORMERLY NS.NIC.DDN.MIL
;
.                        3600000      NS    G.ROOT-SERVERS.NET.
G.ROOT-SERVERS.NET.      3600000      A     192.112.36.4
;
; FORMERLY AOS.ARL.ARMY.MIL
;
.                        3600000      NS    H.ROOT-SERVERS.NET.
H.ROOT-SERVERS.NET.      3600000      A     128.63.2.53
H.ROOT-SERVERS.NET.      3600000      AAAA  2001:500:1::803F:235
;
; FORMERLY NIC.NORDU.NET
;
.                        3600000      NS    I.ROOT-SERVERS.NET.
I.ROOT-SERVERS.NET.      3600000      A     192.36.148.17
I.ROOT-SERVERS.NET.      3600000      AAAA  2001:7FE::53
;
; OPERATED BY VERISIGN, INC.
;
.                        3600000      NS    J.ROOT-SERVERS.NET.
J.ROOT-SERVERS.NET.      3600000      A     192.58.128.30
J.ROOT-SERVERS.NET.      3600000      AAAA  2001:503:C27::2:30
;
; OPERATED BY RIPE NCC
;
.                        3600000      NS    K.ROOT-SERVERS.NET.
K.ROOT-SERVERS.NET.      3600000      A     193.0.14.129
K.ROOT-SERVERS.NET.      3600000      AAAA  2001:7FD::1
;
; OPERATED BY ICANN
;
.                        3600000      NS    L.ROOT-SERVERS.NET.
L.ROOT-SERVERS.NET.      3600000      A     199.7.83.42
L.ROOT-SERVERS.NET.      3600000      AAAA  2001:500:3::42
;
; OPERATED BY WIDE
;
.                        3600000      NS    M.ROOT-SERVERS.NET.
M.ROOT-SERVERS.NET.      3600000      A     202.12.27.33
M.ROOT-SERVERS.NET.      3600000      AAAA  2001:DC3::35
; End of File
EOF

cat > %{buildroot}/etc/namedb/localhost.fwd << "EOF"
$TTL 24H
$ORIGIN localhost.
@	IN	SOA	hostmaster	(
	1	; Serial
	12H	; Refresh
	2H	; Retry
	4W	; Expire
	1D)     ; Minimum TTL
localhost.	IN	NS	localhost.
localhost.	IN	A	127.0.0.1
EOF

cat > %{buildroot}/etc/namedb/localhost.rev << "EOF"
$TTL 24H
$ORIGIN 0.0.127.IN-ADDR.ARPA.
@	IN	SOA	localhost. hostmaster.localhost	(
	1	; Serial
	12H	; Refresh
	2H	; Retry
	4W	; Expire
	1D)     ; Minimum TTL
	IN	NS	localhost.
1	IN	PTR	localhost.
EOF
#	daemonize
pushd blfs-bootscripts-20130512
make DESTDIR=%{buildroot} install-bind
popd
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%pre
if ! getent group named >/dev/null; then
	groupadd -g 20 named
fi
if ! getent passwd named >/dev/null; then
	useradd -c "BIND Owner" -g named -s /bin/false -u 20 named
fi
%postun
/sbin/ldconfig
if getent passwd named >/dev/null; then
	userdel named
fi
if getent group named >/dev/null; then
	groupdel named
fi
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%config(noreplace) /etc/bind.keys
%config(noreplace) /etc/named.conf
%config(noreplace) /etc/namedb/localhost.fwd
%config(noreplace) /etc/namedb/localhost.rev
%config(noreplace) /etc/namedb/named.root
/etc/rc.d/init.d/bind
/etc/rc.d/rc0.d/K49bind
/etc/rc.d/rc1.d/K49bind
/etc/rc.d/rc2.d/K49bind
/etc/rc.d/rc3.d/S22bind
/etc/rc.d/rc4.d/S22bind
/etc/rc.d/rc5.d/S22bind
/etc/rc.d/rc6.d/K49bind
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so*
%{_sbindir}/*
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/licenses/bind/LICENSE
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%changelog
*	Sat Jun 01 2013 baho-utot <baho-utot@columbus.rr.com> 9.9.2-1
-	Initial build.	First version