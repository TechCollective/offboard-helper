from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import OffboardHelperError
from .controllers.base import Base
from .core.gyb_handler import GYBHandler
from .core.gyb_interface import GYBInterface
from .ext.ext_slack import SlackInterface, SlackMessages


# configuration defaults
CONFIG = init_defaults('offboardhelper')
# CONFIG['offboardhelper']['foo'] = 'bar'
# Need a conf file to store gyb_bin, etc
CONFIG['offboardhelper']['client_directory'] = '/home/jeff/Projects/offboard-helper-cement/test_client_folder'
CONFIG['offboardhelper']['project_folders_base'] = '/home/jeff/Projects/offboard-helper-cement/project_folders'

class OffboardHelper(App):
    """Offboard Helper primary application."""

    class Meta:
        label = 'offboardhelper'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
            'offboardhelper.ext.ext_slack',
            'offboardhelper.ext.ext_tinydb'
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
            GYBHandler,
            SlackMessages
        ]
        interfaces = [
            GYBInterface,
            SlackInterface
        ]
        define_hooks = [
            'project_dir_setup',
            'job_finished'
            ]
        # hooks = [
        #     ('post_setup', Base.opening ),
        # ]


class OffboardHelperTest(TestApp,OffboardHelper):
    """A sub-class of OffboardHelper that is better suited for testing."""

    class Meta:
        label = 'offboardhelper'


def main():
    with OffboardHelper() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except OffboardHelperError as e:
            print('OffboardHelperError > %s' % e.args[0])
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
