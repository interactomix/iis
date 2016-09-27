# Language and Framework choices

Several languages (and frameworks) present an obvious choice.  Languages should
be cross platform (to ease installation for future users). The chosen language 
should be one of those already used for the Interactomix set of tools. To the
best of my knowledge that means one of Java, Python or Perl.  

## Language

There being no other requirements, Python is my prefered choice because I 
already have experience using it especially for Web Development.

## Framework

Several web development frameworks are known to me.  In increasing complexity 
these are: Bottle, Flask and Django.  I have ~1 year experience using Django.
It works just fine, but can be complex in places where it doesn't seem 
necessary.  Django also does everything for you (ORM, forms, middleware, etc.) 
out of the box.  This is convenient if one is familiar with Django's
implementation details.  Otherwise this can become confusing if they need to be
interacted with.

Flask provides just the core functionality of a web framework.  Mapping routes
and verbs to python functions.  Everything else is provided by extensions.
This means a concious effort must be made to use features provided in one of 
these extensions.  In the end I think that will lead to a better understanding
(and easier maintenance) than using Django.

### Extensions

Some extensions will be required/convenient.

#### User Login

To allow users to register/login there are at least two options:  Handle user
authentication directly on the IIS, or use OAuth to authenticate users remotely.

OAuth has the advantage that no passwords have to be stored locally.  Direct 
authentication is required however (at least as a fallback) for users that do
not have accounts with any of the OAuth providers.

For OAuth authentication the Flask-Dance or Flask-OAuth extensions look
promising.  For local authentication Flask-User looks good.

#### Database

At least for purposes of User Authentication a DB will have to exist.  There
are multiple options here, both in terms of which extension to use and what 
fundamental DB type is best.  The apparently canonical extension is 
Flask-SQLAlchemy. It supports at least the following relational databases:  
PostgreSQL, MySQL, Oracle and SQLite. Out of the first three I would gravitate
towards PostgreSQL because I am familiar with it's admin tools.  However for 
this project I think SQLite may be more appropriate. There will be a relatively 
small number of entries. It's configuration is considerably simpler, there is 
less to go wrong.

There also exist a number of extensions for other databases.  CouchDB, FluidDB 
and MongoDB (probably) among others are also supported.

##### Migrations

Flask-SQLAlchemy does not provide support for db migrations.  Migrations allow
the state of the db to be recorded in source control for every revision.  This
allows roling the database back to previous points, and upgrading a production
database.  Flask-Migrate performs these functions.

#### Others

This will likely grow as times goes by.  Email functionality could be handled 
by Flask-Mail.
