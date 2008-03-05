%define name sablotron
%define version 1.0.3

%define	altname Sablot
%define builddir $RPM_BUILD_DIR/%{altname}-%{version}
%define libname_orig libsablotron
%define major 0
%define libname %mklibname %{name} %{major}

%{!?jscript: %define jscript 1}
%{!?readline: %define readline 0}
%{!?GPL: %define GPL 0}

Summary:	XSLT, XPath and DOM processor
Name:		%{name}
Version:	%{version}
Release:	%mkrel 3
%if %{GPL} 
License:	GPL
%else
License:	MPL/GPL
%endif
Group:		Development/Other
URL:		http://www.gingerall.cz
Source0:	http://download-1.gingerall.cz/download/sablot/%{altname}-%{version}.tar.bz2
Source1:	http://download-1.gingerall.cz/download/sablot/SabTest-%{version}.tar.bz2
BuildRequires:	expat-devel >= 1.95.2
BuildRequires:	perl-XML-Parser
BuildRequires:	ncurses-devel
BuildRequires:	libstdc++-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9 >= 1.9.2
%if %{jscript}
BuildRequires:	js-devel >= 1.5
%endif 
%if %{readline}
BuildRequires:	readline-devel
%endif
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%package -n	%{libname}-devel
Summary:	The development libraries and header files for Sablotron
Requires:	sablotron = %{version}
Group:		System/Libraries
Requires(post,preun): %{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	sablotron-devel = %{version}

%description -n	%{libname}-devel
These are the development libraries and header files for Sablotron

%prep
%if %{readline} && !%{GPL}
echo "The readline library may not be linked to non GPL'ed programs, so if you want to have readline support in the debugger, you have to choose the GPL from Sablotron license model."
exit 1
%endif

%setup -q -n %{altname}-%{version} -a1
perl -pi -e 's,SABLOT_LIBS="-L\$sab_base/lib",SABLOT_LIBS="-L\$sab_base/%{_lib}",' SabTest-%{version}/configure{.in,}

%build
%if %{jscript}
export CPLUS_INCLUDE_PATH=%{_includedir}/js-1.5
%endif
export CXXFLAGS="%{optflags}"
%if %{GPL}
export SABLOT_GPL=1
%endif
%configure2_5x \
%if %{jscript}
    --enable-javascript \
%endif
%if %{GPL} && %{readline}
    --with-readline \
%endif
    --enable-debugger

%make

# make and run the test suite
make DESTDIR=`pwd`/SabTest-%{version} install
pushd SabTest-%{version}
%configure2_5x --with-sablot=`pwd`/usr
%make
make test
make test-js
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/sablot-config
%endif

# nuke installed docs
rm -rf %{buildroot}%{_datadir}/doc

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(755,root,root)
%{_bindir}/sabcmd
%_mandir/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc README RELEASE doc/misc/NOTES doc/misc/DEBUGGER
%{_libdir}/libsablot.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/apidoc/sablot doc/apidoc/jsdom-ref doc/apidoc/sxp
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/sablot-config
%endif
%{_bindir}/sablot-config
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_includedir}/*.h


