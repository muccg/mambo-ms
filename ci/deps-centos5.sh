set -e

echo "Setting up epel repository..."
wget http://download.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
sudo rpm -Uvh epel-release-5-4.noarch.rpm || true

echo "Installing deps"
sudo yum install -y python26-devel
#postgresql84-devel is needed by mamboms-1.2.1-1.x86_64
#openldap-devel is needed by mamboms-1.2.1-1.x86_64
#openssl-devel is needed by mamboms-1.2.1-1.x86_64
#atlas-devel is needed by mamboms-1.2.1-1.x86_64
#blas-devel is needed by mamboms-1.2.1-1.x86_64
sudo yum erase -y postgresql-devel
sudo yum erase -y postgresql
sudo yum install -y postgresql84-devel
sudo yum install -y openldap-devel
sudo yum install -y openssl-devel
sudo yum install -y atlas-devel
sudo yum install -y blas-devel
sudo yum install -y freetype-devel
sudo yum install -y libpng-devel
sudo yum install -y python-devel
