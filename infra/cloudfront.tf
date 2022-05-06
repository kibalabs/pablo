resource "aws_cloudfront_cache_policy" "default" {
  name = "${local.project}-default"
  default_ttl = 86400
  min_ttl = 0
  max_ttl = 31536000

  parameters_in_cache_key_and_forwarded_to_origin {
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip = true
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "whitelist"
      headers {
        items = [
          "Origin",
          "Access-Control-Request-Method",
          "Access-Control-Allow-Origin",
          "Access-Control-Request-Headers",
        ]
      }
    }
    query_strings_config {
      query_string_behavior = "all"
    }
  }
}

resource "aws_cloudfront_cache_policy" "api" {
  name = "${local.project}-api"
  default_ttl = 60
  min_ttl = 0
  max_ttl = 60

  parameters_in_cache_key_and_forwarded_to_origin {
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip = true
    cookies_config {
      cookie_behavior = "all"
    }
    headers_config {
      # NOTE(krishan711): there is no all here, should be updated as needed with a whitelist
      header_behavior = "whitelist"
      headers {
        items = [
          "Authorization",
        ]
      }
    }
    query_strings_config {
      query_string_behavior = "all"
    }
  }
}

resource "aws_cloudfront_distribution" "api" {
  enabled = true
  price_class = "PriceClass_200"
  is_ipv6_enabled = true
  aliases = [local.root_domain_name]

  origin {
    origin_id = aws_s3_bucket.storage.id
    domain_name = aws_s3_bucket.storage.bucket_regional_domain_name
  }

  origin {
    origin_id = "api"
    domain_name = "pablo-api.kibalabs.com"
    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols = ["TLSv1.2"]
    }
  }

  # any requests with /static/ get sent straight to s3
  ordered_cache_behavior {
    path_pattern = "/static/*"
    compress = true
    target_origin_id = aws_s3_bucket.storage.id
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods = ["GET", "HEAD"]
    cache_policy_id = aws_cloudfront_cache_policy.default.id
  }

  default_cache_behavior {
    target_origin_id = "api"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"]
    cached_methods = ["GET", "HEAD"]
    cache_policy_id = aws_cloudfront_cache_policy.api.id
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.certificate.arn
    ssl_support_method = "sni-only"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    app = local.project
  }
}

output "cdn_url" {
  value = "${aws_cloudfront_distribution.api.domain_name}"
}
