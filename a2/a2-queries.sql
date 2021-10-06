.echo on
--Question 1
SELECT u.uid
FROM users u, ubadges ub, badges b
WHERE u.uid = ub.uid
AND ub.bname = b.bname
AND b.type = 'gold'

INTERSECT

SELECT u.uid
FROM users u, posts p, questions q
WHERE u.uid = p.poster
AND p.pid = q.pid
;


--Question 2
SELECT p.pid, p.title
FROM questions q, posts p
WHERE q.pid = p.pid
AND lower(p.title) like '%relational database%'

UNION

SELECT p.pid, p.title
FROM questions q, tags t, posts p
WHERE p.pid = q.pid
AND q.pid = t.pid
AND lower(t.tag) like '%relational%'
AND lower(t.tag) like '%database%'
;


--Question 3
SELECT p.pid, p.title
FROM questions q, posts p
WHERE q.pid = p.pid

EXCEPT

SELECT p1.pid, p1.title
FROM posts p1, posts p2, questions q, answers a
WHERE q.pid = p1.pid
AND a.qid = q.pid
AND a.pid = p2.pid
AND date(p2.pdate) <= date(p1.pdate, '+3 days')
;


--Question 4
SELECT u.uid
FROM users u
WHERE 2 <
(SELECT COUNT(DISTINCT a.pid)
FROM questions q, answers a, posts p1, posts p2
WHERE q.pid = p1.pid
AND p1.poster = u.uid
AND a.qid = q.pid
AND a.pid = p2.pid
AND p1.poster = p2.poster)
;


--Question 5
SELECT u.uid
FROM users u, posts p1, posts p2, questions q, answers a
WHERE q.pid = p1.pid
AND p1.poster = u.uid
AND a.pid = p2.pid
AND p2.poster = u.uid

INTERSECT

SELECT u.uid
FROM users u
WHERE 4 <
(SELECT COUNT(v.vno)
FROM votes v, posts p
WHERE p.poster = u.uid
AND v.pid = p.pid)
;


--Question 6
SELECT new_tag, pnumber, vnumber
FROM (SELECT t.tag as new_tag, COUNT(DISTINCT p.pid) as pnumber, COUNT(v.vno) as vnumber
FROM tags t, posts p, votes v
WHERE t.pid = p.pid
AND p.pid = v.pid
GROUP BY t.tag)
ORDER BY vnumber DESC
LIMIT 3
;


--Question 7
SELECT new_date, new_tag, countnumber
FROM
(SELECT new_date, max(countnumber) as countnumber
 FROM(SELECT p.pdate as new_date, t.tag as new_tag, COUNT(*) as countnumber
      FROM posts p, tags t
      WHERE p.pid = t.pid
      GROUP BY p.pdate, t.tag)
 GROUP BY new_date)

left outer join

(SELECT p.pdate as new_date, t.tag as new_tag, COUNT(*) as countnumber
 FROM posts p, tags t
 WHERE p.pid = t.pid
 GROUP BY p.pdate, t.tag)
 using (new_date, countnumber)
;


--Question 8
SELECT user_id, questions_number, answers_number, cvote_number, rvote_number
FROM

