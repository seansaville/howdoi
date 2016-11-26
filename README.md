# howdoi

Searchable command-line database for small bits of information.

# What does it do?

Do you waste time looking up huge terminal commands that you use on a regular
basis (and are just different enough each time that you can't simply alias
them)? Maybe there's some things you'd just like to remind yourself about while
you're happily tapping away in your terminal? Then **howdoi** is for you.

**howdoi** lets you store strings in its database, tag them with search tags of
your choice, and then retrieve them with a super-simple terminal command -
letting you get back to working on something awesome.

# howdoi install it?

**howdoi** is a simple Python script (in two files). Simply `git clone` this
repository, then put an alias in your `.bashrc` file:

```
alias howdoi='/location/of/howdoi.py'
```

It's that easy!

# howdoi use it?

**howdoi** is really easy to use. There's only 2 important commands:

```
howdoi -a your awesome bit of information
```
(add "your awesome bit of information" to the database)

```
howdoi awesome
>>> your awesome bit of information
```
(search the database for anything tagged with 'awesome')

# howdoi be an advanced user?

* You can choose if you'd like to tag a string with each significant word of
that string (good for storing plaintext) or with your own tags (better for
terminal commands).

* You can run `howdoi -s` to dump the contents of the database.

* You can run `howdoi -d x` to delete the the item with ID `x`.

# howdoi contribute?

If you run into problems or have suggestions for improvements, file a Github
issue and I'll take a look.

If you're a hands-on person and would prefer to fix things yourself, send me a
pull request!
