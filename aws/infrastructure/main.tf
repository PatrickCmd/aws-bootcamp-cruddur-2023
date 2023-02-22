terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

resource "aws_security_group" "cruddur_security_group" {
  name_prefix = "cruddur_security_group"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "cruddur_ec2_instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = "cruddur_key_pair"
  vpc_security_group_ids = [aws_security_group.cruddur_security_group.id]

  user_data = "linux.sh"

  tags = {
    Name        = "cruddur_ec2_instancee"
    "Terraform" = "Yes"
  }

}