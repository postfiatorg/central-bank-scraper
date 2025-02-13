CREATE TABLE central_banks_g10 (
    id bigserial PRIMARY KEY, -- Unique identifier for each row
    country_name VARCHAR(100) NOT NULL,                      -- Country name
    country_code_alpha_3 CHAR(3) NOT NULL,  -- Country code in ISO 3166-1 alpha-3 format
    date_published TIMESTAMP WITHOUT TIME ZONE,              -- Date and time of file upload EST
    file_url TEXT,                     -- URL of the uploaded file
    full_extracted_text TEXT,          -- Full extracted text from the file
    scraping_machine VARCHAR(100) NOT NULL,             -- Name or identifier of the scraping machine
    scraping_ip VARCHAR(39) NOT NULL,           -- IP address of the scraping machine (supports IPv4 and IPv6)
    scraping_time TIMESTAMP WITHOUT TIME ZONE NOT NULL, -- Date and time of scraping EST
    UNIQUE (file_url)
);