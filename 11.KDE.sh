#!/bin/bash
#################################################
#	Title:	10-KDE.sh			#
#        Date:	2018-02-10			#
#     Version:	1.1				#
#      Author:	baho-utot@columbus.rr.com	#
#     Options:					#
#################################################
set -o errexit	# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
TOPDIR=${PWD}
	#	Build variables
LC_ALL=POSIX
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin
export LC_ALL PATH
#
PARENT=/usr/src/Octothorpe
LOGPATH=${TOPDIR}/LOGS/BLFS
INFOPATH=${TOPDIR}/INFO/BLFS
SPECPATH=${TOPDIR}/SPECS/BLFS
PROVIDESPATH=${TOPDIR}/PROVIDES/BLFS
REQUIRESPATH=${TOPDIR}/REQUIRES/BLFS
RPMPATH=${TOPDIR}/RPMS
#
#	Build functions
#
die() {	
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	exit 1
}
msg() {
	printf "%s\n" "${1}"
}
msg_line() {
	printf "%s" "${1}"
}
msg_failure() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	printf "${_red}%s${_normal}\n" "FAILURE"
	exit 2
}
msg_success() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "SUCCESS"
	return 0
}
end-run() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "Run Complete"
	return
}

maker(){	#	$1:	name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	local _filespec=${SPECPATH}/${1}.spec
	#
	#	Build
	#
	msg_line "	Building: ${1}: "
	if [ -z ${_pkg} ]; then
		rm ${_log}.installed > ${_log} 2>&1	|| true
		rm ${INFOPATH}/${1} > ${_log} 2>&1	|| true
		rpmbuild -ba \
			${_filespec} >> ${_log} 2>&1 && msg_success || msg_failure
		_pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print)
	else
		msg "Skipped"
		#	return
	fi
}
info(){		#	$1:	Name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	#
	#	Info
	#
	msg_line "	Info: ${1}: "
	[ -z ${_pkg} ] && die "ERROR: rpm package not found"
	if [ ! -e ${INFOPATH}/${1} ]; then
		rpm -qilp \
			${_pkg} > ${INFOPATH}/${1} 2>&1 || true
		rpm -qp --provides \
			${_pkg} > ${PROVIDESPATH}/${1} 2>&1 || true
		rpm -qp --requires \
			${_pkg} > ${REQUIRESPATH}/${1} 2>&1 || true
		msg_success
	else
		 msg "Skipped"
	fi
}
installer(){	#	$1:	name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	#
	#	Install
	#
	msg_line "	Installing: ${1}: "
	[ -z ${_pkg} ] && die "ERROR: rpm package not found"
	if [ ! -e ${_log}.installed ]; then
		su -c "rpm -Uvh --nodeps ${_pkg}" >> "${_log}" 2>&1  && msg_success || msg_failure
		mv ${_log} ${_log}.installed
	else
		msg "Skipped"
	fi
}
_prepare() {
	local _log="${LOGPATH}/${1}"
	_wget_list	#	Create wget list
	_md5sum_list	#	Create md5sum list
	#	Fetch source packages
	local DESTDIR=""
	local INPUTFILE=""
	msg_line "	Fetching source: "
		[ -d SOURCES ] || install -vdm 755 ${DESTDIR}
		#	LFS sources
		DESTDIR=${TOPDIR}/SOURCES
		INPUTFILE=${TOPDIR}/SOURCES/kde.wget
		wget --no-clobber --no-check-certificate --input-file=${INPUTFILE} --directory-prefix=${DESTDIR} > /dev/null 2>&1
	msg_success
	msg_line "	Checking source: "
		md5sum -c ${TOPDIR}/SOURCES/kde.md5sum >> ${_log}
	msg_success
	cp config-4.12.7.graphics.patch		SOURCES
	cp config-4.12.7.sound.patch		SOURCES
	cp config-4.12.7.powersave.patch	SOURCES
	return
}
_post() {
	return
	local _log="${LOGPATH}/${1}"
	msg "	Post processing:"
	return
}
_wget_list() {
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/kde.wget <<- EOF
			http://download.kde.org/stable/phonon/4.9.1/phonon-4.9.1.tar.xz
		EOF
		#	dependencies
		cat >> ${PARENT}/SOURCES/kde.wget <<- EOF
			https://curl.haxx.se/download/curl-7.55.1.tar.xz
			https://cmake.org/files/v3.9/cmake-3.9.1.tar.gz
			http://download.kde.org/stable/frameworks/5.37/extra-cmake-modules-5.37.0.tar.xz
			ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.4.1.tar.bz2
			https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.7.tar.xz
			https://ftp.gnu.org/gnu/libtasn1/libtasn1-4.12.tar.gz
			https://github.com/p11-glue/p11-kit/releases/download/0.23.8/p11-kit-0.23.8.tar.gz
			https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.14.tar.xz
			https://github.com//libusb/libusb/releases/download/v1.0.21/libusb-1.0.21.tar.bz2
			https://dbus.freedesktop.org/releases/dbus/dbus-1.10.22.tar.gz
			https://github.com/apple/cups/releases/download/v2.2.4/cups-2.2.4-source.tar.gz
			https://www.openprinting.org/download/cups-filters/cups-filters-1.17.2.tar.xz
			http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
			https://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-1.5.2.tar.gz
			http://download.osgeo.org/libtiff/tiff-4.0.8.tar.gz
			https://downloads.sourceforge.net/qpdf/qpdf-6.0.0.tar.gz
			https://poppler.freedesktop.org/poppler-0.57.0.tar.xz
			https://poppler.freedesktop.org/poppler-data-0.4.8.tar.gz
			https://downloads.sourceforge.net/lcms/lcms2-2.8.tar.gz
			https://downloads.sourceforge.net/openjpeg.mirror/openjpeg-1.5.2.tar.gz
			https://www.cairographics.org/releases/pixman-0.34.0.tar.gz
			https://www.cairographics.org/releases/cairo-1.14.10.tar.xz
			https://archive.mozilla.org/pub/nspr/releases/v4.16/src/nspr-4.16.tar.gz
			https://archive.mozilla.org/pub/security/nss/releases/NSS_3_32_RTM/src/nss-3.32.tar.gz
			https://sqlite.org/2017/sqlite-autoconf-3200000.tar.gz
			https://archive.mozilla.org/pub/security/nss/releases/NSS_3_32_RTM/src/nss-3.32.tar.gz
			http://www.linuxfromscratch.org/patches/blfs/8.1/nss-3.32-standalone-1.patch
			http://download.icu-project.org/files/icu4c/59.1/icu4c-59_1-src.tgz
			https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs921/ghostscript-9.21.tar.gz
			https://downloads.sourceforge.net/gs-fonts/ghostscript-fonts-std-8.11.tar.gz
			https://downloads.sourceforge.net/gs-fonts/gnu-gs-fonts-other-6.0.tar.gz
			https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.4.8.tar.bz2
			http://www.mupdf.com/downloads/archive/mupdf-1.11-source.tar.gz
			http://www.linuxfromscratch.org/patches/blfs/8.1/mupdf-1.11-shared_libs-1.patch
			http://www.linuxfromscratch.org/patches/blfs/8.1/mupdf-1.11-openjpeg-2.patch
			https://github.com/uclouvain/openjpeg/archive/v2.2.0/openjpeg-2.2.0.tar.gz
			https://www.openprinting.org/download/ijs/download/ijs-0.35.tar.bz2
		EOF
	msg_success
	return
}
_md5sum_list(){
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/kde.md5sum <<- EOF
			7896a560f5da345a626e782610c8e71e	SOURCES/phonon-4.9.1.tar.xz
		EOF
		#	Dependencies
		cat >> ${PARENT}/SOURCES/kde.md5sum <<- EOF
			ac4a59c38c47adc160ea71eace20257b	SOURCES/curl-7.55.1.tar.xz
			00f43c6a56d4903436317c14f9ca7f37	SOURCES/cmake-3.9.1.tar.gz
			29883c1580c5b9e4c736a138fc832e1a	SOURCES/extra-cmake-modules-5.37.0.tar.xz
			29fa3e69122d3cf3e8f0e01a0cb1d183	SOURCES/alsa-lib-1.1.4.1.tar.bz2
			82e0545363d111bfdfec2ddbfe62ffd3	SOURCES/libunistring-0.9.7.tar.xz
			5c724bd1f73aaf4a311833e1cd297b21	SOURCES/libtasn1-4.12.tar.gz
			3caf26d841df1527d52549e7adc62966	SOURCES/p11-kit-0.23.8.tar.gz
			1e84b57a472b5f3b01f2c1b7a3a2bcbe	SOURCES/gnutls-3.5.14.tar.xz
			1da9ea3c27b3858fa85c5f4466003e44	SOURCES/libusb-1.0.21.tar.bz2
			baaa10b7cb49086ad91179a8decfadc5	SOURCES/dbus-1.10.22.tar.gz
			d26e5a0a574a69fe1d01079b2931fc49	SOURCES/cups-2.2.4-source.tar.gz
			cbc3d40d572b25a78c828ea04f1248e8	SOURCES/cups-filters-1.17.2.tar.xz
			fc9e586751ff789b34b1f21d572d96af	SOURCES/yasm-1.3.0.tar.gz
			6b4923e297a7eaa255f08511017a8818	SOURCES/libjpeg-turbo-1.5.2.tar.gz
			2a7d1c1318416ddf36d5f6fa4600069b	SOURCES/tiff-4.0.8.tar.gz
			e014bd3ecf1c4d1a520bbc14d84ac20e	SOURCES/qpdf-6.0.0.tar.gz
			bc5a191741604552c90d484103229374	SOURCES/poppler-0.57.0.tar.xz
			00f8989c804de84af0ba2ea629949980	SOURCES/poppler-data-0.4.8.tar.gz
			87a5913f1a52464190bb655ad230539c	SOURCES/lcms2-2.8.tar.gz
			c41772c30fb1c272358b3707233134a1	SOURCES/openjpeg-1.5.2.tar.gz
			e80ebae4da01e77f68744319f01d52a3	SOURCES/pixman-0.34.0.tar.gz
			146f5f4d0b4439fc3792fd3452b7b12a	SOURCES/cairo-1.14.10.tar.xz
			42fd8963a4b394f62d43ba604f03fab7	SOURCES/nspr-4.16.tar.gz
			076abf8ed88b6bb28f3396b072d252ed	SOURCES/nss-3.32.tar.gz
			e262a28b73cc330e7e83520c8ce14e4d	SOURCES/sqlite-autoconf-3200000.tar.gz
			076abf8ed88b6bb28f3396b072d252ed	SOURCES/nss-3.32.tar.gz
			54923fa9fab5b2b83f235fb72523de37	SOURCES/icu4c-59_1-src.tgz
			5f213281761d2750fcf27476c404d17f	SOURCES/ghostscript-9.21.tar.gz
			6865682b095f8c4500c54b285ff05ef6	SOURCES/ghostscript-fonts-std-8.11.tar.gz
			33457d3f37de7ef03d2eea05a9e6aa4f	SOURCES/gnu-gs-fonts-other-6.0.tar.gz
			d1aa446e1e65717311c15d9ac0cf31ee	SOURCES/harfbuzz-1.4.8.tar.bz2
			ab9a6629f572225e803c4cf426bdb09c	SOURCES/mupdf-1.11-source.tar.gz
			269bb0b175476f3addcc0d03bd9a97b6	SOURCES/openjpeg-2.2.0.tar.gz
			896fdcb7a01c586ba6eb81398ea3f6e9	SOURCES/ijs-0.35.tar.bz2
		EOF
	msg_success
	return
}
#
#	Main line
#
[ -z ${PARENT} ]	&& die "${PRGNAME}: Variable: PARENT not set: FAILURE"
#
#	BLFS Desktop system
#
msg "Building KDE"
LIST=""
LIST+="prepare linux "
#
#	extra-cmake-modules-5.37.0
#
LIST+="openssl "
LIST+="Certificate-Authority-Certificates "	#	OpenSSL-1.1.0f
LIST+="curl "					#	Certificate Authority Certificates (runtime) and OpenSSL-1.1.0f
LIST+="libxml2 "				#	none
LIST+="libarchive "				#	libxml2-2.9.4, LZO-2.10, and Nettle-3.3 or OpenSSL-1.1.0f
LIST+="cmake "					#	cURL-7.55.1 and libarchive-3.3.2
LIST+="extra-cmake-modules "			#	CMake-3.9.1
#
#	Phonon-4.9.1
#
LIST+="pcre "					#	none
LIST+="libffi "					#	none
LIST+="Python2 "				#	libffi-3.2.1, openssl
LIST+="Python "					#	libffi-3.2.1, openssl
LIST+="glib "					#	pcre, libffi-3.2.1 and Python-2.7.13 or Python-3.6.2
LIST+="xorg-libs "				#	from .10-Xorg.sh
LIST+="alsa-lib "				#	none
#	QT
#	Python-2.7.13 and Xorg Libraries
#	alsa-lib-1.1.4.1, Certificate Authority Certificates, Cups-2.2.4, GLib-2.52.3, 
LIST+="nettle "					#	none
LIST+="libunistring "				#	none
LIST+="libtasn1 "				#	none
LIST+="p11-kit "				#	Certificate Authority Certificates, libtasn1-4.12, and libffi-3.2.1 
LIST+="gnutls "					#	Nettle-3.3, Certificate Authority Certificates, libunistring-0.9.7, libtasn1-4.12, and p11-kit-0.23.8
LIST+="libusb "					#	none
LIST+="dbus "					#	xorg-libs
LIST+="cups "					#	GnuTLS-3.5.14 Runtime: cups-filters-1.17.2 Gutenprint-5.2.12, Rec: Colord-1.2.12, dbus-1.10.22, and libusb-1.0.21 
#	cups-filter
LIST+="yasm "					#	none
LIST+="libjpeg-turbo "				#	yasm
LIST+="tiff "					#	libjpeg-turbo-1.5.2
LIST+="qpdf "					#	PCRE-8.41
LIST+="fontconfig "				#	10-Xor.sh
LIST+="libpng "					#	none
LIST+="lcms2 "					#	ibjpeg-turbo-1.5.2 and LibTIFF-4.0.8
LIST+="openjpeg "				#	Little CMS-2.8, libpng-1.6.31, LibTIFF-4.0.8
LIST+="pixman "					#	none
LIST+="cairo "					#	libpng-1.6.31 and Pixman-0.34.0 Rec:  Fontconfig-2.12.4, GLib-2.52.3 (required for most GUIs) and Xorg Libraries 
LIST+="nspr "					#	none
LIST+="sqlite-autoconf "				#	none
LIST+="nss "					#	NSPR-4.16 sqlite
LIST+="poppler "				#	Fontconfig-2.12.4, REC:	 Cairo-1.14.10, libjpeg-turbo-1.5.2, libpng-1.6.31, NSS-3.32, and OpenJPEG-1.5.2 
LIST+="ghostscript "				#
LIST+="icu "					#	LLVM-4.0.1 (with Clang), and Doxygen-1.8.13 (for documentation) 
LIST+="harfbuzz "				#	GLib-2.52.3 (required for Pango), ICU-59.1 and FreeType-2.8 (after HarfBuzz-1.4.8 is installed, reinstall FreeType-2.8) 
LIST+="openjpeg2 "				#	CMake-3.9.1:	Little CMS-2.8, libpng-1.6.31, LibTIFF-4.0.8, and Doxygen-1.8.13 (to build the API documentation) 
LIST+="mupdf "					#	Xorg Libraries, REC:  HarfBuzz-1.4.8, libjpeg-turbo-1.5.2, OpenJPEG-2.2.0, and cURL-7.55.1 
LIST+="ijs "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
#	cups-filters-1.17.2:	Cups-2.2.4, GLib-2.52.3, ghostscript-9.21, IJS-0.35, Little CMS-2.8, mupdf-1.11 (mutool), Poppler-0.57.0, and Qpdf-6.0.0
#				libjpeg-turbo-1.5.2, libpng-1.6.31 and LibTIFF-4.0.8
#	Gutenprint-5.2.12 :	Cups-2.2.4


#	QT


#	gst-plugins-base-1.12.2 (QtMultimedia backend), HarfBuzz-1.4.8, ICU-59.1, JasPer-2.0.12,
#	libjpeg-turbo-1.5.2, libmng-2.0.3, libpng-1.6.31, LibTIFF-4.0.8, libxkbcommon-0.7.2,
#	Mesa-17.1.6, mtdev-1.1.5, OpenSSL-1.0.2l Libraries, pcre2-10.30, SQLite-3.20.0,
#	Wayland-1.14.0 (Mesa must be built with Wayland EGL backend), xcb-util-image-0.4.0,
#	xcb-util-keysyms-0.4.0, xcb-util-renderutil-0.3.9, and xcb-util-wm-0.4.1 
#
#LIST+="qt "					#
#LIST+="phonon "				#	CMake-3.9.1, extra-cmake-modules-5.37.0, GLib-2.52.3, and Qt-5.9.1 

LIST+="post"
for i in ${LIST};do
	rm -rf BUILD BUILDROOT
	case ${i} in
		prepare)	_prepare "kde.${i}"	;;
		post)		_post ${i}		;;
		*)		maker ${i}	
				info  ${i}
				installer ${i}		;;
	esac
done
end-run