from django.test import TestCase
from django.test import \
    RequestFactory
from django.urls.base import reverse
from core.models import Movie
from core.views import MovieListView

class MovieListPaginationTest(TestCase):
    Active_PAGINATION_HTML = """
    <li class="page-item active">
        <a href="{}?page={}" class="page-link">{}</a>
    </li>

    """
    def setUp(self):
        for n in range(15):
            Movie.objects.create(
                title='Title {}'.format(n),
                year=1990 + n,
                runtime=100,
            )
    def testFirstPage(self):
        request = RequestFactory().get(reverse('core:movie_list'))
        response = MovieListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['is_paginated'])
        self.assertInHTML(
            self.Active_PAGINATION_HTML.format(
                reverse('core:movie_list'),
                1,
                1,
            ),
            response.rendered_content
        )


# Create your tests here.
