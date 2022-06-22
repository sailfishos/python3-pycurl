Name:           python3-pycurl
Version:        7.43.0.5
Release:        1
Summary:        A Python interface to libcurl
License:        LGPLv2+ or MIT
URL:            https://github.com/sailfishos/python3-pycurl
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
Requires:       libcurl

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package docs
Summary:        Documentation for Python interface to libcurl

%description docs
%{summary}.

%package tests
Summary:        Tests for Python interface to libcurl
Requires:       python3-pycurl = %{version}-%{release}

%description tests
%{summary}.

%prep
%setup -q -n %{name}-%{version}/pycurl
# remove windows-specific build script
rm -f winbuild.py
sed -e 's| winbuild.py||' -i Makefile

# remove binaries packaged by upstream
rm -f tests/fake-curl/libcurl/*.so

# remove a test-case that relies on sftp://web.sourceforge.net being available
rm -f tests/ssh_key_cb_test.py

# remove a test-case that fails in Koji
rm -f tests/seek_cb_test.py

# remove tests depending on the 'flaky' nose plug-in
grep '^import flaky' -r tests | cut -d: -f1 | xargs rm -fv

%{__python3} ./setup.py docstrings

%build
CFLAGS="%{optflags}" %{__python3} ./setup.py build --executable="%{__python3} -s" --with-openssl

%install
export PYCURL_SSL_LIBRARY=openssl
CFLAGS="%{optflags}" %{__python3} ./setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%files
%defattr(-,root,root,-)
%license COPYING-LGPL COPYING-MIT
%{python3_sitearch}/curl/
%{python3_sitearch}/pycurl.*.so
%{python3_sitearch}/pycurl-*.egg-info

%files docs
%defattr(-,root,root,-)
%doc ChangeLog README.rst examples doc
%{python3_sitearch}/curl/
%{python3_sitearch}/pycurl.*.so
%{python3_sitearch}/pycurl-*.egg-info

%files tests
%defattr(-,root,root,-)
%doc tests
