select title, rating from movies inner join ratings
on movies.id = ratings.movie_id where year = 2010 order by rating desc, title;