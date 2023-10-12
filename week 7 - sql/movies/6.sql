select avg(rating) from movies inner join ratings
on movies.id = ratings.movie_id where movies.year = 2012;
