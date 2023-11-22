#!/bin/bash

kubectl exec -it deploy/nissy-sql -- /bin/bash <<EOF
mysql -u cdsl -pcdsl2023 -e "use wordpress; SELECT post_date, cleaned_uri, total_count FROM wp_nissy_kekka_new;"
EOF

echo "END"