#!/bin/bash

echo "DB Connecting"

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

    CREATE TABLE IF NOT EXISTS wp_nissy_counts (
        cleaned_uri VARCHAR(255),
        total_count INT
    );

    INSERT INTO wp_nissy_counts (cleaned_uri, total_count)
    SELECT 
        CASE
            WHEN RIGHT(uri, 1) = '/' THEN LEFT(uri, CHAR_LENGTH(uri) - 1)
            ELSE uri
        END as cleaned_uri,
        SUM(count) AS total_count
    FROM wp_statistics_pages
    GROUP BY cleaned_uri
    ORDER BY total_count DESC;

EOF


echo "Insert Completed."