%define __spec_install_pre /bin/true

Name: boundless-server-geowebcache
Version: REPLACE_VERSION
Release: REPLACE_RELEASE
Summary: Tile caching server supporting a number of tiling standards.
Group: Applications/Engineering
License: LGPL
URL: http://geowebcache.org
BuildRoot: %{_WORKSPACE}/boundless-server-geowebcache/BUILDROOT
Requires(post): bash
Requires(preun): bash
Requires:  unzip, boundless-server-tomcat9 >= 9.0.14, boundless-server-tomcat9 < 9.1
Conflicts: geowebcache, suite-geowebcache
Obsoletes: suite-geowebcache
AutoReqProv: no

%define _rpmdir archive/el/6/
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0
# Don't waste time re-packing jars (http://makewhatis.com/2011/12/remove-unwanted-commpression-in-during-rpmbuild-for-jar-files)
%define __os_install_post %{nil}


%description
GeoWebCache is used to cache map tiles from variety of sources such as OGC Web
Map Service (WMS). It implements various service interfaces (such as WMS-C,
WMTS, TMS, Google Maps KML, Virtual Earth) in order to accelerate and optimize
map image delivery. It can also recombine tiles to work with regular WMS
clients.

%prep

%install
mkdir -p %{buildroot}/opt/boundless/server
unzip %{_WORKSPACE}/SRC/BoundlessServer-war/geowebcache.war -d %{buildroot}/opt/boundless/server/geowebcache

mkdir -p %{buildroot}/etc/tomcat9/Catalina/localhost/
cp %{_WORKSPACE}/suite/packaging/tomcat-context/geowebcache.xml %{buildroot}/etc/tomcat9/Catalina/localhost/
cp %{_WORKSPACE}/suite/packaging/tomcat-context/geowebcache.xml %{buildroot}/etc/tomcat9/Catalina/localhost/geowebcache.xml.new

mkdir -p %{buildroot}/usr/share/doc/
mv %{buildroot}/opt/boundless/server/geowebcache/doc %{buildroot}/usr/share/doc/boundless-server-geowebcache

%pre
if [ -f /etc/tomcat9/Catalina/localhost/geowebcache.xml ]; then
  cp -pf /etc/tomcat9/Catalina/localhost/geowebcache.xml /etc/tomcat9/Catalina/localhost/geowebcache.xml.orig
fi
# Cleanup old license files
if [ -f /usr/share/doc/boundless-server-geowebcache/EULA ]; then
  rm -f /usr/share/doc/boundless-server-geowebcache/EULA
fi
if [ -f /usr/share/doc/boundless-server-geowebcache/LICENSE ]; then
  rm -f /usr/share/doc/boundless-server-geowebcache/LICENSE
fi

%post
if [ ! -d /var/opt/boundless/server/geowebcache/config/ ]; then
  mkdir -p /var/opt/boundless/server/geowebcache/config/
fi
if [ ! -d /var/opt/boundless/server/geowebcache/tilecache/ ]; then
  mkdir -p /var/opt/boundless/server/geowebcache/tilecache/
fi
if [ -f /var/lib/dpkg/info/ca-certificates-java.postinst ]; then
  /var/lib/dpkg/info/ca-certificates-java.postinst configure
fi
chown -R root:root /opt/boundless/
chown -R tomcat9:tomcat9 /var/opt/boundless/
for i in `find /usr/share/doc/boundless-server-geowebcache/ -name *.gz`; do
  gunzip $i
done

%preun

%postun
if [ "$1" = "0" ] || [ "$1" = "remove" ]; then
  if [ -d /opt/boundless/server/geowebcache ]; then
    for dir in `find /opt/boundless/server/geowebcache -type d -exec bash -c '[ "x\`find "{}" -maxdepth 1 -type f\`" = x ] && echo "{}"' \; | sort -r`; do
      rm -rf $dir
    done
  fi
  if [ -f /etc/tomcat9/Catalina/localhost/geowebcache.xml ]; then
    rm -f /etc/tomcat9/Catalina/localhost/geowebcache.xml
  fi
  rm -f /var/lib/dpkg/info/boundless-server-geowebcache.* 2>&1 > /dev/null
fi

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/tomcat9/Catalina/localhost/geowebcache.xml
/usr/share/doc/boundless-server-geowebcache
/opt/boundless/server/geowebcache
/etc/tomcat9/Catalina/localhost/geowebcache.xml.new
