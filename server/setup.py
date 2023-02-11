import mysql.connector
from dotenv import load_dotenv, find_dotenv
from os import environ

load_dotenv (find_dotenv())
conn = mysql.connector.connect(
    host=environ.get('DB_HOST'),
    user=environ.get('DB_USER'),
    passwd = environ.get('DB_PASS'),
    #database=environ.get('DB_NAME'),
);

def create_db(connection):
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + environ.get('DB_NAME'))
    cursor.execute('USE ' + environ.get('DB_NAME'))
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
    ID varchar(32) PRIMARY KEY,
    name varchar(32) NOT NULL,
    email varchar(32) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    donation_preferences JSON
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ngo_data (
    USER_ID varchar(32) NOT NULL,
    NGO_ID varchar(32) PRIMARY KEY,
    name varchar(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mission varchar(255) NOT NULL,
    history varchar(255),
    impact varchar(255),
    plans varchar(255),
    banner_url varchar(64),
    funding_needs varchar(255) NOT NULL,
    location varchar(255) NOT NULL,
    type JSON NOT NULL
    );
    """)

def dummy_data(connection):
    cursor = connection.cursor()
    cursor.execute(r"""
    INSERT INTO user_data (ID, name, email, donation_preferences) 
    VALUES 
    ("user1", "John Doe", "johndoe@email.com", JSON_ARRAY('Environmental', 'Social Welfare')),
    ("user2", "Jane Smith", "janesmith@email.com", JSON_ARRAY('Disaster Relief', 'Education', 'Health')),
    ("user3", "Bob Brown", "bobbrown@email.com", JSON_ARRAY('Animal Welfare', 'Microfinance', 'Women\'s Empowerment')),
    ("user4", "Emma Wilson", "emmawilson@email.com", JSON_ARRAY('Children\'s Rights', 'Disability Rights', 'LGBTQ+ Rights')),
    ("user5", "Michael Johnson", "michaeljohnson@email.com", JSON_ARRAY('Poverty Alleviation', 'Agriculture and Rural Development', 'Water and Sanitation'));
    """);
    #connection.commit()
    cursor.execute(r"""
    INSERT INTO ngo_data (USER_ID, NGO_ID, name, mission, history, impact, plans, funding_needs, location, type) 
    VALUES 
    ("user1", "ngo1", "Greenpeace", "To ensure the ability of the Earth to nurture life in all its diversity.", "Founded in 1971, Greenpeace has been at the forefront of environmental activism.", "Greenpeace has influenced major environmental decisions and actions by governments and corporations.", "Greenpeace aims to continue its environmental activism and expand its reach.", "Greenpeace needs funding to continue its environmental activism and expand its reach.", "International", JSON_ARRAY("Environmental")),
    ("user2", "ngo2", "UNICEF", "To ensure that every child has a happy and healthy childhood.", "Founded in 1946, UNICEF has been providing aid to children in need.", "UNICEF has improved the lives of countless children through its programs.", "UNICEF plans to continue its work to improve the lives of children.", "UNICEF needs funding to continue its work to improve the lives of children.", "International", JSON_ARRAY("Children\'s Rights")),
    ("user3", "ngo3", "World Wildlife Fund", "To conserve nature and reduce the most pressing threats to the diversity of life on Earth.", "Founded in 1961, the World Wildlife Fund has been working to conserve nature and reduce threats to biodiversity.", "The World Wildlife Fund has made significant progress in conserving nature and reducing threats to biodiversity.", "The World Wildlife Fund plans to continue its work in conserving nature and reducing threats to biodiversity.", "The World Wildlife Fund needs funding to continue its work in conserving nature and reducing threats to biodiversity.", "International", JSON_ARRAY("Animal Welfare"));
    """)
    connection.commit()
if __name__ == "__main__":
    create_db(conn)
    dummy_data(conn)
    print("All done!")
    conn.close()