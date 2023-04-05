# Week 7 — Solving CORS with a Load Balancer and Custom Domain

## Custom Domains and Hosted Zones with Route 53

### Link domain to Amazon Web Services

In order to link my domain I registered with [namecheap](namecheap.com) I needed to created a hosted zone using AWS Route 53 service and then link the nameservers with my registered domain in namecheap as the `Custom DNS`

I read articles [here](https://techgenix.com/namecheap-aws-ec2-linux/) and [here](https://www.namecheap.com/support/knowledgebase/article.aspx/10371/2208/how-do-i-link-my-domain-to-amazon-web-services/?psafe_param=1&gclid=Cj0KCQjwuLShBhC_ARIsAFod4fIRfkCKnkNl1Cv5R9N4XX72JYeKck-YHvhgUi3XNPQ5ZYDHB5zeKc8aAk8iEALw_wcB) to properly to complete this setup.

![created hosted zone](./assets/week-7/created_hosted_zone1.png)

![created hosted zone](./assets/week-7/created_hosted_zone2.png)

![created hosted zone](./assets/week-7/created_hosted_zone3_record_set.png)

![created hosted zone](./assets/week-7/nameservers.png)

## Create SSL Certificate and Create records in route 53

Use the cerificate manager to generate the SSL certificate and the create records in route 53.

![request ssl certificate](./assets/week-7/request_certificate1.png)

![request ssl certificate](./assets/week-7/request_certificate2.png)

![request ssl certificate](./assets/week-7/request_certificate3.png)

![request ssl certificate](./assets/week-7/request_certificate4.png)

![request ssl certificate](./assets/week-7/request_certificate5_create_records.png)

![request ssl certificate](./assets/week-7/request_certificate6_create_records.png)

![request ssl certificate](./assets/week-7/request_certificate7.png)

