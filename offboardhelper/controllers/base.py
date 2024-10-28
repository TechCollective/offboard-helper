
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
from prompt_toolkit.shortcuts import clear
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
        #epilog = 'Usage: offboardhelper command1 --foo bar'

        # controller level arguments. ex: 'offboardhelper --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
            ( [ '--no-screen' ], 
              { 'help': "run without screen",
                  'action': 'store_true',
                  'dest': 'no_screen'}
            ),
        ]


    project = Project()

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
        # Slack Example
        # slack = self.app.handler.get('slack', 'slack_messages', setup=True)
        # channel = slack.channel_get_id_from_ticket("T20230729.0004")
        # channel = "C05KCJSJV4N"
        #thread_ts = slack.send_message(channel, "Bot test, please ignore")
        # slack.send_thread(channel, "1693265958.218849", "More bot testing")
        # slack.channels_join(channel)
        
        

        # Need a conf file to store gyb_bin, etc
        # client_directory = "/home/jeff/Projects/offboard-helper-cement/test_client_folder"
        # client_directory = app.config.get('offboardhelper', 'client_directory')
        # project_folders_base = "/home/jeff/Projects/offboard-helper-cement/project_folders"
        # project_folders_base = app.config.get('offboardhelper', 'project_folders_base')
        
        
        # Application(
        #     layout=Layout(self.root_container, focused_element=self.top_window),
        #     key_bindings=self.kb,
        #     mouse_support=True,
        #     full_screen=True,
        # ).run()
        
        #self.figlet_out("Welcome to Offboard Helper", "green")
        self.test_screen()
        # TODO Need to check for updates 
        # bash <(curl -s -S -L https://git.io/gyb-install) -l -d path
            # -h      show help.
            # -d      Directory where gyb folder will be installed. Default is \$HOME/bin/
            # -a      Architecture to install (i686, x86_64, armv7l, aarch64). Default is to detect your arch with "uname -m".
            # -o      OS we are running (linux, osx). Default is to detect your OS with "uname -s".
            # -l      Just upgrade GYB to latest version. Skips project creation and auth.
            # -p      Profile update (true, false). Should script add gyb command to environment. Default is true.
            # -u      Admin user email address to use with GYB. Default is to prompt.
            # -r      Regular user email address. Used to test service account access to user data. Default is to prompt.
            # -v      Version to install (latest, prerelease, draft, 3.8, etc). Default is latest.
        # Move the gyb executible from that location and move it to the correct location
        # Then we have to chown root:techteam chmod o-rwx

        # TODO Need a way to import a csv for jobs    
        self.ui()
        self.project_to_db()
        self.run_jobs()
        #self.run_job_backup(self.project.jobslist.results[0].source_email)

    def figlet_out(self, string, color, font="slant"):
        if colored:
            six.print_(colored(figlet_format(
                string, font=font), color))
        else:
            six.print_(string)

    def test_screen(self):
        if self.app.pargs.no_screen is not True:
            try:
                STY = os.environ['STY']
            except KeyError:
                self.app.log.error(
                    "This should be run using 'screen'. Please launch 'screen' and rerun."
                )
                sys.exit()

    def set_project_folder(self):
        project_folders_base = self.app.config.get('offboardhelper', 'project_folders_base')
        #self.project.project_folder = self.project_folders_base + "/" + self.project.company_name + "-" + self.project.ticket
        self.project.project_folder = project_folders_base + "/" + self.project.company_name + "-" + self.project.ticket
        #os.makedirs(self.project_folders_base, exist_ok=True)
        os.makedirs(project_folders_base, exist_ok=True)
        # TODO We should alert the user that the folder already exites if it does
        os.makedirs(self.project.project_folder, exist_ok=True)
        os.chdir(self.project.project_folder)
        for res in self.app.hook.run('project_dir_setup', self.app):
            pass
        self.app.log.debug("project folder created and ran hook project_dir_setup")

    def project_to_db(self):
        self.app.db.insert(self.project.to_dict())
        sys.exit()
        
    # UI Stuff
    def ui(self):
        self.ui_header()
        self.get_client()
        self.get_ticket_number()
        self.set_project_folder()
        self.check_project_file()
        self.get_jobs()
        self.get_slack()

    def get_ticket_number(self):
        # TODO once we have the client, we should pull a list of open tickets for the client and put them in a list
        self.project.ticket = inquirer.text(message='What is the ticket number?',
                                            validate=TicketValidator()
                                            ).execute()
        channel_name = self.project.ticket.replace(".", "_").replace("T", "t")

    def check_project_file(self):
        if self.app.db.all():
            self.project.from_tinydb(self.app.db.all())

    def get_client(self):
        #clients_list = [f.name for f in os.scandir(self.client_directory) if f.is_dir()]
        clients_list = [
            f.name for f in os.scandir(
                self.app.config.get('offboardhelper', 'client_directory')
                ) if f.is_dir()
        ]
        
        if clients_list:
            self.project.company_name = inquirer.select(
                message="Pick your client:",
                choices=[
                    clients_list[0],
                    Choice(value="New", name="New"),
                ],
                default=None,
            ).execute()

            if self.project.company_name == "New":
                self.app.log.error('Contact Senior Tech to setup new client!')
            else:
                #self.project.config_folder = self.client_directory + "/" + self.project.company_name
                self.project.config_folder = self.app.config.get('offboardhelper', 'client_directory') + "/" + self.project.company_name
        else:
            self.app.log.error('Contact Senior Tech to setup new client!')

    def get_source_email(self):
        return inquirer.text(
            message="What is the email address we are backing up?",
            validate=EmailValidator()
            ).execute()

    def get_restore_email(self):
        return inquirer.text(
                    message="What is the email address of the user we are restoring to?",
                    validate=EmailValidator()
                ).execute()

    def get_restore_group(self):
        return inquirer.text(
                    message="What is the email address of the Google Group we are restoring to?",
                    validate=EmailValidator()
                ).execute()

    def get_admin_account(self):
        return inquirer.text(
                    message="Group Restore needs to be restore by a Workspace admin. What is an admin account should we use.?",
                    validate=EmailValidator()
                ).execute()

    def setup_new_job(self):
        job = Job()
        job.source_email = self.get_source_email()
        
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
            Choice("zip", name="Zip the backup"),
            Choice("nothing", name="Just backup, nothing else")
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
                job.distination_user = self.get_restore_email()
            if destination == "group":
                job.distination_group = self.get_restore_group()
            if destination == "zip":
                job.distination_archive = "True"
            if destination == "nothing":
                pass
        return job

    def edit_job(self, job):
        choices = [
            Choice('source_email', name = "Source Email: " + job.source_email)
        ]
        if job.distination_group:
            choices.append(Choice('distination_group', name="Restore group address: " + job.distination_group))
        else:
            choices.append(Choice('distination_group', name="Add a group address to restore to"))

        if job.distination_user:
            choices.append(Choice('distination_user', name="Restore to user: " + job.distination_user))
        else:
            choices.append(Choice('distination_user', name="Add a user to restore to"))

        choices.append(Choice('distination_archive', name="Zip backup: " + str(job.distination_archive)))
        choices.append(Separator())
        choices.append(Choice('remove', name="Remove Job"))

        action = inquirer.select(
            message="Select to edit.",
            choices=choices,
            multiselect=False,
        ).execute()
        self.app.log.debug("User is editing job: " + job.source_email + " Action: " + action )
        
        if action == "source_email":
            job.source_email = get_source_email()
        elif action == "distination_user":
            pass
        elif action == "distination_group":
            job.distination_group = self.get_restore_group()
        elif action == "distination_archive":
            if job.distination_archive:
                job.distination_archive = None
            else:
                job.distination_archive = True
        elif action == "remove":
            self.project.jobslist.results.remove(job)

    def ui_header(self):
        clear()
        self.figlet_out("Offboard Helper", color="blue")
        subheader = "Client: "
        if self.project.company_name:
            subheader += self.project.company_name
        else:
            subheader += "None"
            
        subheader += "  |  Ticker Number: "
        if self.project.ticket:
            subheader += self.project.ticket
        else:
            subheader += "None"
        subheader += "  |  Admin Account: "
        if self.project.admin_account:
            subheader += self.project.admin_account
        else:
            subheader += "None"
        
        subheader += "\n___________________________________________________________________________\n"
        print(subheader)

    def check_group_admin(self):
        set_admin = False
       
        if self.project.admin_account == None:
            if self.project.jobslist:
                for result in self.project.jobslist.results:
                    if result.distination_group:
                        set_admin = True
                        break

        if set_admin:
            self.ui_header()
            self.project.admin_account = get_admin_account()
            # TODO, maybe verify this is actually an admin

    def get_jobs(self):
        self.check_group_admin()
        
        another_jobs = True
        # FIXME have a way to cancel add another job, without having to cancel the whole script
        
        while another_jobs:
            self.ui_header()
            choices = []
            if self.project.jobslist:
                for result in self.project.jobslist.results:
                    name = result.source_email + "   | Group: " + str(result.distination_group) + " | User: " + str(result.distination_user) + " | Zip: " + str(result.distination_archive)
                    choices.append(Choice(result.source_email, name=name))

            choices.append(Separator())
            choices.append(Choice("new", name="New Job"))
            choices.append(Separator())
            choices.append(Choice("continue", name="Continue"))
            choices.append(Choice("exit", name="Exit"))

            action = inquirer.select(
                message='Select "New" or picking a job will allow you to edit',
                choices=choices,
                multiselect=False,
            ).execute()
            self.app.log.debug("User picked: " + action)
            
            jobs_list = Jobslist()
            if action == "exit":
                sys.exit()
            elif action == "new":
                job = Job()
                job = self.setup_new_job()
                jobs_list.results.append(job)
                self.project.jobslist = jobs_list
            elif action == "continue":
                break
            else:
                for job in self.project.jobslist.results:
                    if result.source_email == action:
                        self.edit_job(job)
                    
       
        # TODO Might pull a list of emails and let the user pick
        
        # TODO Check for what is currently in the folder.
        # TODO Has a job log somewhere so we can resume jobs.
        # another_jobs = True
        # # FIXME have a way to cancel add another job, without having to cancel the whole script
        # while another_jobs:
        #     if self.project.jobslist == None:
        #         job = Job()
        #         job = self.setup_new_job()
        #         jobs_list.results.append(job)
        #         self.project.jobslist = jobs_list
        #     else:
        #         another_jobs = inquirer.confirm(
        #             message="Add another job",
        #         ).execute()
        #         if another_jobs:
        #             job = Job()
        #             job = self.setup_new_job()
        #             jobs_list.results.append(job)
        #             self.project.jobslist = jobs_list

    def get_slack(self):
        slack = self.app.handler.get('slack', 'slack_messages', setup=True)
        if self.project.slack_channel_id:
            use_slack = inquirer.confirm(message="Do you want to recieve updates via Slack?").execute()
            print("Please wait. Looking for your Slack channel")

            self.project.slack_channel_id = slack.channel_get_id_from_ticket(self.project.ticket)
            slack.channels_join(self.project.slack_channel_id)
        if self.project.slack_status_thread_ts is None:
            opening_message = "*Offboard Helper*\nCheck this thread for updates"
            self.project.slack_status_thread_ts = slack.send_message(self.project.slack_channel_id, opening_message)

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
        # TODO move this to the gyb_handler
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
        # TODO once the jobs start running, we can remind the user how to leave screen
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

