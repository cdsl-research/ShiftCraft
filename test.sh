#!/bin/bash

kubectl exec -i deploy/nissy-sql -- /bin/bash <<EOF
LC_ALL=en_US.UTF-8 mysql -u cdsl -pcdsl2023 -e "use wordpress;SELECT id, cleaned_uri, total_count, post_title, post_type FROM wp_nissy_kekka_new ORDER BY total_count DESC;"
EOF

echo "END"