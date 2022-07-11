CREATE USER pablo_api;
GRANT USAGE ON SCHEMA public TO pablo_api;
GRANT INSERT, SELECT, UPDATE ON tbl_images TO pablo_api;
-- GRANT ALL ON SEQUENCE tbl_images_id_seq TO pablo_api;
GRANT INSERT, SELECT, UPDATE ON tbl_image_variants TO pablo_api;
-- GRANT ALL ON SEQUENCE tbl_image_variants_id_seq TO pablo_api;
GRANT INSERT, SELECT, UPDATE ON tbl_url_uploads TO pablo_api;
GRANT ALL ON SEQUENCE tbl_url_uploads_id_seq TO pablo_api;
