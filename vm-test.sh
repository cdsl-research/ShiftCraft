#!/bin/bash

mariadb -h c0a21099-local1 -P 3306 -u cdsl -pcdsl2023 << EOF
    use wordpress;
    CREATE TABLE IF NOT EXISTS wp_nissy_posts (
    post_title VARCHAR(255),
    post_name VARCHAR(255),
    guid VARCHAR(255),
    post_status VARCHAR(255)
    );

    INSERT INTO wp_nissy_posts (post_title, post_name, guid, post_status)
    SELECT post_title, post_name, guid, post_status
    FROM wp_posts
    WHERE post_status = 'publish';

# exit;
EOF



echo "END"