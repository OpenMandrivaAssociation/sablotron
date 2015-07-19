%define	altname Sablot
%define builddir $RPM_BUILD_DIR/%{altname}-%{version}
%define libname_orig libsablotron

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define jscript 1
%define readline 0
%define GPL 0

Summary:	XSLT, XPath and DOM processor
Name:		sablotron
Version:	1.0.3
Release:	21
%if %{GPL} 
License:	GPL
%else
License:	MPL/GPL
%endif
Group:		Development/Other
URL:		http://www.gingerall.cz
Source0:	http://download-1.gingerall.cz/download/sablot/%{altname}-%{version}.tar.bz2
Source1:	http://download-1.gingerall.cz/download/sablot/SabTest-%{version}.tar.bz2
Patch0:		Sablot-linkage_fix.diff
Patch1:		sablot-automake-1.13.patch
BuildRequires:	expat-devel >= 1.95.2
BuildRequires:	perl-XML-Parser
BuildRequires:	ncurses-devel
BuildRequires:	libstdc++-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9 >= 1.9.2
BuildRequires:	libtool
%if %{jscript}
BuildRequires:	js-devel >= 1.5
BuildRequires:	pkgconfig
%endif 
%if %{readline}
BuildRequires:	readline-devel
%endif

%description
Sablotron is a fast, compact and portable XML toolkit
implementing XSLT, DOM and XPath.

The goal of this project is to create a lightweight,
reliable and fast XML library processor conforming to the W3C
specification, which is available for public and can be used as a base
for multi-platform XML applications.

%package -n	%{libname}
Summary:	Main library for sablotron
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n	%{libname}
Contains the library for sablotron.

%package -n	%{develname}
Summary:	The development libraries and header files for Sablotron
Requires:	sablotron = %{version}
Group:		Development/C
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	sablotron-devel = %{version}
Obsoletes:	%{mklibname %{name} -d 0}

%description -n	%{develname}
These are the development libraries and header files for Sablotron

%prep

%if %{readline} && !%{GPL}
echo "The readline library may not be linked to non GPL'ed programs, so if you want to have readline support in the debugger, you have to choose the GPL from Sablotron license model."
exit 1
%endif

%setup -q -n %{altname}-%{version} -a1
%patch0 -p0
%patch1 -p1 -b .am113~

perl -pi -e 's,SABLOT_LIBS="-L\$sab_base/lib",SABLOT_LIBS="-L\$sab_base/%{_lib}",' SabTest-%{version}/configure{.in,}

%if %{jscript}
JS_INCLUDE_PATH=`pkg-config --cflags libjs|sed -e 's/-I\/usr//'`
perl -pi -e "s|/include/js\b|$JS_INCLUDE_PATH|g" configure*
%endif
touch NEWS AUTHORS ChangeLog
autoreconf -fi
pushd SabTest-%{version}
touch NEWS AUTHORS ChangeLog
autoreconf -fi
popd

%build

export CXXFLAGS="%{optflags}"

%if %{jscript}
export CPLUS_INCLUDE_PATH=`pkg-config --cflags libjs|sed -e 's/-I//'`
%endif

%if %{GPL}
export SABLOT_GPL=1
%endif

%configure \
%if %{jscript}
    --enable-javascript=%{_prefix} \
%endif
%if %{GPL} && %{readline}
    --with-readline \
%endif
    --enable-debugger

%make

%check
# make and run the test suite
make DESTDIR=`pwd`/SabTest-%{version} install
pushd SabTest-%{version}
touch NEWS AUTHORS ChangeLog
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy
%configure2_5x --with-sablot=`pwd`/usr
%make
make test
make test-js
popd

%install

%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/sablot-config

# nuke installed docs
rm -rf %{buildroot}%{_datadir}/doc

%files
%{_bindir}/sabcmd
%_mandir/man1/*

%files -n %{libname}
%doc README RELEASE doc/misc/NOTES doc/misc/DEBUGGER
%{_libdir}/libsablot.so.*

%files -n %{develname}
%doc doc/apidoc/sablot doc/apidoc/jsdom-ref doc/apidoc/sxp
%{_bindir}/sablot-config
%{multiarch_bindir}/sablot-config
%{_libdir}/lib*.so
%{_includedir}/*.h
