MySliceLib Python module
=======================

MySliceLib python module, for more information: `<https://myslice.info>`

This module is a Library that alows to send Queries to SFA Registry and AMs

Install
=======================

::

    git clone git@gitlab.noc.onelab.eu:onelab/myslicelib.git
    sudo apt-get install libssl-dev libcurl4-openssl-dev #installing OpenSSL Dev and libcurl
    sudo pip3.5 install --upgrade pip
    sudo pip3 install -r requirements.txt
    sudo python3.5 setup.py develop


Configure
=======================

You need a valid Private Key and Certificate matching a user account in SFA Registry

::

    /var/myslice/myslice.pkey
    /var/myslice/myslice.cert

