#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    # Install some custom requirements on OS X
    # e.g. brew install pyenv-virtualenv
    brew install pyenv-virtualenv;
    eval "$(pyenv init -)";
    pyenv install python3.5
    pyenv global python3.5
    pip install -r requirements.txt
    #case "${TOXENV}" in
    #    py32)
    #
    #        ;;
    #    py33)
    #        # Install some custom Python 3.3 requirements on OS X
    #        ;;
    #esac
else
   echo ""
    # Install some custom requirements on Linux
fi
