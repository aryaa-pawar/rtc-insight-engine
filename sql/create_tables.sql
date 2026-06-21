USE rtc_db;

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(255),
    page_number INT,
    text_content LONGTEXT
);

CREATE TABLE chunks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chunk_id INT,
    report_name VARCHAR(255),
    page_number INT,
    chunk_text LONGTEXT
);

CREATE TABLE metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(255),
    page_number INT,
    metric_value VARCHAR(100),
    metric_description TEXT
);