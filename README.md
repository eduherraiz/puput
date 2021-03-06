# Puput

Puput is a powerful and simple Django app to manage a blog. It uses the awesome Wagtail CMS as content management system.

Puput is the catalan name for [Hoopoe](https://en.wikipedia.org/wiki/Hoopoe) which is indeed a beautiful bird.

![Imgur](http://i.imgur.com/ndZLeWb.png?1)

### Features
* Based on Wagtail CMS and Django
* Comes with a default clean & responsive template
* SEO friendly urls
* Support for Disqus comments
* Archives, tags & categories results pages
* Search form
* Last & popular entries
* Configurable sidebar widgets
* RSS feeds
* Blog post related entries
* Inspired on Wordpress and Zinnia

### Setup

1. Add to `PUPUT_APPS` to your `INSTALLED_APPS` in `settings.py` file. It also includes Wagtail apps and other dependencies.

    ```python
    from puput import PUPUT_APPS
    
    INSTALLED_APPS += PUPUT_APPS
    ```
2. Add Wagtail required middleware classes in `settings.py` file

    ```python
    MIDDLEWARE_CLASSES = (
        ...
        'wagtail.wagtailcore.middleware.SiteMiddleware',
        'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    )
    ```
3. Add `request` context processor to `TEMPLATE_CONTEXT_PROCESSORS` structure in `settings.py` file

    ```python
    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )
    ```
4. Set `WAGTAIL_SITE_NAME` variable in `settings.py` file with your site name
5. Place Puput urls at the __bottom__ of the urlpatterns. It also includes Wagtail urls.

    ```python
    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
    ]
    ```
6. Run `python manage.py migrate` and `python manage.py puput_initial_data` to load initial data to start a blog site.
7. Open your broswer at http://127.0.0.1:8000/blog/ to view your blog home page.

### Setup (as Wagtail plugin)

1. Add `puput`to your `INSTALLED_APPS` in `settings.py` file.
2. If you have previously defined Wagtail urls in `urls.py` set `PUPUT_AS_PLUGIN = True` in the `settings.py`. This will avoid to include Wagtail urls again when you include necessary Puput urls.
3. Include Puput urls in your `urls.py` file.

    ```python
    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
        ...
    ]
    ```
4. Run `python manage.py migrate`
 

### Manage your content

Puput uses the default Wagtail CMS admin page in order to manage the content of the blog. It provides a powerful, clean and modern interface. Just open your browser at http://127.0.0.1:8000/blog_admin/.

This is how adding entry page looks:

![Imgur](http://i.imgur.com/NntrN3i.png?1)

Please visit [Wagtail: an Editor’s guide](http://docs.wagtail.io/en/v1.0/editor_manual/index.html) for details of how to use Wagtail editor's dashboard.

### Comments

Puput allows customize the comment system for your blog entries. Simply go to settings tab while editing blog properties and add the required parameters
depending on which system you want to use. For now, only Disqus comments are supported. Set __Disqus api secret__ and
__Disqus shortname__ with your project values and comments will be displayed in each blog entry.
