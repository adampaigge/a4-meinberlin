#!/bin/sh

set -e -v

if [ -n ${TRAVIS_SSH_SECRET} ]; then
    SSH_ID_ARG="-i ${HOME}/id_rsa"
    cat <<EOF | openssl enc -d -pass env:TRAVIS_SSH_SECRET -aes256 -a -out ~/id_rsa
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
g3zN0QpRYmI7X7N/puZtUQ==
EOF
    chmod 600 ~/id_rsa
fi

ssh -p 22036 ${SSH_ID_ARG} -oStrictHostKeyChecking=no build@benhabib.liqd.net deploy meinberlin master
