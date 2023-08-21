
import six
import os
import shutil
import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from pyfiglet import figlet_format
from cement import Controller, ex, shell
from cement.utils.version import get_version_banner
from ..core.version import get_version
from offboardhelper.models import *

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


VERSION_BANNER = """
Manage Google Workspace data %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Manage Google Workspace data'

        # text displayed at the bottom of --help output
        epilog = 'Usage: offboardhelper command1 --foo bar'

        # controller level arguments. ex: 'offboardhelper --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    project = Project()

    # Need a conf file to store gyb_bin, etc
    client_directory = "/home/jeff/Projects/offboard-helper-cement/test_client_folder"
    project_folders_base = "/home/jeff/Projects/offboard-helper-cement/project_folders"



    # top_buffer = Buffer()
    # bottom_buffer = Buffer()

    # top_window = Window(BufferControl(buffer=top_buffer))
    # bottom_window = Window(BufferControl(buffer=bottom_buffer))

    # body = HSplit(
    #     [
    #         top_window,
    #         # A vertical line in the middle. We explicitly specify the width, to make
    #         # sure that the layout engine will not try to divide the whole width by
    #         # three for all these windows.
    #         Window(height=1, char="_", style="class:line"),
    #         # Display the Result buffer on the right.
    #         bottom_window,
    #     ]
    # )


    # def get_titlebar_text():
    #     return [
    #         ("class:title", figlet_format(
    #             "Offboard Helper", font="slant")),
    #         ("class:title", " (Press [Ctrl-Q] to quit.)"),
    #     ]

    # root_container = HSplit(
    #     [
    #         # The titlebar.
    #         Window(
    #             height=8,
    #             content=FormattedTextControl(get_titlebar_text, style="green"),
    #             align=WindowAlign.CENTER,
    #         ),
    #         # Horizontal separator.
    #         Window(height=1, char="=", style="class:line"),
    #         # The 'body', like defined above.
    #         body,
    #     ]
    # )

    # kb = KeyBindings()
    
    # @kb.add("c-c", eager=True)
    # @kb.add("c-q", eager=True)
    # def _(event):
    #     event.app.exit()


    def _default(self):
        # Application(
        #     layout=Layout(self.root_container, focused_element=self.top_window),
        #     key_bindings=self.kb,
        #     mouse_support=True,
        #     full_screen=True,
        # ).run()
        self.figlet_out("Offboard Helper", color="blue")
        #self.figlet_out("Welcome to Offboard Helper", "green")
#       self.test_screen()
        self.ui()
        self.run_jobs()
        #self.run_job_backup(self.project.jobslist.results[0].source_email)

    def figlet_out(self, string, color, font="slant"):
        if colored:
            six.print_(colored(figlet_format(
                string, font=font), color))
        else:
            six.print_(string)

    def test_screen(self):
        try:
            STY = os.environ['STY']
        except KeyError:
            self.app.log.error(
                "This should be run using 'screen'. Please launch 'screen' and rerun."
            )
            sys.exit()

    def set_project_folder(self):
        self.project.project_folder = self.project_folders_base + "/" + self.project.company_name + "-" + self.project.ticket
        os.makedirs(self.project_folders_base, exist_ok=True)
        # TODO We should alert the user that the folder already exites if it does
        os.makedirs(self.project.project_folder, exist_ok=True)
        os.chdir(self.project.project_folder)

    # UI Stuff
    def ui(self):
        self.get_client()
        self.get_ticket_number()
        self.get_jobs()

    def get_ticket_number(self):
        # TODO once we have the client, we should pull a list of open tickets for the client and put them in a list
        self.project.ticket = inquirer.text(message='What is the ticket number?',
                                            validate=TicketValidator()
                                            ).execute()
        channel_name = self.project.ticket.replace(".", "_").replace("T", "t")
        # FIXME Verify Slack Channel
        #project.slack_channel_id = api.find_channel(channel_name)

    def get_client(self):
        clients_list = [f.name for f in os.scandir(self.client_directory) if f.is_dir()]
        
        if clients_list:
            self.project.company_name = inquirer.select(
                message="Pick your client:",
                choices=[
                    clients_list[0],
                    Choice(value=None, name="New"),
                ],
                default=None,
            ).execute()

            if self.project.company_name == "New":
                self.app.log.error('Contact Senior Tech to setup new client!')
            else:
                self.project.config_folder = self.client_directory + "/" + self.project.company_name
        else:
            self.app.log.error('Contact Senior Tech to setup new client!')

    def setup_new_job(self):
        job = Job()
        job.source_email = inquirer.text(
            message="What is the email address we are backing up?",
            validate=EmailValidator()
            ).execute()
        
        # First email we get check the service account
        if self.project.jobslist == None:
            gyb = self.app.handler.get('gyb', 'gyb_shell', setup=True)
            gyb.check_service_account(
                job.source_email, 
                config_folder=self.project.config_folder
                )    
        
        destination_choices = [
            Separator(),
            Choice("user", name="User's inbox in a subfolder"),
            Choice("group", name="Google Group"),
            Choice("zip", name="Zip the backup")
        ]
        destinations = inquirer.checkbox(
            message="What are we doing with the emails after backing them up?",
            choices=destination_choices,
            validate=lambda result: len(result) >= 1,
            invalid_message="should be at least 1 selection",
            instruction="(select at least 1)",
        ).execute()
        for destination in destinations:
            if destination == "user":
                job.distination_user = inquirer.text(
                    message="What is the email address of the user we are restoring to?",
                    validate=EmailValidator()
                ).execute()
            if destination == "group":
                job.istination_group = inquirer.text(
                    message="What is the email address of the Google Group we are restoring to?",
                    validate=EmailValidator()
                ).execute()
            if destination == "zip":
                job.distination_archive = "True"
        return job

    def get_jobs(self):
        self.set_project_folder()
        jobs_list = Jobslist()
        # TODO Might pull a list of emails and let the user pick
        
        # TODO Check for what is currently in the folder.
        # TODO Has a job log somewhere so we can resume jobs.
        another_jobs = True
        while another_jobs:
            if self.project.jobslist == None:
                job = Job()
                job = self.setup_new_job()
                jobs_list.results.append(job)
                self.project.jobslist = jobs_list
            else:
                another_jobs = inquirer.confirm(
                    message="Add another job",
                ).execute()
                if another_jobs:
                    job = Job()
                    job = self.setup_new_job()
                    jobs_list.results.append(job)
                    self.project.jobslist = jobs_list

    def check_space(self, estimated_size_bytes):
        disk_usage = shutil.disk_usage("./")
        self.app.log.info("Space free: " + str(disk_usage.free))
        if estimated_size_bytes < disk_usage.free:
            return True
        else:
            self.app.log.error("We don't ahve enough space on run the job. Estimated size: " + estimated_size)
            return False

    def translate_to_bytes(self, estimated_size) -> float:
        size_str = estimated_size.strip().lower()
        if size_str.endswith('gb'):
            return float(size_str[:-2]) * (2**30)
        elif size_str.endswith('mb'):
            return float(size_str[:-2]) * (2**20)
        elif size_str.endswith('kb'):
            return float(size_str[:-2]) * (2**10)
        elif size_str.endswith('b'):
            return float(size_str[:-1])
        else:
            self.app.log.error(f"Unknown size format: {estimated_size}")
            sys.exit()

    def run_job_estimate(self, email):
        command = ['gyb --action estimate --email ' + email + ' --service-account --memory-limit 100 --config-folder ' + self.project.config_folder]
        self.app.log.info("Estimating email size for " + email)
        out, err, code = shell.cmd(command, capture=True)
        if code != 0:
            self.app.log.error("GYB exited with code " + str(code))
            self.app.log.error("Error: " + err)
        else:
            estimated = out.decode('utf-8').split("\r")[-2]
            estimated_size = estimated.split(" ")[2]
            estimated_size_bytes = self.translate_to_bytes(estimated_size)
            self.app.log.info("Estimated size: " + estimated_size)
            messages = estimated.split(" ")[3].split("/")[-1]
            self.app.log.info("Number of messages: " + messages)
            self.check_space(estimated_size_bytes)
    
    def process_estimate(self, gyb_estimate):
        estimated_size = estimated.split(" ")[2]
        estimated_size_bytes = self.translate_to_bytes(estimated_size)
        self.app.log.info("Estimated size: " + estimated_size)
        messages = estimated.split(" ")[3].split("/")[-1]
        self.app.log.info("Number of messages: " + messages)
        self.check_space(estimated_size_bytes)

    def run_job_backup(self, email):
        # Check space before running
        self.run_job_estimate(email)
        sys.exit()
        # FIXME run for loop on all source_emails
        # TODO Move this to backup job
        # FIXME move memory-limit to config
        command = ['gyb --action backup --email ' + email + ' --service-account --memory-limit 100 --config-folder ' + self.project.config_folder]
        self.app.log.info("Starting backup job for " + email)
        out, err, code = shell.cmd(command, capture=True)

    def run_jobs(self):
        gyb = self.app.handler.get('gyb', 'gyb_shell', setup=True)
        arguments = {
            'config_folder': self.project.config_folder,
            'memory_limit' : 100, # FIXME Change to config,            
        }
        for job in self.project.jobslist.results:
            # Backup
            backup_finished = False
            if job.source_email:
                gyb_estimate = gyb.actions(action='estimate', email=job.source_email, **arguments)
                backup_finished = gyb.actions(action='backup', email=job.source_email, **arguments)
            
            # Restore
            restore_finished = False
            if job.distination_user:
                restore_finished = gyb.actions(action='restore', email=job.source_email, **arguments)
            
            # Restore Group
            restore_group_finished = False
            if job.distination_group:
                restore_group_finished = gyb.actions(action='restore-group', email=job.source_email, **arguments)
            archive_finished = False
            if job.distination_archive:
                archive = "GYB-GMail-Backup-" +  job.source_email
                self.app.log.info("Archiving " + archive)
                shutil.make_archive(archive, 'zip', archive)
                archive_finished = True

