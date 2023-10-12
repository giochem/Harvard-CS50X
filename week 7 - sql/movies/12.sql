select title from movies
where id in
(select movie_id from stars
where person_id in
(select id from people
where name = "Bradley Cooper" or name = "Jennifer Lawrence")
group by movie_id having count(person_id) = 2)