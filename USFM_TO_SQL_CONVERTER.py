import sqlite3

def convert_usfm_to_sql(usfm_file, sqlite_db):
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    
    # Create the table based on the existing schema
    cursor.execute('''CREATE TABLE IF NOT EXISTS bible (
                        id INTEGER PRIMARY KEY,
                        book TEXT,
                        chapter INTEGER,
                        verse INTEGER,
                        text TEXT
                    )''')
    
    # Parse USFM file and insert into the database
    current_book = None
    current_chapter = 0
    current_verse = 0

    with open(usfm_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if line.startswith('\id'):  # Book identifier
                current_book = line.split(' ')[1]
            elif line.startswith('\c'):  # Chapter identifier
                current_chapter = int(line.split(' ')[1])
                current_verse = 0  # Reset verse for new chapter
            elif line.startswith('\v'):  # Verse identifier
                current_verse = int(line.split(' ')[1])
                text = line[3:].strip()  # Get the verse text
                # Insert into the database
                cursor.execute('''INSERT INTO bible (book, chapter, verse, text) VALUES (?, ?, ?, ?)''', 
                               (current_book, current_chapter, current_verse, text))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Example usage
# convert_usfm_to_sql('example.usfm', 'bible.db')
