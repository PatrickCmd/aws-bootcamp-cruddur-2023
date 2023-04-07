## Transcript
```
0:00
Hello and welcome to another episode of FooBar.
0:04
In today's video, I want to show you how to design a single table
0:10
for this Dynamo single table design based on a real example.
0:16
We are going to model this table based on an existing application,
0:21
but you could do this similar exercise based on some designs that
0:25
you have from your application.
0:26
You don't need to be migrating something.
0:28
It can be a totally new application.
0:31
This exercise will take us to define all the entities in the application.
0:35
Then to create a list of all the access patterns, and finally to model the
0:40
table and it indexes all in paper.
0:44
So let's start.
0:46
So we are going to migrate an existing application using Mongo into Dynamo.
0:52
But for this exercise, this is irrelevant.
0:55
We are not even thinking about where these database is, and we are going to apply
1:00
the single table design while doing that.
1:02
If you don't know what the single table design, basically I have a whole video
1:06
talking about it, but in a nutshell, it means that we will try to minimize
1:11
the amount of queries into Dynamo.
1:14
Dynamo doesn't have joints, so if you have multiple tables, then you need to
1:18
do those joins in your application level and that adds complexity and decrease
1:24
the performance of your application.
1:26
Doing one call to the Dynamo and be able to fetch all the relevant information
1:32
you need is very efficient and it can take advantage of the single digit
1:37
millisecond performance at Dynamo offers.
1:41
The application we are going to migrate is this e-commerce site.
1:45
I have been working with this e-commerce site for a while.
1:48
But that's not important.
1:49
This site has products, it has filters.
1:54
It has filters based on categories on prices.
1:57
It has this kind of search.
1:59
It have users and there are register to the system, you can see the products and
2:04
the products can be purchased by the user.
2:07
So all these features that a normal e-commerce has.
2:11
Then when the user purchase the products, you can see the
2:14
history of these purchases.
2:16
You can see how many items how many times each item was sold.
2:21
Customers can upload their own products because it's an easier
2:25
way to to keep the system active.
2:28
So that's also in in place there.
2:30
So there are all these different features that we need to take
2:35
from whatever is working there into Dynamo and model it there.
2:40
So the first step in our migration is to define all the entities that are in our
2:46
application, and we need to list them.
2:49
So the first entity that is quite obvious is the product.
2:52
It represents a product in our application, and it has multiple
2:56
attributes a name, an id, a description, a price, a category,
3:01
some images, the amount sold.
3:03
That's something we need to have in mind.
3:05
You will see it and who create the the product.
3:08
Another item we have is the users.
3:10
The users are for this particular case, when we implement this, you will see it.
3:14
We are using cognito but still, we need the user somehow reflected in our
3:18
application so we can know the user history and we can know how many which
3:25
products they bought and things of that, and which products they created.
3:28
So here we have the user that the ID is the email and
3:32
we have a name and last name.
3:33
Then another entity that is there is orders.
3:37
And basically this is the list.
3:40
Items that a customer purchase, so it has an id, it has a user, it has a purchase
3:46
date, it has a status if it's completed or it's active, and this is a secret.
3:51
I did some massaging there and our active order is our shopping cart.
3:58
So every user have one.
3:59
We have a total amount, a total items, and then an item list.
4:04
And the item list is this order items.
4:07
That basically is the list of items.
4:10
Is the specific items that they user wants to purchase or purchase
4:15
has the order ID, where it relates to a product id, the user id.
4:19
The quantity.
4:20
How many of these items are a title and image and then some total amount.
4:26
So these are the different entities and you'll need to, you'll go and
4:31
massage them a little bit the more you do the single table design.
4:34
For example, a good example here is the image and title in the order items.
4:40
So what I started this process, I didn't have the title and image in this entity.
4:45
And then when I realize that if I have it here, then I don't need
4:50
query my table and ask for that information from products all the time.
4:55
If I put it here, it's way easier.
4:56
So I add it.
4:57
So sometimes these entities will go into a little massage and iterations while
5:02
you are developing, and that's fine.
5:04
You don't need to get a hundred percent all the attributes for the
5:08
entities, but it's very important that you get as much as possible and you
5:11
do a lot of the thinking in paper.
5:14
This will remove cycles of you going back and forth and go back and forth.
5:18
And some things are very easy to add.
5:20
Some things are quite painful to add.
5:23
So after having all these entities now listed, we have four entities.
5:27
This is a simple example.
5:29
The next thing we need to do is to draw an entity relational diagram,
5:34
and you'll be like, Marcia, this is not a relational database.
5:38
Why are we doing this?
5:41
And I will tell you again, we have naming issues.
5:45
There are servers in serverless, and there are relations in non relational databases.
5:50
There is data, and data has relation by itself.
5:54
That's definition of databases.
5:56
So it's we are not to store those relations somehow and not
6:00
to understand those relations.
6:03
So Dynamo is a key value database or a wide column database, but I will
6:08
not call it non-relational database.
6:11
There are quite a lot of relations.
6:13
So let's look how this diagram looks.
6:15
I draw it with draw.io.
6:18
You can use any tool you want, but basically here I have my four entities
6:23
and how they relate to each other.
6:24
So this helps me to write a little bit my access patterns
6:28
and model the table later on.
6:30
So we have the users, we have the orders the users as orders.
6:34
The orders have order items and the order item has products.
6:37
The users publishes products.
6:39
And you can see here the relations, how many they have.
6:43
Good.
6:43
So now we have done our work with entities.
6:45
We have the relationship between them.
6:48
Now we can start working on the access patterns.
6:50
This is a little different maybe from the traditional aspect, because now when we
6:55
are working, for example, in a traditional example, you will be finding the entities.
6:59
You will do the entity modeling, and then you'll start normalizing the data.
7:04
Now what we want to do is to find the access pattern.
7:07
So please don't normalize the data.
7:09
And in this step is where you need to do a lot of work.
7:12
You really need to think.
7:13
Dynamo is not flexible.
7:15
So the more access patterns you can find and you can get your head around, the less
7:20
you will find in your development stage.
7:22
And you might need to come and redo this later on.
7:26
So this is a good exercise and it'll take you a while to try to figure
7:31
out all the access patterns and get it right, so don't get frustrated.
7:34
For me, it took me a couple of iterations to, to get it right
7:37
and I don't think it's right.
7:39
So then no, it's better what is started.
7:42
I'm pretty sure people in the comment will be asking me why you're
7:45
doing that, and why you're doing.
7:47
There is always better ways, but it's important to try to minimize
7:51
the amount of times you will go to the database to do operations.
7:55
That's the idea of finding these access patterns to go one time to the
7:59
database and get everything you need in order to resolve that access pattern.
8:03
So how you build this access patterns?
8:05
If you have specs, you go through the specs.
8:08
If you have UI like I do, you go through the UI.
8:12
If you have a service integration, you might go through the APIs.
8:15
So depending on your situation is how you start finding those access patterns.
8:20
So let's find the first access patterns.
8:23
And for that I'm using a spreadsheet and my spreadsheet has these columns.
8:27
Access pattern, operation, target parameters and nodes, and basically
8:33
in each of the columns I will write different things and that will
8:36
help me later when I'm coding.
8:38
So in the first column, I will write the name for the access pattern.
8:42
Then I will write operation, if it's a read or a write, you will
8:44
see write happens in the main table, and that's the target.
8:47
If it's an index, or the main table.
8:50
Then we have the parameters.
8:51
I usually write the primary key and the sort key there.
8:54
And then if I have any notes, I put them in the notes.
8:57
So the first patterns, let's start with the most simple ones so we
9:03
know what we are getting into.
9:05
So let's create a product.
9:06
That's the first pattern.
9:08
It'll happen in the main table because it's a right.
9:10
Operation.
9:11
Rights happen in the main table.
9:13
Indexes you cannot write in an index.
9:15
So yeah, so the parameter is the primary key is the product id.
9:20
And then I will check for uniqueness in that product id.
9:25
So it's a very simple pattern that everybody can do, and that's how you
9:32
will build your product table if you will not have the single table design.
9:36
The next access pattern is a CRUD read operation update, delete on a product.
9:40
And this is a read write operation that also happens in the main table.
9:44
And we are going to do it again with the product id.
9:47
And here it'll be mixed with the create because create CRUD.
9:51
But yeah, so this is the two access patterns that I have.
9:54
Now, let start modeling a little bit different patterns for the product.
10:00
So we are going to do some filtering.
10:02
So we are going to do some interesting search in the product.
10:06
We have saw in the UI that we have filters by categories by price and by search.
10:14
So we can filter by categories.
10:16
And this is a read operation and we are going to do this in an index.
10:21
And then, because we already are using the primary main table with the
10:25
product id, so then I'm going to do primary key that is the category id.
10:31
And you can see here that I started my category ID with the product and star.
10:36
So that helps me to understand what is in here and I will change also
10:41
that primary key in the main table to be product and then the hash.
10:47
And then we can get all the products and this, I will do it in the secondary
10:51
index and I will just create a primary key that says product hash and that
10:56
will return me all the products.
10:57
This works very well if you have a reasonable amount of products.
11:01
If you have a massive amount of product, you will exceed your partition size.
11:05
And this will not work.
11:07
But in my case, I'm not planning to have so many products.
11:10
Then I'm going to do a filter by price range, and then this one
11:15
will be in a different index.
11:16
In the secondary index.
11:17
Again, I'm going to get all the products and then I'm going
11:21
to apply a sort key on it.
11:24
And I will use the sort key because it's a range key.
11:27
I can do filter by price, so if it's price is bigger or smaller
11:31
than something I can play with it.
11:33
So that's nice to do these range operations on the sort key.
11:38
And then I will do another filter based on the search.
11:42
So this will be a very kind of basic search operation where I will be doing
11:49
it in the index number three, and I will be doing basic with the title.
11:55
So it'll be a, begins with operation on the title.
12:00
And this will happen also in the sort key.
12:03
So in this way it's very easy for me to do.
12:06
I don't know, begins with aws, begins with sticker and then I can bring it.
12:10
Now let's move on to more access patterns.
12:13
These ones are simple, they're user access pattern.
12:16
Let's create a user.
12:17
Let's do CRUD operations on the user.
12:20
This will happen on the main table.
12:22
These are read and write operations, and we are going to use the primary
12:26
key, like the user user id, this case, the user email, and I'm going to change
12:32
that primary key for a product to be the product hash and then product
12:37
id to be consistent with the rest.
12:40
So that's good.
12:41
And here we will like to do also uniqueness on the email.
12:45
So that's something that you might want to have in mind.
12:49
And finally, we are going to do operations on the order.
12:52
So we are going to do CRUD operations on the orders.
12:56
These are read and write operations, create an order, update an
13:00
order, delete an order, whatever.
13:02
And these are going to happen with the primary key user.
13:05
So every user will have all the orders inside the partition.
13:10
So whenever I want to bring all the orders for a particular user, I just
13:15
get the user and it comes with orders.
13:17
So easy, piecy and the sort key is the order id.
13:20
So then I can do some filtering and if I will put the orders with
13:24
some kind of sorting mechanism in their ID, there will be time sorted.
13:28
Win will situation.
13:30
We mentioned that we have two types of orders.
13:32
We have the current order and the purchased orders.
13:35
So if I want to get the current cart that's the current order, I
13:39
will just use that in an index.
13:41
It's a read operation and I will pass the primary key, the user id, and then
13:47
the status will be current and that should return me the current order.
13:52
Then we have the order items, and these ones are basically the
13:58
product and the order kind of showing information together.
14:01
So this will also happen in the main table because they're read and write operations.
14:06
So we are going to do them there.
14:08
And then the primary key will be the order id.
14:12
So inside every order Id, we'll have all the products inside that partition key.
14:19
So whenever we bring the order id, boom, we have all the products
14:23
that are inside the order.
14:24
So in that way it's handy.
14:27
And then we have, the final thing is the user history.
14:31
So this is all the orders that the user has except the current one.
14:37
So we can we can bring that easily from the main table, which has
14:43
the primary key is the user.
14:46
And then we can do a filter in the sort key basically that we remove that and
14:53
boom, we have everything that we need.
14:56
So that's it.
14:57
Now we have all the access patterns and now we can know more
15:02
or less how to access this data.
15:03
This takes you a little iterations you might not get it right in the
15:07
first time, or you might get little different, you might go back and
15:10
forth, so that's totally normal.
15:12
But this chart will help you a lot when building the application because you can
15:16
just basically look at it and say, Hey, this is what I need to build and build it.
15:20
Don't need to think that much.
15:22
The last step is to build the table diagram or how you're going to
15:28
build this table with the indexes.
15:30
So this is a summary of the access patterns that we have.
15:34
So here we have the entities, we have the primary key and the sort key of the
15:39
main table, and we have the indexes.
15:41
I know the orders are using the order index Number three.
15:45
I went around so many times with this thing that it end up being
15:49
like that and I will not change it.
15:50
But but you can see that the product is using three indexes and the
15:54
main table, and that's because all the filtering that there is there.
15:58
Then we have the users that is only using the main table.
16:00
We have the orders that is in the main table, and then the order the
16:04
index number three basically to get the current order super fast.
16:09
And then we have the order.
16:10
That is using the main table as well.
16:12
So this is what we need to build.
16:14
We know we need to build a table with a primary key called PK and sk, and
16:18
then we need to build three indexes.
16:20
And then one index has to have a numeric sort sort key that help us with
16:25
range operation and then we have it.
16:27
And that's all.
16:29
I hope this video help you.
16:30
And again, a disclaimer, this may not be the best way to do this.
16:34
This is the way I found after tinkering with this for a while.
16:38
So I don't want to spend a thousand years on this design.
16:41
This is a demo.
16:41
It works.
16:42
You will see it at the end.
16:43
It's quite fast, and that's what it needs to do.
16:45
But there's always better ways to things.
16:47
So this is not the final best In the world just for you, that
16:51
you're going to comment that.
16:52
What I want to show you here is the steps on how you can go from UI or from an
16:57
specification into a table that then you can implement as infrastructure as code.
17:02
These are the steps.
17:03
Build the entities, find the entities, find how the entities
17:06
connect, build the access patterns, and then build the table with that.
17:11
And it comes together quite fast.
17:13
And you can do that all in paper.
17:15
No need to code.
17:16
No need to spend any time figuring in the code that it doesn't work.
17:20
So this video is part of a series of me talking about Dynamo.
17:24
You can find the full playlist here, but if you want to go and check my interview
17:29
with Alex DeBrie that he explains the same but nicer, go and check that video.
17:34
It's quite good, and you'll find all the steps as well, exactly the
17:37
same steps I'm showing you for a different use case and you might
```