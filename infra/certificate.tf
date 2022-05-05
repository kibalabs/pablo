resource "aws_acm_certificate" "certificate" {
  provider = aws.acm
  domain_name = local.root_domain_name
  validation_method = "DNS"
  subject_alternative_names = []

  tags = {
    app = local.project
  }
}
