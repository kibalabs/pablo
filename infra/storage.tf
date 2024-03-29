resource "aws_s3_bucket" "storage" {
  bucket = "kiba-${local.project}"
  lifecycle {
    prevent_destroy = true
  }

  tags = {
    app = local.project
  }
}

resource "aws_s3_bucket_acl" "example_bucket_acl" {
  bucket = aws_s3_bucket.storage.id
  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "example" {
  bucket = aws_s3_bucket.storage.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = [
      "http://localhost:3000",
      "http://localhost:3001",
      "http://localhost:3002",
      "https://pfpkit.xyz",
      "https://tokenhunt.io",
      "https://stormdrop.spriteclubnft.com",
      "https://milliondollartokenpage.com",
      "https://*.milliondollartokenpage.com",
      "https://rudeboys.io",
      "https://*.rudeboys.io",
      "https://*.tokenpage.xyz",
    ]
    expose_headers = ["ETag", "Access-Control-Allow-Origin", "Location"]
    max_age_seconds = 86400
  }
}

resource "aws_s3_bucket_public_access_block" "storage" {
  bucket = aws_s3_bucket.storage.id
  block_public_acls = false
  block_public_policy = false
  ignore_public_acls = false
  restrict_public_buckets = false
}
