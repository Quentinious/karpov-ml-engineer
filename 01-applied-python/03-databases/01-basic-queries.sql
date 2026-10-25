-- Inspect a small sample of user records; row order is unspecified.
SELECT *
FROM "user"
LIMIT 10;

-- List distinct post topics.
SELECT DISTINCT topic
FROM post;

-- Inspect users older than 30 who use iOS.
SELECT *
FROM "user"
WHERE age > 30 AND os = 'iOS'
LIMIT 10;


SELECT *
FROM "user"
WHERE country != 'Russia' AND exp_group != 0 AND exp_group != 3 OR city = 'Minsk'
LIMIT 5;


SELECT country, AVG(age)
FROM "user"
GROUP BY country;


SELECT exp_group, os, COUNT(user) AS "total_users", MAX(age) AS "max_age", MIN(age) AS "min_age"
FROM "user"
GROUP BY exp_group, os;


SELECT topic
FROM post
GROUP BY topic
HAVING MAX(LENGTH(text)) > 25000;


SELECT country, COUNT(user)
FROM "user"
GROUP BY country
HAVING COUNT(user) > 1000
ORDER BY COUNT(user);


SELECT country, exp_group, COUNT(id)
FROM "user"
GROUP BY country, exp_group;


SELECT exp_group, COUNT(id)
FROM "user"
WHERE city = 'Moscow'
GROUP BY exp_group
HAVING AVG(age) > 27.2;


SELECT topic, COUNT(post)
FROM post
GROUP BY topic
ORDER BY COUNT(post) DESC;


SELECT *
FROM "user"
WHERE city = 'Voronezh'
ORDER BY age DESC;
