-- MySQL schema for cultural relics knowledge graph (Section 6.3.1)
-- Relational layer: detailed artifact data, users, and business records

CREATE DATABASE IF NOT EXISTS cultural_relics_kg
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cultural_relics_kg;

CREATE TABLE IF NOT EXISTS artifacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    artifact_id VARCHAR(128) NOT NULL UNIQUE,
    external_id VARCHAR(64) NOT NULL,
    name VARCHAR(512) NOT NULL,
    image_url TEXT NOT NULL,
    local_image_path TEXT,
    age VARCHAR(256),
    dynasty VARCHAR(128),
    artifact_type VARCHAR(256),
    material VARCHAR(512),
    introduction TEXT,
    detail_url TEXT NOT NULL,
    museum_name VARCHAR(256) NOT NULL,
    museum_location VARCHAR(256),
    artist VARCHAR(256),
    culture VARCHAR(256),
    country_of_origin VARCHAR(128),
    department VARCHAR(256),
    crawled_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_dynasty (dynasty),
    INDEX idx_material (material),
    INDEX idx_museum (museum_name),
    INDEX idx_name (name(128))
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    role VARCHAR(32) DEFAULT 'viewer',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS crawl_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    museum_target VARCHAR(64) NOT NULL,
    status VARCHAR(32) DEFAULT 'pending',
    artifacts_count INT DEFAULT 0,
    triples_count INT DEFAULT 0,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME
) ENGINE=InnoDB;
