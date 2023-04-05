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

### Create hosted zone records

Create records that point to the load balancer listening to both `backend` and `frontend`

![create records](./assets/week-7/create_record_point_to_lb.png)

![create records](./assets/week-7/create_record_point_to_lb2.png)

![create records](./assets/week-7/create_record_point_to_lb3.png)

## Update load balancer listeners

Add a listener to redirect `HTTP` request on port `80` to `HTTPS` on port `443`

![Update load balancer listeners](./assets/week-7/update_lb_listeners1.png)

![Update load balancer listeners](./assets/week-7/update_lb_listeners2.png)

![Update load balancer listeners](./assets/week-7/update_lb_listeners3.png)

![Update load balancer listeners](./assets/week-7/update_lb_listeners4.png)

### Modify listener rules

![Update load balancer listeners](./assets/week-7/update_lb_listeners5_modify_rules.png)

![Update load balancer listeners](./assets/week-7/update_lb_listeners6_modify_rules.png)

