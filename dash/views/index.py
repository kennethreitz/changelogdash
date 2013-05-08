# -*- coding: utf-8 -*-

import json
from operator import attrgetter

import otter
import requests
import redi
from flask import Blueprint, g, render_template


index = Blueprint('home', __name__)


PAGE_SIZE = 3
FORBIDDEN_USERS = ('blog',)


class Repo(object):
    """Repo!"""
    def __init__(self):
        self.user = None
        self.name = None
        self.description = None
        self.watchers = None
        self.hits = None
        self.lang = None

    @property
    def url(self):
        return 'https://github.com/{0}/{1}'.format(self.user, self.name)

    def __repr__(self):
        return '<repo {0}/{1}>'.format(self.user, self.name)


def search_topsy(term, window):
    for page in range(PAGE_SIZE):

        search = otter.Resource('search')
        search(q=term, window=window, offset=page*10)

        for link in search.response.list:
            yield dict(
                title=link.title,
                url=link.url,
                hits=link.hits
            )


def fetch_repo_meta(user, repo):
    url = 'https://api.github.com/repos/{0}/{1}'.format(user, repo)

    r = requests.get(url)
    meta = json.loads(r.content)

    return meta


def get_window(window):
    repos = redi.s.reflogdash._(window, 'list')

    return repos[0] or []


def store_window(window):
    repos =  fetch_repos_for(window)

    r_repos = redi.s.reflogdash._(window, 'list')
    r_repos.lpush(repos)


def fetch_repos_for(window):
    results = []

    for result in search_topsy('github.com', window[0]):

        if result.get('url').startswith('https://github.com/'):

            url = result.get('url').replace('https://github.com/', '').split('/')

            if len(url) >= 2:
                repo = Repo()
                repo.user = url[0]
                repo.name = url[1]

                meta = fetch_repo_meta(repo.user, repo.name)

                repo.description = meta.get('description', '')
                repo.watchers = meta.get('watchers', None)
                repo.hits = result.get('hits', None)
                try:
                    repo.lang = meta.get('language').lower()
                except AttributeError:
                    pass


                if repo.user not in FORBIDDEN_USERS:
                    if repo.name not in [r.name for r in results]:
                        results.append(repo)

    return sorted(results, key=attrgetter('hits'), reverse=True)



@index.route('/')
def view_index():
    return render_template('index.html',
        day=get_window('day'),
        week=get_window('week'),
        month=get_window('month'),
    )


@index.route('/sync')
def view_sync_url():
    for window in ('day', 'week', 'month'):
        store_window(window)

    return '\o/'


@index.route('/debug')
def view_debug():
    return str(g.r.keys('*'))