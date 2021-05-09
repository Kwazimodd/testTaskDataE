p_app = """INSERT INTO apps (name, genre, rating, version, size_bytes, is_awesome) 
            VALUES ("{}", "{}", "{}", "{}", "{}", "{}");"""

p_movie = """INSERT INTO movies 
             (original_title, original_language, budget, is_adult, release_date, original_title_normalized) 
             VALUES ("{}", "{}", "{}", "{}", "{}", "{}");"""

p_song = """INSERT INTO songs (artist_name, title, year, release_, ingestion_time)
             VALUES ("{}", "{}", "{}", "{}", "{}");"""