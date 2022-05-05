resource "aws_iam_group" "users" {
  name = "${local.project}-users"
}

resource "aws_iam_user" "user_api" {
  name = "${local.project}-user-api"
  tags = {
    app = local.project
  }
}

resource "aws_iam_access_key" "user_api" {
  user = aws_iam_user.user_api.name
}

resource "aws_iam_user_group_membership" "user_api" {
  user = aws_iam_user.user_api.name

  groups = [
    aws_iam_group.users.name,
  ]
}

output "user_api_name" {
  value = aws_iam_user.user_api.name
  sensitive = true
}

output "user_api_iam_key" {
  value = aws_iam_access_key.user_api.id
  sensitive = true
}

output "user_api_iam_secret" {
  value = aws_iam_access_key.user_api.secret
  sensitive = true
}

resource "aws_iam_group_policy_attachment" "users_read_from_work_queue" {
  group = aws_iam_group.users.name
  policy_arn = aws_iam_policy.read_from_work_queue.arn
}

resource "aws_iam_group_policy_attachment" "users_read_from_work_queue_dl" {
  group = aws_iam_group.users.name
  policy_arn = aws_iam_policy.read_from_work_queue_dl.arn
}

resource "aws_iam_group_policy_attachment" "users_write_to_work_queue" {
  group = aws_iam_group.users.name
  policy_arn = aws_iam_policy.write_to_work_queue.arn
}

resource "aws_iam_group_policy_attachment" "users_write_to_storage" {
  group = aws_iam_group.users.name
  policy_arn = aws_iam_policy.write_to_storage.arn
}
