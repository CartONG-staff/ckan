from flask import Blueprint
from flask import render_template, render_template_string

import ckan.plugins as p


def hello_plugin():
    '''A simple view function'''
    return 'Hello World, this is served from an extension'


def override_pylons_about():
    '''A simple replacement for the pylons About page.'''
    return render_template('about.html')


def override_flask_hello():
    '''A simple replacement for the flash Hello view function.'''
    html = '''<!DOCTYPE html>
    <html>
        <head>
            <title>Hello from Flask</title>
        </head>
        <body>Hello World, this is served from an extension, overriding the flask url.</body>
    </html>'''

    return render_template_string(html)


def helper_not_here():

    '''A simple template with a helper that doesn't exist. Rendering with a
    helper that doesn't exist shouldn't raise an exception.'''

    html = '''<!DOCTYPE html>
    <html>
        <head>
            <title>Hello from Flask</title>
        </head>
        <body>Hello World, {{ h.nohere() }} no helper here</body>
    </html>'''

    return render_template_string(html)


def helper_here():

    '''A simple template with a helper that exists. Rendering with a helper
    shouldn't raise an exception.'''

    html = '''<!DOCTYPE html>
    <html>
        <head>
            <title>Hello from Flask</title>
        </head>
        <body>Hello World, helper here: {{ h.lang() }}</body>
    </html>'''

    return render_template_string(html)


class ExampleFlaskIRoutesPlugin(p.SingletonPlugin):
    '''
    An example IRoutes plugin to demonstrate Flask routing from an extension.
    '''
    p.implements(p.IRoutes, inherit=True)

    def get_blueprint(self):
        '''Return a Flask Blueprint object to be registered by the app.'''

        # Create Blueprint for plugin
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = 'templates'
        # Add plugin url rules to Blueprint object
        rules = [
            ('/hello_plugin', 'hello_plugin', hello_plugin),
            ('/about', 'about', override_pylons_about),
            ('/hello', 'hello', override_flask_hello),
            ('/helper_not_here', 'helper_not_here', helper_not_here),
            ('/helper', 'helper_here', helper_here),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint
