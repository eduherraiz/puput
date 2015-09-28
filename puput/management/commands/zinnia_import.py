# -*- coding: utf-8 -*-

from django import VERSION as DJANGO_VERSION
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.conf import settings

from wagtail.wagtailcore.models import Page, Site
from puput.models import Category as PuputCategory
from puput.models import CategoryEntryPage as PuputCategoryEntryPage
from zinnia.models import Category as ZinniaCategory
from zinnia.models import Entry as ZinniaEntry
from puput.models import EntryPage
from wagtail.wagtailimages.models import Image as WagtailImage


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

        # Create example blog page
        blogpage = Page(
            title="Blog",
            content_type=blogpage_content_type,
            slug='blog',
        )

        rootpage.add_child(instance=blogpage)
        revision = rootpage.save_revision()
        revision.publish()

        print("Importing categories...")
        categories = ZinniaCategory.objects.all()
        for category in categories:
            print("\t%s" % category)
            new_category, created  = PuputCategory.objects.update_or_create(
                name=category.title,
                slug=category.slug,
                description=category.description
            )
            new_category.save()

        print("Importing entries...")
        entries = ZinniaEntry.objects.all()
        for entry in entries:

            print entry.title

            # Header images
            if entry.image:
                header_image = WagtailImage(file=entry.image)
                # print header_image.filename
                header_image.save()
            else:
                header_image = None

            # Content images
            import lxml.html as LH
            root = LH.fromstring(entry.content)
            for el in root.iter('img'):
                if  el.attrib['src'].startswith(settings.MEDIA_URL):
                    old_image = el.attrib['src'].replace(settings.MEDIA_URL,'')
                    new_image = WagtailImage(file=settings.MEDIA_ROOT+'/'+old_image)
                    new_image.save()

                    el.attrib['src'] = new_image

            content = LH.tostring(root, pretty_print=True)


            page = EntryPage(
                title=entry.title,
                body=content,
                slug=entry.slug,
                first_published_at=entry.start_publication,
                expire_at=entry.end_publication,
                latest_revision_created_at=entry.creation_date,
                date=entry.creation_date,
                owner=entry.authors.first(),
                seo_title=entry.title,
                live=entry.is_visible,
                header_image=header_image
            )
            blogpage.add_child(instance=page)
            revision = blogpage.save_revision()
            revision.publish()

            ## TODO: Tags for entry
            # entry.tags field

            ## Categories for entry
            for category in entry.categories.all():
                print('\t\tAdd category: %s' % category.title)
                pc = PuputCategory.objects.get(name=category.title)
                PuputCategoryEntryPage(category=pc, page=page)



