import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS meetings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  friend_name TEXT,
                  meeting_time TEXT,
                  location TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def add_meeting(user_id, friend_name, meeting_time, location):
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO meetings (user_id, friend_name, meeting_time, location)
                 VALUES (?, ?, ?, ?)''', 
              (user_id, friend_name, meeting_time, location))
    
    conn.commit()
    meeting_id = c.lastrowid
    conn.close()
    return meeting_id

def get_user_meetings(user_id):
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    
    c.execute('''SELECT friend_name, meeting_time, location FROM meetings 
                 WHERE user_id = ? ORDER BY meeting_time''', (user_id,))
    
    meetings = c.fetchall()
    conn.close()
    return meetings
