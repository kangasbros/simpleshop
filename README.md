simpleshop
==========
A very simple Bitcoin shop solution.

Requirements
------------
* Python >= 2.5
* Django 1.4

Installation
------------
1. Modify your project's `settings.py` to add `simpleshop` to the `INSTALLED_APPS` array.
2. Modify your project's `settings.py` to include the templates directory within `simpleshop`.
3. Modify your project's `urls.py` to add a route to `include('simpleshop.urls')`.
4. Run `python manage.py syncdb` to create the databases simpleshop requires.

That's it!
