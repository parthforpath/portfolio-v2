import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'


def _load_json(filename):
    with (DATA_DIR / filename).open('r', encoding='utf-8') as file:
        return json.load(file)


def load_projects():
    return _load_json('projects.json')


def load_project_by_slug(slug):
    return next((project for project in load_projects() if project.get('slug') == slug), None)


def load_blogs():
    return _load_json('blogs.json')


def load_blog_by_slug(slug):
    return next((blog for blog in load_blogs() if blog.get('slug') == slug), None)


def load_experiences():
    return _load_json('experiences.json')
