import os
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import MyAppError
from .controllers.base import Base
from .controllers.create_apps import AppSetup

# configuration defaults
CONFIG = init_defaults('kluff')
BASE_DIR, _ = os.path.split(os.path.abspath(__file__))
CONFIG['kluff']['base_dir'] = BASE_DIR
CONFIG['kluff']['templates'] = os.path.join(BASE_DIR, 'templates')

class MyApp(App):
    """Kluff CLI primary application."""

    class Meta:
        label = 'kluff'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            AppSetup
        ]


class MyAppTest(TestApp,MyApp):
    """A sub-class of MyApp that is better suited for testing."""

    class Meta:
        label = 'kluff'


def main():
    with MyApp() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except MyAppError as e:
            print('MyAppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
