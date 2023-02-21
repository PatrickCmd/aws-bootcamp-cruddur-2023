terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

resource "aws_key_pair" "cruddur_key_pair" {
  key_name   = "cruddur_key_pair"
  public_key = file("~/.ssh/cruddur_key_pair.pub")
}

resource "aws_security_group" "cruddur_security_group" {
  name_prefix = "cruddur_security_group"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.2.0.0/16"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.2.0.0/16"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.2.0.0/16"]
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
  key_name               = aws_key_pair.cruddur_key_pair.key_name
  vpc_security_group_ids = [aws_security_group.cruddur_security_group.id]

  network_interface {
    network_interface_id = var.network_interface_id
    device_index         = 0
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo yum install -y docker",
      "sudo usermod -aG docker ec2-user",
      "sudo systemctl enable docker",
      "sudo systemctl start docker",
      "sudo curl -L \"https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose"
    ]
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("~/.ssh/cruddur_key_pair.pem")
    host        = self.public_ip
  }

}