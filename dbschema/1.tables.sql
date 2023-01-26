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
    id BIGSERIAL PRIMARY KEY,
    created_date TIMESTAMP NOT NULL,
    updated_date TIMESTAMP NOT NULL,
    image_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    is_preview BOOLEAN NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    area INTEGER NOT NULL
);
CREATE UNIQUE INDEX tbl_image_variants_image_id_is_preview_width_height ON tbl_image_variants (image_id, is_preview, width, height);
CREATE INDEX tbl_image_variants_updated_date ON tbl_image_variants (updated_date);
CREATE INDEX tbl_image_variants_image_id_is_preview_area_width_height ON tbl_image_variants (image_id, is_preview, area, width, height);
CREATE INDEX tbl_image_variants_image_id_is_preview_area ON tbl_image_variants (image_id, is_preview, area);
CREATE INDEX tbl_image_variants_image_id ON tbl_image_variants (image_id);
CREATE INDEX tbl_image_variants_area ON tbl_image_variants (area);
CREATE INDEX tbl_image_variants_is_preview ON tbl_image_variants (is_preview);

CREATE TABLE tbl_url_uploads (
    id BIGSERIAL PRIMARY KEY,
    created_date TIMESTAMP NOT NULL,
    updated_date TIMESTAMP NOT NULL,
    url TEXT NOT NULL,
    image_id TEXT NOT NULL
);
CREATE UNIQUE INDEX tbl_url_uploads_url ON tbl_url_uploads (url);
CREATE INDEX tbl_url_uploads_updated_date ON tbl_url_uploads (updated_date);
CREATE INDEX tbl_url_uploads_image_id ON tbl_url_uploads (image_id);
