# -*- coding: utf-8 -*-

from django import VERSION as DJANGO_VERSION
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from wagtail.wagtailcore.models import Page, Site
from puput.models import Category as PuputCategory
from zinnia.models import Category as ZinniaCategory
from zinnia.models import Entry as ZinniaEntry
from puput.models import EntryPage

class Command(BaseCommand):
    help = "Load Puput data from zinnia blog app"

    def handle(self, *args, **options):
        # Get blogpage content type
        blogpage_content_type, created = ContentType.objects.get_or_create(
            model='blogpage',
            app_label='puput',
            defaults={'name': 'page'} if DJANGO_VERSION < (1, 8) else {}
        )

        # Get root page
        rootpage = Page.objects.first()

        # Set site root page as root site page
        site = Site.objects.first()
        site.root_page = rootpage
        site.save()

        print "Importing categories..."
        categories = ZinniaCategory.objects.all()
        for category in categories:
            print "\t%s" % category
            new_category, created  = PuputCategory.objects.update_or_create(name=category)
            new_category.save()

        print "Importing entries..."
        entries = ZinniaEntry.objects.all()
        for entry in entries:
            # Create example blog page
            print "\t%s" % entry.title
            blogpage, created = EntryPage.objects.update_or_create(
                title=entry.title,
                body=entry.content,
                slug=entry.slug,
            )

            if created:
                # Add blog page as a child for homepage
                rootpage.add_child(instance=blogpage)
                revision = blogpage.save_revision()
                revision.publish()