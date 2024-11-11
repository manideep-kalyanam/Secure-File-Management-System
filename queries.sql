show databases;
CREATE DATABASE FCS_Project;
use FCS_Project;

CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    public_key TEXT,
    private_key_encrypted TEXT
);

desc user;
select * from user;

CREATE TABLE File (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(255) NOT NULL,
    encrypted_aes_key TEXT NOT NULL,
    owner_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES User(id)
);
desc file;

CREATE TABLE SharedFile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT NOT NULL,
    recipient_id INT NOT NULL,
    owner_id INT NOT NULL,
    encrypted_aes_key TEXT NOT NULL,
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES File(id),
    FOREIGN KEY (recipient_id) REFERENCES User(id),
    FOREIGN KEY (owner_id) REFERENCES User(id)
);
desc SharedFile;

show tables;