(SELECT user_id, questions_number, answers_number, cvote_number, rvote_number
FROM
(SELECT user_id, questions_number, answers_number
FROM
(SELECT user_id, questions_number, answers_number
FROM
(SELECT u.uid as user_id, COUNT(DISTINCT q.pid) as questions_number
FROM users u, questions q, posts p1
WHERE q.pid = p1.pid
AND p1.poster = u.uid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(DISTINCT a.pid) as answers_number
FROM users u, answers a, posts p2
WHERE a.pid = p2.pid
AND p2.poster = u.uid
GROUP BY u.uid)
using(user_id)
UNION
SELECT user_id, questions_number, answers_number
FROM
(SELECT u.uid as user_id, COUNT(DISTINCT a.pid) as answers_number
FROM users u, answers a, posts p2
WHERE a.pid = p2.pid
AND p2.poster = u.uid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(DISTINCT q.pid) as questions_number
FROM users u, questions q, posts p1
WHERE q.pid = p1.pid
AND p1.poster = u.uid
GROUP BY u.uid)
using(user_id)))

left outer join

(SELECT user_id, cvote_number, rvote_number
FROM
(SELECT user_id, cvote_number, rvote_number
FROM
(SELECT u.uid as user_id, COUNT(*) as cvote_number
FROM users u, votes v1
WHERE u.uid = v1.uid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(*) as rvote_number
FROM users u, posts p, votes v2
WHERE u.uid = p.poster
AND v2.pid = p.pid
GROUP BY u.uid)
using(user_id)
UNION
SELECT user_id, cvote_number, rvote_number
FROM
(SELECT u.uid as user_id, COUNT(*) as rvote_number
FROM users u, posts p, votes v2
WHERE u.uid = p.poster
AND v2.pid = p.pid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(*) as cvote_number
FROM users u, votes v1
WHERE u.uid = v1.uid
GROUP BY u.uid)
using(user_id))) using(user_id)


UNION


SELECT user_id, questions_number, answers_number, cvote_number, rvote_number
FROM

(SELECT user_id, cvote_number, rvote_number
FROM
(SELECT user_id, cvote_number, rvote_number
FROM
(SELECT u.uid as user_id, COUNT(*) as cvote_number
FROM users u, votes v1
WHERE u.uid = v1.uid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(*) as rvote_number
FROM users u, posts p, votes v2
WHERE u.uid = p.poster
AND v2.pid = p.pid
GROUP BY u.uid)
using(user_id)
UNION
SELECT user_id, cvote_number, rvote_number
FROM
(SELECT u.uid as user_id, COUNT(*) as rvote_number
FROM users u, posts p, votes v2
WHERE u.uid = p.poster
AND v2.pid = p.pid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(*) as cvote_number
FROM users u, votes v1
WHERE u.uid = v1.uid
GROUP BY u.uid)
using(user_id)))

left outer join

(SELECT user_id, questions_number, answers_number
FROM
(SELECT user_id, questions_number, answers_number
FROM
(SELECT u.uid as user_id, COUNT(DISTINCT q.pid) as questions_number
FROM users u, questions q, posts p1
WHERE q.pid = p1.pid
AND p1.poster = u.uid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(DISTINCT a.pid) as answers_number
FROM users u, answers a, posts p2
WHERE a.pid = p2.pid
AND p2.poster = u.uid
GROUP BY u.uid)
using(user_id)
UNION
SELECT user_id, questions_number, answers_number
FROM
(SELECT u.uid as user_id, COUNT(DISTINCT a.pid) as answers_number
FROM users u, answers a, posts p2
WHERE a.pid = p2.pid
AND p2.poster = u.uid
GROUP BY u.uid)
left outer join
(SELECT u.uid as user_id, COUNT(DISTINCT q.pid) as questions_number
FROM users u, questions q, posts p1
WHERE q.pid = p1.pid
AND p1.poster = u.uid
GROUP BY u.uid)
using(user_id)))using(user_id))
;


--Question 9
--DROP VIEW questionInfo;
CREATE VIEW questionInfo
AS SELECT pid, uid, theaid, voteCnt, ansCnt
FROM
(SELECT q.pid as pid, u.uid as uid, q.theaid as theaid, COUNT(DISTINCT v.vno) as voteCnt, COUNT(DISTINCT a.pid) as ansCnt
FROM questions q left outer join posts p on q.pid = p.pid
               left outer join users u on p.poster = u.uid
               left outer join answers a on q.pid = a.qid
               left outer join votes v on v.pid = q.pid
WHERE date(p.pdate) >= date('now', '-1 month')
GROUP BY q.pid)
;


SELECT pid, uid, theaid, voteCnt, ansCnt
FROM questionInfo
;


--Question 10
SELECT users_city, COUNT(*) as n_o_u, SUM(per_user_gold_badges) as total_users_gold_badges, AVG(per_user_questions) as total_user_questions, SUM(per_user_votes) as total_user_votes
FROM
(SELECT u.city as users_city, u.uid as users_uid, COUNT(ub.bname) as per_user_gold_badges, COUNT(DISTINCT q.pid) as per_user_questions, COUNT(v.vno) as per_user_votes
 FROM users u left join questionInfo q on q.uid = u.uid
 left join (posts p left join votes v on v.pid = p.pid and date(v.vdate) >= date('now', '-1 month')) on p.poster = u.uid
 left join (ubadges ub left join badges b on ub.bname = b.bname and b.type = 'gold') on u.uid = ub.uid
GROUP BY u.uid)
GROUP BY users_city
;
