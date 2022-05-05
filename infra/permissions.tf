resource "aws_iam_policy" "read_from_work_queue" {
  name = "${local.project}-read-queue-${aws_sqs_queue.work_queue.name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Effect = "Allow"
        Action = [
            "sqs:GetQueueUrl",
            "sqs:GetQueueAttributes",
            "sqs:ReceiveMessage",
            "sqs:ChangeMessageVisibility",
            "sqs:ChangeMessageVisibilityBatch",
            "sqs:DeleteMessage",
            "sqs:DeleteMessageBatch",
        ]
        Resource = aws_sqs_queue.work_queue.arn
    }]
  })
}

resource "aws_iam_policy" "read_from_work_queue_dl" {
  name = "${local.project}-read-queue-${aws_sqs_queue.work_queue_dl.name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Effect = "Allow"
        Action = [
            "sqs:GetQueueUrl",
            "sqs:GetQueueAttributes",
            "sqs:ReceiveMessage",
            "sqs:ChangeMessageVisibility",
            "sqs:ChangeMessageVisibilityBatch",
            "sqs:DeleteMessage",
            "sqs:DeleteMessageBatch",
        ]
        Resource = aws_sqs_queue.work_queue_dl.arn
    }]
  })
}

resource "aws_iam_policy" "write_to_work_queue" {
  name = "${local.project}-write-queue-${aws_sqs_queue.work_queue.name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
        Effect = "Allow"
        Action = [
            "sqs:GetQueueUrl",
            "sqs:GetQueueAttributes",
            "sqs:SendMessage",
            "sqs:SendMessageBatch",
        ]
        Resource = aws_sqs_queue.work_queue.arn
    }]
  })
}

resource "aws_iam_policy" "write_to_storage" {
  name = "${local.project}-write-storage-${aws_s3_bucket.storage.bucket}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:DeleteObject",
        "s3:DeleteObjectTagging",
        "s3:DeleteObjectVersion",
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:PutObjectRetention",
        "s3:PutObjectTagging",
        "s3:PutObjectLegalHold"
      ],
      Resource = [
        aws_s3_bucket.storage.arn,
        "${aws_s3_bucket.storage.arn}/*",
      ]
    }]
  })
}
