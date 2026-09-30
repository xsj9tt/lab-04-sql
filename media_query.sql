SELECT
    users.username,
    posts.context,
    posts.created
FROM users
JOIN posts ON users.user_id = posts.user_id
WHERE users.user_id <= 5;
