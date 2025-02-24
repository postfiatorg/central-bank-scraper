-- delete tables if they exist
DROP TABLE IF EXISTS central_banks_g10_links;
DROP TABLE IF EXISTS central_banks_g10_categories;
DROP TABLE IF EXISTS central_banks_g10;
CREATE TABLE central_banks_g10 (
    id bigserial PRIMARY KEY, -- Unique identifier for each row
    country_name VARCHAR(100) NOT NULL,                      -- Country name
    country_code_alpha_3 CHAR(3) NOT NULL,  -- Country code in ISO 3166-1 alpha-3 format
    date_published TIMESTAMP WITHOUT TIME ZONE,              -- Date and time of file upload EST
    file_url TEXT NOT NULL,                     -- URL 
    full_extracted_text TEXT,          -- Full extracted text from the file
    scraping_machine VARCHAR(100) NOT NULL,             -- Name or identifier of the scraping machine
    scraping_ip VARCHAR(39) NOT NULL,           -- IP address of the scraping machine (supports IPv4 and IPv6)
    scraping_time TIMESTAMP WITHOUT TIME ZONE NOT NULL, -- Date and time of scraping EST
    UNIQUE (file_url)
);

CREATE TABLE central_banks_g10_categories (
    id bigserial PRIMARY KEY, -- Unique identifier for each row
    file_url TEXT NOT NULL REFERENCES central_banks_g10 (file_url),  -- URL 
    category_name VARCHAR(100) NOT NULL, -- Category name
    UNIQUE (file_url, category_name)
);

CREATE TABLE central_banks_g10_links (
    id bigserial PRIMARY KEY, -- Unique identifier for each row
    file_url TEXT NOT NULL REFERENCES central_banks_g10 (file_url),  -- URL 
    link_url TEXT NOT NULL,                     -- URL of the link
    link_name TEXT NOT NULL,                    -- Name of the link
    full_extracted_text TEXT,
    UNIQUE (file_url, link_url)
);