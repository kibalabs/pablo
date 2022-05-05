CREATE TABLE tbl_images (
    id TEXT PRIMARY KEY,
    created_date TIMESTAMP NOT NULL,
    updated_date TIMESTAMP NOT NULL,
    format TEXT NOT NULL,
    filename TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    area INTEGER NOT NULL
);
CREATE INDEX tbl_images_updated_date ON tbl_images (updated_date);

CREATE TABLE tbl_image_variants (
    id TEXT PRIMARY KEY,
    created_date TIMESTAMP NOT NULL,
    updated_date TIMESTAMP NOT NULL,
    image_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    area INTEGER NOT NULL
);
CREATE INDEX tbl_images_updated_date ON tbl_images (updated_date);
CREATE INDEX tbl_image_variants_image_id_area ON tbl_image_variants (image_id, area);
CREATE INDEX tbl_image_variants_image_id ON tbl_image_variants (image_id);
CREATE INDEX tbl_image_variants_area ON tbl_image_variants (area);

CREATE TABLE tbl_url_uploads (
    id TEXT PRIMARY KEY,
    created_date TIMESTAMP NOT NULL,
    updated_date TIMESTAMP NOT NULL,
    url TEXT NOT NULL,
    image_id TEXT NOT NULL
);
CREATE UNIQUE INDEX tbl_images_url ON tbl_images (url);
CREATE INDEX tbl_images_updated_date ON tbl_images (updated_date);
CREATE INDEX tbl_images_image_id ON tbl_images (image_id);
