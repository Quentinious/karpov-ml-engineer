
SELECT f.post_id, f.time, u.age, u.os
FROM feed_action AS f
JOIN "user" AS u
    ON f.user_id = u.id
WHERE u.city = 'Omsk'
    AND f.action = 'like'
ORDER BY f.time DESC
LIMIT 100;


SELECT u.city, COUNT(*) AS views_count
FROM "user" AS u
JOIN feed_action AS f ON u.id = f.user_id
JOIN post AS p ON f.post_id = p.id
WHERE u.age = 36 AND DATE(f.time) = '2021-12-01' AND p.topic = 'covid' AND f.action = 'view'
GROUP BY u.city
ORDER BY views_count ASC
LIMIT 1;


SELECT f.post_id, MAX(p.text), COUNT(f.post_id), MAX(f.time)
FROM feed_action f
JOIN post p ON f.post_id = p.id
WHERE f.action = 'like'
GROUP BY f.post_id
ORDER BY COUNT(f.post_id) DESC;
